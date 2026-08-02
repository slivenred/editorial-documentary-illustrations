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


class PlanningTests(unittest.TestCase):
    def test_kimi_four_minute_article_recommends_three_images(self):
        result = recommender.recommend_count(4, 4, 5, True)
        self.assertEqual(result["recommended_total"], 3)

    def test_short_article_is_not_forced_to_five_images(self):
        result = recommender.recommend_count(2, 7, 6, True)
        self.assertEqual(result["recommended_total"], 1)

    def test_long_article_caps_at_eight(self):
        result = recommender.recommend_count(30, 20, 20, True)
        self.assertEqual(result["recommended_total"], 8)

    def test_valid_template(self):
        errors, warnings = validator.validate_manifest(manifest())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_old_version_is_rejected(self):
        data = manifest()
        data["version"] = 4
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("version" in error for error in errors))

    def test_auto_count_rejects_overproduction(self):
        data = manifest()
        extra = copy.deepcopy(data["shots"][-1])
        extra["id"] = "04"
        extra["filename"] = "04-extra-image.png"
        extra["placement"]["section_index"] = 5
        extra["placement"]["after_paragraph_index"] = 11
        extra["placement"]["after_paragraph_excerpt"] = "Extra paragraph for an unnecessary image."
        data["shots"].append(extra)
        data["article"]["target_count"] = 4
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("Auto image count recommends 3" in error for error in errors))

    def test_fixed_mode_allows_explicit_override(self):
        data = manifest()
        data["article"]["image_count_mode"] = "fixed"
        data["article"]["target_count"] = 2
        data["shots"] = data["shots"][:2]
        errors, warnings = validator.validate_manifest(data)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_inline_images_need_two_paragraph_gap(self):
        data = manifest()
        data["shots"][2]["placement"]["after_paragraph_index"] = 5
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("at least two paragraph" in error for error in errors))

    def test_hero_must_be_first_when_enabled(self):
        data = manifest()
        data["shots"][0], data["shots"][1] = data["shots"][1], data["shots"][0]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("exactly one hero must be the first" in error for error in errors))

    def test_generic_headline_is_rejected(self):
        data = manifest()
        data["shots"][0]["headline"] = "重點整理"
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("headline" in error and "generic" in error for error in errors))


class PromptTests(unittest.TestCase):
    def test_still_prompt_is_context_first_and_not_semantic_contract_heavy(self):
        data = manifest()
        style_lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        prompt = renderer.render_still(style_lock, data["article"], data["visual_bible"], data["shots"][0])
        self.assertIn("ARTICLE CONTEXT", prompt)
        self.assertIn("EXPLAINER-TO-VISUAL MAPPING", prompt)
        self.assertIn("hero-explainer", prompt)
        self.assertNotIn("NON-NEGOTIABLE SEMANTIC CONTRACT", prompt)
        self.assertNotIn("Blind-caption", prompt)
        self.assertIn("Do not over-engineer", prompt)

    def test_prompt_preserves_final_text_meaning_but_forbids_rendered_text(self):
        data = manifest()
        style_lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        prompt = renderer.render_still(style_lock, data["article"], data["visual_bible"], data["shots"][0])
        self.assertIn(data["shots"][0]["headline"], prompt)
        self.assertIn("No text, letters, numbers", prompt)

    def test_motion_prompt(self):
        data = manifest()
        style_lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        prompt = renderer.render_motion(style_lock, data["article"], data["visual_bible"], data["shots"][0])
        self.assertIn("exactly 10-second", prompt)
        self.assertIn("No voiceover", prompt)

    def test_render_cli_smoke(self):
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            manifest_path = temp / "manifest.json"
            output = temp / "out"
            manifest_path.write_text(json.dumps(manifest(), ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    "python3", str(ROOT / "scripts/render_prompts.py"), str(manifest_path),
                    "--mode", "still", "--output", str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output / "01-kimi-linear-overview-still.txt").is_file())
            self.assertTrue((output / "delivery.md").is_file())


class AnnotationTests(unittest.TestCase):
    def test_font_groups(self):
        self.assertEqual(annotator.font_group("zh-TW"), "zh")
        self.assertEqual(annotator.font_group("ja"), "ja")
        self.assertEqual(annotator.font_group("ar"), "arabic")
        self.assertEqual(annotator.font_group("en"), "latin")

    def test_layout_boxes(self):
        hero = annotator.card_boxes(1600, 900, "hero-explainer", 3)
        mechanism = annotator.card_boxes(1600, 900, "mechanism-focus", 3)
        self.assertEqual(len(hero), 3)
        self.assertEqual(len(mechanism), 3)
        self.assertGreater(hero[1][0], hero[0][0])
        self.assertGreater(mechanism[1][1], mechanism[0][1])

    def test_annotator_requires_version_five(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            data = manifest()
            path.write_text(json.dumps(data), encoding="utf-8")
            self.assertEqual(annotator.load_manifest(path)["version"], 5)

    def test_annotation_render_smoke(self):
        mods = annotator.pillow()
        Image = mods[0]
        with tempfile.TemporaryDirectory() as directory:
            temp = Path(directory)
            source = temp / "source.png"
            target = temp / "target.png"
            Image.new("RGB", (1600, 900), "#DFC99B").save(source)
            font = annotator.find_font(None, "zh-TW", "測試文字")
            annotator.annotate_image(mods, source, target, manifest()["shots"][0], font, "zh-TW")
            self.assertTrue(target.is_file())
            with Image.open(target) as image:
                self.assertEqual(image.size, (1600, 900))


if __name__ == "__main__":
    unittest.main()
