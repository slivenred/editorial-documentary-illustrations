# Prompt Assembly

## 五層結構

每張底圖 prompt 使用固定順序：原創性、Immutable Style Lock、Article Visual Bible、Shot、硬性限制。不要讓 Agent 自由重排。

## 靜態底圖範本

```text
Create one standalone original 16:9 editorial documentary article illustration.
Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.

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
One image, one core idea. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. The base image must contain no text, letters, numbers, labels, logos, watermarks, UI, flowchart boxes, or dashboard elements. Preserve the exact article visual bible.
```

## 為什麼底圖不放文字

- 圖像模型不是穩定的多語排版器。
- 名稱、數字與語言需要可校對、可重現。
- 同一張底圖可以在明確需求下製作不同語言版本。
- 最終文字由 `scripts/annotate_images.py` 根據 `article.annotation_language` 後製。

## Prompt 壓縮原則

生成失敗時依序刪 supporting elements、降低人物數、只留一條路徑、移除次要 accent、合併動作，最後才更換構圖。

## 參考圖

若模型支援 reference image，第一張合格 calibration frame 只用於鎖定材質、色盤、剪紙邊緣、陰影、鏡頭與人物比例，不複製構圖。
