#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module

validator = load("validator", ROOT / "scripts/validate_manifest.py")
renderer = load("renderer", ROOT / "scripts/render_prompts.py")
annotator = load("annotator", ROOT / "scripts/annotate_images.py")


def manifest():
    return {
        "version": 2,
        "article": {"title": "Editorial workflow", "slug": "editorial-workflow", "language": "zh-TW",
                    "summary": "A reusable manifest that verifies prompt and annotation tooling behavior.", "target_count": 1},
        "visual_bible": {
            "world_summary": "An editorial parchment world with restrained paper cutouts and semantic callouts.",
            "background": "Warm aged parchment with fibers, a faint grid, and two gentle paper creases.",
            "palette": ["ink for outlines", "terracotta for actors", "ochre for routes", "sage for outcomes"],
            "camera": "top-down-map-15deg", "lighting": "Soft upper-left light and short lower-right shadows.",
            "character_system": "Simplified paper figures with minimal faces, readable silhouettes, and no detailed hands.",
            "recurring_motif": "one continuous ochre route",
            "continuity_rules": ["Same parchment", "Same camera", "Same shadows", "No base-image text", "Same annotation tags"],
        },
        "shots": [{
            "id": "01", "placement_after": "After the workflow explanation", "anchor": "One article becomes one visual system.",
            "role": "process-station", "core_idea": "A visual bible keeps every image and label consistent.",
            "composition": "A paper worktable receives notes from the left and sends a coherent sequence of scenes to the right, leaving quiet upper space.",
            "main_subject": "visual-bible worktable", "supporting_elements": ["notes", "route", "framed scenes"],
            "motion_cues": ["notes approach the table", "frames unfold along the route"], "density": "low", "people_count": 1,
            "filename": "01-consistent-system.png", "alt_text_zh_tw": "羊皮紙工作台把文章轉成一致風格與標註的系列文內圖。", "caption_zh_tw": "",
            "annotation": {"enabled": True, "language": "zh-TW", "layout_status": "final",
                "headline": {"text": "先鎖定世界，再生成每張圖", "x": .38, "y": .05, "accent": "terracotta", "font_size": 42, "angle": 0},
                "labels": [
                    {"text": "文章錨點", "x": .05, "y": .2, "target_x": .22, "target_y": .43, "accent": "indigo", "font_size": 30, "angle": -2},
                    {"text": "同一視覺語言", "x": .43, "y": .25, "target_x": .53, "target_y": .50, "accent": "terracotta", "font_size": 31, "angle": 1},
                    {"text": "一致成品", "x": .76, "y": .2, "target_x": .82, "target_y": .48, "accent": "sage", "font_size": 30, "angle": -1},
                ]},
            "motion_beats": ["World appears", "Notes move", "Frames expand", "Final tableau holds"],
        }],
    }


class Tests(unittest.TestCase):
    def test_valid_manifest(self):
        errors, warnings = validator.validate_manifest(manifest())
        self.assertEqual(errors, []); self.assertEqual(warnings, [])

    def test_version_one_rejected(self):
        data = manifest(); data["version"] = 1
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_annotation_count_required(self):
        data = manifest(); data["shots"][0]["annotation"]["labels"] = []
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_still_prompt_reserves_space_but_hides_text(self):
        data = manifest(); lock = (ROOT / "references/style-lock.txt").read_text()
        output = renderer.render_still(lock, data["visual_bible"], data["shots"][0])
        self.assertIn("deterministic post-production", output)
        self.assertIn("Do not render text", output)
        self.assertNotIn("文章錨點", output)

    def test_motion_prompt(self):
        data = manifest(); lock = (ROOT / "references/style-lock.txt").read_text()
        output = renderer.render_motion(lock, data["visual_bible"], data["shots"][0])
        self.assertIn("exactly 10-second", output); self.assertIn("No voiceover", output)

    def test_explicit_local_font_path_is_preferred(self):
        with tempfile.TemporaryDirectory() as directory:
            font = Path(directory) / "local-font.ttc"
            font.write_bytes(b"placeholder")
            self.assertEqual(annotator.find_font(str(font)), font)


if __name__ == "__main__": unittest.main()
