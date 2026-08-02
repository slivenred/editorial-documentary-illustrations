# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 把文章的機制、對比、因果鏈與結果，轉成語意正確、風格一致，並帶有可讀標註的 16:9 羊皮紙剪紙文內圖。

**Editorial Documentary Illustrations** 是可安裝到 Codex，以及其他能執行 `SKILL.md` 工作流程之 AI Agent 的文章配圖 Skill。它不會再把「看起來像 VOX」視為完成，而是先為每張圖建立可驗證的文章語意合約，強制無字底圖本身呈現文章專屬的實體、機制與關係。

## 這次解決的核心問題

羊皮紙、剪紙、土色系與俯視鏡頭可以很漂亮，但如果只要換掉標籤，同一張圖就能套到幾十篇其他文章，代表它只是風格正確，內容並不正確。

新版 Skill 將工作拆成六層：

- **Article Map 與認知錨點**：找出真正需要被看見的機制、關係、取捨、變化與結果。
- **文章級語意基礎**：固定 `article_type`、`visual_thesis`、`topic_signature` 與 `global_must_avoid`。
- **每張圖的 Semantic Contract**：定義來源依據、必須看見的內容、視覺證據映射、文章專屬詞、盲測描述與 Hero Artifact。
- **Visual Bible 與 Style Lock**：只負責統一材質、色盤、鏡頭、光線、比例與標註樣式，不得取代文章機制。
- **語言感知的確定性標註**：先生成無字底圖，再使用文章或目標讀者語言後製文字。
- **三階段 QA**：Semantic Preflight、Base QA、Annotation QA。

## 語意優先於風格

拿掉所有標註後，圖片仍必須看得出文章專屬機制。標註只能命名已存在的視覺證據，不能把泛用機器、城市、工廠、機器人、腦、伺服器塔、道路、盾牌或工作人員，事後硬解釋成文章中的技術架構。

技術研究預設優先順序：

1. `literal-technical`
2. `hybrid-metaphor`
3. `literal-scene`
4. 只有無法忠實呈現時才使用 `abstract-metaphor`

`technical-research` 的精選圖片禁止使用 `abstract-metaphor`。

## 工作流程

```text
文章與主要來源
  ↓
Article Map + 文章類型
  ↓
Visual Thesis + Topic Signature
  ↓
Version 4 Semantic Contract
  ↓
Semantic Preflight
  ↓
無字 Calibration Frame
  ↓
Label-off + Blind-caption + Neighbor-article 測試
  ↓
其餘語意正確的無字底圖
  ↓
語言解析 + Annotation Plan
  ↓
確定性紙片標註渲染
  ↓
Final Annotation QA
```

## Semantic Contract 包含什麼

每張圖必須包含：

- `image_role`：`hero` 或 `inline`
- `visualization_mode`
- `source_basis`
- `must_show`
- `must_not_show`
- `visual_evidence`：概念 → 可見形式 → 必須成立的關係
- `specificity_terms`
- `expected_blind_caption`
- Hero 圖必填 `hero_artifact`

Hero 必須是第一張且全篇只能有一張，至少包含三個 `must_show`，並至少有兩個文章專屬詞和 `topic_signature` 重疊。

## 三項強制語意測試

### Label-off Test

隱藏全部標註後，底圖仍要看得出機制與關係。

### Blind-caption Test

不看 Prompt 與標註，只描述底圖一句話。Hero 的描述必須自然包含至少兩個文章專屬錨點，以及正確的關係或取捨。

### Neighbor-article Test

只換標籤就能套用到另一篇文章，判定失敗。

## 標註語言解析

依序使用：

1. 使用者明確指定。
2. 文章 frontmatter、locale 或 `lang`。
3. 標題、導言、段落標題與主要正文的主導語言。
4. 混合語言文章以多數解說正文為準，忽略程式碼、網址、引文、參考資料、品牌名與專有名詞。
5. 只有文章太短或無法判斷時，才使用對話語言。

最終使用具體 BCP 47 tag，例如 `zh-TW`、`en`、`ja`、`ko`、`es`。不得保留 `auto` 或 `und`。產品名、模型名、benchmark、縮寫、版本、數字、百分比與單位保留原文，除非使用者明確要求翻譯。

## 預設輸出

- 16:9 橫式文章文內圖。
- 一篇通常 3–7 張，長文最多 9 張。
- 每張成品包含一個核心判斷與 3–6 個短標註。
- 無字底圖與最終標註圖分開保存。

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

## 安裝

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

本套件不附帶任何字型檔。渲染器會依 `article.annotation_language` 選擇本機字型，也可用 `--font` 指定。

## 使用方式

### 只規劃

```text
Use $editorial-documentary-illustrations
分析文章與主要來源，建立 5 張圖片的 version 4 manifest。
選構圖前先決定 article_type、visual_thesis、topic_signature、global_must_avoid，並替每張圖建立 semantic_contract。
先不要生成圖片。

<文章內容>
```

### 直接生成完整成品

```text
Use $editorial-documentary-illustrations
替文章生成 5 張 16:9 羊皮紙剪紙文內圖。
語意優先於風格；拿掉標註後，底圖仍須呈現文章專屬機制，並通過 Label-off、Blind-caption、Neighbor-article 三項測試。
先生成無字底圖，再依目標讀者語言加入經校對的標註。

<文章內容>
```

### 技術研究文章

```text
Use $editorial-documentary-illustrations
這是 technical-research 文章。規劃精選圖片前，先讀 abstract、architecture／method figure、method、results 與 limitations。
Hero 必須使用文章領域中的真實架構 Artifact，不得用泛用工作人員、工廠、城市、機器人、腦、齒輪或伺服器塔取代技術機制。
```

## 驗證、語意預檢、Prompt 與標註

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/semantic_preflight.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts-still

python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

## Version 4 重點

```json
{
  "version": 4,
  "article": {
    "article_type": "technical-research",
    "visual_thesis": "3:1 混合堆疊保留精確檢索，同時用固定狀態取代大部分持續成長的 KV cache。",
    "topic_signature": [
      "固定遞迴狀態",
      "全注意力檢索層",
      "3:1 分層比例",
      "持續成長的 KV cache"
    ],
    "global_must_avoid": [
      "泛用 AI 機器人或發光大腦",
      "與架構無關的工作人員操作機器"
    ]
  },
  "shots": [
    {
      "image_role": "hero",
      "visualization_mode": "literal-technical",
      "role": "architecture-stack",
      "semantic_contract": {
        "source_basis": ["來源主張一", "來源主張二"],
        "must_show": ["必要架構", "必要關係", "必要資源對比"],
        "must_not_show": ["沒有架構映射的泛用機器"],
        "visual_evidence": [
          {
            "concept": "3:1 分層比例",
            "visible_form": "單一四層堆疊，三個赤陶色模組與一個靛藍色模組",
            "relationship": "四個模組交錯組成同一個架構"
          }
        ],
        "specificity_terms": ["3:1 分層比例", "固定遞迴狀態"],
        "expected_blind_caption": "四層混合架構將固定狀態和持續成長的 KV cache 放在同一個對比中。",
        "hero_artifact": "一個交錯式四層注意力架構堆疊"
      }
    }
  ]
}
```

完整格式請查看 [`templates/manifest.template.json`](templates/manifest.template.json)、[`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json) 與 [`references/semantic-grounding.md`](references/semantic-grounding.md)。

## 專案結構

```text
.
├── SKILL.md
├── README*.md
├── references/
│   ├── semantic-grounding.md
│   ├── article-analysis.md
│   ├── composition-patterns.md
│   ├── prompt-template.md
│   ├── qa-checklist.md
│   └── ...
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── semantic_preflight.py
│   ├── validate_manifest.py
│   ├── render_prompts.py
│   └── annotate_images.py
└── tests/test_tooling.py
```

## 出處與授權

- 本專案採用 [MIT License](LICENSE)。
- 多步驟工作流程參考並改寫自 Ian 的 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)，詳見 [`NOTICE.md`](NOTICE.md)。
- 本 repo 不包含原專案的小黑 IP、範例圖片、複製提示詞或字型檔。
- 本專案與 Vox Media 無關，也未獲其背書。請勿複製特定影片影格、logo、標題卡、字體或品牌素材。
