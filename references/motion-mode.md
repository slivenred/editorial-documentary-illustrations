# Motion Mode — Exactly 10 Seconds

Motion mode inherits the same `semantic_contract` as the approved still image. It may animate the mechanism, but it may not replace or simplify it into generic activity.

## Fixed specification

- exactly 10 seconds;
- smooth 24fps;
- one continuous scene;
- no voiceover, dialogue, subtitles, text overlays, logo, or watermark;
- only subtle ambient sound is implied;
- preserve the same Visual Bible, hero artifact, must-show items, component identity, counts, order, comparisons, and resource behavior;
- camera locked or one slow subtle drift;
- final 0.5–0.8 seconds holds on a stable tableau.

## Four beats

### 0.0–1.5 seconds — Establish

Reveal the article-specific artifact and the initial state. Do not open with generic parchment decoration.

### 1.5–4.0 seconds — Transform

Animate the central mechanism, state transition, comparison, or causal action defined by `visual_evidence`.

### 4.0–7.5 seconds — Expand

Make the scale, resource, route, ordering, or result change visible. Technical research should animate component behavior, not add decorative crowds.

### 7.5–10.0 seconds — Resolve

Resolve the visual thesis into one readable relationship. Hold the final frame long enough to inspect.

## Semantic tests

- Pause the animation at 5–7 seconds and run the Label-off test.
- The final frame must still approach `expected_blind_caption`.
- Replacing labels must not make the animation suitable for a neighboring article.
- Every must-show item must appear long enough to be understood.

## Prompt order

1. Non-negotiable Semantic Contract.
2. Visual Evidence Mapping.
3. Technical-research instruction when applicable.
4. Style Lock.
5. Visual Bible.
6. Story beats.
7. Motion and output constraints.

The renderer in `scripts/render_prompts.py` follows this order automatically.

## Common failures

- style-consistent animation with an unrelated mechanism;
- generic people moving around a machine instead of the actual architecture;
- ten hard cuts inside ten seconds;
- counts, order, ratios, state size, or comparison conditions changing between frames;
- fast advertising-style zooms and transitions;
- final tableau too brief to inspect;
- text cards or voiceover used to explain a semantically weak scene.
