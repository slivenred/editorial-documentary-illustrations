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


validator = load("validator", ROOT / "scripts/validate_manifest.py")
renderer = load("renderer", ROOT / "scripts/render_prompts.py")
annotator = load("annotator", ROOT / "scripts/annotate_images.py")


def manifest() -> dict:
    return json.loads((ROOT / "templates/manifest.template.json").read_text(encoding="utf-8"))


class SemanticGroundingTests(unittest.TestCase):
    def test_valid_version_four_manifest(self):
        errors, warnings = validator.validate_manifest(manifest())
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_old_manifest_version_is_rejected(self):
        data = manifest()
        data["version"] = 3
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("version" in error for error in errors))

    def test_generic_topic_signature_is_rejected(self):
        data = manifest()
        data["article"]["topic_signature"] = ["AI", "model", "data"]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("generic terms" in error for error in errors))

    def test_hero_requires_three_must_show_items(self):
        data = manifest()
        data["shots"][0]["semantic_contract"]["must_show"] = ["bounded state", "retrieval layer"]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("at least 3 items" in error for error in errors))

    def test_technical_hero_cannot_use_abstract_metaphor(self):
        data = manifest()
        data["shots"][0]["visualization_mode"] = "abstract-metaphor"
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("abstract-metaphor" in error for error in errors))

    def test_technical_hero_requires_domain_faithful_role(self):
        data = manifest()
        data["shots"][0]["role"] = "physical-metaphor"
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("domain-faithful role" in error for error in errors))

    def test_hero_requires_topic_signature_overlap(self):
        data = manifest()
        contract = data["shots"][0]["semantic_contract"]
        contract["specificity_terms"] = ["unrelated object one", "unrelated object two"]
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("specificity_terms" in error for error in errors))

    def test_blind_caption_requires_article_specific_anchors(self):
        data = manifest()
        data["shots"][0]["semantic_contract"]["expected_blind_caption"] = (
            "A generic machine processes information through a clean paper scene."
        )
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("expected_blind_caption" in error for error in errors))

    def test_only_one_hero_and_hero_is_first(self):
        data = manifest()
        second = copy.deepcopy(data["shots"][0])
        second["id"] = "02"
        second["filename"] = "02-second-hero.png"
        data["article"]["target_count"] = 2
        data["shots"].append(second)
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("At most one" in error for error in errors))

    def test_annotation_language_must_match_article_target(self):
        data = manifest()
        data["shots"][0]["annotation"]["language"] = "zh-TW"
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("annotation.language" in error for error in errors))

    def test_unmapped_generic_factory_is_rejected_for_technical_hero(self):
        data = manifest()
        data["shots"][0]["composition"] = (
            "A generic factory with office workers around a machine, leaving quiet space at the top."
        )
        errors, _ = validator.validate_manifest(data)
        self.assertTrue(any("unmapped generic technical substitute" in error for error in errors))

    def test_kimi_linear_regression_contract_is_specific(self):
        data = manifest()
        data["article"].update({
            "title": "Kimi Linear",
            "slug": "kimi-linear",
            "visual_thesis": (
                "A 3:1 KDA–MLA interleave keeps exact retrieval in selected layers while replacing most growing KV cache with fixed recurrent state."
            ),
            "topic_signature": [
                "KDA", "MLA", "3:1 layer ratio", "fixed recurrent state",
                "growing KV cache", "1M-token decoding",
            ],
        })
        shot = data["shots"][0]
        shot["core_idea"] = "Three KDA layers and one MLA layer form one hybrid stack with bounded state and reduced KV growth."
        shot["semantic_contract"].update({
            "source_basis": [
                "Kimi Linear interleaves KDA and MLA in a 3:1 layer ratio.",
                "KDA uses fixed recurrent state while full attention retains a context-growing KV cache.",
            ],
            "must_show": [
                "one four-layer stack containing three KDA modules and one MLA module",
                "a fixed recurrent-state capsule beside a growing KV cache trail",
                "one token stream passing through the interleaved KDA and MLA stack",
            ],
            "visual_evidence": [
                {
                    "concept": "3:1 layer ratio",
                    "visible_form": "one stack with three terracotta KDA modules and one indigo MLA module",
                    "relationship": "all four modules are interleaved inside the same model stack",
                },
                {
                    "concept": "fixed recurrent state",
                    "visible_form": "one compact state capsule that does not lengthen",
                    "relationship": "the capsule stays bounded while the comparison KV trail grows",
                },
                {
                    "concept": "growing KV cache",
                    "visible_form": "a visibly lengthening trail of memory cards",
                    "relationship": "the trail expands with context beside the fixed KDA state",
                },
            ],
            "specificity_terms": ["KDA", "MLA", "3:1 layer ratio", "fixed recurrent state"],
            "expected_blind_caption": (
                "A Kimi Linear stack interleaves three KDA modules with one MLA module while fixed recurrent state is contrasted with a growing KV cache trail."
            ),
            "hero_artifact": "one interleaved Kimi Linear KDA–MLA four-layer stack",
        })
        errors, warnings = validator.validate_manifest(data)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_prompt_places_meaning_before_style(self):
        data = manifest()
        style_lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        output = renderer.render_still(
            style_lock, data["article"], data["visual_bible"], data["shots"][0]
        )
        semantic_index = output.index("NON-NEGOTIABLE SEMANTIC CONTRACT")
        style_index = output.index("ORIGINAL EDITORIAL DOCUMENTARY CUTOUT STYLE LOCK")
        self.assertLess(semantic_index, style_index)
        self.assertIn("MEANING OVERRIDES STYLE", output)
        self.assertIn("3:1 layer ratio", output)
        self.assertIn("Expected blind caption", output)

    def test_prompt_does_not_leak_annotation_text(self):
        data = manifest()
        style_lock = (ROOT / "references/style-lock.txt").read_text(encoding="utf-8")
        output = renderer.render_still(
            style_lock, data["article"], data["visual_bible"], data["shots"][0]
        )
        self.assertNotIn("3 bounded-state layers", output)
        self.assertNotIn("Most layers keep state compact", output)
        self.assertIn("Do not render text", output)

    def test_annotation_plan_carries_semantic_contract(self):
        data = manifest()
        plan = renderer.annotation_plan(data)
        self.assertIn("semantic_contract", plan["images"][0])
        self.assertEqual(plan["images"][0]["image_role"], "hero")

    def test_annotator_requires_version_four(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "manifest.json"
            path.write_text(json.dumps(manifest()), encoding="utf-8")
            loaded = annotator.load_manifest(path)
            self.assertEqual(loaded["version"], 4)

    def test_font_group_follows_annotation_language(self):
        self.assertEqual(annotator.font_group("zh-TW"), "zh")
        self.assertEqual(annotator.font_group("ja"), "ja")
        self.assertEqual(annotator.font_group("ar"), "arabic")
        self.assertEqual(annotator.font_group("en"), "latin")

    def test_render_cli_smoke(self):
        data = manifest()
        with tempfile.TemporaryDirectory() as directory:
            directory_path = Path(directory)
            manifest_path = directory_path / "manifest.json"
            output_path = directory_path / "out"
            manifest_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [
                    "python", str(ROOT / "scripts/render_prompts.py"), str(manifest_path),
                    "--mode", "still", "--output", str(output_path),
                ],
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((output_path / "01-hybrid-attention-stack-still.txt").is_file())
            self.assertTrue((output_path / "annotation-plan.json").is_file())


if __name__ == "__main__":
    unittest.main()
