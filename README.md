# Editorial Documentary Illustrations

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> Turn an article’s mechanisms, comparisons, causal chains, and results into a consistent series of semantically grounded 16:9 parchment-cutout illustrations with reviewed annotations.

**Editorial Documentary Illustrations** is an installable Skill for Codex and other agents that can follow `SKILL.md`. It does not treat a recognizable visual style as proof of relevance. Before generation, every image receives a source-grounded semantic contract that defines what the unannotated base image must visibly show, how the concepts relate, and which generic substitutions are forbidden.

## The failure this update addresses

A polished parchment-cutout image can still be useless when it could illustrate dozens of unrelated articles after changing only the labels. This happens when the workflow locks style but leaves article meaning as free-form prose.

The Skill now separates six responsibilities:

- **Article map and cognitive anchors** — identify the mechanism, relationship, trade-off, change, or result worth visualizing.
- **Article semantic foundation** — define `article_type`, `visual_thesis`, `topic_signature`, and `global_must_avoid`.
- **Per-shot semantic contract** — define source claims, must-show evidence, visual mappings, specificity terms, blind-caption target, and hero artifact.
- **Article Visual Bible and Style Lock** — keep material, palette, camera, lighting, proportions, and annotation style consistent without replacing the article mechanism.
- **Language-aware deterministic annotations** — generate text-free images, then add reviewed labels in the resolved article or audience language.
- **Three-stage QA** — Semantic Preflight, Base QA, and Annotation QA.

## Meaning overrides style

The unannotated image must already be article-specific. An annotation may name a visible component, but it may not turn a generic machine, city, factory, robot, brain, server tower, road, shield, or group of workers into a technical mechanism after the fact.

For technical research, the default priority is:

1. `literal-technical`
2. `hybrid-metaphor`
3. `literal-scene`
4. `abstract-metaphor` only when no domain-faithful structure is possible

A technical-research hero may not use `abstract-metaphor`.

## Workflow

```text
Article and primary sources
  ↓
Article map + article type
  ↓
Visual thesis + topic signature
  ↓
Version 4 semantic contracts
  ↓
Semantic Preflight
  ↓
Text-free calibration image
  ↓
Label-off + Blind-caption + Neighbor-article tests
  ↓
Remaining grounded base images
  ↓
Language resolution + annotation plan
  ↓
Deterministic paper-tag rendering
  ↓
Final Annotation QA
```

## The semantic contract

Every shot includes:

- `image_role`: `hero` or `inline`
- `visualization_mode`
- `source_basis`
- `must_show`
- `must_not_show`
- `visual_evidence`: concept → visible form → required relationship
- `specificity_terms`
- `expected_blind_caption`
- `hero_artifact` for a hero image

A hero must be first, must be unique, must contain at least three must-show items, and must overlap the article topic signature with at least two specificity terms.

## Three mandatory semantic tests

### Label-off test

Hide every annotation. The mechanism and relationship must still be visible.

### Blind-caption test

Describe the unannotated image in one sentence. The description must contain at least two article-specific anchors for a hero and preserve the intended relationship.

### Neighbor-article test

If changing labels alone would make the same image suitable for another article, the base image fails.

## Annotation language resolution

The Skill resolves the target language in this order:

1. explicit user instruction;
2. article frontmatter, locale, or `lang` metadata;
3. dominant reader-facing language in title, introduction, headings, and body;
4. majority explanatory prose for mixed-language articles, ignoring code, URLs, quotations, references, brands, and proper nouns;
5. conversation language only when the article is too short or ambiguous.

The result is a concrete BCP 47 tag such as `zh-TW`, `en`, `ja`, `ko`, or `es`. `auto` and `und` are rejected. Product names, model names, benchmarks, acronyms, versions, numbers, units, and percentages remain in their source form unless the user requests otherwise.

## Default output

- 16:9 horizontal article illustrations.
- Usually 3–7 images; up to 9 for long-form content.
- One insight headline and 3–6 short callouts per final image.
- Text-free base images plus deterministic annotated images.
- Separate raw and final assets:

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── annotation-plan.json
├── prompts/
├── images/
│   ├── raw/
│   └── 01-*.png
└── delivery.md
```

## Installation

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

No font files are bundled. The renderer selects a compatible local font based on `article.annotation_language`, or accepts a local path through `--font`.

## Usage

### Plan without generating

```text
Use $editorial-documentary-illustrations
Analyze the article and its primary sources. Create a version 4 manifest for five images.
Before choosing compositions, define the article type, visual thesis, topic signature, global must-avoid list, and a semantic contract for every shot.
Do not generate images yet.

<article>
```

### Generate a complete grounded set

```text
Use $editorial-documentary-illustrations
Create five 16:9 parchment-cutout article illustrations.
Meaning must override style. The unannotated base image must express the article-specific mechanism and pass the Label-off, Blind-caption, and Neighbor-article tests.
Generate text-free bases first, then add reviewed annotations in the resolved reader language.

<article>
```

### Technical research

```text
Use $editorial-documentary-illustrations
This is a technical-research article. Read the abstract, architecture or method figure, method, results, and limitations before planning the hero.
Use a domain-faithful architecture artifact. Do not replace the mechanism with generic workers, factories, cities, robots, brains, gears, or server towers.
```

## Validation, preflight, prompt rendering, and annotation

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/semantic_preflight.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts-still

python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

## Version 4 manifest excerpt

```json
{
  "version": 4,
  "article": {
    "article_type": "technical-research",
    "visual_thesis": "A 3:1 hybrid stack retains precise retrieval while replacing most growing KV cache with bounded recurrent state.",
    "topic_signature": [
      "bounded recurrent state",
      "full-attention retrieval layer",
      "3:1 layer ratio",
      "growing KV cache"
    ],
    "global_must_avoid": [
      "generic AI robot or glowing brain",
      "unrelated office workers operating a machine"
    ]
  },
  "shots": [
    {
      "image_role": "hero",
      "visualization_mode": "literal-technical",
      "role": "architecture-stack",
      "semantic_contract": {
        "source_basis": ["Grounded claim one", "Grounded claim two"],
        "must_show": ["Required structure", "Required relationship", "Required resource contrast"],
        "must_not_show": ["Generic machine with no architecture mapping"],
        "visual_evidence": [
          {
            "concept": "3:1 layer ratio",
            "visible_form": "one four-module stack with three terracotta and one indigo module",
            "relationship": "the modules form one interleaved architecture"
          }
        ],
        "specificity_terms": ["3:1 layer ratio", "bounded recurrent state"],
        "expected_blind_caption": "A four-layer hybrid stack contrasts bounded state with a growing KV cache trail.",
        "hero_artifact": "one interleaved four-layer attention stack"
      }
    }
  ]
}
```

See [`templates/manifest.template.json`](templates/manifest.template.json), [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json), and [`references/semantic-grounding.md`](references/semantic-grounding.md).

## Repository structure

```text
.
├── SKILL.md
├── README*.md
├── references/
│   ├── semantic-grounding.md
│   ├── article-analysis.md
│   ├── composition-patterns.md
│   ├── prompt-template.md
│   ├── qa-checklist.md
│   └── ...
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── semantic_preflight.py
│   ├── validate_manifest.py
│   ├── render_prompts.py
│   └── annotate_images.py
└── tests/test_tooling.py
```

## Attribution and license

- Released under the [MIT License](LICENSE).
- The multi-step workflow was inspired by and adapted from Ian’s [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations); see [`NOTICE.md`](NOTICE.md).
- This repository does not include the original Xiaohei character IP, example images, copied prompts, or font files.
- This project is not affiliated with, endorsed by, or produced by Vox Media. Do not copy specific frames, logos, title cards, typefaces, or branded assets.
