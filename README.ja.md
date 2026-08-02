# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <strong>日本語</strong> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 記事の長さと内容から最適な画像数と挿入位置を自動で選び、文脈に合った VOX-inspired の羊皮紙カットアウト図解と説明文を生成します。

完成画像の情報階層は固定です。

```text
eyebrow → 結論見出し → 補足文 → カットアウト主視覚 → 2〜4 枚の説明カード
```

Version 5 は、文字なし画像だけにすべての技術情報を詰め込まず、汎用 AI 画像を大量のラベルで後付け説明する方法も避けます。

## 画像数の自動決定

| 読了時間 | 最大画像数 |
|---|---:|
| 1〜2 分 | 1 |
| 3〜4 分 | 3 |
| 5〜6 分 | 4 |
| 7〜9 分 | 5 |
| 10〜12 分 | 6 |
| 13〜16 分 | 7 |
| 17 分以上 | 8 |

最終枚数は、読了時間の容量と、重複しない高価値な視覚アンカー数の小さい方です。Hero も総数に含まれます。

## 挿入位置

- Hero は記事タイトルの直後。
- 本文画像は、概念が最初に十分説明された段落の後。
- 本文画像の間には少なくとも 2 段落を空ける。
- FAQ、参考文献、記事末尾に装飾目的で追加しない。

## 6 つのレイアウト

`hero-explainer`、`mechanism-focus`、`process-strip`、`comparison-split`、`timeline-route`、`result-board`。

## インストール

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

## 使用例

```text
Use $editorial-documentary-illustrations
記事を分析し、最適な画像数と挿入位置を自動で決めてください。
各画像は該当段落に直接対応し、VOX-inspired の羊皮紙カットアウト場面、見出し、補足文、2〜4 枚の説明カードを含めてください。
5 枚固定にはしないでください。

<記事本文>
```

## コマンド

```bash
python3 scripts/recommend_image_count.py --reading-minutes 4 --anchors 4 --sections 5 --include-hero
python3 scripts/validate_manifest.py path/to/manifest.json
python3 scripts/render_prompts.py path/to/manifest.json --mode still --output path/to/prompts
python3 scripts/annotate_images.py path/to/manifest.json --input path/to/images/raw --output path/to/images --force
```

完全な形式は [`templates/manifest.template.json`](templates/manifest.template.json) を参照してください。

MIT License で公開されており、Vox Media とは無関係です。第三者フォントや元キャラクター素材は含みません。
