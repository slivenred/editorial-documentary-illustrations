#!/usr/bin/env python3
"""Validate an Editorial Documentary Illustrations version 5 manifest."""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
RECOMMENDER = ROOT / "scripts" / "recommend_image_count.py"

LANGUAGE = re.compile(r"^(?:[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*|mul|und)$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHOT_ID = re.compile(r"^[0-9]{2}$")
FILENAME = re.compile(r"^[0-9]{2}-[a-z0-9-]+\.png$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
CAMERAS = {"top-down-map-15deg", "flat-orthographic", "soft-isometric"}
PURPOSES = {"overview", "mechanism", "process", "comparison", "timeline", "evidence", "result"}
LAYOUTS = {
    "hero-explainer", "mechanism-focus", "process-strip",
    "comparison-split", "timeline-route", "result-board",
}
ACCENTS = {"ink", "terracotta", "ochre", "sage", "indigo", "brick"}
GENERIC_HEADLINES = {
    "重點", "重點整理", "流程", "流程圖", "結果", "系統架構", "系統架構圖",
    "overview", "workflow", "process", "result", "architecture", "key points",
}
EXPECTED_LAYOUT = {
    "overview": "hero-explainer",
    "mechanism": "mechanism-focus",
    "process": "process-strip",
    "comparison": "comparison-split",
    "timeline": "timeline-route",
    "result": "result-board",
}


def load_recommender():
    spec = importlib.util.spec_from_file_location("image_count_recommender", RECOMMENDER)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {RECOMMENDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value or "").strip().casefold())


def require_dict(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{path}.{key}` must be an object.")
        return {}
    return value


def require_list(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"`{path}.{key}` must be an array.")
        return []
    return value


def require_text(
    parent: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    minimum: int = 1,
    maximum: int | None = None,
) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"`{path}.{key}` must be text of at least {minimum} characters.")
        return ""
    value = value.strip()
    if maximum is not None and len(value) > maximum:
        errors.append(f"`{path}.{key}` must be at most {maximum} characters.")
    return value


def require_language(parent: dict[str, Any], key: str, path: str, errors: list[str], *, allow_und=False, allow_mul=False) -> str:
    value = require_text(parent, key, path, errors, 2)
    lower = value.casefold()
    invalid = lower in {"auto", "detect", "automatic"} or not LANGUAGE.fullmatch(value)
    invalid = invalid or (lower == "und" and not allow_und) or (lower == "mul" and not allow_mul)
    if value and invalid:
        errors.append(f"`{path}.{key}` must be a resolved BCP 47 language tag, not {value!r}.")
    return value


def require_int(parent: dict[str, Any], key: str, path: str, errors: list[str], low: int, high: int) -> int | None:
    value = parent.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or not low <= value <= high:
        errors.append(f"`{path}.{key}` must be an integer from {low} to {high}.")
        return None
    return value


def require_number(parent: dict[str, Any], key: str, path: str, errors: list[str], low: float, high: float) -> float | None:
    value = parent.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= float(value) <= high:
        errors.append(f"`{path}.{key}` must be a number from {low} to {high}.")
        return None
    return float(value)


def anchor_matches(anchor: str, context: str) -> bool:
    left = normalize(anchor)
    right = normalize(context)
    if not left or not right:
        return False
    if left in right or right in left:
        return True
    left_bigrams = {left[index:index + 2] for index in range(max(0, len(left) - 1))}
    right_bigrams = {right[index:index + 2] for index in range(max(0, len(right) - 1))}
    if not left_bigrams:
        return False
    return len(left_bigrams & right_bigrams) / len(left_bigrams) >= 0.35


def validate_manifest(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Manifest root must be an object."], warnings
    if data.get("version") != 5:
        errors.append("`version` must be the integer 5.")

    article = require_dict(data, "article", "root", errors)
    require_text(article, "title", "article", errors)
    slug = require_text(article, "slug", "article", errors)
    if slug and not SLUG.fullmatch(slug):
        errors.append("`article.slug` must be lowercase kebab-case.")
    source_language = require_language(article, "language", "article", errors, allow_und=True, allow_mul=True)
    annotation_language = require_language(article, "annotation_language", "article", errors, allow_mul=True)
    require_text(article, "summary", "article", errors, 20, 500)
    reading_minutes = require_number(article, "reading_minutes", "article", errors, 0.1, 120)
    section_count = require_int(article, "section_count", "article", errors, 1, 100)
    image_count_mode = require_text(article, "image_count_mode", "article", errors)
    if image_count_mode not in {"auto", "fixed"}:
        errors.append("`article.image_count_mode` must be `auto` or `fixed`.")
    include_hero = article.get("include_hero")
    if not isinstance(include_hero, bool):
        errors.append("`article.include_hero` must be boolean.")
    anchor_count = require_int(article, "high_value_anchor_count", "article", errors, 1, 30)
    target_count = require_int(article, "target_count", "article", errors, 1, 8)
    require_text(article, "count_reason", "article", errors, 12, 320)
    if source_language == "mul" and annotation_language != "mul":
        warnings.append("The article is multilingual; confirm the single annotation language is intentional.")

    visual_bible = require_dict(data, "visual_bible", "root", errors)
    require_text(visual_bible, "background", "visual_bible", errors, 20)
    palette = require_list(visual_bible, "palette", "visual_bible", errors)
    if not 4 <= len(palette) <= 7:
        errors.append("`visual_bible.palette` must contain 4–7 items.")
    camera = require_text(visual_bible, "camera", "visual_bible", errors)
    if camera not in CAMERAS:
        errors.append("Unsupported `visual_bible.camera`.")
    require_text(visual_bible, "lighting", "visual_bible", errors, 10)
    require_text(visual_bible, "cutout_style", "visual_bible", errors, 20)
    require_text(visual_bible, "typography", "visual_bible", errors, 20)
    continuity = require_list(visual_bible, "continuity_rules", "visual_bible", errors)
    if not 4 <= len(continuity) <= 12:
        errors.append("`visual_bible.continuity_rules` must contain 4–12 items.")

    shots = require_list(data, "shots", "root", errors)
    if not 1 <= len(shots) <= 8:
        errors.append("`shots` must contain 1–8 items.")
    if isinstance(target_count, int) and len(shots) != target_count:
        errors.append("`article.target_count` must equal the number of shots.")

    if (
        image_count_mode == "auto"
        and reading_minutes is not None
        and anchor_count is not None
        and section_count is not None
        and isinstance(include_hero, bool)
        and target_count is not None
    ):
        recommended = load_recommender().recommend_count(
            reading_minutes, anchor_count, section_count, include_hero
        )["recommended_total"]
        if target_count != recommended:
            errors.append(
                f"Auto image count recommends {recommended}, but `article.target_count` is {target_count}. "
                "Change the anchor count or use `image_count_mode: fixed` for an explicit override."
            )

    ids: list[str] = []
    filenames: list[str] = []
    hero_indexes: list[int] = []
    inline_paragraph_indexes: list[int] = []
    placement_keys: list[tuple[int, int]] = []

    for index, shot in enumerate(shots):
        path = f"shots[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"`{path}` must be an object.")
            continue
        shot_id = require_text(shot, "id", path, errors)
        ids.append(shot_id)
        if shot_id and not SHOT_ID.fullmatch(shot_id):
            errors.append(f"`{path}.id` must use two digits.")
        kind = require_text(shot, "kind", path, errors)
        if kind not in {"hero", "inline"}:
            errors.append(f"`{path}.kind` must be `hero` or `inline`.")
        if kind == "hero":
            hero_indexes.append(index)

        placement = require_dict(shot, "placement", path, errors)
        require_text(placement, "section_heading", f"{path}.placement", errors, 1, 180)
        section_index = require_int(placement, "section_index", f"{path}.placement", errors, 0, 100)
        paragraph_index = require_int(placement, "after_paragraph_index", f"{path}.placement", errors, 0, 1000)
        require_text(placement, "after_paragraph_excerpt", f"{path}.placement", errors, 5, 240)
        require_text(placement, "reason", f"{path}.placement", errors, 10, 280)
        if section_index is not None and paragraph_index is not None:
            placement_keys.append((section_index, paragraph_index))
        if kind == "hero" and paragraph_index not in {None, 0}:
            errors.append(f"`{path}` hero must use `after_paragraph_index: 0`.")
        if kind == "inline" and paragraph_index is not None:
            if paragraph_index < 1:
                errors.append(f"`{path}` inline image must follow a real paragraph.")
            inline_paragraph_indexes.append(paragraph_index)

        purpose = require_text(shot, "purpose", path, errors)
        if purpose not in PURPOSES:
            errors.append(f"Unsupported purpose at `{path}`.")
        layout = require_text(shot, "layout", path, errors)
        if layout not in LAYOUTS:
            errors.append(f"Unsupported layout at `{path}`.")
        expected_layout = EXPECTED_LAYOUT.get(purpose)
        if expected_layout and layout != expected_layout:
            warnings.append(
                f"`{path}` purpose `{purpose}` usually uses `{expected_layout}`, not `{layout}`."
            )
        if kind == "hero" and layout != "hero-explainer":
            warnings.append(f"`{path}` hero usually uses `hero-explainer`.")

        require_text(shot, "eyebrow", path, errors, 1, 40)
        headline = require_text(shot, "headline", path, errors, 4, 90)
        if normalize(headline) in GENERIC_HEADLINES:
            errors.append(f"`{path}.headline` is generic; write a conclusion or relationship.")
        require_text(shot, "subheadline", path, errors, 8, 180)
        visual_story = require_text(shot, "visual_story", path, errors, 40, 1200)
        key_elements = require_list(shot, "key_elements", path, errors)
        if not 2 <= len(key_elements) <= 6:
            errors.append(f"`{path}.key_elements` must contain 2–6 items.")
        if len({normalize(str(value)) for value in key_elements}) != len(key_elements):
            errors.append(f"`{path}.key_elements` contains duplicates.")

        explainers = require_list(shot, "explainers", path, errors)
        if not 2 <= len(explainers) <= 4:
            errors.append(f"`{path}.explainers` must contain 2–4 items.")
        explainer_titles: list[str] = []
        context = visual_story + " " + " ".join(str(value) for value in key_elements)
        for explainer_index, explainer in enumerate(explainers):
            item_path = f"{path}.explainers[{explainer_index}]"
            if not isinstance(explainer, dict):
                errors.append(f"`{item_path}` must be an object.")
                continue
            title = require_text(explainer, "title", item_path, errors, 1, 60)
            explainer_titles.append(normalize(title))
            require_text(explainer, "body", item_path, errors, 4, 150)
            accent = require_text(explainer, "accent", item_path, errors)
            if accent not in ACCENTS and not HEX.fullmatch(accent):
                errors.append(f"`{item_path}.accent` is unsupported.")
            anchor = require_text(explainer, "visual_anchor", item_path, errors, 3, 160)
            if anchor and context and not anchor_matches(anchor, context):
                warnings.append(
                    f"`{item_path}.visual_anchor` is not clearly present in `visual_story` or `key_elements`."
                )
        if len(set(explainer_titles)) != len(explainer_titles):
            errors.append(f"`{path}` repeats explainer titles.")

        motion_cues = require_list(shot, "motion_cues", path, errors)
        if not 1 <= len(motion_cues) <= 4:
            errors.append(f"`{path}.motion_cues` must contain 1–4 items.")
        filename = require_text(shot, "filename", path, errors)
        filenames.append(filename)
        if filename and not FILENAME.fullmatch(filename):
            errors.append(f"`{path}.filename` must be lowercase kebab-case PNG.")
        if shot_id and filename and not filename.startswith(shot_id + "-"):
            errors.append(f"`{path}.filename` must start with `{shot_id}-`.")
        require_text(shot, "alt_text", path, errors, 12, 240)
        caption = shot.get("caption")
        if not isinstance(caption, str) or len(caption) > 300:
            errors.append(f"`{path}.caption` must be text of at most 300 characters.")

    if isinstance(include_hero, bool):
        if include_hero and hero_indexes != [0]:
            errors.append("When `article.include_hero` is true, exactly one hero must be the first shot.")
        if not include_hero and hero_indexes:
            errors.append("When `article.include_hero` is false, no shot may use `kind: hero`.")

    if len(set(placement_keys)) != len(placement_keys):
        errors.append("Two shots use the same section and paragraph placement.")
    for previous, current in zip(inline_paragraph_indexes, inline_paragraph_indexes[1:]):
        if current <= previous:
            errors.append("Inline image paragraph indexes must increase through the article.")
        elif current - previous < 2:
            errors.append("Inline images must be separated by at least two paragraph indexes.")

    for label, values in (("shot id", ids), ("filename", filenames)):
        duplicates = [value for value, count in Counter(values).items() if value and count > 1]
        if duplicates:
            errors.append(f"Duplicate {label}(s): {', '.join(duplicates)}.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    errors, warnings = validate_manifest(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"OK: {args.manifest} — {len(data['shots'])} shot(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
