# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 依文章長度與內容，自動選擇最佳圖片數量與插入位置，再生成符合上下文、帶有整合式解釋文字的 VOX-inspired 羊皮紙剪紙文內圖。

這是一個可安裝到 Codex，以及其他能執行 `SKILL.md` 工作流程之 AI Agent 的文章配圖 Skill。

每張最終圖片使用固定資訊層級：

```text
小標 → 核心判斷 → 一行補充 → 剪紙主視覺 → 2–4 張解釋卡
```

圖片和文字共同完成解釋，不再要求無字底圖單獨塞入全部技術細節，也不使用散亂標籤替泛用 AI 圖硬找意義。

## Version 5 改了什麼

上一版過度強調語意合約、盲測、括號、比較線與技術結構，容易產生「看起來嚴謹，實際更難讀」的圖片。

新版改為：

- 圖片數量自動計算，不固定 5 張。
- 插入位置綁定真實段落片段。
- 一張圖只回答一個問題。
- 主場景只保留 2–6 類關鍵物件。
- Headline、subheadline 與解釋卡採固定版面。
- 精確名稱、比例、數字與限制放在短卡片中。
- 不使用大量散落貼紙與交叉 callout 線。

## 自動決定圖片數量

| 閱讀時間 | 圖片總數上限 |
|---|---:|
| 1–2 分鐘 | 1 |
| 3–4 分鐘 | 3 |
| 5–6 分鐘 | 4 |
| 7–9 分鐘 | 5 |
| 10–12 分鐘 | 6 |
| 13–16 分鐘 | 7 |
| 17 分鐘以上 | 8 |

最終數量：

```text
min(閱讀時間容量, 7 分以上且互不重複的視覺錨點數)
```

Hero 也計入總數。沒有足夠內容時，不為了湊數硬配圖。

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 4 \
  --sections 5 \
  --include-hero
```

四分鐘左右的 Kimi Linear 文章會建議 3 張，而不是 4–5 張。

## 自動決定插入位置

- Hero 放在文章標題後。
- Inline 圖放在概念第一次完整說明的段落後。
- 不直接放在章節標題後、第一句前。
- 兩張 Inline 至少間隔兩個正文段落。
- 不在 FAQ、參考資料、作者資訊或文章尾端硬塞圖。
- Manifest 保存章節、段落索引、真實段落片段與放置理由。

## 六種版型

- `hero-explainer`：上方結論、中間主視覺、下方三張卡。
- `mechanism-focus`：左側機制、右側解釋卡。
- `process-strip`：中間流程、下方階段卡。
- `comparison-split`：左右對比、下方兩側說明與總結。
- `timeline-route`：彎曲時間路徑與階段卡。
- `result-board`：結果場景與數字／決策卡。

## 安裝

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

本套件不附帶任何字型檔。渲染器會依 `article.annotation_language` 尋找本機字型，也可用 `--font` 指定。

## 使用方式

### 只規劃

```text
Use $editorial-documentary-illustrations
分析這篇文章，自動決定最佳圖片數量與插入位置。
每個被選中的段落建立一張 version 5 shot，使用整合式圖解版型。
先不要生成圖片。

<文章內容>
```

### 直接生成完整成品

```text
Use $editorial-documentary-illustrations
依文章內容自動生成最佳數量的 16:9 VOX-inspired 羊皮紙剪紙文內圖。
不要固定生成 5 張。每張圖必須直接對應所在段落，並以文章語言加入一個 headline、一行 subheadline 與 2–4 張短解釋卡。
先生成無字底圖，再渲染整合式文字版面。

<文章內容>
```

## 指令

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts

python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

完整格式請查看 [`templates/manifest.template.json`](templates/manifest.template.json) 與 [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json)。

## 專案結構

```text
.
├── SKILL.md
├── README*.md
├── references/
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── recommend_image_count.py
│   ├── validate_manifest.py
│   ├── render_prompts.py
│   └── annotate_images.py
└── tests/test_tooling.py
```

## 授權與聲明

- 本專案採用 [MIT License](LICENSE)。
- 多步驟工作流程參考並改寫自 Ian 的 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)，詳見 [`NOTICE.md`](NOTICE.md)。
- 不包含原專案的小黑 IP、範例圖片、複製提示詞或字型檔。
- 本專案與 Vox Media 無關；VOX-inspired 只描述一般解說新聞剪紙語法。
