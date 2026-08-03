# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 自動產生標題導向的文章精選圖片，以及最合適數量與位置的文內圖；全部使用同一套 VOX-inspired 羊皮紙剪紙解說視覺。

這個 Skill 適用於 Codex 與其他能執行 `SKILL.md` 的 Agent。它不固定輸出幾張圖，而是把整篇文章的觀看與理解體驗一起規劃。

## 會產生什麼

- 1 張直接回應文章標題的精選圖片。
- 0–6 張依文章長度、上下文與理解增益自動挑選的文內圖。
- 每張文內圖的精確插入位置。
- 直接帶有可讀解釋文字的 16:9 最終圖片。
- 精選圖與所有文內圖共用同一份 Visual Bible。

## 通過驗證的視覺系統

- 暖色 aged parchment、淡網格與輕微摺痕。
- 細緻雙線邊框與克制角飾。
- 上方置中 eyebrow、headline 與 subheadline。
- 中下方是一個有紙雕厚度的敘事場景。
- 2–4 個短標註卡與短引線。
- 可選底部結論旗帶與一句短但書。
- 人物可有可無；物件能說清楚時就不硬加人物。

文內圖必須延續精選圖的羊皮紙、邊框、標題階層、紙雕深度、陰影、色彩、標註卡與結論旗帶，不可降級成白底簡圖、左右文字面板、PPT 卡片或泛用向量圖。

## 精選圖片 Title Contract

產圖前先解析：

- `claim`：標題最主要的宣稱。
- `key_result`：最值得記住的結果、數字或改變。
- `mechanism`：造成結果的核心原因。

精選圖必須直接呈現 `claim`，並至少包含 `key_result` 或 `mechanism` 其中一項。

## 自動圖片數量

總數包含精選圖：

| 閱讀時間 | 圖片總數上限 |
|---|---:|
| 1 分鐘 | 1 |
| 2 分鐘 | 2 |
| 3–4 分鐘 | 3 |
| 5–6 分鐘 | 4 |
| 7–9 分鐘 | 5 |
| 10–12 分鐘 | 6 |
| 13 分鐘以上 | 7 |

最終數量：

```text
min(閱讀時間容量, 高價值且不重複的視覺錨點數)
```

不為了湊數量而硬配圖。兩張最好懂，就只做兩張。

## 自動插入位置

- 精選圖：文章標題後。
- 文內圖：對應概念第一次完整解釋的段落後。
- 兩張文內圖通常至少間隔兩個正文段落。
- 不在 FAQ、參考資料、作者資訊或純結論之後塞裝飾圖。

Manifest 會保存章節、全文段落索引、段落片段與放置理由。

## 安裝

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

本 repo 不附帶任何字型檔。

## 使用方式

### 只規劃

```text
Use $editorial-documentary-illustrations
分析文章，建立 Title Contract，自動決定最佳圖片總數與插入位置。
輸出 version 6 manifest，先不要生圖。

<文章內容>
```

### 直接生成完整配圖

```text
Use $editorial-documentary-illustrations
生成文章精選圖片與最合適數量的文內圖。
精選圖必須回應文章標題；每張文內圖都要使用精選圖作為風格參考，只解釋一個上下文核心。
圖中文字使用文章讀者語言，並完整檢查錯字、裁切、遮擋與跨圖一致性。

<文章內容>
```

### 連同 HTML Demo

```text
Use $editorial-documentary-illustrations
生成完整配圖與 HTML demo，依建議位置把精選圖和文內圖放回文章。
圖片數量與位置自動決定，以最佳觀看與理解體驗為優先。

<文章內容>
```

## 工具

```bash
python3 scripts/recommend_image_count.py \
  --reading-minutes 4 \
  --anchors 3 \
  --include-hero

python3 scripts/validate_manifest.py path/to/manifest.json

python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts
```

`annotate_images.py` 只作為直接生圖文字出錯時的備援修字／確定性排字工具；主流程先生成整合完成的最終圖片。

## Version 6

Version 6 新增：

- Title Contract
- 自動圖片數量
- 精確段落位置
- 視覺錨點評分
- 整合式圖中文字
- 精選圖到文內圖的風格連續性
- 1600 × 900 安全版面合約

完整格式請查看 [`templates/manifest.template.json`](templates/manifest.template.json) 與 [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json)。

## 設計原則

- 精選圖先回答標題，不拿次要小節代替。
- 每張文內圖只解釋一個上下文核心。
- 只有真的能提升理解時才插圖。
- 圖像和文字一起設計。
- 文內圖必須像精選圖的同一套專題。
- 文字與物件不得被遮擋、裁切或推出邊框。
- 人物不是必填元素。

## 出處與授權

- 採用 [MIT License](LICENSE)。
- 認知錨點、一圖一意、物理隱喻、短文字與 QA 迭代等一般工作流原則，參考並改寫自 Ian 的 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)，詳見 [`NOTICE.md`](NOTICE.md)。
- 本 repo 不包含小黑角色 IP、範例圖片、複製提示詞或字型檔。
- 本專案與 Vox Media 無關。請勿複製特定影片影格、logo、標題卡、字體或品牌資產。
