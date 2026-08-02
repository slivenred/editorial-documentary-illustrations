# Changelog

## 3.0.0 — 2026-08-02

- Simplified the illustration workflow after the version 4 Kimi Linear regression produced technically dense but less readable images.
- Replaced the fixed semantic-contract and blind-caption pipeline with an integrated editorial explainer board: eyebrow, headline, subheadline, context-specific VOX-inspired cutout visual, and 2–4 explanation cards.
- Added automatic image-count planning based on reading time, high-value non-redundant anchors, section count, and whether a hero image is requested.
- Added automatic placement rules using the exact section, paragraph index, paragraph excerpt, and placement reason.
- Added six layouts: hero explainer, mechanism focus, process strip, comparison split, timeline route, and result board.
- Added `scripts/recommend_image_count.py` and upgraded the manifest to version 5.
- Reworked prompt rendering so image and text explain the idea together instead of forcing the text-free base to carry every technical detail.
- Reworked deterministic annotation rendering into one stable reading hierarchy without scattered sticker callouts or crossing leader lines.
- Updated validation, QA, retry rules, motion mode, Visual Bible, style rules, templates, tests, README documentation, and the default Agent prompt.
- Added a Kimi Linear planning example that recommends three total images for a four-minute article: one overview hero, one KDA mechanism image, and one long-context result image.
- Abstracted only the general information-hierarchy lessons visible in dbskill diagrams; no dbskill SVG, CSS, layout coordinates, source assets, or code were copied.
- Removed the obsolete `references/semantic-grounding.md` and `scripts/semantic_preflight.py` from the published package.
- No demo assets, font files, or GitHub Actions workflows were added.

## 2.0.0 — 2026-08-02

- Added a mandatory source-grounded semantic contract for every hero and inline illustration.
- Upgraded the shot manifest to version 4.
- Added Label-off, Blind-caption, and Neighbor-article tests.
- Added `scripts/semantic_preflight.py`.

## 1.3.0 — 2026-07-29

- Added English, Traditional Chinese, Simplified Chinese, Japanese, Korean, and Spanish README documentation.

## 1.2.0 — 2026-07-29

- Replaced the hard-coded Traditional Chinese annotation default with automatic article-language resolution.
- Upgraded the manifest to version 3 with language-neutral `alt_text` and `caption` fields.
- Added language-aware local-font selection and RTL-aware rendering.

## 1.1.0 — 2026-07-29

- Added deterministic semantic annotations to text-free base images.
- Added annotation planning, QA, and local-font rendering.

## 1.0.0 — 2026-07-29

- Initial release.
- Added article analysis, Visual Bible, Style Lock, static still prompts, 10-second motion prompts, validation, QA, and retry rules.
