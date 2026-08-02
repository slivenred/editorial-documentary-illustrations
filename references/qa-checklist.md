# QA Checklist

Still mode requires three gates:

1. **Semantic Preflight** before generation.
2. **Base QA** on the text-free image.
3. **Annotation QA** on the final image.

## Semantic Preflight hard failures

- `visual_thesis` is a topic label instead of a relationship or claim.
- `topic_signature` contains only generic terms.
- A shot has fewer than 2 must-show items; a hero has fewer than 3.
- A hero has no domain-specific `hero_artifact`.
- A technical-research hero uses `abstract-metaphor`.
- Visual evidence does not map the article concepts to visible forms and relationships.
- The planned composition could fit many unrelated articles after changing labels.

## Base QA hard failures

- The image is not safely usable as 16:9.
- It contains model-generated text, numbers, logo, watermark, UI, or fake writing.
- It copies an existing frame or branded asset.
- It leaves the locked parchment-cutout world without a justified user override.
- It has severe anatomy or object failures.
- It becomes a generic PPT, corporate vector scene, game-like 3D render, anime image, or children's illustration.
- Cross-image palette, camera, paper, scale, or shadow direction drifts.
- Any `must_show` item is missing or visually unreadable.
- The visible relationships contradict `visual_evidence`.
- The hero does not center the `hero_artifact`.
- The base image only becomes relevant after annotations are added.
- The blind caption does not match `expected_blind_caption` or fails to mention at least two article-specific anchors.
- The same image could illustrate a neighboring article by replacing the labels.
- Technical research is replaced by generic robots, brains, factories, cities, workers, gears, server towers, shields, or roads without an explicit semantic mapping.
- There is no calm region for deterministic annotation.

## Label-off test

Hide every annotation. Ask:

- What mechanism or relationship is visible?
- Which two details make this image specific to the article?
- What would be lost if the labels were removed?

If the answer is only “a system processes information,” “people operate a machine,” or similar generic language, fail the base image.

## Blind-caption test

Write a one-sentence description without reading the prompt. Compare it with `expected_blind_caption`.

Pass only when the description contains:

- at least two specificity anchors; and
- the intended relationship, sequence, trade-off, or change.

## Final Annotation QA hard failures

When the base is correct, fix only the annotation plan for:

- unresolved or incorrect language;
- spelling, grammar, regional wording, direction, or font errors;
- names, ratios, numbers, units, or terms that disagree with the article;
- a generic headline;
- labels pointing to missing, wrong, or semantically empty objects;
- labels that rename generic decoration instead of identifying meaningful visual evidence;
- text covering the hero artifact, must-show elements, people, or core relationships;
- crossing callout lines, excessive labels, PPT-like density, or unreadable mobile scale.

## 100-point score

1. Semantic contract coverage — 25
2. Article specificity — 15
3. Relationship and causal fidelity — 15
4. Paragraph or article-role relevance — 10
5. Style lock — 10
6. Composition and readability — 8
7. Cross-image continuity — 7
8. Generation quality — 5
9. Annotation semantic quality — 3
10. Annotation layout quality — 2

## Delivery threshold

- no hard failure;
- total at least 88;
- semantic contract coverage at least 22/25;
- article specificity at least 12/15;
- relationship fidelity at least 12/15;
- style lock at least 8/10.

Style cannot compensate for low semantic fidelity.
