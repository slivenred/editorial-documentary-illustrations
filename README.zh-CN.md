# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>简体中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 根据文章长度与内容，自动选择最佳图片数量和插入位置，再生成符合上下文、带有整合式解释文字的 VOX-inspired 羊皮纸剪纸文内图。

每张最终图片采用固定信息层级：

```text
小标题 → 核心判断 → 一行补充 → 剪纸主视觉 → 2–4 张解释卡
```

Version 5 不再强迫无文字底图独自承载全部技术细节，也不再用大量散落标签拯救泛用 AI 图片。

## 自动图片数量

| 阅读时间 | 图片总数上限 |
|---|---:|
| 1–2 分钟 | 1 |
| 3–4 分钟 | 3 |
| 5–6 分钟 | 4 |
| 7–9 分钟 | 5 |
| 10–12 分钟 | 6 |
| 13–16 分钟 | 7 |
| 17 分钟以上 | 8 |

最终数量为阅读时间容量与高价值、非重复视觉锚点数量中的较小值。Hero 计入总数。

## 自动插入位置

- Hero 放在文章标题后。
- 文内图放在概念第一次完整解释的段落后。
- 两张文内图至少间隔两个正文段落。
- 不在 FAQ、参考资料或文章结尾硬塞图片。
- Manifest 保存章节、段落索引、真实段落片段与放置理由。

## 六种版式

`hero-explainer`、`mechanism-focus`、`process-strip`、`comparison-split`、`timeline-route`、`result-board`。

它们都遵循“上方结论、中间 VOX-inspired 剪纸场景、下方或侧边解释卡”的阅读顺序。

## 安装

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

## 使用

```text
Use $editorial-documentary-illustrations
分析文章，自动决定最佳图片数量与插入位置。
每张图直接对应所在段落，使用 VOX-inspired 羊皮纸剪纸场景，并加入一个 headline、一行 subheadline 与 2–4 张短解释卡。
不要固定生成 5 张。

<文章内容>
```

## 工具

```bash
python3 scripts/recommend_image_count.py --reading-minutes 4 --anchors 4 --sections 5 --include-hero
python3 scripts/validate_manifest.py path/to/manifest.json
python3 scripts/render_prompts.py path/to/manifest.json --mode still --output path/to/prompts
python3 scripts/annotate_images.py path/to/manifest.json --input path/to/images/raw --output path/to/images --force
```

完整格式请查看 [`templates/manifest.template.json`](templates/manifest.template.json)。

本项目采用 [MIT License](LICENSE)，与 Vox Media 无关，也不包含第三方字体或原始角色素材。
