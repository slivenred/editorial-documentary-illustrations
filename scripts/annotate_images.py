#!/usr/bin/env python3
"""Render integrated editorial headlines and explainer cards onto version 5 base images."""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ACCENTS = {
    "ink": "#49382B",
    "terracotta": "#A84E3E",
    "ochre": "#C58B2D",
    "sage": "#607B59",
    "indigo": "#4C617C",
    "brick": "#A74636",
}
RTL_LANGS = {"ar", "fa", "he", "ur", "yi", "ps"}
FONT_GROUPS = {
    "zh": [
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "C:/Windows/Fonts/msjh.ttc",
    ],
    "ja": [
        "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/meiryo.ttc",
    ],
    "ko": [
        "/System/Library/Fonts/AppleSDGothicNeo.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/malgun.ttf",
    ],
    "arabic": [
        "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansArabic-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ],
    "hebrew": [
        "/usr/share/fonts/truetype/noto/NotoSansHebrew-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ],
    "devanagari": [
        "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansDevanagari-Regular.ttf",
    ],
    "thai": [
        "/usr/share/fonts/truetype/noto/NotoSansThai-Regular.ttf",
        "C:/Windows/Fonts/tahoma.ttf",
    ],
    "latin": [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ],
    "universal": [
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}
FONT_QUERIES = {
    "zh": ["Noto Sans CJK TC", "Noto Sans CJK SC", "WenQuanYi Zen Hei"],
    "ja": ["Noto Sans CJK JP", "Noto Sans JP"],
    "ko": ["Noto Sans CJK KR", "Noto Sans KR"],
    "arabic": ["Noto Sans Arabic", "DejaVu Sans"],
    "hebrew": ["Noto Sans Hebrew", "DejaVu Sans"],
    "devanagari": ["Noto Sans Devanagari", "Noto Sans"],
    "thai": ["Noto Sans Thai", "Noto Sans"],
    "latin": ["Noto Sans", "DejaVu Sans", "Liberation Sans"],
    "universal": ["Noto Sans", "DejaVu Sans"],
}


def pillow():
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps, features
    except ImportError as exc:
        raise RuntimeError("Install Pillow with `python3 -m pip install -r requirements-annotation.txt`.") from exc
    return Image, ImageDraw, ImageFilter, ImageFont, ImageOps, features


def language_prefix(language: str) -> str:
    return (language or "und").split("-", 1)[0].lower()


def font_group(language: str, sample_text: str = "") -> str:
    prefix = language_prefix(language)
    if prefix == "zh":
        return "zh"
    if prefix == "ja":
        return "ja"
    if prefix == "ko":
        return "ko"
    if prefix in {"ar", "fa", "ur", "ps"}:
        return "arabic"
    if prefix in {"he", "yi"}:
        return "hebrew"
    if prefix in {"hi", "mr", "ne", "sa"}:
        return "devanagari"
    if prefix == "th":
        return "thai"
    if any("\u4e00" <= character <= "\u9fff" for character in sample_text):
        return "zh"
    return "latin"


def find_font(explicit: str | None, language: str, sample_text: str) -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise RuntimeError(f"Explicit font does not exist: {path}")
        return path
    environment_font = os.getenv("EDITORIAL_ANNOTATION_FONT")
    if environment_font:
        path = Path(environment_font).expanduser()
        if path.is_file():
            return path
        raise RuntimeError(f"EDITORIAL_ANNOTATION_FONT does not exist: {path}")

    group = font_group(language, sample_text)
    for value in [*FONT_GROUPS.get(group, []), *FONT_GROUPS["universal"]]:
        path = Path(value)
        if path.is_file():
            return path
    try:
        for query in [*FONT_QUERIES.get(group, []), *FONT_QUERIES["universal"]]:
            result = subprocess.run(
                ["fc-match", query, "-f", "%{file}"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            ).stdout.strip()
            if result and Path(result).is_file():
                return Path(result)
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    raise RuntimeError(
        f"No local font found for annotation language {language!r}. "
        "Pass --font or set EDITORIAL_ANNOTATION_FONT."
    )


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 5 or not isinstance(data.get("shots"), list):
        raise ValueError("Expected a version 5 manifest with shots.")
    return data


def has_raqm(features) -> bool:
    try:
        return bool(features.check("raqm"))
    except Exception:
        return False


def direction_kwargs(language: str, features) -> dict[str, str]:
    if language_prefix(language) in RTL_LANGS and has_raqm(features):
        return {"direction": "rtl"}
    return {}


def font_for(ImageFont, features, path: Path, size: int):
    kwargs: dict[str, Any] = {}
    if has_raqm(features) and hasattr(ImageFont, "Layout"):
        kwargs["layout_engine"] = ImageFont.Layout.RAQM
    return ImageFont.truetype(str(path), max(10, size), **kwargs)


def is_cjk(language: str, text: str) -> bool:
    if language_prefix(language) in {"zh", "ja", "ko"}:
        return True
    return any("\u4e00" <= character <= "\u9fff" for character in text)


def text_width(draw, text: str, font, kwargs: dict[str, str]) -> float:
    if not text:
        return 0
    box = draw.textbbox((0, 0), text, font=font, **kwargs)
    return box[2] - box[0]


def wrap_text(draw, text: str, font, max_width: int, language: str, kwargs: dict[str, str]) -> list[str]:
    if not text:
        return []
    tokens = list(text) if is_cjk(language, text) else text.split()
    separator = "" if is_cjk(language, text) else " "
    lines: list[str] = []
    current = ""
    for token in tokens:
        candidate = token if not current else current + separator + token
        if text_width(draw, candidate, font, kwargs) <= max_width or not current:
            current = candidate
        else:
            lines.append(current)
            current = token
    if current:
        lines.append(current)
    return lines


def fit_wrapped_text(
    mods,
    text: str,
    font_path: Path,
    language: str,
    max_width: int,
    max_lines: int,
    start_size: int,
    min_size: int,
):
    Image, ImageDraw, _, ImageFont, _, features = mods
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    kwargs = direction_kwargs(language, features)
    for size in range(start_size, min_size - 1, -1):
        font = font_for(ImageFont, features, font_path, size)
        lines = wrap_text(probe, text, font, max_width, language, kwargs)
        if len(lines) <= max_lines:
            return font, lines, kwargs
    font = font_for(ImageFont, features, font_path, min_size)
    lines = wrap_text(probe, text, font, max_width, language, kwargs)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        if lines:
            lines[-1] = lines[-1].rstrip("…") + "…"
    return font, lines, kwargs


def draw_lines(draw, xy: tuple[int, int], lines: list[str], font, fill: str, spacing: int, kwargs: dict[str, str]) -> int:
    x, y = xy
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=fill, **kwargs)
        box = draw.textbbox((x, current_y), line, font=font, **kwargs)
        current_y = box[3] + spacing
    return current_y


def add_panel(mods, canvas, box: tuple[int, int, int, int], radius: int, fill, outline, shadow_offset: int = 6):
    Image, ImageDraw, ImageFilter, _, _, _ = mods
    x1, y1, x2, y2 = box
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (x1 + shadow_offset, y1 + shadow_offset, x2 + shadow_offset, y2 + shadow_offset),
        radius=radius,
        fill=(57, 39, 22, 50),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(max(3, radius // 5))))
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=max(1, radius // 8))


def header_box(width: int, height: int, layout: str) -> tuple[int, int, int, int]:
    margin_x = round(width * 0.04)
    top = round(height * 0.035)
    bottom = round(height * (0.235 if layout == "hero-explainer" else 0.215))
    return margin_x, top, width - margin_x, bottom


def card_boxes(width: int, height: int, layout: str, count: int) -> list[tuple[int, int, int, int]]:
    margin = round(width * 0.04)
    gap = round(width * 0.014)
    if layout == "mechanism-focus":
        x1 = round(width * 0.665)
        x2 = width - margin
        top = round(height * 0.25)
        bottom = height - round(height * 0.04)
        total_gap = gap * (count - 1)
        card_height = (bottom - top - total_gap) // count
        return [
            (x1, top + index * (card_height + gap), x2, top + index * (card_height + gap) + card_height)
            for index in range(count)
        ]

    top = round(height * (0.735 if layout == "hero-explainer" else 0.72))
    bottom = height - round(height * 0.035)
    available = width - margin * 2 - gap * (count - 1)
    card_width = available // count
    return [
        (margin + index * (card_width + gap), top, margin + index * (card_width + gap) + card_width, bottom)
        for index in range(count)
    ]


def render_header(mods, canvas, shot: dict[str, Any], font_path: Path, language: str):
    _, ImageDraw, _, _, _, features = mods
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    box = header_box(width, height, shot["layout"])
    radius = round(width * 0.012)
    add_panel(mods, canvas, box, radius, (244, 228, 196, 235), (169, 124, 72, 180))
    x1, y1, x2, y2 = box
    padding_x = round(width * 0.018)
    padding_y = round(height * 0.018)
    scale = width / 1600
    kwargs = direction_kwargs(language, features)

    accent_color = ACCENTS.get(shot["explainers"][0]["accent"], shot["explainers"][0]["accent"])
    draw.rounded_rectangle(
        (x1 + padding_x, y1 + padding_y, x1 + padding_x + round(width * 0.035), y1 + padding_y + max(5, round(height * 0.007))),
        radius=3,
        fill=accent_color,
    )
    eyebrow_font = font_for(mods[3], features, font_path, round(19 * scale))
    draw.text(
        (x1 + padding_x + round(width * 0.045), y1 + padding_y - round(height * 0.004)),
        shot["eyebrow"],
        font=eyebrow_font,
        fill=accent_color,
        **kwargs,
    )

    content_width = x2 - x1 - padding_x * 2
    headline_font, headline_lines, headline_kwargs = fit_wrapped_text(
        mods,
        shot["headline"],
        font_path,
        language,
        content_width,
        2,
        round(44 * scale),
        round(28 * scale),
    )
    headline_y = y1 + padding_y + round(height * 0.035)
    next_y = draw_lines(
        draw,
        (x1 + padding_x, headline_y),
        headline_lines,
        headline_font,
        "#2F261F",
        max(2, round(height * 0.006)),
        headline_kwargs,
    )
    sub_font, sub_lines, sub_kwargs = fit_wrapped_text(
        mods,
        shot["subheadline"],
        font_path,
        language,
        content_width,
        2,
        round(23 * scale),
        round(16 * scale),
    )
    draw_lines(
        draw,
        (x1 + padding_x, min(next_y + round(height * 0.004), y2 - round(height * 0.05))),
        sub_lines,
        sub_font,
        "#6A5542",
        max(2, round(height * 0.004)),
        sub_kwargs,
    )


def render_card(mods, canvas, box, item: dict[str, Any], index: int, font_path: Path, language: str, layout: str):
    _, ImageDraw, _, _, _, features = mods
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    radius = round(width * 0.011)
    add_panel(mods, canvas, box, radius, (246, 232, 205, 242), (177, 137, 86, 190), shadow_offset=max(3, round(width * 0.003)))
    x1, y1, x2, y2 = box
    padding_x = round(width * 0.013)
    padding_y = round(height * 0.013)
    scale = width / 1600
    accent_color = ACCENTS.get(item["accent"], item["accent"])
    kwargs = direction_kwargs(language, features)

    circle_radius = max(10, round(width * 0.011))
    circle_x = x1 + padding_x + circle_radius
    circle_y = y1 + padding_y + circle_radius
    draw.ellipse(
        (circle_x - circle_radius, circle_y - circle_radius, circle_x + circle_radius, circle_y + circle_radius),
        fill=accent_color,
    )
    index_font = font_for(mods[3], features, font_path, max(12, round(17 * scale)))
    index_text = f"{index:02d}"
    index_box = draw.textbbox((0, 0), index_text, font=index_font, **kwargs)
    draw.text(
        (circle_x - (index_box[2] - index_box[0]) / 2, circle_y - (index_box[3] - index_box[1]) / 2 - 1),
        index_text,
        font=index_font,
        fill="#FFF7E7",
        **kwargs,
    )

    text_x = x1 + padding_x
    title_y = y1 + padding_y + circle_radius * 2 + round(height * 0.008)
    max_width = x2 - x1 - padding_x * 2
    start_title = 34 if layout == "result-board" else 28
    title_font, title_lines, title_kwargs = fit_wrapped_text(
        mods,
        item["title"],
        font_path,
        language,
        max_width,
        2,
        round(start_title * scale),
        round(17 * scale),
    )
    body_y = draw_lines(
        draw,
        (text_x, title_y),
        title_lines,
        title_font,
        accent_color,
        max(2, round(height * 0.004)),
        title_kwargs,
    )
    body_font, body_lines, body_kwargs = fit_wrapped_text(
        mods,
        item["body"],
        font_path,
        language,
        max_width,
        3 if layout == "mechanism-focus" else 2,
        round(20 * scale),
        round(13 * scale),
    )
    draw_lines(
        draw,
        (text_x, body_y + round(height * 0.005)),
        body_lines,
        body_font,
        "#5B493A",
        max(2, round(height * 0.004)),
        body_kwargs,
    )


def normalize_aspect(mods, image):
    _, _, _, _, ImageOps, _ = mods
    width, height = image.size
    target_height = round(width * 9 / 16)
    if abs(height - target_height) <= max(2, round(target_height * 0.01)):
        return image
    return ImageOps.fit(image, (width, target_height), method=mods[0].Resampling.LANCZOS, centering=(0.5, 0.5))


def annotate_image(mods, source: Path, target: Path, shot: dict[str, Any], font_path: Path, language: str):
    Image, _, _, _, _, _ = mods
    canvas = normalize_aspect(mods, Image.open(source).convert("RGBA"))
    render_header(mods, canvas, shot, font_path, language)
    boxes = card_boxes(canvas.width, canvas.height, shot["layout"], len(shot["explainers"]))
    for index, (box, item) in enumerate(zip(boxes, shot["explainers"]), start=1):
        render_card(mods, canvas, box, item, index, font_path, language, shot["layout"])
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
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        language = data["article"]["annotation_language"]
        sample_text = " ".join(
            text
            for shot in data["shots"]
            for text in [
                shot["eyebrow"],
                shot["headline"],
                shot["subheadline"],
                *[item["title"] + " " + item["body"] for item in shot["explainers"]],
            ]
        )
        font_path = find_font(args.font, language, sample_text)
        report = {
            "manifest_version": 5,
            "annotation_language": language,
            "font": str(font_path),
            "images": [],
        }
        for shot in data["shots"]:
            source = args.input / shot["filename"]
            target = args.output / shot["filename"]
            if not source.is_file():
                raise FileNotFoundError(source)
            annotate_image(mods, source, target, shot, font_path, language)
            report["images"].append(
                {
                    "path": str(target),
                    "layout": shot["layout"],
                    "explainer_count": len(shot["explainers"]),
                }
            )
        (args.output / "annotation-render-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"Annotated {len(report['images'])} image(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
