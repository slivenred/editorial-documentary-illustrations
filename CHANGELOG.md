# Changelog

## 2.0.0 — 2026-08-02

- Added a mandatory source-grounded semantic contract for every hero and inline illustration.
- Upgraded the shot manifest to version 4 with `article_type`, `visual_thesis`, `topic_signature`, `global_must_avoid`, `image_role`, `visualization_mode`, and per-shot `semantic_contract` fields.
- Added explicit hero-image rules: one hero maximum, first position, domain-specific hero artifact, three or more must-show items, and article-signature overlap.
- Added domain-faithful technical-research modes and composition patterns for architecture stacks, mechanisms, resource contrasts, and claim comparisons.
- Reordered prompt assembly so the non-negotiable semantic contract and visual-evidence mapping appear before the Style Lock and Visual Bible.
- Added Label-off, Blind-caption, and Neighbor-article tests to prevent attractive but interchangeable illustrations.
- Added deterministic `scripts/semantic_preflight.py` and strengthened manifest validation so semantically generic plans are rejected before image generation.
- Updated Base QA, annotation rules, retry strategies, motion mode, template, renderer, annotation tool, tests, English README, and Traditional Chinese README.
- Added a Kimi Linear regression case to document why generic factories, cities, workers, gears, and server towers cannot substitute for KDA, MLA, a 3:1 interleave, bounded recurrent state, or growing KV cache.
- No demo assets, example images, font files, or GitHub Actions workflows were added.

## 1.3.0 — 2026-07-29

- Reworked the default `README.md` as an English entry point for international users.
- Added complete Traditional Chinese, Simplified Chinese, Japanese, Korean, and Spanish README translations.
- Added a consistent language switcher to every README.
- Synchronized installation, version 3 manifest, language-resolution, annotation, validation, attribution, and brand-safety documentation across all languages.

## 1.2.0 — 2026-07-29

- Replaced the hard-coded Traditional Chinese annotation default with automatic article-language resolution.
- Added explicit `article.annotation_language` using concrete BCP 47 tags; rejected unresolved `auto`/`und` values and required concrete per-shot languages.
- Added deterministic precedence rules for user overrides, article metadata, dominant reader-facing prose, mixed-language content, and conversation fallback.
- Preserved product names, model names, benchmarks, acronyms, versions, numbers, units, and percentages from the source article.
- Upgraded the manifest to version 3 with language-neutral `alt_text` and `caption` fields.
- Added validator checks that keep per-shot annotation languages aligned with the article target language, while supporting explicit multilingual output through `mul`.
- Made the annotation renderer select local fonts by language/script instead of always requiring a CJK font.
- Added RTL-aware rendering when Pillow has RAQM support.

## 1.1.0 — 2026-07-29

- Changed still-image output from text-free final art to a two-layer workflow: text-free model base image plus deterministic semantic annotation.
- Added one insight headline and 3–6 contextual callout labels as the default final-image contract.
- Added `references/annotation-system.md` with semantic writing, color, layout, coordinate, typography, and mobile-readability rules.
- Added `scripts/annotate_images.py` for reproducible paper-tag annotation rendering with locally installed fonts.
- Added separate base-image and final-annotation QA gates plus annotation-specific retry strategies.

## 1.0.0 — 2026-07-29

- Initial release.
- Added article cognitive-anchor workflow.
- Added article-level visual bible and immutable style lock.
- Added static 16:9 documentary cutout prompt mode.
- Added exactly 10-second, 24fps motion prompt mode.
- Added JSON Schema, validator, prompt renderer, QA scoring, retry ladder, template, and tests.
- Added MIT attribution for the Ian Xiaohei Illustrations workflow adaptation.
