# Editorial Documentary Illustrations

<p align="center">
  <strong>English</strong> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> One self-contained Skill prompt that analyzes an article, generates a title-led featured image and the optimal number of contextual inline illustrations, validates them, and inserts them into the source content.

## Version 6: one-prompt SOP

[`SKILL.md`](SKILL.md) now contains the complete runtime workflow. Give the agent an article URL, source file, or full text and it will:

1. Resolve the title claim, result, mechanism, language, and reading time.
2. Select only high-value, non-redundant visual anchors.
3. Decide the optimal total image count and paragraph-level placements.
4. Generate the featured image first.
5. Use the approved featured image as a style reference for inline images.
6. Generate final 16:9 parchment paper-craft illustrations with integrated text.
7. Check spelling, clipping, overlap, overflow, context relevance, and visual continuity.
8. Insert the images into Markdown, MDX, or HTML.

The key change is prompt isolation: article analysis and QA stay in the agent layer, while each image model receives only exact text, one physical scene, a few required objects, one compact style lock, and safe-layout constraints.

## Usage

```text
Use $editorial-documentary-illustrations

Read the following article URL, source file, or text. Generate one title-led featured image and the optimal number of inline illustrations, validate them, and insert them at the best positions.

<article URL, file path, or article text>
```

## Approved references

The Skill first looks for:

```text
assets/style-reference/approved-featured.png
assets/style-reference/approved-mechanism.png
assets/style-reference/approved-comparison.png
```

`.jpg` and `.webp` are also accepted. If the files are unavailable, the Skill continues with its fixed compact Style Lock instead of stopping.

## License

MIT License. This project is not affiliated with Vox Media and does not include Ian Xiaohei character assets or example compositions.
