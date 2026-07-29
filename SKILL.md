---
name: editorial-documentary-illustrations
description: 為中文或英文文章規劃、生成與修訂 VOX-inspired／現代解說新聞式的羊皮紙剪紙紀錄片正文配圖。當使用者提到 VOX 風格、紀錄片剪紙、歷史地圖動畫、aged parchment、paper cutout、文章配圖、文配圖、shot list、文章插圖、因果鏈、歷史過程、地圖路徑、10 秒動畫提示詞、去文字或統一畫風時使用。預設輸出 16:9、無圖中文字、同篇文章共用 visual bible，並依 QA 門檻自動重試；不複製特定既有影片畫面或品牌資產。
---

# Editorial Documentary Illustrations

## 核心任務

把文章裡真正需要被「看見」的判斷、機制、時間進程、因果關係、規模變化與社會互動，轉成原創的 16:9 羊皮紙剪紙紀錄片配圖。

這不是把每個段落畫成圖，也不是把文章壓成 PPT 資訊圖。每張圖必須像一個被凍結的 time-lapse 關鍵畫面：讀者先感受到場景正在發生，再在一秒內理解該段落的核心意思。

## 預設值

除非使用者另有指定：

- 模式：`still` 靜態文章配圖。
- 數量：5 張。
- 比例：16:9 橫式。
- 圖中文字：0；標題、caption 與 alt text 放在圖片外。
- 語言：輸出說明與 metadata 跟隨使用者語言；生圖 prompt 使用英文。
- 視覺：暖色舊羊皮紙、淡網格與摺痕、手繪剪紙／紙貼紙人物、柔和短陰影、俯視地圖或輕微等角鏡頭、自然土色。
- 人物：簡化剪紙人形，不畫細緻手指、不做臉部特寫。
- 原創性：只使用抽象視覺語法，不重製任何特定既有畫面、logo、標題卡或品牌資產。

## 需要時才讀取參考

不要一次把所有參考檔塞入上下文。依任務逐步讀取：

- `references/article-analysis.md`：文章拆解、認知錨點評分與配圖數量。
- `references/visual-bible.md`：同篇文章的連續性鎖定。
- `references/style-dna.md`：視覺 DNA、色盤、鏡頭、材質與禁忌。
- `references/character-system.md`：剪紙人物、群眾、物件與文化表現。
- `references/composition-patterns.md`：可用構圖與避免 PPT 化的方法。
- `references/prompt-template.md`：靜態生圖 prompt 組裝規則。
- `references/motion-mode.md`：exactly 10 seconds 動畫模式。
- `references/qa-checklist.md`：硬性失敗項與 100 分制驗收。
- `references/retry-ladder.md`：依失敗類型重試，不盲目追加形容詞。
- `references/originality-and-brand-safety.md`：公開命名、原創性與品牌界線。
- `references/style-lock.txt`：每張 prompt 必須逐字重複的不可變風格鎖。

## 模式判定

### `plan`

使用者說「先分析」「只做 shot list」「先不要生圖」時：

1. 讀文章。
2. 建立 article map。
3. 選擇認知錨點。
4. 建立 visual bible。
5. 輸出 shot list／manifest。
6. 不呼叫圖像工具。

### `still`

使用者說「生成」「做圖」「產出文章配圖」時：

1. 先完成 manifest。
2. 先生成一張低至中密度的 calibration frame。
3. 自行依 QA 驗收；不要停下來要求使用者確認。
4. 校準圖合格後，再逐張生成其餘圖片。
5. 每張圖單獨呼叫圖像工具，不要拼圖。
6. 支援參考圖時，把第一張合格圖片當作後續 style reference；不支援時，每張 prompt 逐字重複 style lock 與 visual bible。
7. 若本環境沒有圖像生成工具，只交付完整 prompt 與 manifest，明確說明未實際生成圖片；不得假稱已生圖。

### `motion`

使用者要求 10 秒動畫、time-lapse、影片分鏡或 Gemini／Veo prompt 時：

1. 以現有 still shot 或 article anchor 為基礎。
2. 按 `references/motion-mode.md` 拆成四個時間節拍。
3. 保持 exactly 10 seconds、24fps、no voiceover、no text overlays。
4. 只輸出一個連續場景，不把四段做成硬切投影片。

### `hybrid`

使用者同時要配圖與動畫時：

1. 先完成 still。
2. 通過 QA 後，再由同一 visual bible 產出 motion prompt。
3. 動畫不得重新發明人物、色盤、鏡頭或核心意象。

## 工作流

### 1. 消化文章，不要平均配圖

讀取正文、Markdown、文件、網頁、截圖或單一觀點，提煉：

- 一句話主張。
- 時間或因果主線。
- 關鍵角色與物件。
- 讀者最難想像的隱藏機制。
- 規模從小到大的轉折。
- 最值得被記住的結果或矛盾。

依 `references/article-analysis.md` 評分候選段落。優先挑能產生「物理動作、路徑、聚集、變形、組裝、擴散、排隊、拆解、回流」的認知錨點。

不要為純背景資訊、重複論點或只需一句 caption 就能說清楚的段落配圖。

### 2. 決定數量

- 800 字以下：1–3 張。
- 800–2,500 字：3–5 張。
- 2,500–5,000 字：5–7 張。
- 5,000 字以上：6–9 張。

這只是上限指南，不是平均分配公式。若 3 張已足夠，就不要硬做 7 張。

### 3. 建立 Article Visual Bible

生成任何圖片前，固定以下欄位：

- 背景羊皮紙與紋理強度。
- 文章專屬 4–6 色色盤。
- 鏡頭角度與構圖安全區。
- 光源方向與陰影長度。
- 人物剪紙比例、服裝色與臉部簡化方式。
- 一個貫穿全文的 recurring motif。
- 路徑線、箭頭或移動軌跡的形式。
- 由低到高的畫面密度節奏。
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
- `filename`。
- `alt_text_zh_tw`。
- `caption_zh_tw`，可留空。
- motion 模式可再加 `motion_beats`。

優先使用 `schemas/shot-manifest.schema.json`。若 workspace 可執行 Python，先跑：

```bash
python3 scripts/validate_manifest.py <manifest.json>
```

### 5. 組裝 Prompt

每張 prompt 必須依序包含：

1. 原創性聲明。
2. `references/style-lock.txt` 全文，逐字不變。
3. Article Visual Bible。
4. 當張 shot 的核心意思與構圖。
5. 「凍結 time-lapse」的動態暗示。
6. 畫面密度與人物數。
7. 負面限制。
8. 16:9 與安全區要求。

不要把多張 shot 放進同一個 prompt。不要要求圖像模型生成中文標題、caption、logo 或數字表格。

### 6. Calibration-first 生成

第一張優先選：

- 低至中密度。
- 1–5 個人物。
- 一個清楚主體。
- 能同時測試羊皮紙、剪紙邊緣、陰影、路徑與人物比例。

第一張低於 85 分或有硬性失敗項時，先依 retry ladder 修正，不能帶著錯誤畫風繼續批量生成。

### 7. QA 與自動重試

依 `references/qa-checklist.md`：

- 任何硬性失敗項直接重做或局部編輯。
- 總分低於 85 不交付。
- 同一問題最多採同一修正策略重試 2 次；仍失敗就換構圖，不要無限堆疊形容詞。
- 群眾畸形時，改用剪紙群組、背影、側影或分層 silhouette，不要求模型畫更多細節。
- 畫面像 PPT 時，移除方框、節點、文字與整齊箭頭，改成物理場景、道路、桌面、攤位、機械或地形。

### 8. 保存與交付

保存至：

```text
assets/<article-slug>-editorial-documentary/
```

建議內容：

```text
manifest.json
prompts/01-*.txt
images/01-*.png
delivery.md
```

按順序命名，不能覆蓋既有檔案，除非使用者明確要求。

最終回報需包含：

- 實際生成／規劃幾張。
- 每張圖對應哪個段落與用途。
- 圖片或 prompt 路徑。
- 每張繁中 alt text。
- 哪一張是 calibration frame。
- 哪些圖片曾重試以及原因。
- 若未能實際生圖，清楚標示只完成 prompt／manifest。

## 永久禁忌

- 不複製特定 VOX 或其他媒體既有影片畫面。
- 不加入 Vox logo、品牌字體、黃色標題卡或足以暗示官方合作的元素。
- 不使用照片寫實、3D render、企業扁平向量、動漫、兒童繪本、遊戲 UI 或 PPT 模板感。
- 不在圖內生成標題、長句、logo、浮水印、字幕或旁白文字。
- 不畫精細手指、近距離手部操作或寫實臉部特寫。
- 不用十幾個獨立細節人物硬湊「熱鬧」；群眾應使用簡化剪紙群組。
- 不讓每張圖換一套色盤、鏡頭或紙張。
- 不把風格詞堆得比畫面內容更長；先減少元素，再精準修正。
