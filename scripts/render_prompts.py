#!/usr/bin/env python3
"""Render text-free still prompts, motion prompts, and annotation plans."""
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
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def join(values: list[str]) -> str:
    return "; ".join(v.strip() for v in values if v.strip())


def people(count: int) -> str:
    if count == 0: return "Use objects and routes as narrative actors; no people required."
    if count <= 3: return f"Show {count} clear simplified paper-cutout figure(s), with no detailed hands."
    if count <= 8: return f"Show about {count} simplified figures using a few readable poses and minimal faces."
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
            if name not in regions: regions.append(name)
    return ", ".join(regions[:6]) or "upper and side parchment pockets"


def render_still(style_lock: str, vb: dict[str, Any], shot: dict[str, Any]) -> str:
    ann = shot.get("annotation") or {}; labels = len(ann.get("labels") or []) if ann.get("enabled") else 0
    return f"""Create one standalone original 16:9 editorial documentary article illustration.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

{style_lock.strip()}

{bible(vb)}

SHOT
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Composition: {shot['composition']}
Supporting elements: {join(shot['supporting_elements']) or 'None beyond the main subject.'}
Motion cues frozen into the still frame: {join(shot['motion_cues'])}
Density: {shot['density']}
People count strategy: {people(shot['people_count'])}

ANNOTATION RESERVATION
The final image will receive one short insight headline and {labels} semantic callout tag(s) in deterministic post-production. Keep calm parchment pockets in these broad regions: {annotation_regions(ann)}. Do not put every face, critical object, or section of the main route inside these quiet pockets. Do not draw placeholder tags, fake writing, letters, numbers, empty UI boxes, or symbols that resemble text.

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core idea. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. Keep people as simplified paper cutouts. Do not render text, letters, numbers, labels, logos, watermarks, UI, flowchart boxes, or dashboard elements in the base image. Do not add unnecessary objects. Preserve the exact article visual bible.
"""


def beats(shot: dict[str, Any]) -> list[str]:
    if shot.get("motion_beats"): return shot["motion_beats"]
    cues = shot.get("motion_cues") or []
    return [
        cues[0] if cues else "The setting appears on the parchment.",
        cues[1] if len(cues) > 1 else shot["core_idea"],
        cues[2] if len(cues) > 2 else "Routes, people, or objects expand organically.",
        cues[3] if len(cues) > 3 else "The core idea resolves into a stable tableau.",
    ]


def render_motion(style_lock: str, vb: dict[str, Any], shot: dict[str, Any]) -> str:
    b = beats(shot)
    return f"""Create an exactly 10-second, smooth 24fps original editorial documentary paper-cutout animation.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

{style_lock.strip()}

{bible(vb)}

STORY BEATS
0.0–1.5 seconds — Establish: {b[0]}
1.5–4.0 seconds — Transform: {b[1]}
4.0–7.5 seconds — Expand: {b[2]}
7.5–10.0 seconds — Resolve: {b[3]}

SHOT INTENT
Core idea: {shot['core_idea']}
Composition role: {shot['role']}
Main subject: {shot['main_subject']}
Base composition: {shot['composition']}
Supporting elements: {join(shot['supporting_elements']) or 'None beyond the main subject.'}
People strategy: {people(shot['people_count'])}

All elements unfold, slide, rotate, assemble, or move along organic map-like paths with smooth easing. Keep the camera locked or use only a slow subtle drift. No voiceover, dialogue, subtitles, text overlays, logo, or watermark. Only ambient sound is implied. Hold the final tableau for 0.5–0.8 seconds.
"""


def annotation_plan(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": data["version"], "article": data["article"], "images": [
        {"id": s["id"], "filename": s["filename"], "placement_after": s["placement_after"],
         "core_idea": s["core_idea"], "annotation": s["annotation"]} for s in data["shots"]]}


def delivery(out: Path, data: dict[str, Any], mode: str) -> None:
    lines = [f"# {data['article']['title']} — {mode.title()} Prompt Delivery", "",
             f"- Shots: {len(data['shots'])}", "", "| ID | Placement | Filename | Annotation headline |",
             "|---|---|---|---|"]
    for s in data["shots"]:
        headline = ((s.get("annotation") or {}).get("headline") or {}).get("text", "（停用）").replace("|", "／")
        lines.append(f"| {s['id']} | {s['placement_after'].replace('|','／')} | `{s['filename']}` | {headline} |")
    if mode == "still":
        lines += ["", "Generate text-free bases, finalize annotation coordinates, then run:", "",
                  "```bash", "python3 scripts/annotate_images.py manifest.json --input images/raw --output images --force", "```"]
    (out / "delivery.md").write_text("\n".join(lines)+"\n", encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__); p.add_argument("manifest", type=Path)
    p.add_argument("--mode", choices=("still", "motion"), default="still")
    p.add_argument("--output", type=Path, required=True); p.add_argument("--force", action="store_true")
    a = p.parse_args()
    try:
        data = json.loads(a.manifest.read_text(encoding="utf-8"))
        errors, warnings = validator().validate_manifest(data)
        for w in warnings: print(f"WARNING: {w}")
        if errors: raise ValueError("; ".join(errors))
        if a.output.exists():
            if not a.force: raise FileExistsError(f"Output exists: {a.output}; pass --force.")
            shutil.rmtree(a.output)
        a.output.mkdir(parents=True)
        lock = STYLE_LOCK.read_text(encoding="utf-8")
        for s in data["shots"]:
            suffix = "motion.txt" if a.mode == "motion" else "still.txt"
            text = render_motion(lock, data["visual_bible"], s) if a.mode == "motion" else render_still(lock, data["visual_bible"], s)
            (a.output / f"{Path(s['filename']).stem}-{suffix}").write_text(text, encoding="utf-8")
        (a.output / "manifest.json").write_text(json.dumps(data, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        if a.mode == "still":
            (a.output / "annotation-plan.json").write_text(json.dumps(annotation_plan(data), ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
        delivery(a.output, data, a.mode)
        print(f"Rendered {len(data['shots'])} {a.mode} prompt(s) to {a.output}.")
        return 0
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1


if __name__ == "__main__":
    raise SystemExit(main())
