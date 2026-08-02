---
name: editorial-documentary-illustrations
description: 為各語言文章規劃、生成與修訂 VOX-inspired／現代解說新聞式的羊皮紙剪紙正文配圖。當使用者要求文章配圖、精選圖片、文內圖、shot list、歷史地圖動畫、paper cutout、認知標註、多語文字、10 秒動畫提示詞、統一畫風或圖文語意對齊時使用。預設先建立文章語意合約與 Visual Bible，確保無字底圖本身能表達文章專屬機制，再依文章或目標讀者語言後製核心判斷與短標註；依 Semantic Preflight、Base QA、Annotation QA 自動重試。不複製特定既有影片畫面或品牌資產。
---

# Editorial Documentary Illustrations

## 核心任務

把文章中的判斷、機制、時間進程、因果關係、規模變化與結果，轉成原創的 16:9 羊皮紙剪紙文內圖。

**風格一致不是成功條件，只是基本條件。** 無字底圖必須在沒有標註時，就能讓讀者看出文章專屬的實體、機制與關係。不能先畫一張泛用 VOX 風格圖片，再靠文字把它硬解釋成文章內容。

每張最終成品包含：

1. **語意正確的無字底圖**：圖像模型負責場景、物件、機制、關係、材質與動態暗示。
2. **可控認知標註**：Agent 依文章與讀者語言撰寫，使用程式後製核心判斷、名稱、數字、階段與 callout。

先讀 `references/semantic-grounding.md`，再進行視覺規劃。

## 標註語言解析

生成 manifest 前決定 `article.annotation_language`：

1. 使用者明確指定。
2. 文章 frontmatter、locale、`lang` 或 metadata。
3. 標題、導言、段落標題與主要正文的主導語言。
4. 混合語言文章以多數解說正文為準，忽略程式碼、網址、引用、參考資料與專有名詞。
5. 只有文章太短或無法判斷時，才使用對話語言。

使用具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。不得保留 `auto` 或 `und`；`mul` 只用於文章層的明確多語輸出。除非使用者要求翻譯，`article.language`、`article.annotation_language`、`alt_text`、`caption` 與圖內標註使用同一語言。產品名、模型名、benchmark、縮寫、版本、單位與數字保留原文。

## 預設值

- 模式：`still`
- 數量：5 張
- 比例：16:9
- 最終文字：1 個核心判斷 + 3–6 個短標註
- 底圖 prompt：英文
- 標註語言：`article.annotation_language`
- 標註方式：`scripts/annotate_images.py`
- 視覺：暖色羊皮紙、淡網格、紙張摺痕、手繪剪紙物件、柔和短陰影、俯視或輕微等角鏡頭
- 原創性：不重製任何特定影格、logo、標題卡、字體或品牌資產

## 必讀參考

依任務讀取：

- `references/article-analysis.md`
- `references/semantic-grounding.md`
- `references/visual-bible.md`
- `references/style-dna.md`
- `references/composition-patterns.md`
- `references/prompt-template.md`
- `references/annotation-system.md`
- `references/qa-checklist.md`
- `references/retry-ladder.md`
- `references/motion-mode.md`
- `references/originality-and-brand-safety.md`
- `references/style-lock.txt`

## 模式

### `plan`

1. 讀文章與主要來源。
2. 解析文章與標註語言。
3. 設定 `article_type`、`visual_thesis`、`topic_signature`、`global_must_avoid`。
4. 建立 Visual Bible。
5. 為每張圖建立 `semantic_contract`。
6. 撰寫構圖、headline 與 labels 草案。
7. 輸出 version 4 manifest；不生圖。

### `still`

1. 完成並驗證 manifest。
2. 執行 Semantic Preflight；未通過不得生圖。
3. 先生成一張低至中密度的無字 calibration frame。
4. 以 Label-off、Blind-caption、Neighbor-article 三項測試驗收底圖。
5. 通過後才逐張生成其他底圖；參考圖只鎖材質與畫風，不覆寫每張語意合約。
6. 逐張確認 `must_show`、`visual_evidence`、hero artifact 與可標註區。
7. 更新 annotation 座標與 `layout_status: final`。
8. 執行 `scripts/annotate_images.py`。
9. 執行 Annotation QA。
10. 底圖語意正確而標註失敗時，只改 annotation plan；語意不正確時必須重生底圖。

### `motion`

以已通過語意 QA 的 still shot 為基礎，建立 exactly 10 seconds、24fps、單一連續場景、無 voiceover、無 text overlay 的動畫 prompt。不得在動畫版本重新發明機制。

### `hybrid`

先完成帶標註 still，再從同一 semantic contract 與 Visual Bible 產出 motion prompt。

## 工作流

### 1. 建立 Article Map

提煉：文章主張、起點、轉化、隱藏機制、規模／資源變化、結果與限制。

### 2. 建立文章級語意基礎

Manifest 的 `article` 必須包含：

- `article_type`
- `visual_thesis`
- `topic_signature`
- `global_must_avoid`

`topic_signature` 至少包含三個文章專屬項目，不能只寫 AI、model、data、speed、system 等泛詞。

### 3. 技術研究先讀主要來源

`technical-research` 需優先讀 abstract、architecture／method figure、method、result figure 與 limitations。預設使用 `literal-technical` 或 `hybrid-metaphor`。不得把模型架構隨意變成城市、工廠、辦公室人群、機器人、腦、齒輪或伺服器塔。

### 4. 建立 Article Visual Bible

固定背景、色盤、鏡頭、光線、剪紙材質、人物比例、recurring motif、密度與標註樣式。Visual Bible 只能統一畫風，不能取代文章專屬內容。

### 5. 建立 Shot Manifest

每張圖至少包含：

- `image_role`: `hero` 或 `inline`
- `visualization_mode`
- `placement_after`
- `anchor`
- `role`
- `core_idea`
- `composition`
- `main_subject`
- `supporting_elements`
- `motion_cues`
- `density`
- `people_count`
- `semantic_contract`
- `filename`
- `alt_text`
- `caption`
- `annotation`

### 6. Semantic Contract

每張圖必須包含：

- `source_basis`
- `must_show`
- `must_not_show`
- `visual_evidence`
- `specificity_terms`
- `expected_blind_caption`
- `hero_artifact`；inline 可留空，hero 不可留空

Hero 規則：

- 最多一張；若存在，必須是第一張。
- 至少 3 個 `must_show`。
- 至少兩個 `specificity_terms` 與 `article.topic_signature` 重疊。
- 必須呈現一個關係、取捨或變化，不可只堆符號。
- 精選圖片不是泛用 world-building 場景。

### 7. 組裝 Prompt

順序固定為：

1. Non-negotiable Semantic Contract
2. Visual evidence mapping
3. Style Lock
4. Visual Bible
5. Shot composition
6. Annotation reservation
7. Output constraints

Prompt 必須明寫：**Meaning overrides style**、底圖不得依賴後製文字才成立、不得用泛用 AI 符號替代文章機制。

### 8. 三項語意測試

#### Label-off Test

隱藏所有標註後，底圖仍須表達機制與關係。

#### Blind-caption Test

不看 prompt，描述底圖一句話。描述必須包含至少兩個文章專屬錨點與正確關係，並接近 `expected_blind_caption`。

#### Neighbor-article Test

若只換標籤就能讓同一底圖套用到其他文章，視為失敗。

### 9. Annotation

標註只能命名或解釋已存在的 visual evidence。不得把泛用齒輪、道路或機器硬標成文章中的特定機制。

### 10. 保存

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── annotation-plan.json
├── prompts/
├── images/
│   ├── raw/
│   └── 01-*.png
└── delivery.md
```

## 永久禁忌

- 不以 VOX 風格正確取代內容正確。
- 不生成可套用到大量其他文章的泛用 AI 圖。
- 不讓標註拯救與文章無關的底圖。
- 不忽略 `must_show`、`visual_evidence` 或 hero artifact。
- 不把技術研究預設畫成人類操作泛用機器。
- 不要求圖像模型直接排任何語言的文字、數字表格、logo 或字幕。
- 不硬編碼標註語言。
- 不翻譯未要求翻譯的專有名詞、模型名、benchmark、縮寫、版本與數字。
- 不複製媒體或品牌既有畫面。
