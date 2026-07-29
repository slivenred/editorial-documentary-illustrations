#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_module("validator", ROOT / "scripts" / "validate_manifest.py")
renderer = load_module("renderer", ROOT / "scripts" / "render_prompts.py")


def valid_manifest() -> dict:
    return {
        "version": 1,
        "article": {
            "title": "Editorial documentary illustration workflow",
            "slug": "editorial-documentary-workflow",
            "language": "zh-TW",
            "summary": "A reusable manifest used only to verify validation and prompt rendering behavior.",
            "target_count": 1,
        },
        "visual_bible": {
            "world_summary": "An original editorial documentary world rendered as restrained paper cutouts on parchment.",
            "background": "Warm aged parchment with subtle fibers, a faint map grid, and two gentle paper creases.",
            "palette": [
                "dark ink brown for outlines",
                "terracotta for the main actor",
                "mustard ochre for routes",
                "muted sage for supporting objects",
            ],
            "camera": "top-down-map-15deg",
            "lighting": "Soft warm light from upper left with short shadows falling lower right.",
            "character_system": "Simplified paper-cutout figures with minimal faces, readable silhouettes, and no detailed hands.",
            "recurring_motif": "a single ochre route line",
            "continuity_rules": [
                "Keep the same parchment tone.",
                "Keep the same camera angle.",
                "Keep the same shadow direction.",
                "Use no text inside the image.",
            ],
        },
        "shots": [
            {
                "id": "01",
                "placement_after": "After the core workflow explanation",
                "anchor": "One article becomes one consistent visual system.",
                "role": "process-station",
                "core_idea": "A visual bible keeps every generated image consistent.",
                "composition": "A central paper-cutout worktable receives article notes from the left and sends one coherent sequence of framed scenes to the right.",
                "main_subject": "the central visual-bible worktable",
                "supporting_elements": ["article notes", "route line", "three framed scenes"],
                "motion_cues": ["notes slide toward the worktable", "frames unfold along one route"],
                "density": "low",
                "people_count": 1,
                "filename": "01-consistent-visual-system.png",
                "alt_text_zh_tw": "羊皮紙上的剪紙工作台把文章內容轉成一致風格的系列配圖。",
                "caption_zh_tw": "",
                "motion_beats": [
                    "The parchment and worktable appear.",
                    "Article notes move into the worktable.",
                    "Three consistent scenes unfold along one route.",
                    "The final sequence holds as a stable tableau.",
                ],
            }
        ],
    }


class ToolingTests(unittest.TestCase):
    def test_manifest_validates(self):
        errors, warnings = validator.validate_manifest(valid_manifest())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_prompt_rendering(self):
        data = valid_manifest()
        style_lock = (ROOT / "references" / "style-lock.txt").read_text(encoding="utf-8")
        bible = data["visual_bible"]
        shot = data["shots"][0]

        still = renderer.render_still(style_lock, bible, shot)
        motion = renderer.render_motion(style_lock, bible, shot)

        self.assertIn("16:9", still)
        self.assertIn("No text inside the image", still)
        self.assertIn("exactly 10-second", motion)
        self.assertIn("No voiceover", motion)
        self.assertIn(bible["recurring_motif"], still)

    def test_people_cluster_strategy(self):
        text = renderer.people_strategy(18, "high")
        self.assertIn("crowd clusters", text)
        self.assertNotIn("Show about 18 simplified", text)


if __name__ == "__main__":
    unittest.main()
