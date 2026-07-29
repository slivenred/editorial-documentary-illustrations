# Changelog

## 1.1.0 — 2026-07-29

- Changed still-image output from text-free final art to a two-layer workflow: text-free model base image plus deterministic semantic annotation.
- Added one insight headline and 3–6 contextual callout labels as the default final-image contract.
- Added `references/annotation-system.md` with semantic writing, color, layout, coordinate, typography, and mobile-readability rules.
- Upgraded the shot manifest to version 2 with normalized annotation coordinates and callout targets.
- Added `scripts/annotate_images.py` for reproducible paper-tag annotation rendering with locally installed CJK fonts.
- Updated prompt rendering to reserve quiet annotation regions without asking the image model to draw text.
- Added separate base-image and final-annotation QA gates plus annotation-specific retry strategies.
- Updated the default Agent prompt, template, schema, validator, tests, README, and package manifest.
- Added a Pillow dependency file for annotation rendering; no font files are bundled.

## 1.0.0 — 2026-07-29

- Initial release.
- Added article cognitive-anchor workflow.
- Added article-level visual bible and immutable style lock.
- Added static 16:9 documentary cutout prompt mode.
- Added exactly 10-second, 24fps motion prompt mode.
- Added JSON Schema, no-dependency validator, and prompt renderer.
- Added QA scoring and issue-specific retry ladder.
- Added a reusable manifest template and self-contained tooling tests.
- Added MIT attribution for the Ian Xiaohei Illustrations workflow adaptation.
