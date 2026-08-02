#!/usr/bin/env python3
"""Validate a version 4 Editorial Documentary Illustrations manifest."""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any

CAMERAS = {"top-down-map-15deg", "flat-orthographic", "soft-isometric"}
ARTICLE_TYPES = {
    "technical-research", "product-or-company", "historical", "policy-or-economy",
    "social-or-cultural", "process-or-howto", "general",
}
IMAGE_ROLES = {"hero", "inline"}
VISUALIZATION_MODES = {"literal-technical", "literal-scene", "hybrid-metaphor", "abstract-metaphor"}
ROLES = {
    "process-station", "route-network", "timeline-journey", "before-after",
    "scale-up-crowd", "cutaway-mechanism", "ecosystem-tableau", "physical-metaphor",
    "evidence-chain", "origin-map", "technical-mechanism", "architecture-stack",
    "resource-contrast", "claim-comparison",
}
TECHNICAL_ROLES = {"technical-mechanism", "architecture-stack", "resource-contrast", "claim-comparison"}
DENSITIES = {"low", "medium", "high", "resolved-medium"}
ACCENTS = {"ink", "terracotta", "ochre", "sage", "indigo", "brick"}
GENERIC_SIGNATURE = {
    "ai", "artificial intelligence", "model", "models", "system", "systems", "data",
    "speed", "performance", "efficiency", "technology", "software", "hardware", "network",
    "process", "workflow", "machine", "people", "flow", "memory",
    "人工智慧", "人工智能", "模型", "系統", "系统", "資料", "数据", "速度", "效能", "性能",
    "技術", "技术", "流程", "網路", "网络", "記憶體", "内存", "效率",
}
GENERIC_LABELS = {
    "流程", "結果", "重點", "系統", "資料", "工作流程", "系統架構圖", "重點整理",
    "flow", "workflow", "process", "result", "results", "key point", "key points",
    "system", "data", "overview", "diagram", "architecture",
}
TECHNICAL_GENERIC_OBJECTS = {
    "office workers", "workers around", "factory", "server city", "unrelated city",
    "generic robot", "glowing brain", "decorative gears", "server tower",
}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHOT_ID = re.compile(r"^[0-9]{2}$")
FILENAME = re.compile(r"^[0-9]{2}-[a-z0-9-]+\.png$")
LANGUAGE = re.compile(r"^(?:[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*|und|mul)$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "").strip().casefold()
    return re.sub(r"\s+", " ", value)


def terms_overlap(first: list[str], second: list[str]) -> set[str]:
    """Return source terms that materially appear in the comparison values."""
    matches: set[str] = set()
    right = [normalized(value) for value in second if isinstance(value, str) and value.strip()]
    for original in first:
        if not isinstance(original, str) or not original.strip():
            continue
        left = normalized(original)
        if any(left == item or (len(left) >= 3 and left in item) or (len(item) >= 3 and item in left) for item in right):
            matches.add(original)
    return matches


def _dict(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{path}.{key}` must be an object.")
        return {}
    return value


def _list(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"`{path}.{key}` must be an array.")
        return []
    return value


def _text(parent: dict[str, Any], key: str, path: str, errors: list[str], minimum: int = 1) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"`{path}.{key}` must be a string of at least {minimum} characters.")
        return ""
    return value.strip()


def _strings(parent: dict[str, Any], key: str, path: str, errors: list[str], low: int, high: int) -> list[str]:
    values = _list(parent, key, path, errors)
    if not low <= len(values) <= high:
        errors.append(f"`{path}.{key}` must contain {low}–{high} items.")
    result: list[str] = []
    for index, value in enumerate(values):
        if not isinstance(value, str) or not value.strip():
            errors.append(f"`{path}.{key}[{index}]` must be meaningful text.")
        else:
            result.append(value.strip())
    return result


def _language(parent: dict[str, Any], key: str, path: str, errors: list[str], *, allow_und=False, allow_mul=False) -> str:
    value = _text(parent, key, path, errors, 2)
    lower = value.casefold()
    invalid = lower in {"auto", "detect", "automatic"} or not LANGUAGE.fullmatch(value)
    invalid |= lower == "und" and not allow_und
    invalid |= lower == "mul" and not allow_mul
    if value and invalid:
        errors.append(f"`{path}.{key}` must be a resolved BCP 47 language tag, not {value!r}.")
    return value


def _number(parent: dict[str, Any], key: str, path: str, errors: list[str], low: float, high: float) -> None:
    value = parent.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not low <= float(value) <= high:
        errors.append(f"`{path}.{key}` must be a number from {low} to {high}.")


def _annotation_item(item: Any, path: str, errors: list[str], *, headline: bool) -> str:
    if not isinstance(item, dict):
        errors.append(f"`{path}` must be an object.")
        return ""
    value = _text(item, "text", path, errors, 2 if headline else 1)
    if len(value) > (80 if headline else 50):
        errors.append(f"`{path}.text` is too long.")
    _number(item, "x", path, errors, 0, 1)
    _number(item, "y", path, errors, 0, 1)
    if not headline:
        _number(item, "target_x", path, errors, 0, 1)
        _number(item, "target_y", path, errors, 0, 1)
    accent = _text(item, "accent", path, errors)
    if accent not in ACCENTS and not HEX.fullmatch(accent):
        errors.append(f"`{path}.accent` is not supported.")
    size = item.get("font_size")
    low, high = (28, 56) if headline else (22, 44)
    if not isinstance(size, int) or not low <= size <= high:
        errors.append(f"`{path}.font_size` must be {low}–{high}.")
    _number(item, "angle", path, errors, -4, 4)
    return value


def _semantic_contract(
    contract: dict[str, Any], path: str, *, image_role: str, article_type: str,
    topic_signature: list[str], errors: list[str], warnings: list[str],
) -> None:
    source_basis = _strings(contract, "source_basis", path, errors, 1, 4)
    must_show = _strings(contract, "must_show", path, errors, 2, 6)
    _strings(contract, "must_not_show", path, errors, 0, 8)
    specificity = _strings(contract, "specificity_terms", path, errors, 2, 10)
    blind_caption = _text(contract, "expected_blind_caption", path, errors, 20)
    hero_artifact = contract.get("hero_artifact")
    if not isinstance(hero_artifact, str):
        errors.append(f"`{path}.hero_artifact` must be a string, which may be empty.")
        hero_artifact = ""

    evidence = _list(contract, "visual_evidence", path, errors)
    if not 2 <= len(evidence) <= 6:
        errors.append(f"`{path}.visual_evidence` must contain 2–6 items.")
    for index, item in enumerate(evidence):
        item_path = f"{path}.visual_evidence[{index}]"
        if not isinstance(item, dict):
            errors.append(f"`{item_path}` must be an object.")
            continue
        _text(item, "concept", item_path, errors, 3)
        _text(item, "visible_form", item_path, errors, 8)
        _text(item, "relationship", item_path, errors, 8)

    required_overlap = 2 if image_role == "hero" else 1
    if len(terms_overlap(specificity, topic_signature)) < required_overlap:
        errors.append(
            f"`{path}.specificity_terms` must overlap `article.topic_signature` by at least "
            f"{required_overlap} item(s)."
        )
    if len(terms_overlap(topic_signature, [blind_caption])) < required_overlap:
        errors.append(
            f"`{path}.expected_blind_caption` must contain at least {required_overlap} "
            "article-specific topic signature anchor(s)."
        )

    if image_role == "hero":
        if len(source_basis) < 2:
            errors.append(f"`{path}.source_basis` must contain at least 2 grounded claims for a hero image.")
        if len(must_show) < 3:
            errors.append(f"`{path}.must_show` must contain at least 3 items for a hero image.")
        if len(hero_artifact.strip()) < 5:
            errors.append(f"`{path}.hero_artifact` must name a domain-specific central artifact for a hero image.")
    elif hero_artifact.strip():
        warnings.append(f"`{path}.hero_artifact` is set for an inline image; confirm it is necessary.")

    generic = [value for value in specificity if normalized(value) in GENERIC_SIGNATURE]
    if generic:
        warnings.append(f"`{path}` contains generic specificity term(s): {', '.join(generic)}.")


def validate_manifest(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Manifest root must be an object."], warnings
    if data.get("version") != 4:
        errors.append("`version` must be the integer 4.")

    article = _dict(data, "article", "root", errors)
    title = _text(article, "title", "article", errors)
    slug = _text(article, "slug", "article", errors)
    source_language = _language(article, "language", "article", errors, allow_und=True, allow_mul=True)
    annotation_language = _language(article, "annotation_language", "article", errors, allow_mul=True)
    _text(article, "summary", "article", errors, 20)
    target_count = article.get("target_count")
    if not isinstance(target_count, int) or not 1 <= target_count <= 9:
        errors.append("`article.target_count` must be 1–9.")
    if slug and not SLUG.fullmatch(slug):
        errors.append("`article.slug` must be lowercase kebab-case.")
    if len(title) > 160:
        warnings.append("Article title is unusually long.")
    article_type = _text(article, "article_type", "article", errors)
    if article_type not in ARTICLE_TYPES:
        errors.append("`article.article_type` is unsupported.")
    visual_thesis = _text(article, "visual_thesis", "article", errors, 20)
    topic_signature = _strings(article, "topic_signature", "article", errors, 3, 10)
    global_avoid = _strings(article, "global_must_avoid", "article", errors, 1, 12)
    if topic_signature and all(normalized(item) in GENERIC_SIGNATURE for item in topic_signature):
        errors.append("`article.topic_signature` contains only generic terms; add named entities, mechanisms, ratios, or outcomes.")
    if len({normalized(value) for value in topic_signature}) != len(topic_signature):
        errors.append("`article.topic_signature` must not contain duplicates.")
    if len({normalized(value) for value in global_avoid}) != len(global_avoid):
        errors.append("`article.global_must_avoid` must not contain duplicates.")
    if len(visual_thesis.split()) < 4:
        warnings.append("`article.visual_thesis` may be too vague; state a relationship or trade-off.")
    if source_language == "mul" and annotation_language != "mul":
        warnings.append("The article is multilingual; confirm the single annotation language is intentional.")

    visual_bible = _dict(data, "visual_bible", "root", errors)
    _text(visual_bible, "world_summary", "visual_bible", errors, 20)
    _text(visual_bible, "background", "visual_bible", errors, 20)
    palette = _list(visual_bible, "palette", "visual_bible", errors)
    if not 4 <= len(palette) <= 7:
        errors.append("`visual_bible.palette` must contain 4–7 items.")
    camera = _text(visual_bible, "camera", "visual_bible", errors)
    if camera not in CAMERAS:
        errors.append("Unsupported visual_bible camera.")
    _text(visual_bible, "lighting", "visual_bible", errors, 10)
    _text(visual_bible, "character_system", "visual_bible", errors, 20)
    _text(visual_bible, "recurring_motif", "visual_bible", errors, 10)
    continuity = _list(visual_bible, "continuity_rules", "visual_bible", errors)
    if not 4 <= len(continuity) <= 12:
        errors.append("`visual_bible.continuity_rules` must contain 4–12 items.")

    shots = _list(data, "shots", "root", errors)
    if not 1 <= len(shots) <= 9:
        errors.append("`shots` must contain 1–9 items.")
    if isinstance(target_count, int) and len(shots) != target_count:
        errors.append("target_count does not match shots length.")

    ids: list[str] = []
    filenames: list[str] = []
    roles: list[str] = []
    shot_languages: list[str] = []
    hero_indexes: list[int] = []

    for index, shot in enumerate(shots):
        path = f"shots[{index}]"
        if not isinstance(shot, dict):
            errors.append(f"`{path}` must be an object.")
            continue
        shot_id = _text(shot, "id", path, errors)
        ids.append(shot_id)
        if shot_id and not SHOT_ID.fullmatch(shot_id):
            errors.append(f"`{path}.id` must use two digits.")
        image_role = _text(shot, "image_role", path, errors)
        if image_role not in IMAGE_ROLES:
            errors.append(f"Unsupported image role at `{path}`.")
        if image_role == "hero":
            hero_indexes.append(index)
        visualization_mode = _text(shot, "visualization_mode", path, errors)
        if visualization_mode not in VISUALIZATION_MODES:
            errors.append(f"Unsupported visualization mode at `{path}`.")
        if article_type == "technical-research" and image_role == "hero" and visualization_mode == "abstract-metaphor":
            errors.append("A technical-research hero may not use `abstract-metaphor`.")

        _text(shot, "placement_after", path, errors, 3)
        _text(shot, "anchor", path, errors, 5)
        role = _text(shot, "role", path, errors)
        roles.append(role)
        if role not in ROLES:
            errors.append(f"Unsupported role at `{path}`.")
        if article_type == "technical-research" and image_role == "hero" and role not in TECHNICAL_ROLES:
            errors.append(
                "A technical-research hero must use a domain-faithful role: technical-mechanism, "
                "architecture-stack, resource-contrast, or claim-comparison."
            )
        _text(shot, "core_idea", path, errors, 10)
        composition = _text(shot, "composition", path, errors, 30)
        main_subject = _text(shot, "main_subject", path, errors, 5)
        if len(_list(shot, "supporting_elements", path, errors)) > 8:
            errors.append(f"`{path}.supporting_elements` may contain at most 8 items.")
        motion_cues = _list(shot, "motion_cues", path, errors)
        if not 1 <= len(motion_cues) <= 5:
            errors.append(f"`{path}.motion_cues` must contain 1–5 items.")
        density = _text(shot, "density", path, errors)
        if density not in DENSITIES:
            errors.append(f"Unsupported density at `{path}`.")
        people_count = shot.get("people_count")
        if not isinstance(people_count, int) or not 0 <= people_count <= 30:
            errors.append(f"`{path}.people_count` must be 0–30.")

        contract = _dict(shot, "semantic_contract", path, errors)
        _semantic_contract(
            contract, f"{path}.semantic_contract", image_role=image_role,
            article_type=article_type, topic_signature=topic_signature,
            errors=errors, warnings=warnings,
        )
        if article_type == "technical-research":
            composition_text = normalized(f"{composition} {main_subject}")
            mapped = [*contract.get("must_show", [])]
            for item in contract.get("visual_evidence", []):
                if isinstance(item, dict):
                    mapped.extend([str(item.get("concept", "")), str(item.get("visible_form", ""))])
            mapped_text = normalized(" ".join(str(value) for value in mapped))
            unmapped = sorted(term for term in TECHNICAL_GENERIC_OBJECTS if term in composition_text and term not in mapped_text)
            if unmapped:
                message = (
                    f"`{path}.composition` uses unmapped generic technical substitute(s): "
                    f"{', '.join(unmapped)}. Map them explicitly in visual_evidence or remove them."
                )
                (errors if image_role == "hero" else warnings).append(message)

        filename = _text(shot, "filename", path, errors)
        filenames.append(filename)
        if filename and not FILENAME.fullmatch(filename):
            errors.append(f"`{path}.filename` must be lowercase kebab-case PNG.")
        if shot_id and filename and not filename.startswith(shot_id + "-"):
            errors.append(f"`{path}.filename` must start with `{shot_id}-`.")
        alt_text = _text(shot, "alt_text", path, errors, 12)
        if len(alt_text) > 240:
            errors.append(f"`{path}.alt_text` must be ≤240 characters.")
        caption = shot.get("caption")
        if not isinstance(caption, str) or len(caption) > 300:
            errors.append(f"`{path}.caption` must be a string ≤300 characters.")

        annotation = _dict(shot, "annotation", path, errors)
        enabled = annotation.get("enabled")
        if not isinstance(enabled, bool):
            errors.append(f"`{path}.annotation.enabled` must be boolean.")
        shot_language = _language(annotation, "language", f"{path}.annotation", errors)
        shot_languages.append(shot_language)
        if annotation_language and annotation_language != "mul" and shot_language.casefold() != annotation_language.casefold():
            errors.append(
                f"`{path}.annotation.language` ({shot_language}) must match "
                f"`article.annotation_language` ({annotation_language})."
            )
        status = _text(annotation, "layout_status", f"{path}.annotation", errors)
        if status not in {"draft", "final"}:
            errors.append(f"`{path}.annotation.layout_status` must be draft or final.")
        if enabled:
            headline = _annotation_item(annotation.get("headline"), f"{path}.annotation.headline", errors, headline=True)
            labels = annotation.get("labels")
            if not isinstance(labels, list) or not 3 <= len(labels) <= 7:
                errors.append(f"`{path}.annotation.labels` must contain 3–7 items.")
                labels = []
            label_texts = [
                _annotation_item(item, f"{path}.annotation.labels[{label_index}]", errors, headline=False)
                for label_index, item in enumerate(labels)
            ]
            if normalized(headline) in GENERIC_LABELS:
                warnings.append(f"`{path}` headline is generic; write a concrete insight.")
            for value in label_texts:
                if normalized(value) in GENERIC_LABELS:
                    warnings.append(f"`{path}` contains generic label `{value}`.")
            normalized_labels = [normalized(value) for value in label_texts if value]
            if len(set(normalized_labels)) != len(normalized_labels):
                warnings.append(f"`{path}` repeats annotation labels.")

        motion_beats = shot.get("motion_beats")
        if motion_beats is not None and (not isinstance(motion_beats, list) or len(motion_beats) != 4):
            errors.append(f"`{path}.motion_beats` must contain exactly 4 items.")

    if len(hero_indexes) > 1:
        errors.append("At most one shot may use `image_role: hero`.")
    if hero_indexes and hero_indexes[0] != 0:
        errors.append("The hero shot must be the first shot in the manifest.")
    for label, values in (("shot id", ids), ("filename", filenames)):
        duplicates = [value for value, count in Counter(values).items() if value and count > 1]
        if duplicates:
            errors.append(f"Duplicate {label}(s): {', '.join(duplicates)}.")
    for role, count in Counter(roles).items():
        if role and count > 2:
            warnings.append(f"Role `{role}` is used {count} times; vary composition patterns.")
    if annotation_language == "mul" and len({value.casefold() for value in shot_languages if value}) < 2:
        warnings.append("`article.annotation_language` is `mul`, but fewer than two shot languages are used.")
    if shots and shots[0].get("density") not in {"low", "medium"}:
        warnings.append("The first calibration shot should be low/medium density.")
    if shots and isinstance(shots[0].get("people_count"), int) and shots[0]["people_count"] > 5:
        warnings.append("The calibration shot should usually contain ≤5 people.")
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
