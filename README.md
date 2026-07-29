# Editorial Documentary Illustrations

> 把文章中的關鍵判斷、歷史過程、因果鏈、系統機制與規模變化，轉成穩定一致的 16:9 羊皮紙剪紙紀錄片配圖。

這是一個可安裝到 Codex／支援 `SKILL.md` 工作流之 AI Agent 的文章配圖 Skill。使用者可以用「VOX 風格」「紀錄片剪紙」「歷史地圖動畫」「文章文配圖」等語句觸發它，但套件對外採品牌中立名稱，並以具體視覺規則取代單純依賴品牌名稱。

## 它解決什麼問題

單一超長提示詞通常會出現四種漂移：

1. 同一篇文章的每張圖像是不同畫風。
2. 羊皮紙背景、剪紙邊緣、人物比例與陰影不一致。
3. 抽象段落被畫成 PPT 流程圖，而不是有敘事感的場景。
4. 圖片塞入太多文字、箭頭、人物與細節，導致錯字和畸形。

本 Skill 使用四層穩定機制：

- **文章認知錨點**：不平均配圖，只挑真正值得視覺化的段落。
- **Article Visual Bible**：一篇文章先建立一份固定的背景、色盤、人物、鏡頭、光影與重複意象。
- **Immutable Style Lock**：每張圖逐字重複同一段風格鎖定，不讓模型自行改寫。
- **QA + Retry Ladder**：先驗收校準圖，再生成後續圖；低於門檻就依問題類型重試。

## 預設輸出

- 16:9 橫式文章正文配圖。
- 一篇文章 3–7 張；長文最多 9 張。
- 圖內預設無文字、無標題、無 logo。
- 每張圖包含：建議插入位置、核心意思、構圖類型、畫面描述、動態暗示、檔名、繁中 alt text、可選 caption。
- 圖片保存到：

```text
assets/<article-slug>-editorial-documentary/
├── manifest.json
├── prompts/
├── images/
└── delivery.md
```

## 安裝

將整個資料夾複製到 Codex skills 目錄：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安裝後可這樣使用：

```text
Use $editorial-documentary-illustrations
分析下面文章，先產出 5 張 VOX 式紀錄片剪紙文配圖的 shot list，不要生圖。

<貼上文章>
```

直接生成：

```text
Use $editorial-documentary-illustrations
替下面文章生成 5 張 16:9 羊皮紙剪紙紀錄片正文配圖。
同篇文章必須共用相同色盤、人物語言、光線與地圖路徑意象。
圖內不要文字。

<貼上文章>
```

產出 10 秒動畫提示詞：

```text
Use $editorial-documentary-illustrations
把第 3 張配圖改寫成 exactly 10 seconds、24fps 的紀錄片剪紙動畫提示詞。
不要配音、不要字幕，只保留環境音與流暢 time-lapse。
```


## 驗證與編譯提示詞

套件附帶無外部依賴的 Python 工具。

先將 `templates/manifest.template.json` 複製成自己的 manifest 並填妥內容，再執行以下指令。

驗證 shot manifest：

```bash
python3 scripts/validate_manifest.py path/to/manifest.json
```

編譯靜態圖片提示詞：

```bash
python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts-still
```

編譯 10 秒動畫提示詞：

```bash
python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode motion \
  --output path/to/prompts-motion
```

## 目錄結構

```text
.
├── SKILL.md
├── README.md
├── LICENSE
├── NOTICE.md
├── agents/
│   └── openai.yaml
├── references/
├── schemas/
│   └── shot-manifest.schema.json
├── templates/
│   └── manifest.template.json
├── scripts/
│   ├── render_prompts.py
│   └── validate_manifest.py
├── templates/
│   └── manifest.template.json
├── tests/
│   └── test_tooling.py
└── third_party/
    └── ian-xiaohei-illustrations-LICENSE.txt
```

## 為什麼不用「exact VOX style」作為唯一提示

品牌名稱只是一個模糊捷徑，不同模型對它的理解不一致。這套 Skill 會把目標拆成可檢查的視覺 DNA：羊皮紙、淡網格、剪紙邊緣、貼紙陰影、俯視地圖鏡頭、簡化人物、路徑移動、自然土色、無文字與單一敘事焦點。

因此它仍能回應使用者口中的「VOX 風格」，但實際執行採用可重複、可驗收、可商業化管理的原創視覺規則。

## 授權與聲明

- 本套件採 MIT License。
- 工作流架構參考並改寫自 Ian 的 `ian-xiaohei-illustrations`，原專案同樣採 MIT License；詳見 `NOTICE.md` 與 `third_party/ian-xiaohei-illustrations-LICENSE.txt`。
- 本套件不包含原專案的小黑 IP 或範例圖片。
- 本套件與 Vox Media 無關，也不應宣稱為 Vox 官方產品。不得複製特定既有影片畫面、logo、字體或品牌資產。
