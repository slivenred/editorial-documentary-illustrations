#!/usr/bin/env python3
"""Render final-image prompts, placement plans, and delivery metadata from a v6 manifest."""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STYLE_LOCK = ROOT / "references" / "style-lock.txt"
VALIDATOR = ROOT / "scripts" / "validate_manifest.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("manifest_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def join(values: list[str]) -> str:
    return "; ".join(value.strip() for value in values if isinstance(value, str) and value.strip())


def visual_bible_text(vb: dict[str, Any]) -> str:
    layout = vb["layout_contract"]
    return f"""ARTICLE VISUAL BIBLE
Background: {vb['background']}
Border: {vb['border']}
Palette: {join(vb['palette'])}
Typography: {vb['typography']}
Scene style: {vb['scene_style']}
Camera: {vb['camera']}
Lighting: {vb['lighting']}
Label style: {vb['label_style']}
Takeaway style: {vb['takeaway_style']}
Continuity rules: {join(vb['continuity_rules'])}
Canvas: {layout['canvas_width']}x{layout['canvas_height']}
Outer safe margin: {layout['outer_margin_px']}px
Maximum labels: {layout['max_labels']}
Text over subject: forbidden
Overflow: forbidden"""


def exact_text_block(shot: dict[str, Any]) -> str:
    labels = "\n".join(f"- {item['text']}" for item in shot["labels"])
    caveat = shot["caveat"] or "None"
    takeaway = shot["bottom_takeaway"] or "None"
    return f"""EXACT TEXT — RENDER VERBATIM AND ADD NO OTHER TEXT
Eyebrow: {shot['eyebrow'] or 'None'}
Headline: {shot['headline']}
Subheadline: {shot['subheadline']}
Labels:
{labels}
Bottom takeaway: {takeaway}
Caveat: {caveat}"""


def render_still(style_lock: str, data: dict[str, Any], shot: dict[str, Any]) -> str:
    article = data["article"]
    placement = shot["placement"]
    role_intro = "featured / hero" if shot["image_role"] == "hero" else "inline article"
    if shot["image_role"] == "hero":
        context = f"""TITLE CONTRACT
Claim: {article['title_contract']['claim']}
Key result: {article['title_contract']['key_result']}
Mechanism: {article['title_contract']['mechanism']}
Required coverage: {join(shot['title_coverage'])}
The featured image must visibly answer the article title before it explains secondary details."""
        style_reference = "This is the calibration image for the article. Establish the final visual system."
    else:
        context = f"""ARTICLE CONTEXT
Section: {placement['section_heading']}
Paragraph excerpt: {placement['after_paragraph_excerpt']}
Core idea: {shot['core_idea']}
Placement reason: {placement['reason']}"""
        style_reference = """Use the approved featured image only as a style reference. Match its parchment tone, fine double-line border, corner ornaments, centered title hierarchy, paper-crafted depth, shadow direction, label-card treatment, accent colors, and bottom takeaway ribbon. Do not copy its composition."""

    people = "Include people only when they improve comprehension." if shot["people_required"] else "No human figure is required; let the paper-crafted objects carry the explanation."
    labels = "\n".join(
        f"- {item['text']}: visually point to or explain {item['meaning']} using {item['accent']} accent."
        for item in shot["labels"]
    )
    layout = data["visual_bible"]["layout_contract"]
    return f"""Create one final production-ready 16:9 {role_intro} editorial illustration.

{context}

{exact_text_block(shot)}

MAIN TABLEAU
Layout pattern: {shot['layout']}
Scene: {shot['scene']}
Required scene elements: {join(shot['scene_elements'])}
{people}
Label meanings and accents:
{labels}

STYLE REFERENCE
{style_reference}

{style_lock.strip()}

{visual_bible_text(data['visual_bible'])}

LAYOUT AND SAFETY
- Render at {layout['canvas_width']}x{layout['canvas_height']} or the exact same 16:9 ratio.
- Keep at least {layout['outer_margin_px']}px of clear outer safe margin inside the border.
- Center the eyebrow, headline, and subheadline in the upper area.
- Keep the main tableau in the middle and lower area without touching the frame.
- Keep all labels near their targets with short non-crossing leader lines.
- Never place a text card over the main subject or decisive comparison.
- Keep every glyph, card, road, machine, door, box, flag, ornament, and shadow fully inside the border.
- Verify every requested string for spelling and punctuation before final output.
- Do not add placeholder text, extra labels, fake writing, logo, watermark, or unrelated objects.

FINAL SELF-CHECK
1. Does the image immediately communicate the intended title or paragraph idea?
2. Does it look like the same editorial series as the approved featured image?
3. Is every requested string exact and readable?
4. Is any important element covered or cropped?
If any answer is no, correct the image before output.
"""


def render_motion(style_lock: str, data: dict[str, Any], shot: dict[str, Any]) -> str:
    return f"""Create an exactly 10-second, smooth 24fps paper-craft editorial animation based on this approved still concept.

Core idea: {shot['core_idea']}
Scene: {shot['scene']}
Required elements: {join(shot['scene_elements'])}

{style_lock.strip()}

Use one continuous scene. Animate the physical mechanism, comparison, burden, path, or transformation. No voiceover, no dialogue, no text overlays, no logo, and no watermark. Keep the camera locked or use one subtle drift. Hold the final tableau for 0.5–0.8 seconds.
"""


def placement_plan(data: dict[str, Any]) -> str:
    lines = [
        f"# {data['article']['title']} — Image Placement Plan",
        "",
        f"- Reading time: {data['article']['reading_minutes']} minutes",
        f"- High-value anchors: {data['article']['high_value_anchor_count']}",
        f"- Final image count: {data['article']['target_count']}",
        "",
        "| ID | Role | Section | After paragraph | Reason | Filename |",
        "|---|---|---|---:|---|---|",
    ]
    for shot in data["shots"]:
        placement = shot["placement"]
        lines.append(
            f"| {shot['id']} | {shot['image_role']} | {placement['section_heading'].replace('|', '／')} | "
            f"{placement['after_paragraph_global_index']} | {placement['reason'].replace('|', '／')} | `{shot['filename']}` |"
        )
    return "\n".join(lines) + "\n"


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
        lock = STYLE_LOCK.read_text(encoding="utf-8")
        for shot in data["shots"]:
            prompt = render_motion(lock, data, shot) if args.mode == "motion" else render_still(lock, data, shot)
            suffix = "motion.txt" if args.mode == "motion" else "still.txt"
            (args.output / f"{Path(shot['filename']).stem}-{suffix}").write_text(prompt, encoding="utf-8")
        (args.output / "manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        (args.output / "placement-plan.md").write_text(placement_plan(data), encoding="utf-8")
        print(f"Rendered {len(data['shots'])} {args.mode} prompt(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
