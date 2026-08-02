---
name: editorial-documentary-illustrations
description: 為各語言文章自動規劃並生成 VOX-inspired／現代解說新聞式的羊皮紙剪紙精選圖片與文內圖。會依文章長度、段落結構與內容價值，自動決定最佳圖片數量、用途與插入位置；每張圖以符合上下文的剪紙場景搭配整合式解釋文字，不以泛用 AI 圖或散亂 callout 取代文章內容。支援多語標註、16:9 靜態圖與 exactly 10 seconds 動畫提示詞。
---

# Editorial Documentary Illustrations

## 核心任務

把文章中真正需要視覺化的機制、對比、流程、時間變化、數字結果與決策意義，轉成一組風格一致、內容直接對應上下文的 16:9 羊皮紙剪紙解說圖。

最終圖不是「一張無字插畫＋散落標籤」，而是一張完整的 editorial explainer board：

1. 上方：一句核心判斷與一行補充說明。
2. 中間：符合該段上下文的 VOX-inspired 羊皮紙剪紙場景。
3. 下方或側邊：2–4 個短解釋卡，依固定閱讀順序補足名稱、因果、比例或結果。

圖像與文字共同完成解釋。不要要求無字底圖單獨承擔所有技術細節，也不要讓文字替一張不相關的泛用圖片硬找意義。

## 預設行為

除非使用者另有指定：

- 模式：`still`。
- 比例：16:9。
- 圖片數量：`auto`，不固定 5 張。
- 圖片類型：需要時產生 1 張 hero，其餘為 inline。
- 標註語言：自動跟隨文章或使用者指定的目標讀者語言。
- 圖中文字：1 個短 headline、1 個 subheadline、2–4 個解釋卡。
- 生圖 prompt：英文；最終文字：`article.annotation_language`。
- 視覺：暖色羊皮紙、低對比網格、手工剪紙、柔和短陰影、俯視或輕微等角鏡頭、自然土色。
- 文字後製：`scripts/annotate_images.py`。
- 不複製特定既有影片影格、logo、標題卡、字體或品牌資產。

## 標註語言

依序判斷：

1. 使用者明確指定。
2. 文章 frontmatter、locale、`lang` 或 metadata。
3. 標題、導言、段落標題與主要正文的主導語言。
4. 混合語言文章以多數解說正文為準，忽略程式碼、網址、引文、參考資料與專有名詞。
5. 文章太短或無法判斷時，才使用目前對話語言。

最終寫入具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。產品名、模型名、benchmark、縮寫、版本號、數字、百分比與單位保留原文，除非使用者要求翻譯。

## 需要時讀取

- `references/article-analysis.md`：自動選圖數量與位置。
- `references/composition-patterns.md`：六種圖解版型。
- `references/visual-bible.md`：同篇文章畫風一致。
- `references/style-dna.md`：VOX-inspired 剪紙視覺規則。
- `references/prompt-template.md`：無字底圖 prompt。
- `references/annotation-system.md`：整合式文字版面。
- `references/qa-checklist.md`：內容、視覺與文字驗收。
- `references/retry-ladder.md`：最小修正策略。
- `references/motion-mode.md`：10 秒動畫。
- `references/originality-and-brand-safety.md`：品牌與原創界線。
- `references/style-lock.txt`：底圖固定風格鎖。

## 模式

### `plan`

1. 解析文章語言、閱讀時間、段落與章節。
2. 找出候選視覺錨點並評分。
3. 自動計算最佳圖片數量。
4. 選擇每張圖的用途、版型與插入位置。
5. 建立 Visual Bible 與 version 5 manifest。
6. 不呼叫圖像工具。

### `still`

1. 完成 version 5 manifest。
2. 驗證自動圖片數量與位置。
3. 逐張生成無字底圖；第一張合格圖可作為後續 style reference。
4. 檢查底圖是否直接對應該段上下文，且保留指定文字安全區。
5. 使用 `scripts/annotate_images.py` 加入 headline、subheadline 與解釋卡。
6. 對最終成品做 QA；文字錯誤只改文字層，畫面不相關才重生底圖。

### `motion`

以已通過 still QA 的 shot 為基礎，轉成 exactly 10 seconds、24fps、單一連續場景、無 voiceover、無 text overlay 的動畫 prompt。靜態解釋文字不燒進動畫。

## 自動決定圖片數量

先計算或讀取 `reading_minutes`。沒有 metadata 時：

- 中文、日文、韓文：以可見文字長度估算閱讀時間。
- 其他語言：以正文單字數估算。

再依文章找出 7 分以上且不重複的視覺錨點。圖片總數為：

```text
min(依閱讀時間的容量, 高價值錨點數量)
```

閱讀時間容量：

- 1–2 分鐘：最多 1 張。
- 3–4 分鐘：最多 3 張。
- 5–6 分鐘：最多 4 張。
- 7–9 分鐘：最多 5 張。
- 10–12 分鐘：最多 6 張。
- 13–16 分鐘：最多 7 張。
- 17 分鐘以上：最多 8 張。

可執行：

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 4 \
  --sections 5 \
  --include-hero
```

不要為了達到數量而硬配圖。若只有兩個真正有價值的錨點，就只做兩張。

## 候選錨點評分

每項 0–2 分，總分至少 7：

- `comprehension_gain`：圖片是否明顯降低理解成本。
- `visual_structure`：是否有可見的流程、對比、變化或關係。
- `context_specificity`：是否直接對應本段，而非泛用概念。
- `non_redundancy`：是否和其他圖功能不同。
- `placement_value`：放在這裡是否能改善閱讀節奏。

## 自動決定插入位置

- Hero 放在文章標題後。
- Inline 圖放在「概念已被完整介紹」的段落後，不放在標題和第一句之間。
- 通常放在該章節第 1–2 個解釋段落後。
- 兩張 inline 圖至少間隔 2 個正文段落。
- 不連續放圖，不在 FAQ、參考資料或純結論後硬塞圖。
- 同一短章節最多 1 張；只有長章節且有兩個不同機制時才例外。
- `placement.after_paragraph_excerpt` 必須引用真實段落片段，避免位置漂移。

## 每張圖的資訊結構

Manifest 每張 shot 包含：

- `kind`：`hero` 或 `inline`
- `placement`
- `purpose`
- `layout`
- `eyebrow`
- `headline`
- `subheadline`
- `visual_story`
- `key_elements`
- `explainers`
- `motion_cues`
- `filename`
- `alt_text`
- `caption`

每個 explainer 包含：

- `title`：2–12 個中文字或同等長度。
- `body`：一句補充說明。
- `accent`：色彩語意。
- `visual_anchor`：底圖中對應的可見物件或區域。

## 六種版型

- `hero-explainer`：上方結論，中間主視覺，下方 3 張解釋卡。
- `mechanism-focus`：上方結論，左側機制主體，右側 2–4 張解釋卡。
- `process-strip`：上方結論，中間流程場景，下方依序排列階段卡。
- `comparison-split`：上方結論，中間左右對比，下方兩側說明與一個總結。
- `timeline-route`：上方結論，中間彎曲時間路徑，下方階段卡。
- `result-board`：上方結論，中間結果場景，下方 2–4 張數字或決策卡。

## 圖像生成原則

- 每張圖只解釋一個核心問題。
- 先決定要說什麼，再決定剪紙場景。
- 技術內容可使用簡化模組、層、Token、記憶卡、比較軌跡，但不要追求論文架構圖的精密複製。
- 不預設加入人物、機器人、城市、工廠、齒輪、發光大腦或伺服器塔。
- 只保留 2–6 個關鍵物件。
- 文字和圖共同解釋，不要求圖像模型直接生成任何文字。

## QA

最終成品必須同時通過：

1. 上下文正確：讀者能看出它在解釋哪一段。
2. 視覺簡單：一個主焦點，沒有過度技術化或過度裝飾。
3. 文字有效：headline 是結論，卡片是原因、階段、對比或結果。
4. 版面清楚：上→中→下或左→右有固定閱讀順序。
5. 圖片數量與位置合理：沒有每節硬塞圖，也沒有兩張相鄰。
6. 同篇一致：羊皮紙、色盤、鏡頭、字體與卡片樣式一致。

## 保存

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── prompts/
├── images/
│   ├── raw/
│   └── 01-*.png
└── delivery.md
```

## 永久禁忌

- 不把 VOX 風格當成內容相關性的替代品。
- 不為每篇文章固定生成 5 張。
- 不使用散亂、交叉的 callout 線與大量貼紙標籤。
- 不要求無字底圖單獨解釋所有細節。
- 不把技術文章變成難懂的論文架構圖。
- 不讓文字遮住主視覺或塞滿超過約 35% 畫面。
- 不要求圖像模型排文字、數字、logo 或字幕。
- 不複製特定媒體既有畫面或品牌資產。
