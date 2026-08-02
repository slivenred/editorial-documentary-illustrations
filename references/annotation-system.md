# Integrated Explainer Text System

## 核心原則

文字是版面的一部分，不是事後散貼在插畫上的補丁。最終圖片採固定閱讀順序：

```text
eyebrow → headline → subheadline → visual → explainer cards
```

## Headline

- 表達結論、因果、取捨或結果。
- 不寫「系統架構」「流程圖」「重點整理」。
- 中文建議 8–22 字；英文 5–14 words。
- 一張圖只保留一個 headline。

## Subheadline

- 一句補充條件或解釋。
- 中文建議 18–45 字；英文 10–28 words。
- 不重複 headline。

## Explainer Cards

每張 2–4 個：

- `title`：名稱、階段、比例或數字。
- `body`：一句作用、原因、限制或結果。
- `visual_anchor`：底圖中對應的可見物件。
- `accent`：全篇固定色彩語意。

卡片不必使用 callout line。版型位置已建立關聯；需要指向時，只允許 1–3 條短線且不可交叉。

## 文字和場景如何配合

- 先確定文字要說什麼，再要求底圖出現相對應的物件。
- 技術細節可由卡片解釋，底圖只需清楚呈現簡化關係。
- 不要求底圖在完全無字時就包含所有術語與數字。
- 但底圖不能與文字無關；每張卡的 `visual_anchor` 必須真的出現在場景中。

## 色彩語意

- `ink`：一般結構。
- `terracotta`：主要機制或主角。
- `ochre`：流程、路徑、規模。
- `sage`：完成、安全、改善。
- `indigo`：對照組、基礎設施、完整注意力。
- `brick`：風險、成本、瓶頸。

## 字體與檔案

- 使用本機可讀字型，不在 repo 內附帶字型檔。
- 文字後製由 Pillow 完成。
- 圖像模型不得生成文字、數字、logo 或假 UI。
