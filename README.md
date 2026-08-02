# Editorial Documentary Illustrations

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> Automatically choose the best number and placement of article illustrations, then create context-specific VOX-inspired parchment cutouts with integrated explanatory text.

This Skill is designed for Codex and other agents that can follow `SKILL.md`. It combines an editorial cutout scene with a clear information hierarchy:

```text
eyebrow → headline → subheadline → cutout visual → 2–4 explainer cards
```

The goal is not a text-free illustration that must encode an entire paper by itself, and not a generic AI image rescued by scattered labels. Image and text are planned together.

## What changed in version 5

The previous workflow became too technical: semantic contracts, blind-caption tests, grouping brackets, comparison bars, and many callouts could produce an accurate-looking diagram that felt less like an editorial illustration.

Version 5 simplifies the workflow:

- image count is automatic rather than fixed at five;
- image placement is tied to real paragraph excerpts;
- one image answers one question;
- the scene uses only 2–6 key object types;
- text is integrated through a stable header and card system;
- technical precision lives in concise explainer cards instead of a dense paper diagram;
- scattered callout stickers and crossing leader lines are avoided.

## Automatic image count

The agent scores non-redundant visual anchors and limits the total by reading time:

| Reading time | Maximum total images |
|---|---:|
| 1–2 min | 1 |
| 3–4 min | 3 |
| 5–6 min | 4 |
| 7–9 min | 5 |
| 10–12 min | 6 |
| 13–16 min | 7 |
| 17+ min | 8 |

The final count is:

```text
min(reading-time capacity, high-value non-redundant anchors)
```

A hero image counts toward the total. The agent never adds an image only to fill a quota.

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 4 \
  --sections 5 \
  --include-hero
```

For a four-minute Kimi Linear article, this recommends three total images rather than four or five.

## Automatic placement

- Hero: after the article title.
- Inline image: after the paragraph that completes the first useful explanation of the concept.
- Never place an image directly after a heading before the concept is introduced.
- Keep at least two body paragraphs between inline images.
- Avoid FAQ, references, author bio, and decorative end-of-article placements.
- Store the section, paragraph index, exact excerpt, and reason in the manifest.

## Six layouts

- `hero-explainer` — headline, central visual, three bottom cards.
- `mechanism-focus` — mechanism on the left, cards on the right.
- `process-strip` — one visual process with ordered stage cards.
- `comparison-split` — two comparable sides plus a takeaway.
- `timeline-route` — one route through three or four stages.
- `result-board` — one result scene plus metric or decision cards.

## Installation

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

No font files are bundled. The renderer finds a compatible local font from `article.annotation_language`, or accepts `--font /path/to/font.ttf`.

## Usage

### Plan only

```text
Use $editorial-documentary-illustrations
Analyze this article. Automatically choose the best image count and insertion positions.
For every selected anchor, create a version 5 shot using one integrated explainer layout.
Do not generate images yet.

<article>
```

### Generate the complete set

```text
Use $editorial-documentary-illustrations
Generate the best number of 16:9 VOX-inspired parchment-cutout article images.
Do not force five images. Each image must directly match its section and include one headline, one subheadline, and 2–4 concise explainer cards in the article language.
Generate text-free bases first, then render the integrated text layout.

<article>
```

## Commands

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts

python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

## Version 5 manifest

```json
{
  "version": 5,
  "article": {
    "reading_minutes": 4,
    "section_count": 5,
    "image_count_mode": "auto",
    "include_hero": true,
    "high_value_anchor_count": 4,
    "target_count": 3,
    "count_reason": "Three non-redundant visual anchors fit a four-minute article."
  },
  "shots": [
    {
      "kind": "hero",
      "layout": "hero-explainer",
      "headline": "Most layers stay linear; a few preserve exact retrieval",
      "subheadline": "A 3:1 hybrid balances bounded memory with precise matching.",
      "visual_story": "A simple four-layer paper stack with three KDA modules and one MLA module...",
      "explainers": [
        {
          "title": "3:1 hybrid",
          "body": "Three KDA layers for every MLA layer.",
          "accent": "terracotta",
          "visual_anchor": "the central four-layer paper stack"
        }
      ]
    }
  ]
}
```

See [`templates/manifest.template.json`](templates/manifest.template.json) and [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json).

## Repository structure

```text
.
├── SKILL.md
├── README*.md
├── references/
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── recommend_image_count.py
│   ├── validate_manifest.py
│   ├── render_prompts.py
│   └── annotate_images.py
└── tests/test_tooling.py
```

## License and attribution

- Released under the [MIT License](LICENSE).
- The multi-step workflow was inspired by Ian's [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations); see [`NOTICE.md`](NOTICE.md).
- No source artwork, Xiaohei character IP, copied prompt, or font file is included.
- This project is not affiliated with Vox Media. “VOX-inspired” describes a general editorial cutout grammar, not permission to copy branded assets.
