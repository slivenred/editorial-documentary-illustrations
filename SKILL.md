---
name: editorial-documentary-illustrations
description: 為各語言文章規劃、生成與修訂 VOX-inspired／現代解說新聞式的羊皮紙剪紙正文配圖。當使用者提到 VOX 風格、紀錄片剪紙、歷史地圖動畫、aged parchment、paper cutout、文章配圖、文配圖、shot list、文章插圖、因果鏈、歷史過程、地圖路徑、認知標註、多語文字、10 秒動畫提示詞或統一畫風時使用。預設先自動判斷文章的主要讀者語言，再生成無字底圖，最後以可控後製加入一個核心判斷與 3–6 個同語言短標註；同篇文章共用 visual bible，並依 QA 門檻自動重試。不複製特定既有影片畫面或品牌資產。
---

# Editorial Documentary Illustrations

## 核心任務

把文章裡真正需要被「看見」的判斷、機制、時間進程、因果關係、規模變化與社會互動，轉成原創的 16:9 羊皮紙剪紙紀錄片配圖。

每張最終成品包含兩層：

1. **無字敘事底圖**：由圖像模型生成，負責場景、人物、物件、路徑、剪紙材質與動態暗示。
2. **可控認知標註**：由 Agent 根據文章上下文與讀者語言撰寫，再用程式後製加入，負責核心判斷、階段名稱、數字與物件指向。

底圖不得要求圖像模型排任何語言文字；最終成品則預設要有有意義、可讀、經校對且語言正確的短標註。

## 標註語言解析

生成 manifest 前先決定 `article.annotation_language`。依序使用：

1. **使用者明確指定**：最高優先級。
2. **文章 metadata**：frontmatter、locale、`lang` 或既有內容設定。
3. **文章主導語言**：標題、導言、段落標題與主要解說正文。
4. **混合語言判定**：以標題、段落標題與多數解說正文為準；忽略程式碼、網址、引用區塊、參考資料標題、品牌名與專有名詞。
5. **最後備援**：只有文章過短或無法判定時，才使用目前對話語言。

規則：

- 最終 manifest 必須寫入具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`；不得保留 `auto` 或 `und`；`mul` 只用於文章層的明確多語輸出。
- `article.language` 記錄文章主語言，`article.annotation_language` 記錄最終標註語言。
- 除非使用者明確要求翻譯，兩者預設相同。
- 同篇文章全部 still 圖預設使用同一標註語言；明確要求多語時才使用 `mul` 並逐張指定。
- 品牌、產品、模型、benchmark、縮寫、版本號、單位與數字保留文章原寫法，不因標註語言而擅自翻譯。
- `alt_text`、`caption` 與圖內標註預設使用 `article.annotation_language`。

## 預設值

除非使用者另有指定：

- 模式：`still`。
- 數量：5 張。
- 比例：16:9。
- 最終圖中文字：1 個核心判斷 + 3–6 個短標註。
- 標註方式：圖像模型不寫字，使用 `scripts/annotate_images.py` 後製。
- 生圖 prompt：英文；標註文字：`article.annotation_language`。
- 視覺：暖色舊羊皮紙、淡網格與摺痕、手繪剪紙人物、柔和短陰影、俯視地圖或輕微等角鏡頭、自然土色。
- 人物：簡化剪紙人形，不畫細緻手指、不做臉部特寫。
- 原創性：不重製任何特定既有畫面、logo、標題卡、字體或品牌資產。

## 需要時才讀取參考

- `references/article-analysis.md`
- `references/visual-bible.md`
- `references/style-dna.md`
- `references/character-system.md`
- `references/composition-patterns.md`
- `references/prompt-template.md`
- `references/annotation-system.md`
- `references/motion-mode.md`
- `references/qa-checklist.md`
- `references/retry-ladder.md`
- `references/originality-and-brand-safety.md`
- `references/style-lock.txt`

## 模式判定

### `plan`

1. 讀文章並建立 article map。
2. 解析 `article.language` 與 `article.annotation_language`。
3. 選擇認知錨點並建立 visual bible。
4. 為每張圖撰寫 `core_idea`、構圖、headline 與 3–6 個 labels。
5. 座標可先使用 provisional 值，但文字必須具體、有來源、語言正確。
6. 輸出 version 3 shot manifest，不呼叫圖像工具。

### `still`

使用者要求生成配圖時，必須完成整個雙層流程：

1. 完成 version 3 manifest，先解析並固定標註語言。
2. 生成低至中密度的無字 calibration frame。
3. 通過 Base QA 後，再逐張生成其餘無字底圖。
4. 支援參考圖時，把第一張合格底圖作為後續 style reference。
5. 逐張檢查底圖，找出可放字的安靜區與 labels 所指向的可見物件。
6. 更新 `annotation.layout_status` 為 `final`，修正座標。
7. 執行 `scripts/annotate_images.py`。
8. 對最終標註圖做 Annotation QA。
9. 底圖正確但文字失敗時，只調整 annotation plan，不重生成底圖。
10. 若環境沒有圖像工具，只交付 prompt、manifest 與 annotation plan，並清楚標示未實際生圖。
11. 若環境缺 Pillow 或對應語言字型，安裝依賴或指定本機字型；不得退回要求圖像模型直接排字。

### `motion`

1. 以 still shot 或 article anchor 為基礎。
2. 拆成 exactly 10 seconds、24fps 的四個連續節拍。
3. No voiceover、no text overlays。
4. 靜態圖的標註不直接燒進動畫；需要文字時交給影片剪輯層。

### `hybrid`

先完成帶標註 still，再由同一 visual bible 產出 motion prompt；不得重新發明人物、色盤、鏡頭或核心意象。

## 工作流

### 1. 消化文章，不要平均配圖

提煉一句話主張、時間或因果主線、關鍵角色與物件、最難想像的隱藏機制、規模轉折，以及最值得記住的結果、數字或矛盾。不要為純背景資訊或重複論點配圖。

### 2. 決定數量

- 800 字以下：1–3 張。
- 800–2,500 字：3–5 張。
- 2,500–5,000 字：5–7 張。
- 5,000 字以上：6–9 張。

### 3. 建立 Article Visual Bible

固定背景、色盤、鏡頭、光線、人物比例、recurring motif、路徑形式、密度節奏、標註紙片、連線、字級與色彩語意。同篇文章不得任意改動。

### 4. 產出 Shot Manifest

每張圖至少包含：

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
- `filename`
- `alt_text`
- `caption`
- `annotation.language`
- `annotation.headline`
- `annotation.labels`
- 可選 `motion_beats`

`annotation.language` 必須等於 `article.annotation_language`；只有 `article.annotation_language` 為 `mul` 時才可逐張不同。

### 5. 組裝無字底圖 Prompt

每張 prompt 依序包含原創性聲明、style lock、visual bible、shot、動態暗示、密度、人物數與標註留白區。不要把實際標註文字放進生圖 prompt；底圖只負責預留空間。

### 6. Calibration-first

第一張使用低至中密度、1–5 個人物、一個清楚主體，並能測試羊皮紙、剪紙邊緣、陰影、路徑、人物比例與標註留白。

### 7. 建立最終 Annotation Plan

1. 確認 headline 與段落一致。
2. 確認每個 label 指向的物件存在。
3. 以 0–1 正規化座標填入標籤位置與 target。
4. 避開人物臉部、手部、主要路徑、主體中心與裁切邊緣。
5. 同張圖的 callout 線不要大量交叉。
6. 將 `layout_status` 改為 `final`。
7. 使用 `scripts/annotate_images.py` 產生 PNG。

### 8. QA 與自動重試

- **Base QA**：場景、敘事、風格、人物與跨圖連續性。
- **Annotation QA**：語言符合目標、事實正確、語意有幫助、字可讀、指向正確、沒有遮擋或 PPT 化。

### 9. 保存與交付

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── annotation-plan.json
├── prompts/
├── images/
│   ├── raw/
│   │   └── 01-*.png
│   └── 01-*.png
└── delivery.md
```

最終回報包含生成張數、插入位置、用途、成品路徑、`alt_text`、calibration frame、重試原因、標註語言與是否完成後製。

## 永久禁忌

- 不複製特定媒體既有畫面或品牌資產。
- 不要求圖像模型直接排任何語言的長句、數字表格、logo、浮水印或字幕。
- 不把標註語言硬編碼成繁中、英文或任何單一語言。
- 不在未經要求時翻譯專有名詞、模型名、縮寫、版本號或數字。
- 不使用泛用標籤，例如「流程圖」「重點」「系統架構」「結果」及其其他語言的同義泛詞。
- 不讓文字遮住主體、人物臉部或主要路徑。
- 不用十幾個標註把畫面塞滿。
- 不畫精細手指、近距離手部操作或寫實臉部特寫。
- 不讓每張圖換一套色盤、鏡頭、紙張或標註樣式。
