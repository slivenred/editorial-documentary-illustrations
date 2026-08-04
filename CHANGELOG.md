# Changelog

## 5.0.0 — 2026-08-03

- Switched the still-image prompt renderer to **lean prompts** (~300-350 words, down from ~1,100).
- **Root cause found by experiment:** the v4 prompt was over-specified — the verbatim style-lock dump, the 15-line visual-bible dump, the 8-bullet layout/safety list, the final self-check, and the per-label meaning lines crowded the model into producing flat, diagrammatic images. Regenerating the same hero with a 334-word prompt (rich scene + exact text + 4-line style) yielded a rich, tactile 3D paper-craft scene — the same model, dramatically better output.
- `render_still()` now emits: a concise context (Title Contract / Article Context), the scene paragraph as the centerpiece, the unchanged exact-text block, and one condensed style line (palette + title hierarchy + light + `outer_margin_px`). The `style-lock.txt` file is retained as human reference but is no longer dumped verbatim into prompts.
- Added the **aesthetic-generation vs text-fix separation** as the default workflow: generate the rich scene with a lean prompt; if a single string is wrong, run a targeted edit-regen (the 修字 prompt) — do not pre-load every text-safety constraint, which is what caused the over-specification.
- Light touch on `render_motion()`: replaced its verbatim style-lock block with a condensed style line (motion was already lean; text is never burned into animation).
- No schema or manifest change; `annotate_images.py` (fallback), `validate_manifest.py`, and `recommend_image_count.py` are unaffected. All 16 tooling tests pass unchanged (the four pinned strings — `RENDER VERBATIM`, `TITLE CONTRACT`, the inline style-reference line, and the `72px` margin — are retained).

## 4.0.0 — 2026-08-03

- Rebuilt the Skill around the approved title-centered parchment-tableau visual system.
- Made the featured image explicitly title-led through a required `title_contract` containing claim, key result, and mechanism.
- Required inline images to inherit the featured image's parchment, border, typography hierarchy, paper-craft depth, shadows, color semantics, compact labels, and takeaway ribbon.
- Replaced the split text-panel and scattered-callout approach with integrated final images: centered headline, concise subheadline, one physical tableau, 2–4 labels, optional takeaway, and optional caveat.
- Made people optional rather than a recurring visual requirement.
- Added automatic total image count based on reading time and high-value non-redundant anchors.
- Added exact paragraph-level placement using section heading, global paragraph index, paragraph excerpt, and placement reason.
- Upgraded the manifest to version 6 with Title Contract, anchor scoring, integrated text fields, style continuity, and a 1600×900 safe-layout contract.
- Updated the prompt renderer to send exact final text to the image model and to use the approved featured image as the inline-image style reference.
- Added hard QA gates for title alignment, context relevance, cropping, overlap, spelling, mobile readability, and cross-image continuity.
- Updated fallback text rendering for manifest version 6.
- Updated all localized README files, schema, template, scripts, tests, Agent prompt, references, and package manifest.
- No demo assets, third-party fonts, or GitHub Actions workflows were added.

## 3.0.0 — 2026-08-02

- Added automatic image-count and placement planning.
- Added integrated explanatory board layouts and manifest version 5.

## 2.0.0 — 2026-08-02

- Added source-grounding rules and semantic preflight.

## 1.3.0 — 2026-07-29

- Added multilingual README documentation.

## 1.2.0 — 2026-07-29

- Added article-aware annotation languages and manifest version 3.

## 1.1.0 — 2026-07-29

- Added deterministic semantic annotations.

## 1.0.0 — 2026-07-29

- Initial release.
