#!/usr/bin/env python3
"""Render still-image or 10-second motion prompts from a validated manifest."""

from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STYLE_LOCK_PATH = ROOT / "references" / "style-lock.txt"
VALIDATOR_PATH = ROOT / "scripts" / "validate_manifest.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("manifest_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load validator: {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bullet_join(values: list[str]) -> str:
    return "; ".join(value.strip() for value in values if value.strip())


def people_strategy(count: int, density: str) -> str:
    if count <= 0:
        return "No human figure is required; use objects and routes as the narrative actors."
    if count <= 3:
        return f"Show {count} clear primary paper-cutout figure(s), with simple faces and no detailed hands."
    if count <= 8:
        return (
            f"Show about {count} simplified paper-cutout figures using a small set of readable poses; "
            "keep faces minimal and avoid detailed hands."
        )
    cluster_count = min(5, max(2, round(count / 5)))
    return (
        f"Suggest the energy of about {count} people using {cluster_count} layered crowd clusters, "
        "plus at most three clearer foreground figures. Do not render every person individually."
    )


def render_bible(bible: dict[str, Any]) -> str:
    palette = bullet_join(bible["palette"])
    continuity = bullet_join(bible["continuity_rules"])
    return f"""ARTICLE VISUAL BIBLE
World summary: {bible['world_summary']}
Background: {bible['background']}
Palette and usage: {palette}
Camera: {bible['camera']}
Lighting and shadows: {bible['lighting']}
Character system: {bible['character_system']}
Recurring motif: {bible['recurring_motif']}
Continuity rules: {continuity}"""


def render_still(style_lock: str, bible: dict[str, Any], shot: dict[str, Any]) -> str:
    return f"""Create one standalone original 16:9 editorial documentary article illustration.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

{style_lock.strip()}

{render_bible(bible)}

SHOT
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Composition: {shot['composition']}
Supporting elements: {bullet_join(shot['supporting_elements']) or 'None beyond the main subject.'}
Motion cues frozen into the still frame: {bullet_join(shot['motion_cues'])}
Density: {shot['density']}
People count strategy: {people_strategy(shot['people_count'], shot['density'])}

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core idea. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. Keep people as simplified paper cutouts, especially in crowds. No text inside the image. No logos, watermarks, captions, labels, UI, formal flowchart boxes, or dashboard elements. Do not add unnecessary objects. Preserve the exact article visual bible.
"""


def infer_motion_beats(shot: dict[str, Any]) -> list[str]:
    cues = shot.get("motion_cues") or []
    cue_1 = cues[0] if cues else "The central setting appears on the parchment."
    cue_2 = cues[1] if len(cues) > 1 else f"The main subject begins the core action: {shot['core_idea']}"
    cue_3 = cues[2] if len(cues) > 2 else "Supporting elements arrive along organic map-like routes and the scene expands."
    cue_4 = cues[3] if len(cues) > 3 else "The action resolves into one clear, stable documentary tableau."
    return [
        f"Establish the setting and main subject. {cue_1}",
        f"Begin the transformation. {cue_2}",
        f"Expand the routes, people, or objects. {cue_3}",
        f"Resolve the core idea in a stable final scene. {cue_4}",
    ]


def render_motion(style_lock: str, bible: dict[str, Any], shot: dict[str, Any]) -> str:
    beats = shot.get("motion_beats") or infer_motion_beats(shot)
    return f"""Create an exactly 10-second, smooth 24fps editorial documentary paper-cutout animation.
It must be an original composition and must not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable layout.

{style_lock.strip()}

{render_bible(bible)}

STORY BEATS
0.0–1.5 seconds — Establish: {beats[0]}
1.5–4.0 seconds — Transform: {beats[1]}
4.0–7.5 seconds — Expand: {beats[2]}
7.5–10.0 seconds — Resolve: {beats[3]}

SHOT INTENT
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Base composition: {shot['composition']}
Supporting elements: {bullet_join(shot['supporting_elements']) or 'None beyond the main subject.'}
People strategy: {people_strategy(shot['people_count'], shot['density'])}

MOTION LANGUAGE
All elements appear, unfold, slide, rotate, assemble, or move along organic map-like paths with smooth easing. People are simplified paper cutouts and move along stylized routes. For crowds, use layered clusters rather than individually detailed figures. Keep the camera locked or use only a very slow subtle drift. Maintain elegant, premium documentary energy.

No voiceover. No dialogue. No subtitles. No text overlays. No logo. No watermark. Only subtle lively ambient background sound is implied. End on a stable final tableau for the last 0.5–0.8 seconds.
"""


def write_delivery(output_dir: Path, data: dict[str, Any], mode: str) -> None:
    article = data["article"]
    lines = [
        f"# {article['title']} — {mode.title()} Prompt Delivery",
        "",
        f"- Slug: `{article['slug']}`",
        f"- Language: `{article['language']}`",
        f"- Shots: {len(data['shots'])}",
        "",
        "| ID | Prompt | Placement | Role | Filename | Alt text |",
        "|---|---|---|---|---|---|",
    ]
    extension = "motion.txt" if mode == "motion" else "still.txt"
    for shot in data["shots"]:
        prompt_name = f"{Path(shot['filename']).stem}-{extension}"
        placement = shot["placement_after"].replace("|", "／")
        alt = shot["alt_text_zh_tw"].replace("|", "／")
        lines.append(
            f"| {shot['id']} | `{prompt_name}` | {placement} | "
            f"`{shot['role']}` | `{shot['filename']}` | {alt} |"
        )
    lines.extend(["", "## Captions", ""])
    for shot in data["shots"]:
        caption = shot["caption_zh_tw"] or "（無 caption）"
        lines.append(f"- **{shot['id']}**：{caption}")
    (output_dir / "delivery.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, help="Path to manifest.json")
    parser.add_argument("--mode", choices=("still", "motion"), default="still")
    parser.add_argument("--output", type=Path, required=True, help="Output directory")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace the output directory if it already exists.",
    )
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except FileNotFoundError:
        print(f"ERROR: File not found: {args.manifest}", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    validator = load_validator()
    errors, warnings = validator.validate_manifest(data)
    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("Refusing to render prompts from an invalid manifest.", file=sys.stderr)
        return 1

    if args.output.exists():
        if not args.force:
            print(
                f"ERROR: Output directory already exists: {args.output}. "
                "Use --force to replace it.",
                file=sys.stderr,
            )
            return 2
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True, exist_ok=False)

    style_lock = STYLE_LOCK_PATH.read_text(encoding="utf-8")
    bible = data["visual_bible"]

    for shot in data["shots"]:
        stem = Path(shot["filename"]).stem
        suffix = "motion.txt" if args.mode == "motion" else "still.txt"
        output_path = args.output / f"{stem}-{suffix}"
        prompt = (
            render_motion(style_lock, bible, shot)
            if args.mode == "motion"
            else render_still(style_lock, bible, shot)
        )
        output_path.write_text(prompt, encoding="utf-8")

    write_delivery(args.output, data, args.mode)
    (args.output / "manifest.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"Rendered {len(data['shots'])} {args.mode} prompt(s) to {args.output}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
