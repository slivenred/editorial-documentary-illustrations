#!/usr/bin/env python3
from __future__ import annotations
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load("validator", ROOT / "scripts/validate_manifest.py")
renderer = load("renderer", ROOT / "scripts/render_prompts.py")
annotator = load("annotator", ROOT / "scripts/annotate_images.py")


def manifest(annotation_language: str = "en"):
    return {
        "version": 3,
        "article": {
            "title": "Editorial workflow", "slug": "editorial-workflow", "language": "en",
            "annotation_language": annotation_language,
            "summary": "A reusable manifest that verifies prompt and annotation tooling behavior.",
            "target_count": 1,
        },
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
            "filename": "01-consistent-system.png", "alt_text": "A parchment worktable turns one article into a consistent illustrated system.", "caption": "",
            "annotation": {"enabled": True, "language": annotation_language, "layout_status": "final",
                "headline": {"text": "Lock the world before generating the series", "x": .34, "y": .05, "accent": "terracotta", "font_size": 42, "angle": 0},
                "labels": [
                    {"text": "Article anchor", "x": .05, "y": .2, "target_x": .22, "target_y": .43, "accent": "indigo", "font_size": 30, "angle": -2},
                    {"text": "Shared visual language", "x": .40, "y": .25, "target_x": .53, "target_y": .50, "accent": "terracotta", "font_size": 31, "angle": 1},
                    {"text": "Consistent output", "x": .72, "y": .2, "target_x": .82, "target_y": .48, "accent": "sage", "font_size": 30, "angle": -1},
                ]},
            "motion_beats": ["World appears", "Notes move", "Frames expand", "Final tableau holds"],
        }],
    }


class Tests(unittest.TestCase):
    def test_valid_language_aware_manifest(self):
        errors, warnings = validator.validate_manifest(manifest("en"))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_auto_language_is_rejected(self):
        data = manifest("en")
        data["article"]["annotation_language"] = "auto"
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_shot_language_must_match_article_target(self):
        data = manifest("en")
        data["shots"][0]["annotation"]["language"] = "zh-TW"
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_undetermined_annotation_language_is_rejected(self):
        data = manifest("und")
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_multilingual_shot_still_requires_concrete_language(self):
        data = manifest("mul")
        data["shots"][0]["annotation"]["language"] = "mul"
        self.assertTrue(validator.validate_manifest(data)[0])

    def test_multilingual_article_allows_per_shot_language(self):
        data = manifest("mul")
        data["shots"][0]["annotation"]["language"] = "ja"
        errors, _ = validator.validate_manifest(data)
        self.assertEqual(errors, [])

    def test_still_prompt_reserves_space_but_hides_text(self):
        data = manifest("en")
        lock = (ROOT / "references/style-lock.txt").read_text()
        output = renderer.render_still(lock, data["visual_bible"], data["shots"][0])
        self.assertIn("deterministic post-production", output)
        self.assertIn("Do not render text", output)
        self.assertNotIn("Article anchor", output)

    def test_motion_prompt(self):
        data = manifest("en")
        lock = (ROOT / "references/style-lock.txt").read_text()
        output = renderer.render_motion(lock, data["visual_bible"], data["shots"][0])
        self.assertIn("exactly 10-second", output)
        self.assertIn("No voiceover", output)

    def test_font_group_follows_language(self):
        self.assertEqual(annotator.font_group("zh-TW"), "zh")
        self.assertEqual(annotator.font_group("ja"), "ja")
        self.assertEqual(annotator.font_group("ar"), "arabic")
        self.assertEqual(annotator.font_group("en"), "latin")

    def test_explicit_local_font_path_is_preferred(self):
        with tempfile.TemporaryDirectory() as directory:
            font = Path(directory) / "local-font.ttf"
            font.write_bytes(b"placeholder")
            self.assertEqual(annotator.find_font(str(font), "en", "Sample"), font)


if __name__ == "__main__":
    unittest.main()
