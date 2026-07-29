#!/usr/bin/env python3
"""Validate a version 3 Editorial Documentary Illustrations manifest."""
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
ROLES = {"process-station", "route-network", "timeline-journey", "before-after",
         "scale-up-crowd", "cutaway-mechanism", "ecosystem-tableau",
         "physical-metaphor", "evidence-chain", "origin-map"}
DENSITIES = {"low", "medium", "high", "resolved-medium"}
ACCENTS = {"ink", "terracotta", "ochre", "sage", "indigo", "brick"}
SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
SHOT_ID = re.compile(r"^[0-9]{2}$")
FILENAME = re.compile(r"^[0-9]{2}-[a-z0-9-]+\.png$")
HEX = re.compile(r"^#[0-9A-Fa-f]{6}$")
LANGUAGE = re.compile(r"^(?:[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*|und|mul)$")
GENERIC_LABELS = {
    "流程", "結果", "重點", "系統", "資料", "工作流程", "系統架構圖", "重點整理",
    "flow", "workflow", "process", "result", "results", "key point", "key points",
    "system", "data", "overview", "diagram", "architecture",
    "フロー", "結果", "システム", "データ", "概要",
    "flujo", "resultado", "sistema", "datos", "resumen",
}


def obj(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{path}.{key}` must be an object.")
        return {}
    return value


def arr(parent: dict[str, Any], key: str, path: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"`{path}.{key}` must be an array.")
        return []
    return value


def text(parent: dict[str, Any], key: str, path: str, errors: list[str], minimum: int = 1) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or len(value.strip()) < minimum:
        errors.append(f"`{path}.{key}` must be a string of at least {minimum} characters.")
        return ""
    return value.strip()


def language(
    parent: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    *,
    allow_und: bool = False,
    allow_mul: bool = False,
) -> str:
    value = text(parent, key, path, errors, 2)
    normalized = value.lower()
    invalid = normalized in {"auto", "detect", "automatic"} or not LANGUAGE.fullmatch(value)
    invalid = invalid or (normalized == "und" and not allow_und) or (normalized == "mul" and not allow_mul)
    if value and invalid:
        allowed = "a concrete BCP 47 language tag"
        if allow_mul:
            allowed += " or `mul`"
        if allow_und:
            allowed += " or `und`"
        errors.append(f"`{path}.{key}` must be {allowed}, not {value!r}.")
    return value


def number(parent: dict[str, Any], key: str, path: str, errors: list[str], low: float, high: float) -> float | None:
    value = parent.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not low <= float(value) <= high:
        errors.append(f"`{path}.{key}` must be a number from {low} to {high}.")
        return None
    return float(value)


def normalized_label(value: str) -> str:
    return unicodedata.normalize("NFKC", value).strip().casefold()


def annotation_item(item: Any, path: str, errors: list[str], headline: bool) -> str:
    if not isinstance(item, dict):
        errors.append(f"`{path}` must be an object.")
        return ""
    value = text(item, "text", path, errors, 2 if headline else 1)
    if len(value) > (80 if headline else 50):
        errors.append(f"`{path}.text` is too long.")
    number(item, "x", path, errors, 0, 1)
    number(item, "y", path, errors, 0, 1)
    if not headline:
        number(item, "target_x", path, errors, 0, 1)
        number(item, "target_y", path, errors, 0, 1)
    acc = text(item, "accent", path, errors)
    if acc not in ACCENTS and not HEX.fullmatch(acc):
        errors.append(f"`{path}.accent` is not supported.")
    size = item.get("font_size")
    low, high = (28, 56) if headline else (22, 44)
    if not isinstance(size, int) or not low <= size <= high:
        errors.append(f"`{path}.font_size` must be {low}–{high}.")
    number(item, "angle", path, errors, -4, 4)
    return value


def validate_manifest(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["Manifest root must be an object."], warnings
    if data.get("version") != 3:
        errors.append("`version` must be the integer 3.")

    article = obj(data, "article", "root", errors)
    title = text(article, "title", "article", errors)
    slug = text(article, "slug", "article", errors)
    source_language = language(article, "language", "article", errors, allow_und=True, allow_mul=True)
    annotation_language = language(article, "annotation_language", "article", errors, allow_mul=True)
    text(article, "summary", "article", errors, 20)
    target = article.get("target_count")
    if not isinstance(target, int) or not 1 <= target <= 9:
        errors.append("`article.target_count` must be 1–9.")
    if slug and not SLUG.fullmatch(slug):
        errors.append("`article.slug` must be lowercase kebab-case.")
    if len(title) > 160:
        warnings.append("Article title is unusually long.")
    if source_language == "mul" and annotation_language != "mul":
        warnings.append("The article is marked multilingual; confirm the single annotation target language is intentional.")

    vb = obj(data, "visual_bible", "root", errors)
    text(vb, "world_summary", "visual_bible", errors, 20)
    text(vb, "background", "visual_bible", errors, 20)
    palette = arr(vb, "palette", "visual_bible", errors)
    if palette and not 4 <= len(palette) <= 7:
        errors.append("`visual_bible.palette` must contain 4–7 items.")
    camera = text(vb, "camera", "visual_bible", errors)
    if camera and camera not in CAMERAS:
        errors.append("Unsupported visual_bible camera.")
    text(vb, "lighting", "visual_bible", errors, 10)
    text(vb, "character_system", "visual_bible", errors, 20)
    text(vb, "recurring_motif", "visual_bible", errors, 10)
    continuity = arr(vb, "continuity_rules", "visual_bible", errors)
    if continuity and not 4 <= len(continuity) <= 12:
        errors.append("`visual_bible.continuity_rules` must contain 4–12 items.")

    shots = arr(data, "shots", "root", errors)
    if shots and not 1 <= len(shots) <= 9:
        errors.append("`shots` must contain 1–9 items.")
    if isinstance(target, int) and shots and len(shots) != target:
        errors.append("target_count does not match shots length.")
    ids: list[str] = []
    filenames: list[str] = []
    roles: list[str] = []
    annotation_languages: list[str] = []

    for i, shot in enumerate(shots):
        path = f"shots[{i}]"
        if not isinstance(shot, dict):
            errors.append(f"`{path}` must be an object.")
            continue
        sid = text(shot, "id", path, errors)
        ids.append(sid)
        if sid and not SHOT_ID.fullmatch(sid):
            errors.append(f"`{path}.id` must use two digits.")
        text(shot, "placement_after", path, errors, 3)
        text(shot, "anchor", path, errors, 5)
        role = text(shot, "role", path, errors)
        roles.append(role)
        if role and role not in ROLES:
            errors.append(f"Unsupported role at `{path}`.")
        text(shot, "core_idea", path, errors, 10)
        text(shot, "composition", path, errors, 30)
        text(shot, "main_subject", path, errors, 5)
        if len(arr(shot, "supporting_elements", path, errors)) > 8:
            errors.append(f"`{path}.supporting_elements` may contain at most 8 items.")
        cues = arr(shot, "motion_cues", path, errors)
        if not 1 <= len(cues) <= 5:
            errors.append(f"`{path}.motion_cues` must contain 1–5 items.")
        density = text(shot, "density", path, errors)
        if density and density not in DENSITIES:
            errors.append(f"Unsupported density at `{path}`.")
        count = shot.get("people_count")
        if not isinstance(count, int) or not 0 <= count <= 30:
            errors.append(f"`{path}.people_count` must be 0–30.")
        filename = text(shot, "filename", path, errors)
        filenames.append(filename)
        if filename and not FILENAME.fullmatch(filename):
            errors.append(f"`{path}.filename` must be lowercase kebab-case PNG.")
        if sid and filename and not filename.startswith(sid + "-"):
            errors.append(f"`{path}.filename` must start with `{sid}-`.")
        alt = text(shot, "alt_text", path, errors, 12)
        if len(alt) > 200:
            errors.append(f"`{path}.alt_text` must be ≤200 characters.")
        caption = shot.get("caption")
        if not isinstance(caption, str) or len(caption) > 240:
            errors.append(f"`{path}.caption` must be a string ≤240 characters.")

        ann = obj(shot, "annotation", path, errors)
        enabled = ann.get("enabled")
        if not isinstance(enabled, bool):
            errors.append(f"`{path}.annotation.enabled` must be boolean.")
        shot_language = language(ann, "language", f"{path}.annotation", errors)
        annotation_languages.append(shot_language)
        if annotation_language and annotation_language != "mul" and shot_language and shot_language.casefold() != annotation_language.casefold():
            errors.append(
                f"`{path}.annotation.language` ({shot_language}) must match "
                f"`article.annotation_language` ({annotation_language})."
            )
        status = text(ann, "layout_status", f"{path}.annotation", errors)
        if status not in {"draft", "final"}:
            errors.append(f"`{path}.annotation.layout_status` must be draft or final.")
        if enabled:
            headline = annotation_item(ann.get("headline"), f"{path}.annotation.headline", errors, True)
            labels = ann.get("labels")
            if not isinstance(labels, list) or not 3 <= len(labels) <= 7:
                errors.append(f"`{path}.annotation.labels` must contain 3–7 items.")
                labels = []
            label_texts = [annotation_item(v, f"{path}.annotation.labels[{j}]", errors, False) for j, v in enumerate(labels)]
            if normalized_label(headline) in GENERIC_LABELS:
                warnings.append(f"`{path}` headline is generic; write a concrete insight.")
            for value in label_texts:
                if normalized_label(value) in GENERIC_LABELS:
                    warnings.append(f"`{path}` contains generic label `{value}`.")
            normalized = [normalized_label(v) for v in label_texts if v]
            if len(set(normalized)) != len(normalized):
                warnings.append(f"`{path}` repeats annotation labels.")
        beat_list = shot.get("motion_beats")
        if beat_list is not None and (not isinstance(beat_list, list) or len(beat_list) != 4):
            errors.append(f"`{path}.motion_beats` must contain exactly 4 items.")

    for label, values in (("shot id", ids), ("filename", filenames)):
        dup = [v for v, n in Counter(values).items() if v and n > 1]
        if dup:
            errors.append(f"Duplicate {label}(s): {', '.join(dup)}.")
    for role, count in Counter(roles).items():
        if role and count > 2:
            warnings.append(f"Role `{role}` is used {count} times; vary composition patterns.")
    used_languages = {v.casefold() for v in annotation_languages if v}
    if annotation_language == "mul" and len(used_languages) < 2:
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
    for value in warnings:
        print(f"WARNING: {value}")
    for value in errors:
        print(f"ERROR: {value}", file=sys.stderr)
    if errors:
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1
    print(f"OK: {args.manifest} — {len(data['shots'])} shot(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
