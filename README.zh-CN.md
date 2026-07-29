# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>简体中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 将文章中的关键判断、历史过程、因果链、隐藏机制与规模变化，转化为风格一致、带有可读认知标注的 16:9 羊皮纸剪纸文内图。

**Editorial Documentary Illustrations** 是一个可安装到 Codex，以及其他能够遵循 `SKILL.md` 工作流的 AI Agent 的文章配图 Skill。它会读取文章、选择真正值得可视化的段落、建立整篇文章共享的 Visual Bible、生成无文字底图，最后根据原文或目标读者的语言加入经过校对的语义标注。

## 为什么需要这个 Skill

单一超长生图提示词经常出现以下问题：

1. 同一篇文章的图片风格不断漂移。
2. 抽象概念被画成 PPT 方框与箭头，而不是具有叙事感的实体场景。
3. 图片看起来漂亮，却不能帮助读者理解文章。
4. 直接要求图像模型排字，容易产生错字、乱码、虚假数字与错误标注。
5. 标注语言被固定成某一种语言，与原文或目标读者不一致。

本 Skill 使用五层稳定机制：

- **文章认知锚点**：不平均配图，只选择具有机制、对比、路径、瓶颈、规模变化或关键结论的段落。
- **Article Visual Bible**：固定整篇文章的羊皮纸、配色、镜头、光线、人物比例、重复意象与标注样式。
- **Immutable Style Lock**：每张底图都重复同一套不可变视觉限制。
- **语言感知标注流程**：先生成无文字底图，再通过确定性程序后期加入经过校对的文字。
- **QA 与 Retry Ladder**：分别验收无文字底图和最终标注图。

## 工作流程

```text
文章
  ↓
Article map 与认知锚点
  ↓
Article Visual Bible
  ↓
Version 3 shot manifest
  ↓
无文字 calibration frame
  ↓
使用风格参考生成其余无文字底图
  ↓
解析标注语言并建立 annotation plan
  ↓
通过程序渲染纸片标签
  ↓
Base QA + Annotation QA
```

## 标注语言如何决定

按照以下优先级解析：

1. 用户明确指定的标注语言。
2. 文章 frontmatter、locale、`lang` 或内容 metadata。
3. 标题、导语、章节标题与主要正文的主导语言。
4. 混合语言文章以多数解释性正文为准；忽略代码、网址、引文、参考资料、品牌名与专有名词。
5. 只有文章过短或无法判断时，才使用当前对话语言。

最终必须写入具体的 BCP 47 语言标签，例如 `zh-CN`、`zh-TW`、`en`、`ja`、`ko`、`es`。最终设置不得保留 `auto` 或 `und`；`mul` 只用于文章层明确的多语言输出，每张图片仍必须使用具体语言。

除非用户明确要求，产品名、模型名、benchmark、缩写、版本号、数字、百分比与单位均保留原文写法。

## 默认输出

- 16:9 横向文章文内图。
- 每篇文章通常 3–7 张，长文最多 9 张。
- 每张最终成品包含 1 个核心判断与 3–6 个短标注。
- 图像模型只生成无文字底图。
- 后期标注包含纸片、连线与 target dot，便于稳定校对和修改。
- `alt_text`、`caption` 与图内标注使用同一目标语言。
- 无文字原图与最终成品分开保存：

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

## 安装

将整个 repo 复制到 Codex Skills 目录：

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

安装标注依赖：

```bash
python3 -m pip install -r requirements-annotation.txt
```

本项目不附带任何字体文件。渲染器会根据 `article.annotation_language` 自动寻找匹配的本地字体，也可以通过 `--font` 指定本地字体。阿拉伯文、希伯来文与部分南亚文字建议使用支持 RAQM 的 Pillow 和相应字体。

## 使用方式

### 只规划，不生成图片

```text
Use $editorial-documentary-illustrations
分析下面的文章，建立 5 张纪录片剪纸文内图的 version 3 shot manifest，暂时不要生成图片。
自动判断文章的主要读者语言，并使用该语言为每张图编写一个核心判断与 3–6 个短标注草案。

<文章内容>
```

### 直接生成完整标注成品

```text
Use $editorial-documentary-illustrations
为下面的文章生成 5 张 16:9 羊皮纸剪纸文内图。
如果我没有另外指定，请自动判断文章的主要读者语言。
先生成无文字底图，再检查实际构图，加入一个核心判断与 3–6 个短标注。
每个标注都必须指向可见对象、保留原文专有名词，并通过事实与语言校对。

<文章内容>
```

### 指定不同标注语言

```text
Use $editorial-documentary-illustrations
文章原文是英文，但文内图面向中国大陆读者。图内标注、alt text 与 caption 请使用 zh-CN；模型名、缩写、benchmark 与数字保留原文。
```

### 生成正好 10 秒的动画提示词

```text
Use $editorial-documentary-illustrations
将第 3 张配图改写为 exactly 10 seconds、24fps 的纪录片剪纸动画提示词。
不要配音、不要图中文字，只保留环境音与一个连续的 time-lapse 场景。
```

## 验证、编译与后期处理

```bash
python3 scripts/validate_manifest.py path/to/manifest.json

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

指定本地字体：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/local-font.ttf \
  --force
```

## Version 3 manifest 要点

```json
{
  "version": 3,
  "article": {
    "title": "示例文章",
    "slug": "example-article",
    "language": "zh-CN",
    "annotation_language": "zh-CN",
    "summary": "文章的一句话摘要与主要论点。",
    "target_count": 5
  },
  "shots": [
    {
      "id": "01",
      "filename": "01-specialist-model.png",
      "alt_text": "专用模型处理主要工作，少数困难任务才升级到大型模型。",
      "caption": "常规任务保留在高效率路径，只有最困难任务才升级。",
      "annotation": {
        "enabled": true,
        "language": "zh-CN",
        "layout_status": "draft",
        "headline": {
          "text": "常规任务留在高效率路径",
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

完整格式请查看 [`templates/manifest.template.json`](templates/manifest.template.json) 与 [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json)。

## 项目结构

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
├── schemas/shot-manifest.schema.json
├── templates/manifest.template.json
├── scripts/
│   ├── annotate_images.py
│   ├── render_prompts.py
│   └── validate_manifest.py
└── tests/test_tooling.py
```

## 设计原则

- 一张图只表达一个核心认知。
- 最终图片必须帮助理解文章，而不只是装饰。
- 图像模型负责建立视觉世界，确定性程序负责文字。
- 标注语言跟随文章，或根据用户指定的目标读者调整。
- 每个标注都必须指向可见对象，并增加认知价值。
- 底图正确但文字错误时，只修改 annotation plan，不浪费生图额度。
- 品牌风格名称只能作为描述捷径，不代表可以复制现有画面或品牌识别。

## 来源与许可

- 本项目采用 [MIT License](LICENSE)。
- 多步骤工作流参考并改写自 Ian 的 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)，详见 [`NOTICE.md`](NOTICE.md)。
- 本 repo 不包含原项目的小黑 IP、示例图片、原始提示词全文或字体文件。
- 本项目与 Vox Media 无关，也未获得其背书。请勿复制特定影片画面、logo、标题卡、字体或品牌素材。
