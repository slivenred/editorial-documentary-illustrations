# Article Analysis

## Goal

Do not ask “what can be drawn for each paragraph?” Ask:

1. What must a reader understand?
2. Which article-specific mechanism, relationship, or change is difficult to imagine?
3. What visible evidence would make that claim recognizable without relying on labels?

Read `semantic-grounding.md` before planning shots.

## 1. Build the Article Map

Answer in six lines or fewer:

1. What is the article's thesis?
2. What starts the event or system?
3. What changes in the middle?
4. Which hidden mechanism determines the outcome?
5. Where do scale, speed, cost, power, memory, or emotion change?
6. What result or limitation should the reader remember?

## 2. Classify the article

Set `article.article_type` before choosing a composition. Technical research, product news, history, policy, social analysis, and how-to content need different levels of literalness.

For technical research, read the primary abstract, architecture figure, method, result figure, and limitations before inventing a metaphor.

## 3. Write the Visual Thesis

`article.visual_thesis` is one visual proposition the entire image set should prove. It must include a relationship, trade-off, sequence, or change.

Weak: `This article is about linear attention.`

Strong: `A 3:1 KDA–MLA hybrid preserves selective full-attention retrieval while replacing most growing KV cache with compact recurrent state.`

## 4. Extract the Topic Signature

Choose 3–10 specific anchors:

- named entities;
- architecture or mechanism;
- relationship, ratio, or sequence;
- result, benchmark, or constraint.

Do not use only broad nouns such as AI, model, data, speed, system, people, or growth.

## 5. Select cognitive anchors

Prioritize:

- origin;
- assembly;
- transformation;
- path;
- hidden mechanism;
- contrast;
- bottleneck;
- scale change;
- verified result;
- limitation or boundary.

Score each candidate from 0–10 using 0–2 points for:

- `explanatory_value`
- `visual_action`
- `narrative_change`
- `article_specificity`
- `placement_value`

Only keep candidates scoring 7 or above. `article_specificity` is mandatory: a visually attractive but generic scene should not pass.

## 6. Decide literalness before metaphor

Use this priority:

1. `literal-technical` for architecture, algorithms, hardware, scientific mechanisms, and benchmarks.
2. `literal-scene` for people, places, events, and physical processes.
3. `hybrid-metaphor` when a literal mechanism needs one controlled analogy.
4. `abstract-metaphor` only for genuinely abstract arguments.

Do not default to markets, roads, factories, cities, workers, gears, robots, brains, shields, or pipelines. These are reusable style objects, not evidence of relevance.

## 7. Build a Semantic Contract for every shot

Every shot must specify:

- source basis;
- image role;
- visualization mode;
- must-show items;
- must-not-show substitutions;
- visual evidence mappings;
- specificity terms;
- expected blind caption;
- hero artifact when applicable.

The first hero shot must cover the article thesis, not merely introduce the visual world.

## 8. Number of images

- under 800 words: 1–3;
- 800–2,500 words: 3–5;
- 2,500–5,000 words: 5–7;
- over 5,000 words: 6–9.

Do not distribute images at fixed word intervals.

## 9. Narrative rhythm

A five-image set may use:

1. thesis-bearing hero or article-specific world;
2. core mechanism;
3. hidden relationship;
4. scale, resource, or performance change;
5. result, limitation, or decision consequence.

Avoid three consecutive generic left-to-right flows.

## Not worth illustrating

- a definition already clear in one sentence;
- repeated conclusions;
- isolated numbers with no relationship;
- generic people added only for decoration;
- scenes that require long labels to become relevant;
- a metaphor whose mapping cannot be stated explicitly;
- a base image that could fit many neighboring articles after relabeling.
