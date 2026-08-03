# Editorial Documentary Illustrations

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> Automatically create a title-led featured image and the optimal number of context-aware inline illustrations in one coherent VOX-inspired parchment paper-cut editorial system.

This Skill is designed for Codex and other agents that follow `SKILL.md`. It plans the complete visual reading experience instead of generating a fixed number of decorative images.

## What it produces

- One featured image that directly answers the article title.
- Zero to six inline images, chosen automatically from article length, reading rhythm, context, and comprehension gain.
- Exact insertion positions for every inline image.
- Final 16:9 images with integrated, reviewed explanatory text.
- One shared Visual Bible across the featured and inline images.

## Approved visual system

- Warm aged parchment with a faint grid and subtle creases.
- Fine double-line border and restrained corner ornaments.
- Centered eyebrow, large headline, and concise subheadline at the top.
- A dimensional paper-craft tableau in the middle and lower canvas.
- Two to four compact labels with short leader lines.
- Optional bottom takeaway ribbon and one short caveat.
- People are optional; objects should carry the explanation when possible.

Inline images must match the approved featured image's parchment, border, typography hierarchy, paper depth, shadows, label cards, accents, and takeaway ribbon. They may not fall back to white sketches, split text panels, PPT cards, or generic vector diagrams.

## Featured-image Title Contract

Before creating the featured image, the Skill resolves:

- `claim`: the article title's main assertion.
- `key_result`: the result, number, or change readers should remember.
- `mechanism`: the main reason the result happens.

The featured image must visibly communicate the claim and at least one of the other two.

## Automatic image count

The total count includes the featured image:

| Reading time | Maximum total images |
|---|---:|
| 1 minute | 1 |
| 2 minutes | 2 |
| 3–4 minutes | 3 |
| 5–6 minutes | 4 |
| 7–9 minutes | 5 |
| 10–12 minutes | 6 |
| 13+ minutes | 7 |

The final count is:

```text
min(reading-time capacity, high-value non-redundant visual anchors)
```

The Skill never fills a quota. If two images explain the article best, it generates two.

## Automatic placement

- Featured image: immediately after the article title.
- Inline image: after the paragraph that first completes the relevant explanation.
- Inline images are normally separated by at least two body paragraphs.
- No decorative image after FAQs, references, author information, or a purely concluding paragraph.

Each manifest placement stores the section heading, global paragraph index, paragraph excerpt, and reason.

## Installation

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

No font files are bundled.

## Usage

### Plan only

```text
Use $editorial-documentary-illustrations
Analyze the article, resolve its Title Contract, and automatically decide the best total image count and insertion positions.
Create a version 6 manifest, but do not generate images yet.

<article>
```

### Generate the complete image set

```text
Use $editorial-documentary-illustrations
Generate the article's featured image and the optimal number of inline images.
The featured image must answer the article title. Every inline image must use the approved featured image as a style reference and explain one specific context anchor.
Use integrated text in the article's reader language and verify spelling, cropping, overlap, and cross-image consistency.

<article>
```

### Generate images and an HTML demo

```text
Use $editorial-documentary-illustrations
Generate the complete article image set and an HTML demo showing each image at its recommended insertion position.
Choose image count and placement automatically for the best reading and comprehension experience.

<article>
```

## Tooling

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 3 \
  --include-hero

python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts
```

`annotate_images.py` is a fallback renderer for repairing or deterministically placing text when direct image-model typography needs correction. The primary workflow generates the integrated final image first.

## Manifest version 6

Version 6 adds:

- `title_contract`
- automatic count inputs
- precise paragraph placement
- visual-anchor scoring
- integrated text fields
- hero-to-inline style continuity
- a fixed 1600×900 safe-layout contract

See [`templates/manifest.template.json`](templates/manifest.template.json) and [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json).

## Design principles

- The featured image answers the title, not a secondary subsection.
- Every inline image explains exactly one context-specific idea.
- Images appear only where they improve understanding.
- Text and imagery are designed together.
- Inline images must look like the same editorial series as the featured image.
- No important object or text may be covered, cropped, or pushed outside the frame.
- People are optional, never mandatory.

## Attribution and license

- Released under the [MIT License](LICENSE).
- The cognitive-anchor, one-image-one-idea, physical-metaphor, short-text, and QA workflow principles were inspired by and adapted from Ian's [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations); see [`NOTICE.md`](NOTICE.md).
- This repository does not include the Xiaohei character IP, example images, copied prompts, or font files.
- This project is not affiliated with, endorsed by, or produced by Vox Media. Do not copy specific frames, logos, title cards, typefaces, or branded assets.
