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


def render_still(_style_lock: str, data: dict[str, Any], shot: dict[str, Any]) -> str:
    # LEAN prompt (v5): one rich evocative scene + the exact verbatim text + a
    # condensed style line (~300-350 words). Over-specified prompts (~1,100 words)
    # produced flat, diagrammatic images; a concise prompt lets the model render a
    # rich, tactile 3D paper-craft scene (validated: a 334-word prompt yielded
    # web-quality output from the same model). `style_lock` is accepted for
    # signature/test compatibility but is no longer dumped verbatim.
    article = data["article"]
    placement = shot["placement"]
    role_intro = "featured / hero" if shot["image_role"] == "hero" else "inline article"
    if shot["image_role"] == "hero":
        context = f"""TITLE CONTRACT
Claim: {article['title_contract']['claim']}
Key result: {article['title_contract']['key_result']}
Mechanism: {article['title_contract']['mechanism']}
The featured image must visibly answer the article title."""
    else:
        context = f"""ARTICLE CONTEXT
Section: {placement['section_heading']}
Core idea: {shot['core_idea']}
Use the approved featured image only as a style reference. Match its parchment tone, fine double-line border, corner ornaments, centered title hierarchy, paper-crafted depth, shadow direction, and accent colors. Do not copy its composition."""

    vb = data["visual_bible"]
    margin = vb["layout_contract"]["outer_margin_px"]
    people_clause = " Include people only if they clearly aid comprehension." if shot.get("people_required") else ""

    return f"""Create one original 16:9 {role_intro} editorial illustration on warm aged parchment with a faint grid, a fine double-line ink border, and small corner ornaments.

{context}

{shot['scene']} Build it as a dimensional handcrafted paper-craft tableau — layered cardstock, parchment, corrugated paper and balsa wood with ink detailing and soft paper shadows; no metal, no glass, no screens, no robot silhouettes.{people_clause}

{exact_text_block(shot)}

STYLE
Palette: {join(vb['palette'])}. A centered editorial title hierarchy (small eyebrow, large high-contrast headline, concise subheadline) sits at the top; the paper-craft tableau occupies the middle and lower canvas; an optional bottom takeaway ribbon closes the composition. Soft warm upper-left light with short consistent lower-right shadows. Compose the whole scene inside the central canvas with generous margin: every road, path, machine, and tall object must stay fully within the double-line border — nothing may touch, cross, or be cropped by the border or the canvas edge, and all text keeps at least {margin}px clear of it; do not overlap text with the subject.
"""


def render_motion(_style_lock: str, data: dict[str, Any], shot: dict[str, Any]) -> str:
    vb = data["visual_bible"]
    return f"""Create an exactly 10-second, smooth 24fps paper-craft editorial animation based on this approved still concept.

Core idea: {shot['core_idea']}
Scene: {shot['scene']}
Required elements: {join(shot['scene_elements'])}

Style: warm aged parchment, fine double-line border; palette {join(vb['palette'])}; dimensional handcrafted paper-craft (cardstock/parchment/wood, no metal or glass); soft warm light, short consistent shadows.

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
