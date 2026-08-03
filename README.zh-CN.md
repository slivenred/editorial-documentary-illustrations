# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <strong>简体中文</strong> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 自动生成标题导向的文章精选图，以及数量和位置最合适的文内图；全部使用同一套 VOX-inspired 羊皮纸剪纸解说视觉。

## 核心能力

- 1 张直接回应文章标题的精选图。
- 0–6 张根据文章长度、上下文和理解增益自动选择的文内图。
- 每张文内图的准确插入位置。
- 带有可读解释文字的 16:9 最终图片。
- 精选图与文内图共享同一份 Visual Bible。

## 视觉系统

暖色旧羊皮纸、淡网格、双线边框、居中标题层级、立体纸雕场景、2–4 个短标注卡，以及可选的底部结论条。人物不是必需元素。

文内图必须延续精选图的羊皮纸、边框、标题、纸雕厚度、阴影、配色、标注卡和结论条，不得降级为白底草图、左右文字面板、PPT 或普通矢量图。

## 自动数量

总数包含精选图：1 分钟最多 1 张；2 分钟 2 张；3–4 分钟 3 张；5–6 分钟 4 张；7–9 分钟 5 张；10–12 分钟 6 张；13 分钟以上 7 张。

最终数量取阅读容量与高价值非重复视觉锚点数的较小值。

## 自动位置

精选图放在标题后；文内图放在对应概念第一次完整说明的段落后。两张文内图通常至少相隔两个正文段落，不在 FAQ、参考资料、作者信息或纯结论后添加装饰图。

## 使用

```text
Use $editorial-documentary-illustrations
为下面文章生成精选图和最合适数量的文内图。
精选图必须回应文章标题；每张文内图都沿用精选图的视觉系统，并只解释一个上下文核心。
自动决定数量和插入位置，检查文字、裁切、遮挡和跨图一致性。

<文章>
```

## 工具

```bash
python3 scripts/recommend_image_count.py --reading-minutes 4 --anchors 3 --include-hero
python3 scripts/validate_manifest.py path/to/manifest.json
python3 scripts/render_prompts.py path/to/manifest.json --mode still --output path/to/prompts
```

完整格式见 [`templates/manifest.template.json`](templates/manifest.template.json)。项目采用 [MIT License](LICENSE)，与 Vox Media 无关，也不包含 Ian 小黑角色或示例素材。
