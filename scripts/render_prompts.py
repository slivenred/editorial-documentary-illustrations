#!/usr/bin/env python3
"""Render context-grounded still or 10-second motion prompts from a version 5 manifest."""
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

LAYOUT_GUIDANCE = {
    "hero-explainer": (
        "Reserve the upper 22% as a calm parchment header, keep the main cutout scene in the middle "
        "roughly 54%, and reserve the lower 24% for three compact explainer cards."
    ),
    "mechanism-focus": (
        "Reserve the upper 20% for the header. Place the mechanism in the left 58–62% and keep a calm "
        "right column for two to four vertically stacked explainer cards."
    ),
    "process-strip": (
        "Reserve the upper 20% for the header. Build one left-to-right process scene in the middle and "
        "reserve the lower 24% for ordered stage cards."
    ),
    "comparison-split": (
        "Reserve the upper 20% for the header. Use a balanced left-versus-right visual comparison in the "
        "middle and reserve the lower 24% for two side cards and an optional center takeaway card."
    ),
    "timeline-route": (
        "Reserve the upper 20% for the header. Use one curved route across three or four visible stages and "
        "reserve the lower 24% for ordered stage cards."
    ),
    "result-board": (
        "Reserve the upper 20% for the header. Keep one simple result or resource-comparison scene in the "
        "middle and reserve the lower 26% for two to four metric or decision cards."
    ),
}


def load_validator():
    spec = importlib.util.spec_from_file_location("manifest_validator", VALIDATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {VALIDATOR_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def join(values: list[str]) -> str:
    return "; ".join(value.strip() for value in values if isinstance(value, str) and value.strip())


def bullet_lines(values: list[str]) -> str:
    return "\n".join(f"- {value.strip()}" for value in values if isinstance(value, str) and value.strip())


def render_visual_bible(data: dict[str, Any]) -> str:
    return f"""ARTICLE VISUAL BIBLE
Background: {data['background']}
Palette and usage: {join(data['palette'])}
Camera: {data['camera']}
Lighting and shadows: {data['lighting']}
Cutout style: {data['cutout_style']}
Typography system for later post-production: {data['typography']}
Continuity rules: {join(data['continuity_rules'])}"""


def render_explainer_mapping(explainers: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for index, item in enumerate(explainers, start=1):
        lines.append(
            f"{index}. Card meaning: {item['title']} — {item['body']}\n"
            f"   The base image must include this visible anchor: {item['visual_anchor']}\n"
            f"   Accent family for later text card: {item['accent']}"
        )
    return "\n".join(lines)


def render_still(style_lock: str, article: dict[str, Any], visual_bible: dict[str, Any], shot: dict[str, Any]) -> str:
    placement = shot["placement"]
    return f"""Create one original wide 16:9 editorial documentary paper-cutout illustration for an article.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

ARTICLE CONTEXT
Article title: {article['title']}
Article summary: {article['summary']}
Section: {placement['section_heading']}
Section anchor excerpt: {placement['after_paragraph_excerpt']}
Image purpose: {shot['purpose']}
The final headline will communicate: {shot['headline']}
The final subheadline will communicate: {shot['subheadline']}

VISUAL STORY
{shot['visual_story']}

KEY ELEMENTS
{bullet_lines(shot['key_elements'])}

EXPLAINER-TO-VISUAL MAPPING
{render_explainer_mapping(shot['explainers'])}

TEXT-SAFE LAYOUT
Layout: {shot['layout']}
{LAYOUT_GUIDANCE[shot['layout']]}
The image model must leave these zones visually calm, but must not draw cards, boxes, placeholder labels, fake writing, or text-shaped marks.

{render_visual_bible(visual_bible)}

{style_lock.strip()}

OUTPUT CONSTRAINTS
- One image, one question, one clear reading direction.
- Use 2–6 key object types and one main focal scene.
- The scene must directly match this section's context.
- It is acceptable for precise names, ratios, metrics, and caveats to be explained later in deterministic text cards.
- Do not over-engineer the scene into a dense paper, architecture, benchmark, or dashboard diagram.
- Do not add generic robots, glowing brains, server cities, office workers, factories, shields, or decorative gears unless explicitly required by the visual story.
- No text, letters, numbers, labels, logos, watermarks, UI, dashboards, formal flowchart boxes, brackets, legends, or fake writing in the base image.
"""


def motion_beats(shot: dict[str, Any]) -> list[str]:
    cues = shot.get("motion_cues") or []
    return [
        cues[0] if cues else "The main cutout scene appears on the parchment.",
        cues[1] if len(cues) > 1 else "The central mechanism or comparison begins.",
        cues[2] if len(cues) > 2 else "The visible process, contrast, or scale change expands.",
        cues[3] if len(cues) > 3 else "The core result resolves into a stable tableau.",
    ]


def render_motion(style_lock: str, article: dict[str, Any], visual_bible: dict[str, Any], shot: dict[str, Any]) -> str:
    beats = motion_beats(shot)
    return f"""Create one original exactly 10-second, smooth 24fps editorial documentary paper-cutout animation.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

ARTICLE CONTEXT
Article: {article['title']}
Image purpose: {shot['purpose']}
Core message: {shot['headline']}
Base visual story: {shot['visual_story']}
Key elements: {join(shot['key_elements'])}

{render_visual_bible(visual_bible)}

{style_lock.strip()}

STORY BEATS
0.0–1.5 seconds — Establish: {beats[0]}
1.5–4.0 seconds — Transform: {beats[1]}
4.0–7.5 seconds — Expand: {beats[2]}
7.5–10.0 seconds — Resolve: {beats[3]}

MOTION CONSTRAINTS
One continuous scene. Camera locked or only a very slow drift. No voiceover, dialogue, subtitles, text overlays, logo, or watermark. Do not animate the static headline or explainer cards. Only subtle ambient sound is implied. Hold the final tableau for 0.5–0.8 seconds.
"""


def write_delivery(output: Path, data: dict[str, Any], mode: str) -> None:
    article = data["article"]
    lines = [
        f"# {article['title']} — {mode.title()} Delivery",
        "",
        f"- Count mode: `{article['image_count_mode']}`",
        f"- Reading time: {article['reading_minutes']} minutes",
        f"- High-value anchors: {article['high_value_anchor_count']}",
        f"- Selected images: {article['target_count']}",
        f"- Count reason: {article['count_reason']}",
        "",
        "| ID | Kind | Section | After paragraph | Purpose | Layout | Filename |",
        "|---|---|---|---:|---|---|---|",
    ]
    for shot in data["shots"]:
        placement = shot["placement"]
        lines.append(
            f"| {shot['id']} | `{shot['kind']}` | {placement['section_heading'].replace('|', '／')} | "
            f"{placement['after_paragraph_index']} | `{shot['purpose']}` | `{shot['layout']}` | `{shot['filename']}` |"
        )
    if mode == "still":
        lines.extend([
            "",
            "After generating text-free bases, render integrated explainer text:",
            "",
            "```bash",
            "python3 scripts/annotate_images.py manifest.json --input images/raw --output images --force",
            "```",
        ])
    (output / "delivery.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--mode", choices=("still", "motion"), default="still")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
        errors, warnings = load_validator().validate_manifest(data)
        for warning in warnings:
            print(f"WARNING: {warning}")
        if errors:
            raise ValueError("; ".join(errors))
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        style_lock = STYLE_LOCK_PATH.read_text(encoding="utf-8")
        for shot in data["shots"]:
            suffix = "motion.txt" if args.mode == "motion" else "still.txt"
            prompt = (
                render_motion(style_lock, data["article"], data["visual_bible"], shot)
                if args.mode == "motion"
                else render_still(style_lock, data["article"], data["visual_bible"], shot)
            )
            (args.output / f"{Path(shot['filename']).stem}-{suffix}").write_text(prompt, encoding="utf-8")
        (args.output / "manifest.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        write_delivery(args.output, data, args.mode)
        print(f"Rendered {len(data['shots'])} {args.mode} prompt(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
