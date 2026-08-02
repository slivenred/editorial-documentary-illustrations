#!/usr/bin/env python3
"""Run deterministic semantic preflight before generating article illustrations."""
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_manifest.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("manifest_validator", VALIDATOR)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {VALIDATOR}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--json", action="store_true", help="Print a machine-readable report.")
    args = parser.parse_args()

    try:
        data = json.loads(args.manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    validator = load_validator()
    errors, warnings = validator.validate_manifest(data)
    topic_signature = data.get("article", {}).get("topic_signature", [])
    rows = []
    for shot in data.get("shots", []):
        contract = shot.get("semantic_contract", {})
        specificity = contract.get("specificity_terms", [])
        expected_caption = contract.get("expected_blind_caption", "")
        rows.append({
            "id": shot.get("id"),
            "image_role": shot.get("image_role"),
            "visualization_mode": shot.get("visualization_mode"),
            "must_show_count": len(contract.get("must_show", [])),
            "visual_evidence_count": len(contract.get("visual_evidence", [])),
            "signature_overlap": sorted(validator.terms_overlap(specificity, topic_signature)),
            "blind_caption_overlap": sorted(validator.terms_overlap(topic_signature, [expected_caption])),
            "hero_artifact": contract.get("hero_artifact", ""),
        })

    report = {
        "version": data.get("version"),
        "article_type": data.get("article", {}).get("article_type"),
        "visual_thesis": data.get("article", {}).get("visual_thesis"),
        "topic_signature": topic_signature,
        "shots": rows,
        "warnings": warnings,
        "errors": errors,
        "pass": not errors,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"Article type: {report['article_type']}")
        print(f"Visual thesis: {report['visual_thesis']}")
        print(f"Topic signature: {'; '.join(topic_signature)}")
        print("")
        print("ID  Role    Mode               Must  Evidence  Signature  Blind caption  Hero artifact")
        print("--  ------  -----------------  ----  --------  ---------  -------------  -------------")
        for row in rows:
            print(
                f"{str(row['id']):<2}  {str(row['image_role']):<6}  {str(row['visualization_mode']):<17}  "
                f"{row['must_show_count']:<4}  {row['visual_evidence_count']:<8}  "
                f"{len(row['signature_overlap']):<9}  {len(row['blind_caption_overlap']):<13}  "
                f"{row['hero_artifact'] or '—'}"
            )
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print("")
        print("PASS" if not errors else "FAILED")

    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
