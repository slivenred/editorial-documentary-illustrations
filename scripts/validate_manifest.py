#!/usr/bin/env python3
"""Validate an Editorial Documentary Illustrations version 6 manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from recommend_image_count import recommend_count

LANGUAGE = re.compile(r"^[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*$")
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHOT_ID = re.compile(r"^[0-9]{2}$")
FILENAME = re.compile(r"^[0-9]{2}-[a-z0-9-]+\.png$")
IMAGE_ROLES = {"hero", "inline"}
LAYOUTS = {
    "hero-comparison", "hybrid-stack-tableau", "mechanism-tableau",
    "growing-burden-comparison", "process-journey",
    "before-after-tableau", "timeline-route",
}
ACCENTS = {"ink", "terracotta", "indigo", "sage", "ochre", "brick"}
TITLE_COVERAGE = {"claim", "key_result", "mechanism"}
GENERIC_HEADLINES = {
    "流程", "重點", "系統架構", "系統架構圖", "結果", "圖解", "overview",
    "workflow", "architecture", "diagram", "process", "results",
}


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", unicodedata.normalize("NFKC", value or "").strip().casefold())


def has_cjk(value: str) -> bool:
    return any("\u3400" <= ch <= "\u9fff" for ch in value)


def claim_overlap(claim: str, target: str) -> bool:
    left, right = norm(claim), norm(target)
    if not left or not right:
        return False
    if left in right or right in left:
        return True
    if has_cjk(left):
        compact = re.sub(r"[^\u3400-\u9fffA-Za-z0-9]", "", left)
        return any(compact[i:i + 4] in right for i in range(max(0, len(compact) - 3)))
    left_tokens = {token for token in re.findall(r"[a-z0-9]+", left) if len(token) >= 4}
    right_tokens = set(re.findall(r"[a-z0-9]+", right))
    return bool(left_tokens & right_tokens)


def require_obj(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> dict[str, Any]:
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


def require_text(parent: dict[str, Any], key: str, path: str, errors: list[str], minimum: int = 1) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"`{path}.{key}` must be text of at least {minimum} characters.")
        return ""
    return value.strip()


def validate_manifest(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Manifest root must be an object."], warnings
    if data.get("version") != 6:
        errors.append("`version` must be the integer 6.")

    article = require_obj(data, "article", "root", errors)
    require_text(article, "title", "article", errors)
    slug = require_text(article, "slug", "article", errors)
    if slug and not SLUG.fullmatch(slug):
        errors.append("`article.slug` must be lowercase kebab-case.")
    for key in ("language", "annotation_language"):
        language = require_text(article, key, "article", errors, 2)
        if language and not LANGUAGE.fullmatch(language):
            errors.append(f"`article.{key}` must be a concrete BCP 47 tag.")
    require_text(article, "summary", "article", errors, 20)
    reading_minutes = article.get("reading_minutes")
    if isinstance(reading_minutes, bool) or not isinstance(reading_minutes, (int, float)) or not 0 < float(reading_minutes) <= 120:
        errors.append("`article.reading_minutes` must be a positive number up to 120.")
        reading_minutes = 1
    include_hero = article.get("include_hero")
    if not isinstance(include_hero, bool):
        errors.append("`article.include_hero` must be boolean.")
        include_hero = True
    anchors = article.get("high_value_anchor_count")
    if not isinstance(anchors, int) or not 1 <= anchors <= 20:
        errors.append("`article.high_value_anchor_count` must be 1–20.")
        anchors = 1
    target_count = article.get("target_count")
    if not isinstance(target_count, int) or not 1 <= target_count <= 7:
        errors.append("`article.target_count` must be 1–7.")
        target_count = 1
    expected_count = recommend_count(float(reading_minutes), anchors, include_hero)
    if target_count != expected_count:
        errors.append(
            f"`article.target_count` must equal the automatic recommendation ({expected_count}) "
            f"for {reading_minutes} reading minutes and {anchors} high-value anchors."
        )

    contract = require_obj(article, "title_contract", "article", errors)
    claim = require_text(contract, "claim", "article.title_contract", errors, 8)
    require_text(contract, "key_result", "article.title_contract", errors, 4)
    require_text(contract, "mechanism", "article.title_contract", errors, 4)

    vb = require_obj(data, "visual_bible", "root", errors)
    for key, minimum in (
        ("background", 20), ("border", 10), ("typography", 20),
        ("scene_style", 20), ("lighting", 10), ("label_style", 15),
        ("takeaway_style", 10),
    ):
        require_text(vb, key, "visual_bible", errors, minimum)
    palette = require_list(vb, "palette", "visual_bible", errors)
    if not 4 <= len(palette) <= 7:
        errors.append("`visual_bible.palette` must contain 4–7 items.")
    continuity = require_list(vb, "continuity_rules", "visual_bible", errors)
    if not 5 <= len(continuity) <= 12:
        errors.append("`visual_bible.continuity_rules` must contain 5–12 items.")
    layout_contract = require_obj(vb, "layout_contract", "visual_bible", errors)
    if layout_contract.get("canvas_width") != 1600 or layout_contract.get("canvas_height") != 900:
        errors.append("The version 6 layout contract requires a 1600x900 canvas.")
    margin = layout_contract.get("outer_margin_px")
    if not isinstance(margin, int) or not 64 <= margin <= 140:
        errors.append("`visual_bible.layout_contract.outer_margin_px` must be 64–140.")
    if layout_contract.get("allow_text_over_subject") is not False:
        errors.append("`allow_text_over_subject` must be false.")
    if layout_contract.get("allow_overflow") is not False:
        errors.append("`allow_overflow` must be false.")
    if layout_contract.get("max_labels") not in {2, 3, 4}:
        errors.append("`max_labels` must be 2–4.")

    shots = require_list(data, "shots", "root", errors)
    if len(shots) != target_count:
        errors.append("The number of shots must equal `article.target_count`.")

    ids: list[str] = []
    filenames: list[str] = []
    hero_indexes: list[int] = []
    inline_indices: list[int] = []

    for index, shot in enumerate(shots):
        path = f"shots[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"`{path}` must be an object.")
            continue
        sid = require_text(shot, "id", path, errors)
        ids.append(sid)
        if sid and not SHOT_ID.fullmatch(sid):
            errors.append(f"`{path}.id` must use two digits.")
        role = require_text(shot, "image_role", path, errors)
        if role not in IMAGE_ROLES:
            errors.append(f"`{path}.image_role` must be hero or inline.")
        if role == "hero":
            hero_indexes.append(index)
        layout = require_text(shot, "layout", path, errors)
        if layout not in LAYOUTS:
            errors.append(f"Unsupported layout at `{path}`.")

        placement = require_obj(shot, "placement", path, errors)
        require_text(placement, "section_heading", f"{path}.placement", errors)
        paragraph_index = placement.get("after_paragraph_global_index")
        if not isinstance(paragraph_index, int) or paragraph_index < 0:
            errors.append(f"`{path}.placement.after_paragraph_global_index` must be a non-negative integer.")
            paragraph_index = 0
        if role == "hero" and paragraph_index != 0:
            errors.append("The hero must be placed immediately after the article title with paragraph index 0.")
        if role == "inline":
            if paragraph_index == 0:
                errors.append(f"Inline shot `{sid}` must be placed after a body paragraph.")
            inline_indices.append(paragraph_index)
        require_text(placement, "after_paragraph_excerpt", f"{path}.placement", errors, 8)
        require_text(placement, "reason", f"{path}.placement", errors, 12)

        score = require_obj(shot, "anchor_score", path, errors)
        score_total = 0
        for key in (
            "comprehension_gain", "visual_structure", "context_specificity",
            "non_redundancy", "placement_value",
        ):
            value = score.get(key)
            if not isinstance(value, int) or not 0 <= value <= 2:
                errors.append(f"`{path}.anchor_score.{key}` must be 0–2.")
            else:
                score_total += value
        if score_total < 7:
            errors.append(f"`{path}` anchor score must total at least 7; got {score_total}.")

        core_idea = require_text(shot, "core_idea", path, errors, 10)
        require_text(shot, "eyebrow", path, errors, 0)
        headline = require_text(shot, "headline", path, errors, 4)
        subheadline = require_text(shot, "subheadline", path, errors, 8)
        if len(headline) > 90:
            errors.append(f"`{path}.headline` must be ≤90 characters.")
        if len(subheadline) > 150:
            errors.append(f"`{path}.subheadline` must be ≤150 characters.")
        if norm(headline) in GENERIC_HEADLINES:
            errors.append(f"`{path}.headline` is generic; write a conclusion or judgment.")
        require_text(shot, "scene", path, errors, 60)
        elements = require_list(shot, "scene_elements", path, errors)
        if not 2 <= len(elements) <= 8:
            errors.append(f"`{path}.scene_elements` must contain 2–8 items.")
        labels = require_list(shot, "labels", path, errors)
        if not 2 <= len(labels) <= 4:
            errors.append(f"`{path}.labels` must contain 2–4 items.")
        label_texts: list[str] = []
        for label_index, label in enumerate(labels):
            label_path = f"{path}.labels[{label_index}]"
            if not isinstance(label, dict):
                errors.append(f"`{label_path}` must be an object.")
                continue
            text = require_text(label, "text", label_path, errors)
            label_texts.append(norm(text))
            require_text(label, "meaning", label_path, errors, 3)
            accent = require_text(label, "accent", label_path, errors)
            if accent not in ACCENTS:
                errors.append(f"`{label_path}.accent` is unsupported.")
        if len(set(label_texts)) != len(label_texts):
            errors.append(f"`{path}` repeats label text.")
        for key in ("bottom_takeaway", "caveat"):
            value = shot.get(key)
            if not isinstance(value, str) or len(value) > 140:
                errors.append(f"`{path}.{key}` must be a string ≤140 characters.")
        if not isinstance(shot.get("people_required"), bool):
            errors.append(f"`{path}.people_required` must be boolean.")
        coverage = require_list(shot, "title_coverage", path, errors)
        if any(item not in TITLE_COVERAGE for item in coverage):
            errors.append(f"`{path}.title_coverage` contains an unsupported value.")
        if role == "hero":
            if "claim" not in coverage or len(coverage) < 2:
                errors.append("The hero must cover `claim` plus `key_result` or `mechanism`.")
            if claim and not claim_overlap(claim, f"{headline} {subheadline} {core_idea}"):
                errors.append("The hero headline/subheadline/core idea must visibly align with `title_contract.claim`.")
        elif coverage:
            warnings.append(f"Inline shot `{sid}` normally leaves `title_coverage` empty.")

        filename = require_text(shot, "filename", path, errors)
        filenames.append(filename)
        if filename and not FILENAME.fullmatch(filename):
            errors.append(f"`{path}.filename` must be a two-digit lowercase kebab-case PNG.")
        if sid and filename and not filename.startswith(sid + "-"):
            errors.append(f"`{path}.filename` must start with `{sid}-`.")
        alt = require_text(shot, "alt_text", path, errors, 12)
        if len(alt) > 240:
            errors.append(f"`{path}.alt_text` must be ≤240 characters.")
        caption = shot.get("caption")
        if not isinstance(caption, str) or len(caption) > 300:
            errors.append(f"`{path}.caption` must be a string ≤300 characters.")

    if include_hero:
        if hero_indexes != [0]:
            errors.append("When `include_hero` is true, exactly one hero must be the first shot.")
    elif hero_indexes:
        errors.append("No hero shot is allowed when `include_hero` is false.")

    if inline_indices != sorted(inline_indices):
        errors.append("Inline shots must be ordered by `after_paragraph_global_index`.")
    for previous, current in zip(inline_indices, inline_indices[1:]):
        if current == previous:
            errors.append("Two inline shots cannot use the same paragraph position.")
        elif current - previous < 2:
            warnings.append("Two inline shots are fewer than two paragraphs apart; confirm the reading rhythm.")

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
