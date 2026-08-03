#!/usr/bin/env python3
from __future__ import annotations

import copy
import importlib.util
import json
import subprocess
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


recommender = load("recommender", ROOT / "scripts/recommend_image_count.py")
validator = load("validator", ROOT / "scripts/validate_manifest.py")
renderer = load("renderer", ROOT / "scripts/render_prompts.py")
annotator = load("annotator", ROOT / "scripts/annotate_images.py")


def manifest() -> dict:
    return json.loads((ROOT / "templates/manifest.template.json").read_text(encoding="utf-8"))


class Tests(unittest.TestCase):
    def test_recommendation_for_four_minute_article_is_three(self):
        self.assertEqual(recommender.recommend_count(4, 3, True), 3)

    def test_short_article_can_use_one_image(self):
        self.assertEqual(recommender.recommend_count(1, 4, True), 1)

    def test_estimate_cjk_reading_time(self):
        minutes = recommender.estimate_reading_minutes("測" * 900, "zh-TW")
        self.assertAlmostEqual(minutes, 2.0, places=1)

    def test_valid_v6_manifest(self):
        errors, warnings = validator.validate_manifest(manifest())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_old_version_is_rejected(self):
        data = manifest()
        data["version"] = 5
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("version" in error for error in errors))

    def test_target_count_must_match_auto_recommendation(self):
        data = manifest()
        data["article"]["target_count"] = 2
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("automatic recommendation" in error for error in errors))

    def test_hero_must_be_first(self):
        data = manifest()
        data["shots"][0], data["shots"][1] = data["shots"][1], data["shots"][0]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("hero" in error.lower() for error in errors))

    def test_hero_must_cover_claim(self):
        data = manifest()
        data["shots"][0]["title_coverage"] = ["key_result", "mechanism"]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("claim" in error for error in errors))

    def test_low_value_anchor_is_rejected(self):
        data = manifest()
        score = data["shots"][1]["anchor_score"]
        for key in score:
            score[key] = 1
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("anchor score" in error for error in errors))

    def test_inline_positions_are_ordered(self):
        data = manifest()
        data["shots"][1]["placement"]["after_paragraph_global_index"] = 7
        data["shots"][2]["placement"]["after_paragraph_global_index"] = 6
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("ordered" in error for error in errors))

    def test_labels_are_limited_to_four(self):
        data = manifest()
        data["shots"][0]["labels"].append(copy.deepcopy(data["shots"][0]["labels"][0]))
        data["shots"][0]["labels"].append(copy.deepcopy(data["shots"][0]["labels"][1]))
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("labels" in error for error in errors))

    def test_prompt_contains_exact_text_and_safe_layout(self):
        data = manifest()
        lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        output = renderer.render_still(lock, data, data["shots"][1])
        self.assertIn("RENDER VERBATIM", output)
        self.assertIn(data["shots"][1]["headline"], output)
        self.assertIn("Use the approved featured image only as a style reference", output)
        self.assertIn("72px", output)

    def test_hero_prompt_contains_title_contract(self):
        data = manifest()
        lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        output = renderer.render_still(lock, data, data["shots"][0])
        self.assertIn("TITLE CONTRACT", output)
        self.assertIn(data["article"]["title_contract"]["claim"], output)

    def test_placement_plan_contains_paragraph_indices(self):
        output = renderer.placement_plan(manifest())
        self.assertIn("After paragraph", output)
        self.assertIn("| 3 |", output)

    def test_annotator_requires_v6(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest(), ensure_ascii=False), encoding="utf-8")
            loaded = annotator.load_manifest(path)
            self.assertEqual(loaded["version"], 6)

    def test_cli_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            manifest_path = directory_path / "manifest.json"
            output_path = directory_path / "out"
            manifest_path.write_text(json.dumps(manifest(), ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    "python3", str(ROOT / "scripts/render_prompts.py"), str(manifest_path),
                    "--mode", "still", "--output", str(output_path),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_path / "00-kimi-linear-featured-still.txt").is_file())
            self.assertTrue((output_path / "placement-plan.md").is_file())


if __name__ == "__main__":
    unittest.main()
