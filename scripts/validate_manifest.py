#!/usr/bin/env python3
"""Validate an Editorial Documentary Illustrations shot manifest.

No third-party dependencies are required. The JSON Schema file is provided for
editors and CI systems; this script performs equivalent high-value checks with
clear human-readable errors and warnings.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ALLOWED_CAMERAS = {"top-down-map-15deg", "flat-orthographic", "soft-isometric"}
ALLOWED_ROLES = {
    "process-station",
    "route-network",
    "timeline-journey",
    "before-after",
    "scale-up-crowd",
    "cutaway-mechanism",
    "ecosystem-tableau",
    "physical-metaphor",
    "evidence-chain",
    "origin-map",
}
ALLOWED_DENSITIES = {"low", "medium", "high", "resolved-medium"}
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
ID_RE = re.compile(r"^[0-9]{2}$")
FILENAME_RE = re.compile(r"^[0-9]{2}-[a-z0-9-]+\.png$")


def _require_dict(parent: dict[str, Any], key: str, errors: list[str]) -> dict[str, Any]:
    value = parent.get(key)
    if not isinstance(value, dict):
        errors.append(f"`{key}` must be an object.")
        return {}
    return value


def _require_list(parent: dict[str, Any], key: str, errors: list[str]) -> list[Any]:
    value = parent.get(key)
    if not isinstance(value, list):
        errors.append(f"`{key}` must be an array.")
        return []
    return value


def _require_str(
    parent: dict[str, Any],
    key: str,
    path: str,
    errors: list[str],
    min_len: int = 1,
) -> str:
    value = parent.get(key)
    if not isinstance(value, str) or len(value.strip()) < min_len:
        errors.append(f"`{path}.{key}` must be a string of at least {min_len} characters.")
        return ""
    return value.strip()


def validate_manifest(data: Any) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(data, dict):
        return ["Manifest root must be a JSON object."], warnings

    if data.get("version") != 1:
        errors.append("`version` must be the integer 1.")

    article = _require_dict(data, "article", errors)
    title = _require_str(article, "title", "article", errors)
    slug = _require_str(article, "slug", "article", errors)
    _require_str(article, "language", "article", errors, min_len=2)
    _require_str(article, "summary", "article", errors, min_len=20)
    target_count = article.get("target_count")
    if not isinstance(target_count, int) or not (1 <= target_count <= 9):
        errors.append("`article.target_count` must be an integer from 1 to 9.")
    if slug and not SLUG_RE.fullmatch(slug):
        errors.append("`article.slug` must be lowercase kebab-case.")
    if title and len(title) > 160:
        warnings.append("Article title is unusually long.")

    bible = _require_dict(data, "visual_bible", errors)
    _require_str(bible, "world_summary", "visual_bible", errors, min_len=20)
    _require_str(bible, "background", "visual_bible", errors, min_len=20)
    palette = _require_list(bible, "palette", errors)
    if palette and not (4 <= len(palette) <= 7):
        errors.append("`visual_bible.palette` must contain 4 to 7 colors/usages.")
    camera = _require_str(bible, "camera", "visual_bible", errors)
    if camera and camera not in ALLOWED_CAMERAS:
        errors.append(f"`visual_bible.camera` must be one of: {sorted(ALLOWED_CAMERAS)}.")
    _require_str(bible, "lighting", "visual_bible", errors, min_len=10)
    _require_str(bible, "character_system", "visual_bible", errors, min_len=20)
    _require_str(bible, "recurring_motif", "visual_bible", errors, min_len=10)
    continuity = _require_list(bible, "continuity_rules", errors)
    if continuity and not (4 <= len(continuity) <= 12):
        errors.append("`visual_bible.continuity_rules` must contain 4 to 12 rules.")

    shots = _require_list(data, "shots", errors)
    if shots and not (1 <= len(shots) <= 9):
        errors.append("`shots` must contain 1 to 9 items.")
    if isinstance(target_count, int) and shots and len(shots) != target_count:
        errors.append(
            f"`article.target_count` is {target_count}, but `shots` contains {len(shots)} items."
        )

    ids: list[str] = []
    filenames: list[str] = []
    roles: list[str] = []
    placements: list[str] = []

    for index, shot in enumerate(shots, start=1):
        path = f"shots[{index - 1}]"
        if not isinstance(shot, dict):
            errors.append(f"`{path}` must be an object.")
            continue

        shot_id = _require_str(shot, "id", path, errors)
        if shot_id and not ID_RE.fullmatch(shot_id):
            errors.append(f"`{path}.id` must use two digits such as `01`.")
        ids.append(shot_id)

        placement = _require_str(shot, "placement_after", path, errors, min_len=3)
        placements.append(placement)
        _require_str(shot, "anchor", path, errors, min_len=5)

        role = _require_str(shot, "role", path, errors)
        roles.append(role)
        if role and role not in ALLOWED_ROLES:
            errors.append(f"`{path}.role` is not supported: {role!r}.")

        _require_str(shot, "core_idea", path, errors, min_len=10)
        _require_str(shot, "composition", path, errors, min_len=30)
        _require_str(shot, "main_subject", path, errors, min_len=5)

        supporting = _require_list(shot, "supporting_elements", errors)
        if len(supporting) > 8:
            errors.append(f"`{path}.supporting_elements` may contain at most 8 items.")

        motion_cues = _require_list(shot, "motion_cues", errors)
        if not (1 <= len(motion_cues) <= 5):
            errors.append(f"`{path}.motion_cues` must contain 1 to 5 items.")

        density = _require_str(shot, "density", path, errors)
        if density and density not in ALLOWED_DENSITIES:
            errors.append(f"`{path}.density` is not supported: {density!r}.")

        people_count = shot.get("people_count")
        if not isinstance(people_count, int) or not (0 <= people_count <= 30):
            errors.append(f"`{path}.people_count` must be an integer from 0 to 30.")
        elif people_count > 8 and density not in {"high", "resolved-medium"}:
            warnings.append(
                f"`{path}` has {people_count} people but density is {density!r}; "
                "use crowd clusters or raise the density."
            )

        filename = _require_str(shot, "filename", path, errors)
        filenames.append(filename)
        if filename and not FILENAME_RE.fullmatch(filename):
            errors.append(
                f"`{path}.filename` must look like `01-topic-name.png` using lowercase kebab-case."
            )
        if filename and shot_id and not filename.startswith(f"{shot_id}-"):
            errors.append(f"`{path}.filename` must begin with its shot id `{shot_id}-`.")

        alt = _require_str(shot, "alt_text_zh_tw", path, errors, min_len=12)
        if len(alt) > 160:
            errors.append(f"`{path}.alt_text_zh_tw` must be at most 160 characters.")

        caption = shot.get("caption_zh_tw")
        if not isinstance(caption, str):
            errors.append(f"`{path}.caption_zh_tw` must be a string, which may be empty.")
        elif len(caption) > 160:
            errors.append(f"`{path}.caption_zh_tw` must be at most 160 characters.")

        beats = shot.get("motion_beats")
        if beats is not None:
            if not isinstance(beats, list) or len(beats) != 4:
                errors.append(f"`{path}.motion_beats`, when present, must contain exactly 4 items.")
            elif any(not isinstance(beat, str) or len(beat.strip()) < 5 for beat in beats):
                errors.append(f"Every item in `{path}.motion_beats` must be meaningful text.")

        if (
            isinstance(people_count, int)
            and people_count > 12
            and role == "scale-up-crowd"
            and "cluster" not in str(shot.get("composition", "")).lower()
        ):
            warnings.append(
                f"`{path}` requests {people_count} people. Describe 2–5 layered crowd clusters "
                "instead of individually detailed figures."
            )

    for label, values in (("shot id", ids), ("filename", filenames)):
        duplicates = [value for value, count in Counter(values).items() if value and count > 1]
        if duplicates:
            errors.append(f"Duplicate {label}(s): {', '.join(sorted(duplicates))}.")

    role_counts = Counter(roles)
    for role, count in role_counts.items():
        if role and count > 2:
            warnings.append(
                f"Role `{role}` is used {count} times. Use more varied composition patterns."
            )

    placement_counts = Counter(placements)
    repeated_placements = [p for p, c in placement_counts.items() if p and c > 1]
    if repeated_placements:
        warnings.append(
            "Multiple shots share the same placement anchor. Confirm they are not redundant: "
            + "; ".join(repeated_placements)
        )

    if shots and shots[0].get("density") not in {"low", "medium"}:
        warnings.append("The first shot should usually be a low/medium-density calibration frame.")
    if shots and isinstance(shots[0].get("people_count"), int) and shots[0]["people_count"] > 5:
        warnings.append("The first calibration shot should usually contain no more than 5 people.")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to manifest.json")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.manifest}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    errors, warnings = validate_manifest(data)

    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if errors:
        print(f"\nFAILED: {len(errors)} error(s), {len(warnings)} warning(s).", file=sys.stderr)
        return 1

    print(
        f"OK: {args.manifest} — {len(data['shots'])} shot(s), "
        f"{len(warnings)} warning(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
