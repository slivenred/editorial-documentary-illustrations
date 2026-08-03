#!/usr/bin/env python3
"""Recommend the total number of featured and inline article illustrations."""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

CJK_PREFIXES = {"zh", "ja", "ko"}


def capacity_for_minutes(reading_minutes: float) -> int:
    if reading_minutes <= 1:
        return 1
    if reading_minutes <= 2:
        return 2
    if reading_minutes <= 4:
        return 3
    if reading_minutes <= 6:
        return 4
    if reading_minutes <= 9:
        return 5
    if reading_minutes <= 12:
        return 6
    return 7


def estimate_reading_minutes(text: str, language: str) -> float:
    prefix = (language or "en").split("-", 1)[0].lower()
    cleaned = re.sub(r"```.*?```", " ", text, flags=re.S)
    cleaned = re.sub(r"https?://\S+", " ", cleaned)
    if prefix in CJK_PREFIXES:
        visible = re.sub(r"\s+", "", cleaned)
        return max(0.5, len(visible) / 450.0)
    words = re.findall(r"\b[\w'-]+\b", cleaned, flags=re.UNICODE)
    return max(0.5, len(words) / 220.0)


def recommend_count(reading_minutes: float, high_value_anchors: int, include_hero: bool = True) -> int:
    if reading_minutes <= 0:
        raise ValueError("reading_minutes must be positive")
    if high_value_anchors < 0:
        raise ValueError("high_value_anchors must be non-negative")
    minimum = 1 if include_hero else 0
    available = max(minimum, high_value_anchors)
    return min(capacity_for_minutes(reading_minutes), available)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--reading-minutes", type=float)
    group.add_argument("--text-file", type=Path)
    parser.add_argument("--language", default="en")
    parser.add_argument("--anchors", type=int, required=True, help="High-value non-redundant anchors, including hero when requested.")
    parser.add_argument("--include-hero", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if args.text_file:
        text = args.text_file.read_text(encoding="utf-8")
        minutes = estimate_reading_minutes(text, args.language)
    else:
        minutes = args.reading_minutes

    count = recommend_count(float(minutes), args.anchors, args.include_hero)
    payload = {
        "reading_minutes": round(float(minutes), 2),
        "capacity": capacity_for_minutes(float(minutes)),
        "high_value_anchor_count": args.anchors,
        "include_hero": args.include_hero,
        "recommended_total_count": count,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"Recommended {count} total image(s): reading time {payload['reading_minutes']} min, "
            f"capacity {payload['capacity']}, high-value anchors {args.anchors}."
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
