# Prompt Assembly

## 原則

圖中文字與主場景一起生成。提示詞必須列出所有文字的精確內容，並要求不得增加其他文字。

## Prompt 順序

1. 圖片用途與對應上下文。
2. 精選圖 Title Contract 或文內圖 Core Idea。
3. 精確文字清單。
4. 主場景與物件關係。
5. Style Lock。
6. Visual Bible。
7. 安全區與 QA 限制。

## 精選圖 Prompt 範本

```text
Create one final 16:9 featured editorial illustration for this article.

TITLE CONTRACT
Claim: {claim}
Key result: {key_result}
Mechanism: {mechanism}
Coverage: {title_coverage}

Render these exact strings and no other text:
Eyebrow: {eyebrow}
Headline: {headline}
Subheadline: {subheadline}
Labels:
- {label_1}
- {label_2}
- {label_3}
Bottom takeaway: {bottom_takeaway}
Caveat: {caveat_or_none}

MAIN TABLEAU
{scene}
Required elements: {scene_elements}

{STYLE_LOCK_VERBATIM}

{VISUAL_BIBLE}

LAYOUT
Canvas 1600x900. Keep at least {outer_margin_px}px outer margin.
Center the eyebrow, headline, and subheadline at the top.
Keep the tableau in the middle/lower area.
Use only short callout lines. Keep every object and every glyph fully inside the border.
No overlap between text cards and the central subject.
```

## 文內圖 Prompt 範本

```text
Create one final 16:9 inline editorial illustration for the following article context.

Context section: {section_heading}
Context excerpt: {after_paragraph_excerpt}
Core idea: {core_idea}

Use the approved featured image only as a style reference.
Match its parchment tone, fine border, corner ornaments, centered title hierarchy,
paper-crafted depth, shadow direction, label-card treatment, accent colors,
and bottom takeaway ribbon. Do not copy its composition.

Render these exact strings and no other text:
Eyebrow: {eyebrow}
Headline: {headline}
Subheadline: {subheadline}
Labels: {labels}
Bottom takeaway: {bottom_takeaway}
Caveat: {caveat_or_none}

Main tableau: {scene}
Required elements: {scene_elements}
People required: {people_required}

{STYLE_LOCK_VERBATIM}

Keep all content inside the safe area. Do not crop or hide any important object.
```

## 修字 Prompt

```text
Edit the provided image without changing the composition, paper-craft objects, colors, border, or lighting.
Replace only the incorrect text "{wrong}" with the exact text "{correct}".
Keep every other pixel and every other string unchanged.
```
