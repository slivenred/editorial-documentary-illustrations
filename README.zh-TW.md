# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 把文章中的關鍵判斷、歷史過程、因果鏈、隱藏機制與規模變化，轉成風格一致、帶有可讀認知標註的 16:9 羊皮紙剪紙文內圖。

**Editorial Documentary Illustrations** 是一個可安裝到 Codex，以及其他能遵循 `SKILL.md` 工作流程之 AI Agent 的文章配圖 Skill。它會讀取文章、挑選真正值得視覺化的段落、建立同篇文章共用的 Visual Bible、生成無字底圖，最後依原文或目標讀者的語言加入經過校對的語意標註。

## 為什麼需要這個 Skill

單一超長生圖提示詞經常出現以下問題：

1. 同篇文章的每張圖像來自不同專案，風格持續漂移。
2. 抽象概念被畫成 PPT 方框與箭頭，而不是有敘事感的實體場景。
3. 圖片看起來漂亮，卻沒有幫助讀者理解文章。
4. 直接要求圖像模型排字，容易產生錯字、亂碼、假數字與錯誤標示。
5. 標註語言被硬性固定，和原文章節或目標讀者不一致。

本 Skill 使用五層穩定機制：

- **文章認知錨點**：不平均配圖，只挑具有機制、對比、路徑、瓶頸、規模變化或關鍵結論的段落。
- **Article Visual Bible**：固定整篇文章的羊皮紙、色盤、鏡頭、光線、人物比例、重複意象與標註樣式。
- **Immutable Style Lock**：每張底圖都重複同一套不可變視覺限制。
- **語言感知標註流程**：先生成無字底圖，再用確定性程式後製經校對的文字。
- **QA 與 Retry Ladder**：分開驗收無字底圖與最終標註圖。

## 工作流程

```text
文章
  ↓
Article map 與認知錨點
  ↓
Article Visual Bible
  ↓
Version 3 shot manifest
  ↓
無字 calibration frame
  ↓
使用風格參考生成其餘無字底圖
  ↓
判斷標註語言與建立 annotation plan
  ↓
以程式渲染紙片標籤
  ↓
Base QA + Annotation QA
```

## 標註語言如何決定

依照下列優先順序解析：

1. 使用者明確指定的標註語言。
2. 文章 frontmatter、locale、`lang` 或內容 metadata。
3. 標題、導言、段落標題與主要正文的主導語言。
4. 混合語言文章以多數解說正文為準；忽略程式碼、網址、引文、參考資料、品牌名與專有名詞。
5. 只有文章太短或無法判斷時，才使用目前的對話語言。

最後必須寫入具體 BCP 47 語言標籤，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。最終設定不得保留 `auto` 或 `und`；`mul` 只用於文章層的明確多語輸出，每一張圖片仍需使用具體語言。

除非使用者明確要求，產品名、模型名、benchmark、縮寫、版本號、數字、百分比與單位都保留原文寫法。

## 預設輸出

- 16:9 橫式文章文內圖。
- 一篇文章通常 3–7 張，長文最多 9 張。
- 每張最終成品包含 1 個核心判斷與 3–6 個短標註。
- 圖像模型只生成無字底圖。
- 後製標註包含紙片、連線與 target dot，可穩定校對與修改。
- `alt_text`、`caption` 與圖內標註使用同一目標語言。
- 無字原圖與最終成品分開保存：

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

將整個 repo 複製到 Codex Skills 目錄：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安裝標註所需套件：

```bash
python3 -m pip install -r requirements-annotation.txt
```

本套件不附帶任何字型檔。渲染器會依 `article.annotation_language` 自動尋找相符的本機字型，也可用 `--font` 指定本機字型。阿拉伯文、希伯來文與部分南亞文字建議使用支援 RAQM 的 Pillow 與相應字型。

## 使用方式

### 只規劃，不生圖

```text
Use $editorial-documentary-illustrations
分析下面文章，建立 5 張紀錄片剪紙文內圖的 version 3 shot manifest，先不要生成圖片。
自動判斷文章的主要讀者語言，並以該語言為每張圖撰寫一個核心判斷與 3–6 個短標註草案。

<文章內容>
```

### 直接生成完整標註成品

```text
Use $editorial-documentary-illustrations
替下面文章生成 5 張 16:9 羊皮紙剪紙文內圖。
若我沒有另外指定，請自動判斷文章的主要讀者語言。
先生成無字底圖，再檢查實際構圖，加入一個核心判斷與 3–6 個短標註。
每個標註都必須指向可見物件、保留原文專有名詞，並通過事實與語言校對。

<文章內容>
```

### 指定不同標註語言

```text
Use $editorial-documentary-illustrations
文章原文是英文，但文內圖要提供給台灣讀者。圖內標註、alt text 與 caption 請使用 zh-TW；模型名、縮寫、benchmark 與數字保留原文。
```

### 產生正好 10 秒的動畫提示詞

```text
Use $editorial-documentary-illustrations
把第 3 張配圖改寫成 exactly 10 seconds、24fps 的紀錄片剪紙動畫提示詞。
不要配音、不要圖中文字，只保留環境音與一個連續的 time-lapse 場景。
```

## 驗證、編譯與後製

驗證 manifest：

```bash
python3 scripts/validate_manifest.py path/to/manifest.json
```

編譯無字底圖提示詞與 annotation plan：

```bash
python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts-still
```

把生成好的無字底圖放入 `images/raw/`，校正標註座標後產生最終圖片：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

需要指定本機字型時：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/local-font.ttf \
  --force
```

## Version 3 manifest 重點

```json
{
  "version": 3,
  "article": {
    "title": "範例文章",
    "slug": "example-article",
    "language": "zh-TW",
    "annotation_language": "zh-TW",
    "summary": "文章的一句話摘要與主要論點。",
    "target_count": 5
  },
  "shots": [
    {
      "id": "01",
      "filename": "01-specialist-model.png",
      "alt_text": "專用模型處理主要工作，少數困難案件才升級到大型模型。",
      "caption": "常規任務留在高效率路徑，只有最困難案件才升級。",
      "annotation": {
        "enabled": true,
        "language": "zh-TW",
        "layout_status": "draft",
        "headline": {
          "text": "常規任務留在高效率路徑",
          "x": 0.38,
          "y": 0.06,
          "accent": "terracotta",
          "font_size": 42,
          "angle": 0
        },
        "labels": []
      }
    }
  ]
}
```

完整格式請查看 [`templates/manifest.template.json`](templates/manifest.template.json) 與 [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json)。

## 專案結構

```text
.
├── SKILL.md
├── README.md
├── README.zh-TW.md
├── README.zh-CN.md
├── README.ja.md
├── README.ko.md
├── README.es.md
├── LICENSE
├── NOTICE.md
├── requirements-annotation.txt
├── agents/openai.yaml
├── references/
│   ├── annotation-system.md
│   ├── article-analysis.md
│   ├── visual-bible.md
│   ├── style-dna.md
│   ├── prompt-template.md
│   ├── qa-checklist.md
│   └── retry-ladder.md
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── annotate_images.py
│   ├── render_prompts.py
│   └── validate_manifest.py
└── tests/test_tooling.py
```

## 設計原則

- 一張圖只說明一個核心認知。
- 最終圖片必須幫助理解文章，而不只是裝飾。
- 圖像模型負責建立視覺世界，確定性程式負責文字。
- 標註語言跟隨文章，或依使用者指定的目標讀者調整。
- 每個標註都必須指向看得見的物件，並增加認知價值。
- 底圖正確但文字錯誤時，只修改 annotation plan，不浪費生圖額度。
- 品牌風格名稱只能作為描述捷徑，不代表可以複製既有畫面或品牌識別。

## 出處與授權

- 本專案採用 [MIT License](LICENSE)。
- 多步驟工作流程參考並改寫自 Ian 的 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)，詳見 [`NOTICE.md`](NOTICE.md)。
- 本 repo 不包含原專案的小黑 IP、範例圖片、原始提示詞全文或字型檔。
- 本專案與 Vox Media 無關，也未獲其背書。請勿複製特定影片影格、logo、標題卡、字體或品牌素材。
