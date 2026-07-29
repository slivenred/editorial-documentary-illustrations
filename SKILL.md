---
name: editorial-documentary-illustrations
description: 為中文或英文文章規劃、生成與修訂 VOX-inspired／現代解說新聞式的羊皮紙剪紙正文配圖。當使用者提到 VOX 風格、紀錄片剪紙、歷史地圖動畫、aged parchment、paper cutout、文章配圖、文配圖、shot list、文章插圖、因果鏈、歷史過程、地圖路徑、認知標註、繁中文字、10 秒動畫提示詞或統一畫風時使用。預設先生成無字底圖，再以可控後製加入一個核心判斷與 3–6 個短標註；同篇文章共用 visual bible，並依 QA 門檻自動重試。不複製特定既有影片畫面或品牌資產。
---

# Editorial Documentary Illustrations

## 核心任務

把文章裡真正需要被「看見」的判斷、機制、時間進程、因果關係、規模變化與社會互動，轉成原創的 16:9 羊皮紙剪紙紀錄片配圖。

每張最終成品包含兩層：

1. **無字敘事底圖**：由圖像模型生成，負責場景、人物、物件、路徑、剪紙材質與動態暗示。
2. **可控認知標註**：由 Agent 根據文章上下文撰寫，再用程式後製加入，負責核心判斷、階段名稱、數字與物件指向。

不要要求圖像模型直接生成繁中長句。底圖必須無文字，最終成品則預設要有有意義、可讀、經校對的短標註。

## 預設值

除非使用者另有指定：

- 模式：`still` 靜態文章配圖。
- 數量：5 張。
- 比例：16:9 橫式。
- 最終圖中文字：1 個核心判斷 + 3–6 個短標註。
- 標註語言：跟隨文章；繁中內容使用台灣繁體中文。
- 標註方式：圖像模型不寫字，使用 `scripts/annotate_images.py` 後製。
- 生圖 prompt：英文。
- 視覺：暖色舊羊皮紙、淡網格與摺痕、手繪剪紙／紙貼紙人物、柔和短陰影、俯視地圖或輕微等角鏡頭、自然土色。
- 人物：簡化剪紙人形，不畫細緻手指、不做臉部特寫。
- 原創性：只使用抽象視覺語法，不重製任何特定既有畫面、logo、標題卡、字體或品牌資產。

## 需要時才讀取參考

依任務逐步讀取，不要一次塞滿上下文：

- `references/article-analysis.md`：文章拆解、認知錨點評分與配圖數量。
- `references/visual-bible.md`：同篇文章的連續性鎖定。
- `references/style-dna.md`：視覺 DNA、色盤、鏡頭、材質與禁忌。
- `references/character-system.md`：剪紙人物、群眾、物件與文化表現。
- `references/composition-patterns.md`：可用構圖與避免 PPT 化的方法。
- `references/prompt-template.md`：無字底圖 prompt 組裝規則。
- `references/annotation-system.md`：核心判斷、短標註、色彩語意、座標與後製規則。
- `references/motion-mode.md`：exactly 10 seconds 動畫模式。
- `references/qa-checklist.md`：底圖與最終標註圖的硬性失敗項、100 分制驗收。
- `references/retry-ladder.md`：依失敗類型重試，不盲目追加形容詞。
- `references/originality-and-brand-safety.md`：公開命名、原創性與品牌界線。
- `references/style-lock.txt`：每張底圖 prompt 必須逐字重複的不可變風格鎖。

## 模式判定

### `plan`

使用者說「先分析」「只做 shot list」「先不要生圖」時：

1. 讀文章並建立 article map。
2. 選擇認知錨點。
3. 建立 visual bible。
4. 為每張圖撰寫 `core_idea`、構圖與**語意標註草案**。
5. 座標可以先使用 provisional 值，但文字本身必須具體、有來源。
6. 輸出 version 2 shot manifest，不呼叫圖像工具。

### `still`

使用者說「生成」「做圖」「產出文章配圖」時，必須完成整個雙層流程，不得停在無字底圖：

1. 完成 version 2 manifest，包含每張圖的語意標註草案。
2. 先生成一張低至中密度的無字 calibration frame。
3. 自行依底圖 QA 驗收；不要停下來要求使用者確認。
4. 校準圖合格後，再逐張生成其餘無字底圖。
5. 支援參考圖時，把第一張合格底圖作為後續 style reference；不支援時，每張 prompt 逐字重複 style lock 與 visual bible。
6. 用視覺能力逐張檢查實際底圖，找出可放字的安靜區與每個標註所指向的可見物件。
7. 更新 manifest 中的 `annotation.layout_status` 為 `final`，修正 `x/y/target_x/target_y`。
8. 執行 `scripts/annotate_images.py`，把語意文字後製到圖片。
9. 對**最終標註圖**再做一次 QA；文字碰撞、錯字、指錯物件或過度遮擋時，只調整 annotation plan，不重生成正確的底圖。
10. 只有底圖內容或風格本身錯誤時才重生成底圖。
11. 若環境沒有圖像生成工具，只交付完整 prompt、manifest 與 annotation plan，明確說明未實際生成圖片；不得假稱已生圖。
12. 若環境無 Pillow，先安裝 `requirements-annotation.txt`；不得退回要求圖像模型直接寫繁中。

### `motion`

使用者要求 10 秒動畫、time-lapse、影片分鏡或 Gemini／Veo prompt 時：

1. 以現有 still shot 或 article anchor 為基礎。
2. 按 `references/motion-mode.md` 拆成四個時間節拍。
3. 保持 exactly 10 seconds、24fps、no voiceover、no text overlays。
4. 只輸出一個連續場景，不把四段做成硬切投影片。
5. 靜態圖的認知標註不直接燒進動畫；需要文字時交給影片剪輯或字幕層處理。

### `hybrid`

使用者同時要配圖與動畫時：

1. 先完成帶標註的 still 成品。
2. 通過 QA 後，再由同一 visual bible 與同一無字底圖邏輯產出 motion prompt。
3. 動畫不得重新發明人物、色盤、鏡頭或核心意象。

## 工作流

### 1. 消化文章，不要平均配圖

提煉：

- 一句話主張。
- 時間或因果主線。
- 關鍵角色與物件。
- 讀者最難想像的隱藏機制。
- 規模從小到大的轉折。
- 最值得被記住的結果、數字或矛盾。

優先挑能產生「物理動作、路徑、聚集、變形、組裝、擴散、排隊、拆解、回流」的認知錨點。不要為純背景資訊、重複論點或只需一句 caption 就能說清楚的段落配圖。

### 2. 決定數量

- 800 字以下：1–3 張。
- 800–2,500 字：3–5 張。
- 2,500–5,000 字：5–7 張。
- 5,000 字以上：6–9 張。

這是上限指南，不是平均分配公式。

### 3. 建立 Article Visual Bible

生成任何底圖前，固定：

- 背景羊皮紙與紋理強度。
- 文章專屬 4–6 色色盤。
- 鏡頭角度與構圖安全區。
- 光源方向與陰影長度。
- 人物剪紙比例、服裝色與臉部簡化方式。
- 一個貫穿全文的 recurring motif。
- 路徑線、箭頭或移動軌跡形式。
- 由低到高的畫面密度節奏。
- 標註紙片、連線、字級與色彩語意。
- 禁止事項。

同篇文章後續圖片不得任意改動 visual bible。

### 4. 產出 Shot Manifest

每張圖至少包含：

- `placement_after`：建議放在哪段後。
- `anchor`：對應原文句子或段落摘要。
- `role`：構圖類型。
- `core_idea`：這張圖只需說懂的一件事。
- `composition`：主要場景與空間安排。
- `main_subject`：唯一主焦點。
- `supporting_elements`：最多 8 項。
- `motion_cues`：靜態畫面如何暗示 time-lapse。
- `density` 與 `people_count`。
- `filename`、`alt_text_zh_tw`、`caption_zh_tw`。
- `annotation.headline`：一句核心判斷，不是文章標題。
- `annotation.labels`：3–6 個短標註，每個必須指向實際可見物件。
- motion 模式可再加 `motion_beats`。

語意文字必須先根據文章寫好；座標則在底圖生成後用實際畫面校正。

### 5. 組裝無字底圖 Prompt

每張 prompt 依序包含：

1. 原創性聲明。
2. `references/style-lock.txt` 全文，逐字不變。
3. Article Visual Bible。
4. 當張 shot 的核心意思與構圖。
5. 「凍結 time-lapse」的動態暗示。
6. 畫面密度與人物數。
7. 後製標註所需的安靜留白區。
8. 負面限制、16:9 與安全區要求。

不要把多張 shot 放進同一個 prompt。不要把實際繁中標註文字放進生圖 prompt。底圖只能保留空間，不負責排字。

### 6. Calibration-first 生成

第一張優先選：

- 低至中密度。
- 1–5 個人物。
- 一個清楚主體。
- 能同時測試羊皮紙、剪紙邊緣、陰影、路徑、人物比例與標註留白。

第一張低於門檻或有硬性失敗項時，先依 retry ladder 修正，不能帶著錯誤畫風繼續批量生成。

### 7. 建立最終 Annotation Plan

底圖完成後逐張執行：

1. 確認核心判斷與段落一致。
2. 確認每個 label 所指向的物件確實存在。
3. 以 0–1 正規化座標填入標籤左上角與 target 點。
4. 避開人物臉部、手部、主要路徑、主體中心與裁切邊緣。
5. 同張圖的 callout 線不要大量交叉。
6. 把 `layout_status` 改為 `final`。
7. 使用 `scripts/annotate_images.py` 產生最終 PNG。

文字原則詳見 `references/annotation-system.md`。

### 8. QA 與自動重試

依 `references/qa-checklist.md` 分兩階段：

- **Base QA**：場景、敘事、風格、人物與跨圖連續性。
- **Annotation QA**：事實正確、語意有幫助、字可讀、指向正確、沒有遮擋或 PPT 化。

任何硬性失敗直接修正。底圖正確而文字失敗時，只改 annotation plan；同一問題最多採同一策略重試 2 次，仍失敗就減少標註或更換標籤位置。

### 9. 保存與交付

保存至：

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

- `images/raw/`：無字模型底圖。
- `images/`：已加入可控認知標註的最終成品。
- 不覆蓋 raw 底圖。
- 最終回報需包含生成張數、插入位置、用途、成品路徑、alt text、calibration frame、重試原因與是否完成後製標註。

## 永久禁忌

- 不複製特定 VOX 或其他媒體既有影片畫面。
- 不加入 Vox logo、品牌字體、黃色標題卡或足以暗示官方合作的元素。
- 不使用照片寫實、遊戲式 3D render、企業扁平向量、動漫、兒童繪本、遊戲 UI 或 PPT 模板感。
- 不要求圖像模型直接寫繁中長句、數字表格、logo、浮水印、字幕或旁白文字。
- 最終圖不使用泛用標籤，例如「流程圖」「重點」「系統架構」「結果」；每個詞都必須來自文章的具體認知。
- 不讓文字遮住主體、人物臉部或主要路徑。
- 不用十幾個標註把畫面塞滿；預設 1 個核心判斷與 3–6 個短標註。
- 不畫精細手指、近距離手部操作或寫實臉部特寫。
- 不用十幾個獨立細節人物硬湊熱鬧；群眾使用簡化剪紙群組。
- 不讓每張圖換一套色盤、鏡頭、紙張或標註樣式。
- 不把風格詞堆得比畫面內容更長；先減少元素，再精準修正。
