# Prompt Assembly

## 原則：底圖與文字分離

每張 still 成品分成兩個獨立步驟：

1. 使用圖像模型生成**完全無字的敘事底圖**。
2. 根據實際底圖，用 `scripts/annotate_images.py` 加入經校對的 headline 與 labels。

不要把繁中標註文字放進生圖 prompt。Prompt 只負責要求模型留下可供後製的安靜區。

## 六層底圖 Prompt

每張底圖 prompt 按固定順序組裝，不要讓 Agent 自由重排。

### Layer 1：原創性

```text
Create one standalone original 16:9 article illustration. Do not reproduce any existing frame, branded asset, logo, title card, typography, or identifiable composition.
```

### Layer 2：Immutable Style Lock

逐字放入 `style-lock.txt`，不能摘要、改寫或只寫 `same style`。

### Layer 3：Article Visual Bible

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

### Layer 5：Annotation Reservation

只描述需要預留的空間，不放真實標註文字：

```text
ANNOTATION RESERVATION
The final image will receive one short insight headline and 3–6 semantic callout tags in deterministic post-production. Keep calm parchment pockets in these broad regions: upper center, left middle, right lower. Do not put faces, critical objects, or the main route inside every quiet pocket. Do not draw placeholder labels or fake writing.
```

區域由 manifest 的 provisional annotation coordinates 自動推導。底圖完成後，Agent 必須重新看圖並校正座標。

### Layer 6：硬性限制

```text
COMPOSITION AND OUTPUT CONSTRAINTS
- One image, one core idea.
- Keep the focal action inside the central 84% safe area.
- Leave enough parchment breathing room for later semantic callout tags.
- No model-generated text inside the base image.
- No logos, watermarks, captions, labels, UI, or formal diagram nodes.
- Do not add objects that are not needed for the core idea.
- Preserve the exact article visual bible.
```

## 靜態底圖 Prompt 範本

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
The final image will receive one short insight headline and {label_count} semantic callout tags in deterministic post-production. Keep calm parchment pockets in these broad regions: {annotation_regions}. Do not draw placeholder labels, fake writing, symbols that resemble text, or empty UI boxes.

COMPOSITION AND OUTPUT CONSTRAINTS
One image, one core idea. Keep the focal action inside the central 84% safe area. Preserve generous parchment breathing room. Keep people as simplified paper cutouts, especially in crowds. Do not render any text, letters, numbers, captions, labels, logos, watermarks, UI, formal flowchart boxes, or dashboard elements in the base image. Do not add unnecessary objects. Preserve the exact article visual bible.
```

## Annotation Plan 範本

文字與座標保存在 manifest，不寫入 image prompt：

```json
{
  "enabled": true,
  "language": "zh-TW",
  "layout_status": "draft",
  "headline": {
    "text": "小而專精，取代全面依賴",
    "x": 0.44,
    "y": 0.06,
    "accent": "terracotta",
    "font_size": 42,
    "angle": 0
  },
  "labels": [
    {
      "text": "5B 活躍參數",
      "x": 0.46,
      "y": 0.27,
      "target_x": 0.58,
      "target_y": 0.51,
      "accent": "terracotta",
      "font_size": 34,
      "angle": 1
    }
  ]
}
```

- 生成前先寫語意文字。
- 生成後才以實際畫面更新座標並將 `layout_status` 改為 `final`。
- `render_prompts.py` 會輸出 `annotation-plan.json` 供後製使用。

## 為什麼不讓圖像模型直接寫字

- 繁中、數字與專有名詞容易錯字或亂碼。
- 文字會把圖像模型推向 PPT 或 UI。
- 模型可能創造文章不存在的數字與標籤。
- 底圖可跨語言重用。
- 程式後製可精準校對、改字、移位與重用。

## Prompt 壓縮原則

生成失敗時依序刪減：

1. supporting elements。
2. people count。
3. 次路徑。
4. 次要 accent color。
5. 第二個動作。
6. 仍失敗才改構圖 pattern。

不要用增加文字或畫框來補救敘事不清；先把物理場景畫清楚。

## 參考圖

若圖像模型支援 reference image：

- 第一張合格 calibration frame 作為 style reference。
- 參考強度以保留材質、色盤、人物比例與陰影為主。
- 不要求複製第一張構圖。
- prompt 明確寫：`Match the material, palette, cutout edge, shadow direction, camera angle, and character proportions; invent a new composition for this shot.`
