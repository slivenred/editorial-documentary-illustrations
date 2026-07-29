#!/usr/bin/env python3
"""Add deterministic semantic paper-tag annotations to text-free base images."""
from __future__ import annotations

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ACCENTS = {
    "ink": "#49382B", "terracotta": "#A84E3E", "ochre": "#C58B2D",
    "sage": "#607B59", "indigo": "#4C617C", "brick": "#A74636",
}
FONT_CANDIDATES = [
    "/System/Library/Fonts/PingFang.ttc", "/Library/Fonts/Arial Unicode.ttf",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "C:/Windows/Fonts/msjhbd.ttc", "C:/Windows/Fonts/msjh.ttc",
]


def pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError as exc:
        raise RuntimeError("Install Pillow with `python3 -m pip install -r requirements-annotation.txt`.") from exc
    return Image, ImageDraw, ImageFilter, ImageFont


def find_font(explicit: str | None) -> Path:
    candidates = [explicit, os.getenv("EDITORIAL_ANNOTATION_FONT"), *FONT_CANDIDATES]
    for value in candidates:
        if value and Path(value).expanduser().is_file():
            return Path(value).expanduser()
    try:
        value = subprocess.run(
            ["fc-match", "Noto Sans CJK TC", "-f", "%{file}"], capture_output=True,
            text=True, timeout=5, check=False,
        ).stdout.strip()
        if value and Path(value).is_file():
            return Path(value)
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    raise RuntimeError("No local CJK font found. Pass --font or set EDITORIAL_ANNOTATION_FONT.")


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 2 or not isinstance(data.get("shots"), list):
        raise ValueError("Expected a version 2 manifest with shots.")
    return data


def norm(value: float, extent: int) -> int:
    return round(float(value) * extent)


def accent(value: str) -> str:
    return ACCENTS.get(value, value)


def font_for(ImageFont, path: Path, requested: int, width: int):
    return ImageFont.truetype(str(path), max(18, round(requested * width / 1600)))


def make_tag(mods, text: str, font_path: Path, spec: dict[str, Any], width: int, headline: bool):
    Image, ImageDraw, ImageFilter, ImageFont = mods
    size = int(spec.get("font_size", 42 if headline else 31))
    font = font_for(ImageFont, font_path, size, width)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    box = probe.textbbox((0, 0), text, font=font)
    tw, th = box[2] - box[0], box[3] - box[1]
    px, py = round(width * (0.017 if headline else 0.012)), round(width * 0.009)
    w, h = tw + px * 2, th + py * 2 + round(width * 0.006)
    tag = Image.new("RGBA", (w + 16, h + 16), (0, 0, 0, 0))
    shadow = Image.new("RGBA", tag.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle((9, 10, w + 7, h + 7), radius=max(7, round(width * .008)), fill=(55, 35, 20, 55))
    tag.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(max(3, round(width * .004)))))
    draw = ImageDraw.Draw(tag)
    rnd = random.Random(text)
    jitter = [rnd.randint(-3, 3) for _ in range(8)]
    polygon = [(5+jitter[0], 5+jitter[1]), (w+6+jitter[2], 4+jitter[3]),
               (w+8+jitter[4], h+6+jitter[5]), (6+jitter[6], h+7+jitter[7])]
    draw.polygon(polygon, fill="#F1DDB1", outline="#B98A4D")
    line_y = h + 1
    draw.line((px, line_y, w-px, line_y-1), fill=accent(spec.get("accent", "ink")), width=max(3, round(width*.003)))
    draw.rectangle((w//2-22, 1, w//2+22, 11), fill=(211, 170, 97, 110))
    draw.text((px, py-1), text, font=font, fill="#49382B", stroke_width=1, stroke_fill="#FFF5DC")
    angle = float(spec.get("angle", 0))
    return tag.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC) if angle else tag


def line_to_target(ImageDraw, canvas, start: tuple[int, int], target: tuple[int, int], color: str, seed: str):
    draw = ImageDraw.Draw(canvas)
    rnd = random.Random(seed)
    x1, y1 = start; x2, y2 = target
    mx, my = (x1+x2)//2 + rnd.randint(-10, 10), (y1+y2)//2 + rnd.randint(-8, 8)
    width = max(3, round(canvas.width * .0025))
    draw.line([(x1, y1), (mx, my), (x2, y2)], fill=color, width=width, joint="curve")
    r = max(5, round(canvas.width * .0035))
    draw.ellipse((x2-r, y2-r, x2+r, y2+r), fill=color)


def place(mods, canvas, tag, spec: dict[str, Any], callout: bool):
    Image, ImageDraw, _, _ = mods
    x, y = norm(spec["x"], canvas.width), norm(spec["y"], canvas.height)
    margin = max(5, round(canvas.width * .006))
    x = min(max(margin, x), max(margin, canvas.width-tag.width-margin))
    y = min(max(margin, y), max(margin, canvas.height-tag.height-margin))
    if callout:
        tx, ty = norm(spec["target_x"], canvas.width), norm(spec["target_y"], canvas.height)
        cx = x + (0 if tx < x else tag.width if tx > x+tag.width else tag.width//2)
        cy = y + tag.height//2
        line_to_target(ImageDraw, canvas, (cx, cy), (tx, ty), accent(spec.get("accent", "ink")), spec["text"])
    canvas.alpha_composite(tag, (x, y))


def annotate(mods, image_path: Path, output_path: Path, annotation: dict[str, Any], font_path: Path):
    Image, _, _, _ = mods
    canvas = Image.open(image_path).convert("RGBA")
    headline = annotation["headline"]
    place(mods, canvas, make_tag(mods, headline["text"], font_path, headline, canvas.width, True), headline, False)
    for label in annotation["labels"]:
        place(mods, canvas, make_tag(mods, label["text"], font_path, label, canvas.width, False), label, True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(output_path, quality=95)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--font")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--allow-draft", action="store_true")
    args = parser.parse_args()
    try:
        data, mods, font_path = load_manifest(args.manifest), pillow(), find_font(args.font)
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        report = {"font": str(font_path), "images": []}
        for shot in data["shots"]:
            ann = shot.get("annotation", {})
            if not ann.get("enabled"):
                continue
            if ann.get("layout_status") != "final" and not args.allow_draft:
                raise ValueError(f"Shot {shot['id']} annotation layout is not final.")
            source, target = args.input / shot["filename"], args.output / shot["filename"]
            if not source.is_file():
                raise FileNotFoundError(source)
            annotate(mods, source, target, ann, font_path)
            report["images"].append(str(target))
        (args.output / "annotation-render-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Annotated {len(report['images'])} image(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
