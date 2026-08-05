# Changelog

## 6.0.0 — 2026-08-05

- Replaced the runtime Skill with one self-contained article-to-images SOP.
- The Skill now performs article analysis, language resolution, Title Contract creation, automatic image count, paragraph-level placement, actual image generation, QA, asset saving, and Markdown/MDX/HTML insertion from one invocation.
- Preserved lean image-model prompts: each generated image receives exact text, one physical scene, 2–6 objects, one compact Style Lock, and safe-layout constraints only.
- Added explicit fallback behavior when approved reference images are unavailable, so the workflow does not stop.
- Added targeted text-edit instructions, retry limits, final delivery requirements, and article-insertion rules.
- Updated the default Agent prompt and English/Traditional Chinese README entry points.
- Added `assets/style-reference/README.md`; no binary reference images, font files, demos, or GitHub Actions workflows were added.

## 5.0.0 — 2026-08-03

- Switched the still-image prompt renderer to lean prompts after experiments showed that over-specified prompts produced flatter, more diagrammatic images.
- Separated aesthetic generation from targeted text repair.

## 4.0.0 — 2026-08-03

- Added title-led featured images, inline visual continuity, automatic image count, paragraph placement, integrated text, and manifest version 6.

## 3.0.0 — 2026-08-02

- Added automatic image-count and placement planning.

## 2.0.0 — 2026-08-02

- Added source-grounding rules and semantic preflight.

## 1.3.0 — 2026-07-29

- Added multilingual README documentation.

## 1.2.0 — 2026-07-29

- Added article-aware annotation languages.

## 1.1.0 — 2026-07-29

- Added deterministic semantic annotations.

## 1.0.0 — 2026-07-29

- Initial release.
