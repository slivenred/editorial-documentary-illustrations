#!/usr/bin/env python3
"""Render semantically grounded text-free still prompts, motion prompts, and annotation plans."""
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


def validator():
    spec = importlib.util.spec_from_file_location("manifest_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def join(values: list[str]) -> str:
    return "; ".join(value.strip() for value in values if isinstance(value, str) and value.strip())


def bullets(values: list[str]) -> str:
    return "\n".join(f"- {value.strip()}" for value in values if isinstance(value, str) and value.strip()) or "- None."


def people(count: int) -> str:
    if count == 0:
        return "Use domain objects, states, and relationships as the narrative actors; no human figure is required."
    if count <= 3:
        return f"Show {count} clear simplified paper-cutout figure(s), with no detailed hands."
    if count <= 8:
        return f"Show about {count} simplified figures using a few readable poses and minimal faces."
    return f"Suggest about {count} people with 2–5 layered crowd clusters and at most three clear foreground figures."


def bible(data: dict[str, Any]) -> str:
    return f"""ARTICLE VISUAL BIBLE
World summary: {data['world_summary']}
Background: {data['background']}
Palette and usage: {join(data['palette'])}
Camera: {data['camera']}
Lighting and shadows: {data['lighting']}
Character system: {data['character_system']}
Recurring motif: {data['recurring_motif']}
Continuity rules: {join(data['continuity_rules'])}"""


def region(x: float, y: float) -> str:
    vertical = "upper" if y < .34 else "middle" if y < .67 else "lower"
    horizontal = "left" if x < .34 else "center" if x < .67 else "right"
    return f"{vertical} {horizontal}"


def annotation_regions(annotation: dict[str, Any]) -> str:
    items = [annotation.get("headline"), *(annotation.get("labels") or [])]
    regions: list[str] = []
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("x"), (int, float)) and isinstance(item.get("y"), (int, float)):
            name = region(float(item["x"]), float(item["y"]))
            if name not in regions:
                regions.append(name)
    return ", ".join(regions[:6]) or "upper and side parchment pockets"


def evidence_lines(values: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for index, item in enumerate(values, start=1):
        lines.append(
            f"{index}. Concept: {item['concept']}\n"
            f"   Visible form: {item['visible_form']}\n"
            f"   Required relationship: {item['relationship']}"
        )
    return "\n".join(lines)


def semantic_contract(article: dict[str, Any], shot: dict[str, Any]) -> str:
    contract = shot["semantic_contract"]
    hero_artifact = contract.get("hero_artifact") or "Not applicable; this is an inline image."
    global_avoid = article.get("global_must_avoid") or []
    shot_avoid = contract.get("must_not_show") or []
    return f"""NON-NEGOTIABLE SEMANTIC CONTRACT — MEANING OVERRIDES STYLE
Article type: {article['article_type']}
Image role: {shot['image_role']}
Visualization mode: {shot['visualization_mode']}
Article visual thesis: {article['visual_thesis']}
Article topic signature: {join(article['topic_signature'])}
Source-grounded claims:
{bullets(contract['source_basis'])}

The unannotated base image MUST visibly show:
{bullets(contract['must_show'])}

Domain-specific hero artifact: {hero_artifact}
Shot specificity terms: {join(contract['specificity_terms'])}
Expected blind caption for the unannotated image: {contract['expected_blind_caption']}

VISUAL EVIDENCE MAPPING
{evidence_lines(contract['visual_evidence'])}

MISLEADING SUBSTITUTIONS TO AVOID
{bullets([*global_avoid, *shot_avoid])}

Semantic requirements:
- The base image must remain article-specific after every annotation is hidden.
- Every important concept must be observable through the mapped visible form and relationship.
- Do not replace the mechanism with generic AI scenery, decorative workers, a city, factory, robot, brain, gears, server tower, shield, road, or pipeline unless that exact object is explicitly required above.
- Annotations will only name evidence already visible in the base image; they must not manufacture relevance after generation.
- If style and semantic fidelity conflict, simplify the style and preserve the article mechanism.
"""


def technical_instruction(article: dict[str, Any], shot: dict[str, Any]) -> str:
    if article["article_type"] != "technical-research":
        return ""
    return f"""TECHNICAL-RESEARCH EXECUTION
Use a domain-faithful architecture, mechanism, state transition, resource comparison, or result relationship. Preserve component identity and topology. The chosen mode is {shot['visualization_mode']}. Do not humanize the architecture with office workers or replace it with a generic machine. A controlled paper-cutout abstraction is acceptable only when every component remains traceable to the visual evidence mapping.
"""


def render_still(style_lock: str, article: dict[str, Any], vb: dict[str, Any], shot: dict[str, Any]) -> str:
    annotation = shot.get("annotation") or {}
    label_count = len(annotation.get("labels") or []) if annotation.get("enabled") else 0
    return f"""Create one standalone original 16:9 editorial documentary article illustration.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

{semantic_contract(article, shot)}
{technical_instruction(article, shot)}
STYLE EXECUTION — APPLY ONLY AFTER THE SEMANTIC CONTRACT
{style_lock.strip()}

{bible(vb)}

SHOT COMPOSITION
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Composition: {shot['composition']}
Supporting elements: {join(shot['supporting_elements']) or 'None beyond the main subject.'}
Motion cues frozen into the still frame: {join(shot['motion_cues'])}
Density: {shot['density']}
People count strategy: {people(shot['people_count'])}

ANNOTATION RESERVATION
The final image will receive one short insight headline and {label_count} semantic callout tag(s) in deterministic post-production. Keep calm parchment pockets in these broad regions: {annotation_regions(annotation)}. Do not place every must-show item, face, or critical relationship inside these quiet pockets. Do not draw placeholder tags, fake writing, letters, numbers, empty UI boxes, or symbols that resemble text.

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core idea, one semantically readable relationship. Keep the focal action inside the central 84% safe area. Preserve enough parchment breathing room for annotation, but never remove a required must-show item merely to create empty space. Keep people as simplified paper cutouts. Do not render text, letters, numbers, labels, logos, watermarks, UI, flowchart boxes, or dashboard elements in the base image. Do not add decorative objects that are absent from the semantic contract. Preserve the exact visual bible without weakening the semantic contract.

FINAL SELF-CHECK BEFORE OUTPUT
1. Label-off test: is the article mechanism recognizable with all text hidden?
2. Blind-caption test: would a reviewer naturally describe at least two specificity terms and the intended relationship?
3. Neighbor-article test: would changing labels alone fail to repurpose this image for a different article?
If any answer is no, rebuild the composition before output.
"""


def beats(shot: dict[str, Any]) -> list[str]:
    if shot.get("motion_beats"):
        return shot["motion_beats"]
    cues = shot.get("motion_cues") or []
    return [
        cues[0] if cues else "The article-specific setting appears on the parchment.",
        cues[1] if len(cues) > 1 else shot["core_idea"],
        cues[2] if len(cues) > 2 else "The mapped components and relationships change visibly.",
        cues[3] if len(cues) > 3 else "The semantic contract resolves into a stable tableau.",
    ]


def render_motion(style_lock: str, article: dict[str, Any], vb: dict[str, Any], shot: dict[str, Any]) -> str:
    story_beats = beats(shot)
    return f"""Create an exactly 10-second, smooth 24fps original editorial documentary paper-cutout animation.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

{semantic_contract(article, shot)}
{technical_instruction(article, shot)}
STYLE EXECUTION — APPLY ONLY AFTER THE SEMANTIC CONTRACT
{style_lock.strip()}

{bible(vb)}

STORY BEATS
0.0–1.5 seconds — Establish: {story_beats[0]}
1.5–4.0 seconds — Transform: {story_beats[1]}
4.0–7.5 seconds — Expand: {story_beats[2]}
7.5–10.0 seconds — Resolve: {story_beats[3]}

SHOT INTENT
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Base composition: {shot['composition']}
Supporting elements: {join(shot['supporting_elements']) or 'None beyond the main subject.'}
People strategy: {people(shot['people_count'])}

All elements unfold, slide, rotate, assemble, compare, compress, retain, or move in ways that preserve the mapped mechanism. Keep the camera locked or use only a slow subtle drift. Do not substitute generic time-lapse activity for the article-specific relationship. No voiceover, dialogue, subtitles, text overlays, logo, or watermark. Only ambient sound is implied. Hold the final tableau for 0.5–0.8 seconds.
"""


def annotation_plan(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "version": data["version"],
        "article": data["article"],
        "images": [
            {
                "id": shot["id"],
                "image_role": shot["image_role"],
                "filename": shot["filename"],
                "placement_after": shot["placement_after"],
                "core_idea": shot["core_idea"],
                "semantic_contract": shot["semantic_contract"],
                "annotation": shot["annotation"],
            }
            for shot in data["shots"]
        ],
    }


def delivery(output: Path, data: dict[str, Any], mode: str) -> None:
    lines = [
        f"# {data['article']['title']} — {mode.title()} Prompt Delivery",
        "",
        f"- Article type: `{data['article']['article_type']}`",
        f"- Visual thesis: {data['article']['visual_thesis']}",
        f"- Topic signature: {join(data['article']['topic_signature'])}",
        f"- Shots: {len(data['shots'])}",
        "",
        "| ID | Role | Mode | Placement | Filename | Expected blind caption |",
        "|---|---|---|---|---|---|",
    ]
    for shot in data["shots"]:
        caption = shot["semantic_contract"]["expected_blind_caption"].replace("|", "／")
        lines.append(
            f"| {shot['id']} | `{shot['image_role']}` | `{shot['visualization_mode']}` | "
            f"{shot['placement_after'].replace('|', '／')} | `{shot['filename']}` | {caption} |"
        )
    if mode == "still":
        lines += [
            "", "Before generation, run semantic preflight:", "", "```bash",
            "python3 scripts/semantic_preflight.py manifest.json", "```", "",
            "After text-free base images pass Label-off, Blind-caption, and Neighbor-article tests, finalize annotation coordinates and run:",
            "", "```bash", "python3 scripts/annotate_images.py manifest.json --input images/raw --output images --force", "```",
        ]
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
        errors, warnings = validator().validate_manifest(data)
        for warning in warnings:
            print(f"WARNING: {warning}")
        if errors:
            raise ValueError("; ".join(errors))
        if args.output.exists():
            if not args.force:
                raise FileExistsError(f"Output exists: {args.output}; pass --force.")
            shutil.rmtree(args.output)
        args.output.mkdir(parents=True)
        style_lock = STYLE_LOCK.read_text(encoding="utf-8")
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
        if args.mode == "still":
            (args.output / "annotation-plan.json").write_text(
                json.dumps(annotation_plan(data), ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        delivery(args.output, data, args.mode)
        print(f"Rendered {len(data['shots'])} {args.mode} prompt(s) to {args.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
