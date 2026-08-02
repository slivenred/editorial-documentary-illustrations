# Semantic Grounding

## Why this layer exists

A consistent parchment-cutout style is not enough. An image may look polished and still be semantically interchangeable with dozens of unrelated articles. The final image must preserve the article's **specific entities, mechanism, relationship, and outcome** before any annotation is added.

Meaning outranks style. If a decorative style decision conflicts with the article's mechanism, keep the mechanism and simplify the decoration.

## The semantic contract

Every shot must define a `semantic_contract` before image generation:

- `source_basis`: 1–4 concise claims grounded in the article or primary source.
- `must_show`: 2–6 article-specific visual requirements. A hero requires at least 3.
- `must_not_show`: generic or misleading substitutions that would change the meaning.
- `visual_evidence`: a mapping from each important concept to a visible form and relationship.
- `specificity_terms`: concrete entities, mechanisms, ratios, benchmarks, or outcomes that distinguish this article from neighboring topics.
- `expected_blind_caption`: what an informed reviewer should say when describing the **unannotated** base image.
- `hero_artifact`: for a hero image, the central domain-specific object that carries the article thesis.

## Article-level grounding

Before writing shots, resolve these article fields:

### `article_type`

Choose one:

- `technical-research`
- `product-or-company`
- `historical`
- `policy-or-economy`
- `social-or-cultural`
- `process-or-howto`
- `general`

### `visual_thesis`

A single sentence describing the visual claim the image set must prove. It is not the article title.

### `topic_signature`

Select 3–10 concrete items that make the article recognizable. Include a mix of:

- named entity or product;
- mechanism or architecture;
- relationship, ratio, or sequence;
- outcome, benchmark, or constraint.

Weak signature: `AI`, `model`, `speed`, `data`.

Strong signature: `KDA`, `MLA`, `3:1 layer ratio`, `fixed recurrent state`, `growing KV cache`, `1M-token decoding`.

### `global_must_avoid`

List recurring substitutions that would be misleading for this article, such as a generic robot, glowing brain, unrelated city, cyberpunk server room, or decorative gears.

## Source-first rule for technical research

For `technical-research`, establish the semantic contract from primary material before inventing a scene:

1. abstract and contribution list;
2. architecture or method figure;
3. method section describing components and relationships;
4. result figure or table for the claimed outcome;
5. limitations or scope conditions.

Do not convert a technical mechanism into a marketplace, factory, road network, or group of office workers merely because those objects fit the visual style. A metaphor is allowed only when every source concept has an explicit visual mapping and the core relationship remains recognizable.

Default visualization mode for technical research:

1. `literal-technical`
2. `hybrid-metaphor`
3. `literal-scene`
4. `abstract-metaphor` only when no domain-faithful structure is possible

A `technical-research` hero must not use `abstract-metaphor`.

## Visual evidence mapping

Each item in `visual_evidence` has three parts:

```json
{
  "concept": "3:1 KDA-to-MLA layer ratio",
  "visible_form": "four interleaved paper layer modules, three terracotta and one indigo",
  "relationship": "the four modules form one repeated model stack rather than two separate systems"
}
```

The visible form must be observable before labels are added. Annotation may name the concept, but it must not magically turn a generic object into the concept.

## Hero image contract

A featured image is not a generic “world establishment” frame. It must compress the article thesis.

A hero shot must:

- use `image_role: hero`;
- define one `hero_artifact` derived from the article's domain;
- visibly cover at least 3 `must_show` items;
- encode at least one relationship or trade-off, not only a collection of symbols;
- overlap with at least 2 items from `article.topic_signature`;
- remain recognizable after all annotations are hidden.

Only one hero is allowed. When present, it should be the first shot.

## Three mandatory semantic tests

### 1. Label-off test

Hide every headline, label, number, and callout line. The base image must still express the mechanism or relationship. If the image only becomes relevant after labels are added, it fails.

### 2. Blind-caption test

Describe the base image in one sentence without reading the prompt or annotations. Compare the description with `expected_blind_caption`.

Pass: the description includes at least two article-specific anchors and the intended relationship.

Fail: the description is generic, such as “people operate a machine,” “data flows through a system,” or “an AI network processes information.”

### 3. Neighbor-article test

Ask whether the same base image could illustrate a different article merely by replacing the labels.

If a generic robot, brain, server tower, factory, conveyor, gears, city, shield, or road could be relabeled to fit many articles, the shot fails unless the semantic contract explicitly requires and maps that object.

## Kimi Linear regression example

Article-specific anchors:

- KDA refines Gated DeltaNet with finer-grained gating;
- KDA and MLA are interleaved in a 3:1 layer ratio;
- finite recurrent state replaces most growing KV cache;
- the hybrid beats full MLA under matched training;
- up to 75% less KV cache and up to 6× decoding throughput at 1M context.

A weak hero is a generic AI factory, server city, group of workers, or glowing machine. Those objects do not reveal KDA, MLA, the 3:1 interleave, fixed-state memory, or the full-attention comparison.

A stronger hero uses one domain-faithful paper artifact: a four-layer model stack with three KDA state modules and one MLA retrieval module, a token stream passing through it, a compact fixed-state memory capsule beside a visibly growing KV-card trail, and a comparison track showing the hybrid continuing efficiently at long context. Labels may name these parts later, but the structure must already be visible.
