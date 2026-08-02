#!/usr/bin/env python3
"""Add deterministic language-aware semantic paper-tag annotations to text-free base images."""
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
RTL_LANGS = {"ar", "fa", "he", "ur", "yi", "ps"}
FONT_GROUPS = {
    "zh": [
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "C:/Windows/Fonts/msjh.ttc", "C:/Windows/Fonts/msjhbd.ttc",
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
        "C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf",
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
        from PIL import Image, ImageDraw, ImageFilter, ImageFont, features
    except ImportError as exc:
        raise RuntimeError("Install Pillow with `python3 -m pip install -r requirements-annotation.txt`.") from exc
    return Image, ImageDraw, ImageFilter, ImageFont, features


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


def find_font(explicit: str | None, language: str = "und", sample_text: str = "") -> Path:
    if explicit:
        path = Path(explicit).expanduser()
        if not path.is_file():
            raise RuntimeError(f"Explicit font does not exist: {path}")
        return path
    env_font = os.getenv("EDITORIAL_ANNOTATION_FONT")
    if env_font:
        path = Path(env_font).expanduser()
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
            value = subprocess.run(
                ["fc-match", query, "-f", "%{file}"], capture_output=True,
                text=True, timeout=5, check=False,
            ).stdout.strip()
            if value and Path(value).is_file():
                return Path(value)
    except (FileNotFoundError, subprocess.SubprocessError):
        pass
    raise RuntimeError(
        f"No local font found for annotation language {language!r}. "
        "Pass --font or set EDITORIAL_ANNOTATION_FONT."
    )


def load_manifest(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 4 or not isinstance(data.get("shots"), list):
        raise ValueError("Expected a version 4 manifest with shots.")
    return data


def norm(value: float, extent: int) -> int:
    return round(float(value) * extent)


def accent(value: str) -> str:
    return ACCENTS.get(value, value)


def has_raqm(features) -> bool:
    try:
        return bool(features.check("raqm"))
    except Exception:
        return False


def font_for(ImageFont, features, path: Path, requested: int, width: int):
    kwargs: dict[str, Any] = {}
    if has_raqm(features) and hasattr(ImageFont, "Layout"):
        kwargs["layout_engine"] = ImageFont.Layout.RAQM
    return ImageFont.truetype(str(path), max(18, round(requested * width / 1600)), **kwargs)


def direction_kwargs(language: str, features) -> dict[str, str]:
    if language_prefix(language) in RTL_LANGS and has_raqm(features):
        return {"direction": "rtl"}
    return {}


def make_tag(mods, text: str, font_path: Path, language: str, spec: dict[str, Any], width: int, headline: bool):
    Image, ImageDraw, ImageFilter, ImageFont, features = mods
    size = int(spec.get("font_size", 42 if headline else 31))
    font = font_for(ImageFont, features, font_path, size, width)
    kwargs = direction_kwargs(language, features)
    probe = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
    box = probe.textbbox((0, 0), text, font=font, **kwargs)
    text_width, text_height = box[2] - box[0], box[3] - box[1]
    padding_x = round(width * (0.017 if headline else 0.012))
    padding_y = round(width * 0.009)
    tag_width = text_width + padding_x * 2
    tag_height = text_height + padding_y * 2 + round(width * 0.006)
    tag = Image.new("RGBA", (tag_width + 16, tag_height + 16), (0, 0, 0, 0))
    shadow = Image.new("RGBA", tag.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle(
        (9, 10, tag_width + 7, tag_height + 7),
        radius=max(7, round(width * .008)), fill=(55, 35, 20, 55),
    )
    tag.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(max(3, round(width * .004)))))
    draw = ImageDraw.Draw(tag)
    randomizer = random.Random(text)
    jitter = [randomizer.randint(-3, 3) for _ in range(8)]
    polygon = [
        (5 + jitter[0], 5 + jitter[1]),
        (tag_width + 6 + jitter[2], 4 + jitter[3]),
        (tag_width + 8 + jitter[4], tag_height + 6 + jitter[5]),
        (6 + jitter[6], tag_height + 7 + jitter[7]),
    ]
    draw.polygon(polygon, fill="#F1DDB1", outline="#B98A4D")
    line_y = tag_height + 1
    draw.line(
        (padding_x, line_y, tag_width - padding_x, line_y - 1),
        fill=accent(spec.get("accent", "ink")), width=max(3, round(width * .003)),
    )
    draw.rectangle((tag_width // 2 - 22, 1, tag_width // 2 + 22, 11), fill=(211, 170, 97, 110))
    draw.text(
        (padding_x, padding_y - 1), text, font=font, fill="#49382B",
        stroke_width=1, stroke_fill="#FFF5DC", **kwargs,
    )
    angle = float(spec.get("angle", 0))
    return tag.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC) if angle else tag


def line_to_target(ImageDraw, canvas, start: tuple[int, int], target: tuple[int, int], color: str, seed: str):
    draw = ImageDraw.Draw(canvas)
    randomizer = random.Random(seed)
    x1, y1 = start
    x2, y2 = target
    middle_x = (x1 + x2) // 2 + randomizer.randint(-10, 10)
    middle_y = (y1 + y2) // 2 + randomizer.randint(-8, 8)
    width = max(3, round(canvas.width * .0025))
    draw.line([(x1, y1), (middle_x, middle_y), (x2, y2)], fill=color, width=width, joint="curve")
    radius = max(5, round(canvas.width * .0035))
    draw.ellipse((x2 - radius, y2 - radius, x2 + radius, y2 + radius), fill=color)


def place(mods, canvas, tag, spec: dict[str, Any], callout: bool):
    _, ImageDraw, _, _, _ = mods
    x, y = norm(spec["x"], canvas.width), norm(spec["y"], canvas.height)
    margin = max(5, round(canvas.width * .006))
    x = min(max(margin, x), max(margin, canvas.width - tag.width - margin))
    y = min(max(margin, y), max(margin, canvas.height - tag.height - margin))
    if callout:
        target_x, target_y = norm(spec["target_x"], canvas.width), norm(spec["target_y"], canvas.height)
        line_x = x + (0 if target_x < x else tag.width if target_x > x + tag.width else tag.width // 2)
        line_y = y + tag.height // 2
        line_to_target(
            ImageDraw, canvas, (line_x, line_y), (target_x, target_y),
            accent(spec.get("accent", "ink")), spec["text"],
        )
    canvas.alpha_composite(tag, (x, y))


def annotate(mods, image_path: Path, output_path: Path, annotation: dict[str, Any], font_path: Path, language: str):
    Image, _, _, _, _ = mods
    canvas = Image.open(image_path).convert("RGBA")
    headline = annotation["headline"]
    place(
        mods, canvas,
        make_tag(mods, headline["text"], font_path, language, headline, canvas.width, True),
        headline, False,
    )
    for label in annotation["labels"]:
        place(
            mods, canvas,
            make_tag(mods, label["text"], font_path, language, label, canvas.width, False),
            label, True,
        )
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
        data, mods = load_manifest(args.manifest), pillow()
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        article_language = data["article"]["annotation_language"]
        report = {"manifest_version": data["version"], "article_annotation_language": article_language, "images": []}
        for shot in data["shots"]:
            annotation = shot.get("annotation", {})
            if not annotation.get("enabled"):
                continue
            if annotation.get("layout_status") != "final" and not args.allow_draft:
                raise ValueError(f"Shot {shot['id']} annotation layout is not final.")
            language = annotation.get("language") or article_language
            texts = " ".join([
                (annotation.get("headline") or {}).get("text", ""),
                *[
                    item.get("text", "")
                    for item in annotation.get("labels", [])
                    if isinstance(item, dict)
                ],
            ])
            font_path = find_font(args.font, language, texts)
            source = args.input / shot["filename"]
            target = args.output / shot["filename"]
            if not source.is_file():
                raise FileNotFoundError(source)
            annotate(mods, source, target, annotation, font_path, language)
            report["images"].append({
                "path": str(target),
                "language": language,
                "font": str(font_path),
                "semantic_contract": shot.get("semantic_contract", {}),
            })
        (args.output / "annotation-render-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        print(f"Annotated {len(report['images'])} image(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
