#!/usr/bin/env python3
"""Fallback text renderer for v6 scenes when direct image-model typography needs repair.

The primary v6 workflow generates fully integrated text and imagery together. This
script is a deterministic fallback: it places the manifest headline, subheadline,
labels, takeaway, and caveat into reserved safe zones on a pre-generated scene.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path
from typing import Any

ACCENTS = {
    "ink": "#49382B",
    "terracotta": "#A84E3E",
    "indigo": "#415A77",
    "sage": "#647A58",
    "ochre": "#B9822D",
    "brick": "#9B4335",
}
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "C:/Windows/Fonts/msjh.ttc",
    "C:/Windows/Fonts/arial.ttf",
]


def pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError as exc:
        raise RuntimeError("Install Pillow with `python3 -m pip install -r requirements-annotation.txt`.") from exc
    return Image, ImageDraw, ImageFilter, ImageFont


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 6 or not isinstance(data.get("shots"), list):
        raise ValueError("Expected a version 6 manifest with shots.")
    return data


def find_font(explicit: str | None) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise RuntimeError(f"Font does not exist: {path}")
        return path
    env_path = os.getenv("EDITORIAL_ANNOTATION_FONT")
    if env_path and Path(env_path).expanduser().is_file():
        return Path(env_path).expanduser()
    for candidate in FONT_CANDIDATES:
        path = Path(candidate)
        if path.is_file():
            return path
    try:
        value = subprocess.run(
            ["fc-match", "Noto Sans", "-f", "%{file}"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        ).stdout.strip()
        if value and Path(value).is_file():
            return Path(value)
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    raise RuntimeError("No local font found. Pass --font or set EDITORIAL_ANNOTATION_FONT.")


def scaled_font(ImageFont, font_path: Path, size: int, width: int):
    return ImageFont.truetype(str(font_path), max(18, round(size * width / 1600)))


def fit_wrapped_text(draw, text: str, font_path: Path, width: int, max_width: int, start_size: int, min_size: int = 24):
    _, _, _, ImageFont = pillow()
    for requested in range(start_size, min_size - 1, -2):
        font = scaled_font(ImageFont, font_path, requested, width)
        approximate_chars = max(4, int(max_width / max(1, requested * width / 1600 * 0.95)))
        lines = textwrap.wrap(text, width=approximate_chars, break_long_words=True, break_on_hyphens=False) or [text]
        rendered = "\n".join(lines)
        box = draw.multiline_textbbox((0, 0), rendered, font=font, spacing=8, align="center")
        if box[2] - box[0] <= max_width:
            return rendered, font
    font = scaled_font(ImageFont, font_path, min_size, width)
    return text, font


def paper_card(mods, size: tuple[int, int], outline: str = "#B98A4D"):
    Image, ImageDraw, ImageFilter, _ = mods
    width, height = size
    layer = Image.new("RGBA", (width + 24, height + 24), (0, 0, 0, 0))
    shadow = Image.new("RGBA", layer.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((12, 13, width + 10, height + 10), radius=10, fill=(70, 45, 20, 45))
    layer.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(6)))
    draw = ImageDraw.Draw(layer)
    draw.rounded_rectangle((5, 5, width + 5, height + 5), radius=8, fill="#F0DDB5", outline=outline, width=2)
    return layer


def render_fallback(mods, source: Path, target: Path, shot: dict[str, Any], font_path: Path, margin: int):
    Image, ImageDraw, _, ImageFont = mods
    canvas = Image.open(source).convert("RGBA")
    width, height = canvas.size
    if (width, height) != (1600, 900):
        canvas = canvas.resize((1600, 900), Image.Resampling.LANCZOS)
        width, height = canvas.size

    veil = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    veil_draw = ImageDraw.Draw(veil)
    veil_draw.rectangle((margin, margin, width - margin, 265), fill=(245, 226, 187, 218))
    canvas.alpha_composite(veil)
    draw = ImageDraw.Draw(canvas)

    eyebrow_font = scaled_font(ImageFont, font_path, 38, width)
    headline_text, headline_font = fit_wrapped_text(draw, shot["headline"], font_path, width, width - margin * 4, 76, 46)
    sub_text, sub_font = fit_wrapped_text(draw, shot["subheadline"], font_path, width, width - margin * 4, 34, 24)

    y = margin + 8
    if shot.get("eyebrow"):
        box = draw.textbbox((0, 0), shot["eyebrow"], font=eyebrow_font)
        draw.text(((width - (box[2] - box[0])) / 2, y), shot["eyebrow"], font=eyebrow_font, fill="#26364A")
        y += 48
    headline_box = draw.multiline_textbbox((0, 0), headline_text, font=headline_font, spacing=8, align="center")
    draw.multiline_text(
        ((width - (headline_box[2] - headline_box[0])) / 2, y),
        headline_text,
        font=headline_font,
        fill="#24140D",
        spacing=8,
        align="center",
    )
    y += headline_box[3] - headline_box[1] + 10
    sub_box = draw.multiline_textbbox((0, 0), sub_text, font=sub_font, spacing=5, align="center")
    draw.multiline_text(
        ((width - (sub_box[2] - sub_box[0])) / 2, y),
        sub_text,
        font=sub_font,
        fill="#A84E3E",
        spacing=5,
        align="center",
    )

    label_x = 1260
    label_y = 325
    label_width = 265
    for label in shot["labels"]:
        font = scaled_font(ImageFont, font_path, 29, width)
        text = label["text"]
        box = draw.textbbox((0, 0), text, font=font)
        card_height = max(64, box[3] - box[1] + 30)
        card = paper_card(mods, (label_width, card_height), ACCENTS[label["accent"]])
        canvas.alpha_composite(card, (label_x, label_y))
        card_draw = ImageDraw.Draw(canvas)
        card_draw.text((label_x + 22, label_y + 18), text, font=font, fill="#49382B")
        label_y += card_height + 22

    if shot.get("bottom_takeaway"):
        takeaway_text, takeaway_font = fit_wrapped_text(
            draw, shot["bottom_takeaway"], font_path, width, width - margin * 4, 36, 25
        )
        box = draw.multiline_textbbox((0, 0), takeaway_text, font=takeaway_font, spacing=5, align="center")
        ribbon_x = margin + 190
        ribbon_y = height - 110
        ribbon_w = width - (margin + 190) * 2
        draw.rounded_rectangle(
            (ribbon_x, ribbon_y, ribbon_x + ribbon_w, height - margin + 8),
            radius=10,
            fill="#D2A05B",
            outline="#8C6333",
            width=3,
        )
        draw.multiline_text(
            ((width - (box[2] - box[0])) / 2, ribbon_y + 18),
            takeaway_text,
            font=takeaway_font,
            fill="#2C1A11",
            spacing=5,
            align="center",
        )

    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(target, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    try:
        data = load_manifest(args.manifest)
        mods = pillow()
        font_path = find_font(args.font)
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        margin = data["visual_bible"]["layout_contract"]["outer_margin_px"]
        report: list[dict[str, str]] = []
        for shot in data["shots"]:
            source = args.input / shot["filename"]
            target = args.output / shot["filename"]
            if not source.is_file():
                raise FileNotFoundError(source)
            render_fallback(mods, source, target, shot, font_path, margin)
            report.append({"source": str(source), "output": str(target), "font": str(font_path)})
        (args.output / "fallback-render-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Rendered {len(report)} fallback image(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
