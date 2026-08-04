---
name: editorial-documentary-illustrations
description: 為各語言文章自動規劃並生成一張標題導向的精選圖片與最合適數量的文內圖。使用 VOX-inspired／現代解說新聞式的羊皮紙剪紙視覺，把文章的主張、機制、對比、流程與結果轉成帶有可讀解釋文字的 16:9 最終圖片。圖片數量與插入位置會依文章長度、段落節奏、上下文與理解增益自動決定；精選圖回應標題，文內圖延續精選圖的完整視覺系統，不固定人物、不平均配圖、不用散亂標籤補救無關畫面。
---

# Editorial Documentary Illustrations

## 核心任務

為文章建立一套完整的「精選圖片 + 文內圖」視覺敘事：

1. **精選圖片**先回應文章標題、最重要結果與造成結果的核心原因。
2. **文內圖**只在能顯著降低理解成本的地方出現。
3. 每張圖都延續同一套羊皮紙、紙雕場景、字體氣質、邊框、色盤、標註卡與陰影。
4. 圖像與文字從一開始就共同設計；最終成品預設直接含有可讀文字。
5. 圖片數量、內容與位置，以最佳觀看體驗、理解速度與閱讀節奏為準。

這不是固定五張圖的模板，也不是論文架構圖、PPT 資訊圖或純裝飾插畫。

## 通過案例所確立的視覺方向

### 精選圖片

- 1600 × 900 或等比例 16:9。
- 暖色 aged parchment、低對比網格、細緻雙線邊框與簡潔角飾。
- 上方置中：短 eyebrow、文章核心 headline、結果型 subheadline。
- 中下方：一個可讀的紙雕敘事場景，例如競賽、路徑、機械、負擔、門、閘門、堆疊或轉化。
- 右側或靠近目標物：2–4 個短標註卡，使用短線與圓點，不讓線條穿過主體。
- 底部可加入一句結論旗帶或紙條。
- 人物不是必要條件；若物件已能說清楚，就不硬加人物。

### 文內圖

文內圖必須使用與精選圖相同的：

- 羊皮紙色與網格強度。
- 邊框與角飾。
- 標題位置、字級比例與色彩語意。
- 紙雕深度、陰影方向與物件材質。
- 標註卡、短引線、結論旗帶。

文內圖不可降級成白底簡圖、左右資訊面板、散落貼紙、傳統流程圖或普通向量圖。

## 精選圖片的 Title Contract

在規劃精選圖片前，先解析：

- `claim`：標題最主要的宣稱。
- `key_result`：最值得被記住的結果、數字或改變。
- `mechanism`：造成結果的核心原因。

精選圖必須在 headline、subheadline、主場景與標註中覆蓋至少兩項，且 `claim` 必須被直接呈現。

錯誤：只畫文章中的一個技術小節，卻沒有呈現標題主張。

正確：先以標題主張建立主場景，再用最重要結果與核心機制支撐它。

## 標註語言

依序決定 `article.annotation_language`：

1. 使用者明確指定。
2. 文章 frontmatter、locale、`lang` 或 metadata。
3. 標題、導言、段落標題與主要正文的主導語言。
4. 混合語言文章以多數解說正文為準；忽略程式碼、網址、引文、參考資料與專有名詞。
5. 文章過短或無法判斷時，才使用目前對話語言。

最終使用具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。產品名、模型名、benchmark、縮寫、版本、數字、百分比與單位保留原文，除非使用者要求翻譯。

## 預設行為

除非使用者另有指定：

- 模式：`still`。
- 比例：16:9。
- 精選圖：1 張。
- 文內圖數量：`auto`。
- 圖內文字：有，且是最終成品的一部分。
- 生圖 prompt：英文；要渲染的文字使用 `article.annotation_language`。
- 生圖 prompt 採 **lean 風格（v5，約 300-350 字）**：一段豐富敘事場景＋逐字文字清單＋一行濃縮風格。**不預載**大量版面/材質/文字安全限制——過度約束（v4 的 ~1,100 字 prompt）會把模型推向平面、圖表化產出；精簡 prompt 讓模型渲染豐富、有深度的紙雕敘事場景（已實驗驗證）。見 `references/prompt-template.md`。
- 第一張合格精選圖作為後續文內圖的 style reference。
- 在 Codex 中優先使用內建 `$imagegen`／支援高品質多語文字的圖片模型。
- 若模型文字有錯，只修文字或局部編輯；若場景與上下文不符，重新生成場景。
- 不新增 GitHub Actions 或任何自動部署流程。

## 需要時讀取

- `references/article-analysis.md`：文章拆解、自動圖片數量與插入位置。
- `references/visual-bible.md`：精選圖到文內圖的連續性。
- `references/style-dna.md`：通過案例所確立的視覺 DNA。
- `references/composition-patterns.md`：精選圖與文內圖構圖。
- `references/prompt-template.md`：整合式生圖提示詞。
- `references/annotation-system.md`：文字階層與直接生圖／修字策略。
- `references/qa-checklist.md`：標題對應、裁切、遮擋、文字與閱讀體驗。
- `references/retry-ladder.md`：最小修正策略。
- `references/motion-mode.md`：10 秒動畫。
- `references/originality-and-brand-safety.md`：原創與品牌界線。
- `references/style-lock.txt`：所有圖片必須遵守的風格鎖。

## 模式

### `plan`

1. 解析文章標題、摘要、正文、章節與閱讀時間。
2. 建立 `title_contract`。
3. 找出高價值且不重複的視覺錨點。
4. 自動決定總圖片數量。
5. 決定每張文內圖的精確插入位置。
6. 建立 Article Visual Bible。
7. 輸出 version 6 manifest，不生圖。

### `still`

1. 完成 version 6 manifest 並驗證。
2. 先生成精選圖。
3. 驗收精選圖是否對應標題、結果與機制。
4. 把合格精選圖作為文內圖 style reference。
5. 逐張生成文內圖；每張只解釋一個段落核心。
6. 驗收所有文字、邊界、遮擋、圖文關聯與跨圖一致性。
7. 若文字有錯，優先使用圖片編輯修正指定文字；不得因一個錯字重發明整張構圖。
8. 若場景不符合段落，重做該張圖。

### `hybrid`

先完成圖片，再依 manifest 中的 `placement` 產出 HTML demo 或整合到文章。Demo 必須呈現建議插入位置，不可只是圖片總覽。

### `motion`

由一張已通過 QA 的 still shot 產生 exactly 10 seconds、24fps、單一連續場景的動畫 prompt。靜態圖中文字不直接燒進動畫；需要文字時交給影片後製層。

## 自動決定圖片數量

先取得或估算 `reading_minutes`，再找出 7 分以上且互不重複的候選視覺錨點。

### 閱讀時間容量

- 1 分鐘：最多 1 張。
- 2 分鐘：最多 2 張。
- 3–4 分鐘：最多 3 張。
- 5–6 分鐘：最多 4 張。
- 7–9 分鐘：最多 5 張。
- 10–12 分鐘：最多 6 張。
- 13 分鐘以上：最多 7 張。

最終數量：

```text
min(閱讀時間容量, 高價值且不重複的視覺錨點數)
```

精選圖計入總數。若只有兩個真正有用的錨點，就只做兩張。

可執行：

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 3 \
  --include-hero
```

## 候選視覺錨點評分

每項 0–2 分：

- `comprehension_gain`：圖片是否明顯降低理解成本。
- `visual_structure`：是否有可見的機制、對比、流程或變化。
- `context_specificity`：是否直接對應該段上下文。
- `non_redundancy`：是否避免重複其他圖片。
- `placement_value`：插在該處是否改善閱讀。

總分至少 7 才保留。

## 自動插入位置

- 精選圖：文章標題後。
- 文內圖：概念第一次被完整解釋的段落後。
- 不直接放在章節標題後。
- 兩張文內圖通常至少間隔兩個正文段落。
- 不在 FAQ、參考資料、作者資訊或純結尾後加裝飾圖。
- 第一張文內圖通常位於正文約 20–40% 處。
- 最後一張圖通常在結論或限制段落之前，而不是之後。

Manifest 必須保存：

- 章節標題。
- 全文段落索引。
- 對應段落片段。
- 為何放在此處。

## 圖片文字階層

每張圖預設：

- Eyebrow：0–1 個。
- Headline：1 個，2–3 行內。
- Subheadline：1 個，1–2 行內。
- Labels：2–4 個。
- Bottom takeaway：0–1 個。
- Caveat：0–1 個，只有必要時使用。

Headline 必須是判斷，不是「系統架構圖」「流程」「重點」等圖表類型名稱。

## 安全版面

- 建議畫布：1600 × 900。
- 外安全邊界：至少 72 px。
- 重要文字與物件不得貼邊或被裁切。
- 標題區與主場景不可互相遮擋。
- 標註引線短而清楚，不穿過主體。
- 任何文字卡不得遮住核心物件、路徑、比較結果或人物臉部。
- 縮至 600 px 寬時，headline、主要數字與標籤仍要可讀。

## 人物規則

人物是可選元素，不是固定 IP：

- 有助於呈現負擔、競賽、操作或決策時才加入。
- 純機制、門、閘門、記憶盒、路徑、堆疊或資源比較，不需要人物也可以成立。
- 不為了「有故事感」硬塞人物。

## 精選圖到文內圖的連續性

後續每張文內圖都必須明確要求：

```text
Use the approved featured image only as a style reference.
Match its parchment tone, fine border, corner ornaments, centered title hierarchy,
paper-crafted depth, shadow direction, label-card treatment, accent colors,
and bottom takeaway ribbon. Do not copy its composition.
```

若文內圖不像精選圖所屬的同一套專題，視為失敗。

## 保存與交付

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── prompts/
├── images/
│   ├── 00-featured.png
│   ├── 01-inline-*.png
│   └── ...
└── delivery.md
```

交付需包含：

- 自動決定的總圖片數量。
- 精選圖對應的 Title Contract。
- 每張文內圖的段落、用途與插入位置。
- 圖片路徑、alt text 與 caption。
- 任何重試、修字或裁切修正紀錄。

## 永久禁忌

- 不固定輸出五張。
- 不平均為每個小節配圖。
- 不讓文內圖降級成和精選圖不同的視覺系統。
- 不使用散落的大量 callout 補救無關畫面。
- 不強迫無字底圖獨自承擔所有技術細節。
- 不讓文字遮住主體或讓物件超出範圍。
- 不把人物當成必填元素。
- 不用泛用 AI 機器、城市、齒輪或伺服器塔硬套任何技術文章。
- 不生成傳統 PPT、企業向量圖、密集論文圖、兒童卡通或遊戲式 3D 畫面。
- 不複製特定 Vox 或其他媒體現成畫面、logo、字體與標題卡。
