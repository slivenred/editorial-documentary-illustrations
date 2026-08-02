# Prompt Assembly

每張無字底圖 prompt 使用以下順序：

1. Article context。
2. Visual story。
3. Key elements。
4. Explainer-to-visual mapping。
5. Layout reservation。
6. Style Lock。
7. Output constraints。

## 靜態底圖範本

```text
Create one original 16:9 editorial documentary paper-cutout illustration for an article.

ARTICLE CONTEXT
Article summary: {article_summary}
Section anchor: {anchor_summary}
Image purpose: {purpose}
Headline meaning: {headline}

VISUAL STORY
{visual_story}

KEY ELEMENTS
{key_elements}

EXPLAINER-TO-VISUAL MAPPING
{explainer_mappings}

TEXT-SAFE LAYOUT
Use the {layout} composition. Reserve the required header and explainer-card zones. Keep the central visual readable and do not place faces or essential objects under those zones.

{STYLE_LOCK_VERBATIM}

OUTPUT CONSTRAINTS
No text, letters, numbers, labels, logos, watermarks, UI, dashboards, formal flowchart boxes, or fake writing in the base image. Use one clear focal scene with 2–6 key object types. The scene must directly match the article section, but it does not need to encode every technical detail without the later explanatory text.
```

## 技術內容

- 使用簡化且可辨識的模組、Token、狀態、記憶卡、層或對比軌跡。
- 不追求精密論文圖重製。
- 不把演算法變成一群人操作泛用機器。
- 精確比例與數字可放入後製解釋卡。

## 參考圖

第一張合格底圖只鎖定羊皮紙、剪紙材質、色盤、鏡頭、陰影與物件比例，不複製後續構圖。
