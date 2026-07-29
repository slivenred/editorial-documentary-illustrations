# Editorial Documentary Illustrations

> 把文章中的關鍵判斷、歷史過程、因果鏈、系統機制與規模變化，轉成穩定一致、帶有可讀認知標註的 16:9 羊皮紙剪紙紀錄片配圖。

這是一個可安裝到 Codex／支援 `SKILL.md` 工作流之 AI Agent 的文章配圖 Skill。使用者可以用「VOX 風格」「紀錄片剪紙」「歷史地圖動畫」「文章文配圖」等語句觸發它，但套件對外採品牌中立名稱，並以具體視覺與標註規則取代單純依賴品牌名稱。

## 它解決什麼問題

單一超長提示詞常見五種失敗：

1. 同一篇文章的每張圖像是不同畫風。
2. 羊皮紙背景、剪紙邊緣、人物比例與陰影不一致。
3. 抽象段落被畫成 PPT 流程圖，而不是有敘事感的場景。
4. 圖片只漂亮但不幫助理解文章。
5. 直接讓圖像模型寫繁中，容易錯字、亂碼、假數字或錯誤標示。

本 Skill 使用五層穩定機制：

- **文章認知錨點**：不平均配圖，只挑真正值得視覺化的段落。
- **Article Visual Bible**：先固定背景、色盤、人物、鏡頭、光影與重複意象。
- **Immutable Style Lock**：每張底圖逐字重複同一段風格鎖定。
- **Two-layer Annotation Pipeline**：先生成無字底圖，再用程式後製加入經校對的核心判斷與短標註。
- **QA + Retry Ladder**：分別驗收底圖與最終標註圖，低於門檻就依問題類型修正。

## 預設輸出

- 16:9 橫式文章正文配圖。
- 一篇文章 3–7 張；長文最多 9 張。
- 每張最終成品包含 1 個核心判斷與 3–6 個短標註。
- 圖像模型只負責無字底圖；繁中使用可控程式後製，避免模型錯字。
- 每張圖包含建議插入位置、核心意思、構圖類型、畫面描述、動態暗示、annotation plan、檔名、繁中 alt text 與可選 caption。
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

## 文字標註長什麼樣

每張圖的文字不是逐字摘要，也不是資訊圖表，而是：

- 一句能直接說出該段核心判斷的短標題。
- 3–6 個指向實際物件的短標註。
- 紙片標籤、手繪感連線、目標點與克制的色彩語意。
- 名稱、比例、數字與專有名詞必須和文章一致。
- 不使用「流程圖」「重點」「結果」等泛用標籤。

文字由 Agent 根據上下文撰寫，再以 Pillow 後製到圖片，不交給圖像模型猜字。

## 安裝

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

標註渲染需要 Pillow：

```bash
python3 -m pip install -r requirements-annotation.txt
```

套件不附帶任何字型檔。渲染器會嘗試尋找系統中的 PingFang TC、Microsoft JhengHei、Noto Sans CJK TC 或其他 CJK 字型，也可用 `--font` 指定本機字型。

## 使用方式

### 只規劃

```text
Use $editorial-documentary-illustrations
分析下面文章，先產出 5 張紀錄片剪紙文配圖的 version 2 shot manifest，不要生圖。
每張要包含一個核心判斷與 3–6 個繁中短標註草案。

<貼上文章>
```

### 直接生成完整成品

```text
Use $editorial-documentary-illustrations
替下面文章生成 5 張 16:9 羊皮紙剪紙正文配圖。
先生成無字底圖，再根據實際畫面加入繁中認知標註。
每張保留一個核心判斷與 3–6 個短標註，文字必須指向可見物件並經過校對。
同篇文章共用相同色盤、人物語言、光線、路徑意象與標註樣式。

<貼上文章>
```

### 10 秒動畫提示詞

```text
Use $editorial-documentary-illustrations
把第 3 張配圖改寫成 exactly 10 seconds、24fps 的紀錄片剪紙動畫提示詞。
不要配音、不要字幕，只保留環境音與流暢 time-lapse。
```

## 驗證、編譯與後製

驗證 manifest：

```bash
python3 scripts/validate_manifest.py path/to/manifest.json
```

編譯無字底圖 prompt 與 annotation plan：

```bash
python3 scripts/render_prompts.py \
  path/to/manifest.json \
  --mode still \
  --output path/to/prompts-still
```

把模型生成的底圖放在 `images/raw/`，確認並更新 annotation 座標後執行：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --force
```

需要指定字型時：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/your-cjk-font.ttc \
  --force
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
├── requirements-annotation.txt
├── agents/
│   └── openai.yaml
├── references/
│   ├── annotation-system.md
│   └── ...
├── schemas/
│   └── shot-manifest.schema.json
├── templates/
│   └── manifest.template.json
├── scripts/
│   ├── annotate_images.py
│   ├── render_prompts.py
│   └── validate_manifest.py
├── tests/
│   └── test_tooling.py
└── third_party/
    └── ian-xiaohei-illustrations-LICENSE.txt
```

## 為什麼不用圖像模型直接寫字

圖像模型適合建立場景、材質與視覺隱喻，但不是穩定的繁中排版器。這套 Skill 將兩件事拆開：

1. 圖像模型生成乾淨、可標註的視覺底圖。
2. Agent 讀文章、校對文字，再用確定性程式加入標籤。

因此既保留圖像模型的畫面品質，也能讓名稱、數字、階段與因果說法準確可讀。

## 為什麼不用「exact VOX style」作為唯一提示

品牌名稱只是一個模糊捷徑。這套 Skill 把目標拆成可檢查的視覺 DNA：羊皮紙、淡網格、剪紙邊緣、貼紙陰影、俯視地圖鏡頭、簡化人物、路徑移動、自然土色、單一敘事焦點，以及後製的短句認知標註。

## 授權與聲明

- 本套件採 MIT License。
- 工作流架構參考並改寫自 Ian 的 `ian-xiaohei-illustrations`，原專案同樣採 MIT License；詳見 `NOTICE.md` 與 `third_party/ian-xiaohei-illustrations-LICENSE.txt`。
- 本套件不包含原專案的小黑 IP、範例圖片或字型檔。
- 本套件與 Vox Media 無關，也不應宣稱為 Vox 官方產品。不得複製特定既有影片畫面、logo、字體或品牌資產。
