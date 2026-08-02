# Prompt Assembly

## Priority order

The image model must receive the semantic contract before the style instructions. Meaning outranks decorative consistency.

Use this fixed order:

1. Non-negotiable semantic contract.
2. Source-grounded visual evidence.
3. Immutable Style Lock.
4. Article Visual Bible.
5. Shot composition.
6. Annotation reservation.
7. Output constraints.

## Text-free still template

```text
Create one standalone original 16:9 editorial documentary article illustration.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

NON-NEGOTIABLE SEMANTIC CONTRACT — MEANING OVERRIDES STYLE
Article type: {article_type}
Article visual thesis: {visual_thesis}
Article topic signature: {topic_signature}
Image role: {image_role}
Visualization mode: {visualization_mode}
Source basis: {source_basis}
Hero artifact: {hero_artifact_or_none}
Must visibly show: {must_show}
Must not show or substitute: {must_not_show_and_global_avoids}
Specificity terms: {specificity_terms}
Expected blind caption for the unannotated base image: {expected_blind_caption}
Visual evidence mappings:
{visual_evidence_lines}

The unannotated base image must independently communicate the claim. Do not rely on later labels to rescue a generic or unrelated scene. Do not substitute a generic robot, brain, server room, city, factory, road, shield, conveyor, gears, or office workers unless the semantic contract explicitly requires and maps that object.

{STYLE_LOCK_VERBATIM}

ARTICLE VISUAL BIBLE
World summary: {world_summary}
Background: {background}
Palette and usage: {palette}
Camera: {camera}
Lighting and shadows: {lighting}
Character system: {character_system}
Recurring motif: {recurring_motif}
Continuity rules: {continuity_rules}

SHOT
Core idea: {core_idea}
Composition role: {role}
Main subject: {main_subject}
Composition: {composition}
Supporting elements: {supporting_elements}
Motion cues frozen into the still frame: {motion_cues}
Density: {density}
People count strategy: {people_count_strategy}

ANNOTATION RESERVATION
The final image will receive one short insight headline and {label_count} semantic callout tags in deterministic post-production. Reserve calm parchment pockets in: {annotation_regions}. Do not draw placeholder tags, fake writing, letters, numbers, or text-like symbols.

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core claim. Preserve every must-show item and the relationships defined in visual evidence. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. The base image must contain no text, letters, numbers, labels, logos, watermarks, UI, or dashboard elements. A paper-cutout technical mechanism is allowed; a generic PPT flowchart is not.
```

## Technical research rule

For `literal-technical` and `hybrid-metaphor` shots, explicitly ask for recognizable components, count, ordering, state, comparison conditions, and resource behavior. Do not convert the method into unrelated people doing office work.

## Reference image rule

A calibration frame may lock material, palette, cutout edge, shadow direction, camera, and character proportions. It must not lock or overwrite the semantic contract of later shots.
