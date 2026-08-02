#!/usr/bin/env python3
"""Recommend the total number of article illustrations from reading time and useful anchors."""
from __future__ import annotations

import argparse
import json


def capacity_for_minutes(reading_minutes: float) -> int:
    if reading_minutes <= 2:
        return 1
    if reading_minutes <= 4:
        return 3
    if reading_minutes <= 6:
        return 4
    if reading_minutes <= 9:
        return 5
    if reading_minutes <= 12:
        return 6
    if reading_minutes <= 16:
        return 7
    return 8


def recommend_count(
    reading_minutes: float,
    high_value_anchors: int,
    section_count: int,
    include_hero: bool = True,
) -> dict[str, int | float | bool | str]:
    if reading_minutes <= 0:
        raise ValueError("reading_minutes must be greater than zero")
    if high_value_anchors < 1:
        raise ValueError("high_value_anchors must be at least one")
    if section_count < 1:
        raise ValueError("section_count must be at least one")

    capacity = capacity_for_minutes(reading_minutes)
    semantic_limit = min(high_value_anchors, section_count + (1 if include_hero else 0))
    recommended = max(1, min(capacity, semantic_limit, 8))
    return {
        "reading_minutes": reading_minutes,
        "capacity": capacity,
        "high_value_anchors": high_value_anchors,
        "section_count": section_count,
        "include_hero": include_hero,
        "recommended_total": recommended,
        "reason": (
            f"Reading-time capacity is {capacity}; after limiting by {high_value_anchors} "
            f"high-value anchors and {section_count} sections, recommend {recommended} image(s) total."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reading-minutes", type=float, required=True)
    parser.add_argument("--anchors", type=int, required=True)
    parser.add_argument("--sections", type=int, required=True)
    parser.add_argument("--include-hero", action="store_true")
    args = parser.parse_args()
    try:
        result = recommend_count(
            args.reading_minutes,
            args.anchors,
            args.sections,
            args.include_hero,
        )
    except ValueError as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
