# Semantic Annotation System

## 核心原則

最終文內圖由兩個互補層次組成：

- **場景層**：把抽象內容變成可見的物理動作、路徑、角色與結果。
- **認知標註層**：指出讀者應該看懂的判斷、名稱、數字、階段與轉折。

圖像模型不得直接負責排字。先生成無字底圖，逐張看圖後，再用程式後製已校對的文字。

## 標註語言自動判定

先解析並固定 `article.annotation_language`：

1. 使用者明確指定的語言。
2. 文章 metadata、frontmatter、locale 或 `lang`。
3. 標題、導言、段落標題與主要解說正文的主導語言。
4. 混合語言文章以標題、段落標題與多數解說正文為準。
5. 只有文章太短或無法判斷時，才使用對話語言。

判定時忽略：程式碼、網址、引用區塊、參考資料標題、品牌名、模型名、縮寫、版本號與專有名詞。

輸出規則：

- 使用具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`；不得保留 `auto` 或 `und`；`mul` 只用於文章層的明確多語輸出。
- 未指定翻譯時，`annotation_language` 等於文章主語言。
- 使用者要求翻譯時，標註使用指定語言，但產品名、模型名、benchmark、縮寫、版本號、數字、百分比與單位保留文章原寫法。
- 同篇文章預設使用同一種標註語言。明確需要多語時，將文章層設為 `mul`，並逐張指定具體語言。
- `alt_text` 與 `caption` 預設使用同一標註語言。

## 預設輸出合約

每張 still 成品預設包含：

- 1 個 `headline`：一句核心判斷。
- 3–6 個 `labels`：短標註或階段名。
- 每個 label 有 callout line 與 target dot，指向底圖中的實際物件。
- 全部文字面積通常不超過畫面的 30–35%。
- 底圖、標籤紙片、連線、字體與色彩語意在同篇文章內一致。

## 如何寫 headline

headline 不是文章標題、段落標題或圖表類型，而是這張圖要留下的判斷。

例子：

- `小而專精，取代全面依賴`
- `Specialize the routine, escalate the hard cases`
- `分歧不是噪音，是升級訊號`
- `Disagreement becomes a routing signal`

規則：

- CJK 語言通常 8–20 個字元。
- 使用空格分詞的語言通常 4–12 個詞。
- 優先使用判斷、對比、因果、限制或結果。
- 不重複 caption，不加不必要句號，不使用文章沒有依據的誇張結論。

## 如何寫 labels

每個 label 必須：

1. 有文章依據。
2. 能指向實際可見的模型、人物、路徑、文件、關卡或結果。
3. 有認知價值，而不是只把物件重新命名。

建議：

- CJK 語言通常 2–12 個字元。
- 使用空格分詞的語言通常 1–6 個詞。
- 一張圖 3–6 個，流程型畫面最多 7 個。
- 數字保留單位、百分比或名稱，例如 `16 CVEs`、`5B active parameters`、`16 個 CVE`。
- 語法、拼字、地區用詞與標點符合 `annotation_language`。

禁止：

- 泛用詞及其翻譯，例如 `流程／workflow`、`結果／result`、`重點／key points`、`系統／system`、`資料／data`。
- 冗長說明、FAQ、把 caption 拆回圖內。
- 指向不存在或難以辨識的物件。
- 為湊數而重複同一意思。

## 色彩語意

- `ink`：中性結構、輪廓、一般物件。
- `terracotta`：主角、核心模型、主要行動。
- `ochre`：主流程、路徑、規模、常規工作。
- `sage`：驗證、修補、安全結果、完成狀態。
- `indigo`：通用模型、基礎設施、對照組、次要系統。
- `brick`：風險、警告、攻擊、分歧、升級案件。

同一概念在同篇文章中不要換色。

## 紙片與字體

標註視覺預設：

- 暖米色不規則紙片，細褐色邊線。
- 很淡的短陰影，方向跟底圖一致。
- 上方可有半透明紙膠帶。
- 下緣使用 accent 色乾刷線。
- callout line 略有手繪抖動，末端有小圓點。
- headline 比 labels 大一級，但不能像海報主標。
- 使用能完整顯示目標語言的本機字型；可有手寫感，但不可犧牲辨識度。
- 不在 repository 內附帶或分享字型檔。

1600×900 基準：headline 36–46 px、labels 26–34 px、連線 3–5 px、target dot 5–7 px、padding 12–24 px。

渲染器會依 `annotation.language` 選擇字型族。阿拉伯文、希伯來文與部分南亞文字需要對應字型；複雜 shaping 建議使用具 RAQM 支援的 Pillow。

## 座標規則

manifest 使用 0–1 正規化座標：

- `x`、`y`：標籤紙片左上角。
- `target_x`、`target_y`：callout line 指向物件的位置。

## 語意先定、座標後定

生成前先寫好語意文字，底圖 prompt 只要求預留安靜區，不放實際文字。生成後逐張查看底圖，確認物件存在，再更新座標、設為 `layout_status: final`，執行 renderer，最後檢查成品。

## 版面安排

- headline 優先放在上方或大面積安靜區。
- labels 靠近對應物件，連線短、清楚、少交叉。
- 避開人物臉部、手部、主物件中心、路徑交會點與裁切邊緣。
- 流程畫面可沿路徑放階段名，但不能變成正式流程圖節點。
- 文字服從場景，不能讓圖片退化成簡報。

## 何時減少文字

若連線大量交叉、文字覆蓋主體、資訊重複、或縮到行動裝置後不可讀，先減少 labels，不要把字縮到無法辨識。保留順序：headline、最重要名稱或數字、因果轉折、次要階段。

## 後製命令

```bash
python3 scripts/annotate_images.py   path/to/manifest.json   --input path/to/images/raw   --output path/to/images   --force
```

找不到適用於目標語言的系統字型時：

```bash
python3 scripts/annotate_images.py   path/to/manifest.json   --input path/to/images/raw   --output path/to/images   --font /path/to/local-font.ttf   --force
```

## 失敗判斷

直接修正 annotation plan：

- 標註語言與 `article.annotation_language` 不一致。
- 錯字、亂碼、不自然翻譯或不當混用語言。
- 名稱、模型、數字或單位和文章不符。
- headline 沒有判斷。
- label 指錯物件。
- 文字遮住主體或關鍵路徑。
- 標籤太多、太整齊、太像 PPT。
- 目標語言字型缺字或不可讀。

只有底圖本身的主體、構圖或風格錯誤時才重生成底圖。
