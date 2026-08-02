# Composition Patterns

Choose one primary pattern and at most one supporting pattern. Semantic grounding comes first; a pattern is only a spatial tool.

## Technical patterns

### 1. Technical Mechanism

Best for: algorithms, memory systems, model internals, scientific mechanisms, hardware paths.

- Show 2–5 domain-faithful modules.
- Make inputs, state changes, retrieval, or outputs physically visible.
- Use tokens, layer cards, state cells, memory cards, gates, or source-specific artifacts.
- Preserve the article's actual component relationships.

Avoid: generic server rooms, operators around a machine, decorative circuitry, or unlabeled boxes that could represent anything.

### 2. Architecture Stack

Best for: repeated layers, ratios, interleaving, hierarchy, model blocks.

- Use repeated paper modules with visible rhythm.
- Encode ratios through count and order, not only later labels.
- Show that modules belong to one stack.
- Keep one input and one output path.

Avoid: separating one architecture into unrelated buildings or replacing layer count with arbitrary crowds.

### 3. Resource Contrast

Best for: memory growth, latency, throughput, cost, energy, storage.

- Compare the same workload on two visible tracks.
- Show the resource that grows, stays bounded, or changes slope.
- Keep workload and scale conditions visually matched.
- Use containers, card trails, queues, or repeated tokens only when their mapping is explicit.

Avoid: coin piles or speed lines with no visible connection to the measured resource.

### 4. Claim Comparison

Best for: baseline versus proposed method, before/after evaluation, fair comparison.

- Keep inputs and conditions visibly matched.
- Change only the mechanism being compared.
- Show both quality and efficiency only if both are part of the source claim.
- Prefer one decisive relationship over a collage of benchmark symbols.

Avoid: trophy imagery, podiums, generic winners, or unequal input conditions.

## General patterns

### 5. Process Station

Best for: food making, editing, retrieval, assembly, raw material becoming an output.

Use a central workbench or machine only when its input, transformation, and output map directly to the article.

### 6. Route Network

Best for: people, information, goods, money, or influence moving across real or conceptual locations.

Do not use a route merely because the visual style contains map lines.

### 7. Timeline Journey

Best for: history, product evolution, family-to-market change, lifecycle.

Use one continuous route through 3–4 scenes, not slide panels.

### 8. Before / After Landscape

Best for: disorder/order, fragmented/concentrated, manual/automated, quiet/crowded.

Keep conditions comparable and connect the two states through one visible cause.

### 9. Scale-up Crowd

Best for: adoption, demand, queues, public response.

Use crowd clusters and physical evidence of scale. Do not use crowds for technical model architecture.

### 10. Cutaway Mechanism

Best for: RAG, search, recommendation, supply chain, black-box systems.

For technical research, use domain-faithful modules instead of generic rooms or people unless humans are actual actors.

### 11. Ecosystem Tableau

Best for: markets and social systems with multiple real actors.

Do not use it as a default hero for a paper about an internal algorithm.

### 12. Physical Metaphor

Best for: trust, authority, risk, attention, compounding, or other abstract arguments.

A metaphor is valid only when each important source concept has an explicit visible mapping in `semantic_contract.visual_evidence`.

### 13. Evidence Chain

Best for: research argument, GEO citations, verification, trust.

Use source artifacts that converge into a result. Do not replace the studied mechanism with a pile of generic documents.

### 14. Origin Map

Best for: food, culture, language, technology, or product diffusion across places.

Use only when geographic movement is part of the article.

## Anti-repetition and anti-drift

- A pattern cannot override `must_show`.
- The same pattern should not be used more than twice per article.
- A recurring motif may unify images, but it must not replace article-specific artifacts.
- If two shots can use the same generic composition, merge them or make their semantic contracts more specific.
- For technical research, people are optional and usually secondary; do not anthropomorphize a mechanism by default.
