# Article Analysis and Automatic Image Planning

## 目標

圖片數量與位置由文章的理解需求決定，而不是固定配額。

## 1. 建立 Article Map

用六句內回答：

1. 標題最主要的宣稱是什麼？
2. 最重要的結果、數字或改變是什麼？
3. 造成結果的核心機制是什麼？
4. 哪個段落最難靠文字想像？
5. 哪個對比、流程或狀態變化最值得畫？
6. 讀者最後應記住什麼？

前三項形成 `title_contract`：`claim`、`key_result`、`mechanism`。

## 2. 精選圖規劃

精選圖必須：

- 直接呈現 `claim`。
- 至少加入 `key_result` 或 `mechanism` 其中一項。
- 選一個強烈但簡單的物理場景。
- 不把文章所有細節塞進同一張。

## 3. 候選文內圖錨點

每個候選段落依五項各給 0–2 分：

- `comprehension_gain`
- `visual_structure`
- `context_specificity`
- `non_redundancy`
- `placement_value`

只保留總分 7 以上。若兩張圖說同一件事，保留較高分者或合併。

## 4. 閱讀時間容量

- 1 分鐘：1 張。
- 2 分鐘：最多 2 張。
- 3–4 分鐘：最多 3 張。
- 5–6 分鐘：最多 4 張。
- 7–9 分鐘：最多 5 張。
- 10–12 分鐘：最多 6 張。
- 13 分鐘以上：最多 7 張。

最終數量：

```text
min(容量, 高價值且不重複的錨點數)
```

精選圖計入總數。

## 5. 插入位置

- Hero：文章標題後。
- Inline：概念第一次完整解釋的段落後。
- 不直接放在章節標題後。
- 兩張 inline 通常至少間隔兩個正文段落。
- 不在 FAQ、參考資料、作者資訊或純結論之後配裝飾圖。
- 第一張 inline 通常落在正文 20–40% 處。
- 最後一張圖通常在結論／限制之前。

Manifest 必須保存：

- `section_heading`
- `after_paragraph_global_index`
- `after_paragraph_excerpt`
- `reason`

## 6. 文內圖內容分工

常見三圖文章：

1. Hero：標題主張 + 最重要結果 + 核心原因。
2. Inline：核心機制或流程。
3. Inline：對比、規模變化、結果或限制。

避免把 Hero 中已清楚表達的內容，再做一張相同架構圖。
