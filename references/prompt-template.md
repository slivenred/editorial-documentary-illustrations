# Prompt Assembly

## 五層結構

每張圖的 prompt 按固定順序組裝，不要讓 Agent 自由重排。

### Layer 1：原創性

```text
Create one standalone original 16:9 article illustration. Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.
```

### Layer 2：Immutable Style Lock

逐字放入 `style-lock.txt`，不能摘要、改寫或只寫「same style」。

### Layer 3：Article Visual Bible

只放文章級固定項：

```text
ARTICLE VISUAL BIBLE
World summary: ...
Background: ...
Palette and usage: ...
Camera: ...
Lighting and shadows: ...
Character system: ...
Recurring motif: ...
Continuity rules: ...
```

### Layer 4：Shot

```text
SHOT
Core idea: ...
Composition role: ...
Main subject: ...
Composition: ...
Supporting elements: ...
Motion cues frozen into the still frame: ...
Density: ...
People count strategy: ...
```

### Layer 5：硬性限制

```text
COMPOSITION AND OUTPUT CONSTRAINTS
- One image, one core idea.
- Keep the focal action inside the central 84% safe area.
- Leave enough parchment breathing room for article placement.
- No text inside the image.
- No logos, watermarks, captions, labels, UI, or formal diagram nodes.
- Do not add objects that are not needed for the core idea.
- Preserve the exact article visual bible.
```

## 靜態 prompt 範本

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

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core idea. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. Keep people as simplified paper cutouts, especially in crowds. No text inside the image. No logos, watermarks, captions, labels, UI, formal flowchart boxes, or dashboard elements. Do not add unnecessary objects. Preserve the exact article visual bible.
```

## 為什麼圖內不放文字

- 多語文字容易錯字。
- 文字會把場景推向 PPT。
- 同一圖片可跨語言重用。
- SEO alt text 與 caption 可由文章系統控制。
- 若一定要標示，優先在網站前端疊字，而不是讓圖像模型生成。

## Prompt 壓縮原則

生成失敗時不要無限加形容詞。依順序刪減：

1. 刪 supporting elements。
2. 降低 people count。
3. 只留一條路徑。
4. 移除次要 accent color。
5. 把兩個動作合併成一個。
6. 仍失敗才改構圖 pattern。

## 參考圖

若圖像模型支援 reference image：

- 第一張合格 calibration frame 作為 style reference。
- 參考強度以保留材質、色盤、人物比例與陰影為主。
- 不要求複製第一張的構圖。
- prompt 明確寫：`Match the material, palette, cutout edge, shadow direction, camera angle, and character proportions; invent a new composition for this shot.`
