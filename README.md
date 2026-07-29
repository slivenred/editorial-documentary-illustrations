# Editorial Documentary Illustrations

> 把文章中的關鍵判斷、歷史過程、因果鏈、系統機制與規模變化，轉成穩定一致、帶有可讀認知標註的 16:9 羊皮紙剪紙紀錄片配圖。

這是一個可安裝到 Codex／支援 `SKILL.md` 工作流之 AI Agent 的文章配圖 Skill。它會先理解文章、建立同篇文章共用的 Visual Bible、生成無字底圖，再依文章的主要讀者語言後製認知標註。

## 它解決什麼問題

單一超長提示詞常見五種失敗：

1. 同篇文章的圖片風格不一致。
2. 抽象內容被畫成 PPT，而不是有敘事感的場景。
3. 圖片漂亮，但沒有幫助讀者理解文章。
4. 直接要求圖像模型排字，容易出現錯字、亂碼、假數字或錯誤標示。
5. 標註被硬寫成某一種語言，和原文章節或目標讀者不一致。

本 Skill 使用五層穩定機制：

- **文章認知錨點**：不平均配圖，只挑真正值得視覺化的段落。
- **Article Visual Bible**：固定背景、色盤、人物、鏡頭、光影與重複意象。
- **Immutable Style Lock**：每張底圖逐字重複同一段風格鎖定。
- **Language-aware Annotation Pipeline**：自動判斷標註語言，先生成無字底圖，再用程式後製文字。
- **QA + Retry Ladder**：分別驗收底圖與最終標註圖。

## 標註語言如何決定

依下列優先順序決定：

1. 使用者明確指定的標註語言。
2. 文章 frontmatter、locale 或內容 metadata 中的語言。
3. 標題、導言、標題層級與主要正文的主導語言。
4. 混合語言文章以標題、段落標題與多數解說正文為準；忽略程式碼、網址、引用、參考資料標題與專有名詞。
5. 文章太短而無法判斷時，才使用對話語言作為最後備援。

最後必須把結果寫成具體 BCP 47 語言標籤，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。不能把 `auto` 留在最終 manifest。產品名、模型名、基準測試、縮寫、版本號與數字保留文章中的原始寫法。

## 預設輸出

- 16:9 橫式文章正文配圖。
- 一篇文章 3–7 張；長文最多 9 張。
- 每張最終成品包含 1 個核心判斷與 3–6 個短標註。
- 圖像模型只負責無字底圖；標註語言由文章自動判定，文字使用可控程式後製。
- `alt_text`、`caption` 與圖內標註使用相同的目標語言，除非使用者另有指定。
- 原始與成品分開保存：

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

## 安裝

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations   "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

套件不附帶任何字型檔。渲染器會依 `article.annotation_language` 自動尋找相符的本機字型，也可用 `--font` 指定本機字型。阿拉伯文、希伯來文與部分南亞文字建議使用具 RAQM 支援的 Pillow 與對應 Noto 字型。

## 使用方式

### 只規劃

```text
Use $editorial-documentary-illustrations
分析下面文章，先產出 5 張紀錄片剪紙文配圖的 version 3 shot manifest，不要生圖。
自動判斷文章的主要讀者語言，並以該語言撰寫每張圖的一個核心判斷與 3–6 個短標註草案。

<貼上文章>
```

### 直接生成完整成品

```text
Use $editorial-documentary-illustrations
替下面文章生成 5 張 16:9 羊皮紙剪紙正文配圖。
先自動判斷文章的主要讀者語言；若我沒有另外指定，圖內標註、alt text 與 caption 都沿用文章主語言。
先生成無字底圖，再根據實際畫面加入一個核心判斷與 3–6 個短標註。
文字必須指向可見物件、保留原文專有名詞，並經過校對。

<貼上文章>
```

### 指定不同標註語言

```text
Use $editorial-documentary-illustrations
文章是英文，但最終文內圖要給台灣讀者，請使用 zh-TW 標註；模型名、縮寫與數字保留英文原樣。
```

### 10 秒動畫提示詞

```text
Use $editorial-documentary-illustrations
把第 3 張配圖改寫成 exactly 10 seconds、24fps 的紀錄片剪紙動畫提示詞。
不要配音、不要字幕，只保留環境音與流暢 time-lapse。
```

## 驗證、編譯與後製

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/render_prompts.py   path/to/manifest.json   --mode still   --output path/to/prompts-still

python3 scripts/annotate_images.py   path/to/manifest.json   --input path/to/images/raw   --output path/to/images   --force
```

需要指定字型時：

```bash
python3 scripts/annotate_images.py   path/to/manifest.json   --input path/to/images/raw   --output path/to/images   --font /path/to/local-font.ttf   --force
```

## 目錄結構

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE.md
├── requirements-annotation.txt
├── agents/openai.yaml
├── references/
│   ├── annotation-system.md
│   └── ...
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── annotate_images.py
│   ├── render_prompts.py
│   └── validate_manifest.py
├── tests/test_tooling.py
└── third_party/ian-xiaohei-illustrations-LICENSE.txt
```

## 為什麼不用圖像模型直接寫字

圖像模型適合建立場景、材質與視覺隱喻，但不是穩定的多語排版器。這套 Skill 將兩件事拆開：

1. 圖像模型生成乾淨、可標註的視覺底圖。
2. Agent 判斷文章語言、校對文字，再以確定性程式加入標籤。

## 授權與聲明

- 本套件採 MIT License。
- 工作流架構參考並改寫自 Ian 的 `ian-xiaohei-illustrations`；詳見 `NOTICE.md`。
- 本套件不包含原專案的小黑 IP、範例圖片或字型檔。
- 本套件與 Vox Media 無關，也不應宣稱為 Vox 官方產品。
