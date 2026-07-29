# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <strong>日本語</strong> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 記事の重要な判断、歴史的な流れ、因果関係、見えにくい仕組み、規模の変化を、一貫したスタイルと読みやすい注釈を備えた 16:9 の羊皮紙カットアウト挿絵へ変換します。

**Editorial Documentary Illustrations** は、Codex および `SKILL.md` ワークフローを実行できる AI Agent 向けのインストール可能な Skill です。記事を読み、視覚化する価値の高い箇所を選び、記事全体で共有する Visual Bible を作成し、文字なしのベース画像を生成した後、原文または対象読者に適した言語で校正済みの意味注釈を追加します。

## この Skill が解決する課題

長い画像生成プロンプトだけでは、次の問題が起こりがちです。

1. 同じ記事内でも画像ごとにスタイルが変わる。
2. 抽象概念が物語性のある場面ではなく、PPT の箱と矢印になる。
3. 見栄えは良くても、記事理解には役立たない。
4. 画像モデルに文字組みを任せると、誤字、偽の数値、読めない文字が生じる。
5. 注釈言語が固定され、原文や対象読者と一致しない。

本 Skill は、次の 5 層で安定性を高めます。

- **認知アンカー**：仕組み、対比、経路、ボトルネック、規模変化、結論を含む箇所だけを視覚化します。
- **Article Visual Bible**：羊皮紙、配色、カメラ、照明、人物比率、反復モチーフ、注釈スタイルを記事単位で固定します。
- **Immutable Style Lock**：すべてのベース画像プロンプトで同じ視覚制約を繰り返します。
- **言語対応注釈パイプライン**：まず文字なし画像を生成し、次に決定的な後処理で校正済みテキストを追加します。
- **QA と Retry Ladder**：ベース画像と最終注釈画像を別々に検査します。

## ワークフロー

```text
記事
  ↓
Article map と認知アンカー
  ↓
Article Visual Bible
  ↓
Version 3 shot manifest
  ↓
文字なし calibration frame
  ↓
スタイル参照を使った残りのベース画像
  ↓
注釈言語の決定と annotation plan
  ↓
紙タグ注釈の決定的レンダリング
  ↓
Base QA + Annotation QA
```

## 注釈言語の決定方法

次の優先順位で解決します。

1. ユーザーが明示した言語。
2. frontmatter、locale、`lang` などの記事メタデータ。
3. タイトル、リード、見出し、本文の主要言語。
4. 混在言語の記事では、説明本文の多数派言語。コード、URL、引用、参考文献、ブランド名、固有名詞は判定から除外します。
5. 記事が短すぎる、または判定不能な場合のみ、会話言語を使用します。

最終結果は `ja`、`en`、`zh-TW`、`ko`、`es` などの具体的な BCP 47 タグとして保存する必要があります。`auto` と `und` は最終設定で使用できません。`mul` は明示的な多言語記事の設定に限り、各画像には具体的な言語が必要です。

製品名、モデル名、ベンチマーク名、略語、バージョン、数値、単位、割合は、ユーザーが明示しない限り原文表記を維持します。

## デフォルト出力

- 16:9 横長の記事内挿絵。
- 通常は 1 記事につき 3〜7 枚、長文では最大 9 枚。
- 各完成画像に 1 つの判断見出しと 3〜6 個の短い注釈。
- 画像モデルは文字なしのベース画像のみを生成。
- コールアウト線とターゲット点を含む決定的な注釈レンダリング。
- `alt_text`、`caption`、画像内注釈は同じ対象言語を使用。
- ベース画像と完成画像を分離して保存：

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

## インストール

Codex Skills ディレクトリへコピーします。

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

注釈レンダリングの依存関係をインストールします。

```bash
python3 -m pip install -r requirements-annotation.txt
```

フォントファイルは同梱していません。レンダラーは `article.annotation_language` に基づいてローカルフォントを選択します。必要に応じて `--font` でローカルフォントを指定できます。

## 使用例

### 画像を生成せずに計画だけ作成

```text
Use $editorial-documentary-illustrations
以下の記事を分析し、5 枚のドキュメンタリー風カットアウト挿絵用 version 3 shot manifest を作成してください。まだ画像は生成しないでください。
記事の主要読者言語を自動判定し、その言語で各画像の判断見出し 1 件と短い注釈 3〜6 件を下書きしてください。

<記事本文>
```

### 注釈付き完成画像を生成

```text
Use $editorial-documentary-illustrations
以下の記事に対して、16:9 の羊皮紙カットアウト挿絵を 5 枚生成してください。
別の言語を指定しない限り、主要読者言語を自動判定してください。
最初に文字なし画像を生成し、実際の構図を確認してから、判断見出し 1 件と短い注釈 3〜6 件を追加してください。
各注釈は画面内の実物を指し、原文の固有名詞を維持し、事実と言語の校正を通過させてください。

<記事本文>
```

### 注釈言語を上書き

```text
Use $editorial-documentary-illustrations
原文は英語ですが、日本の読者向けです。注釈、alt text、caption は日本語にし、モデル名、略語、ベンチマーク名、数値は原文表記を維持してください。
```

### 正確に 10 秒の動画プロンプトを作成

```text
Use $editorial-documentary-illustrations
ショット 3 を exactly 10 seconds、24fps のドキュメンタリー風カットアウト動画プロンプトに変換してください。
ナレーションと文字オーバーレイは使用せず、環境音と連続した time-lapse シーンだけにしてください。
```

## 検証・プロンプト生成・注釈処理

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

ローカルフォントを指定する場合：

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/local-font.ttf \
  --force
```

## Version 3 manifest の要点

```json
{
  "version": 3,
  "article": {
    "title": "サンプル記事",
    "slug": "example-article",
    "language": "ja",
    "annotation_language": "ja",
    "summary": "記事の要約と中心的な主張。",
    "target_count": 5
  },
  "shots": [
    {
      "id": "01",
      "filename": "01-specialist-model.png",
      "alt_text": "専門モデルが主要作業を処理し、難しい案件だけが大型モデルへ分岐する。",
      "caption": "通常作業は効率的な経路に残し、難しい案件だけを上位モデルへ送る。",
      "annotation": {
        "enabled": true,
        "language": "ja",
        "layout_status": "draft",
        "headline": {
          "text": "通常作業は効率的な経路に残す",
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

完全な形式は [`templates/manifest.template.json`](templates/manifest.template.json) と [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json) を参照してください。

## リポジトリ構成

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

## 設計原則

- 1 枚の画像は 1 つの中心的な認知だけを伝える。
- 完成画像は装飾ではなく、記事理解を助ける必要がある。
- 画像モデルは視覚世界を作り、決定的な後処理が文字を担当する。
- 注釈言語は記事、または明示された対象読者に合わせる。
- 各注釈は画面内の見える対象を指し、認知的な価値を加える。
- ベース画像が正しく、注釈だけが誤っている場合は、画像を再生成せず annotation plan を修正する。
- ブランドスタイル名は説明上の近道であり、既存作品やブランド資産の複製許可ではない。

## クレジットとライセンス

- [MIT License](LICENSE) で公開しています。
- 多段階ワークフローは Ian の [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations) を参考に再設計しています。詳細は [`NOTICE.md`](NOTICE.md) を参照してください。
- 元プロジェクトの小黒キャラクター IP、サンプル画像、プロンプト全文、フォントファイルは含まれていません。
- 本プロジェクトは Vox Media とは無関係で、同社の承認や支援を受けたものではありません。特定の映像フレーム、ロゴ、タイトルカード、書体、ブランド素材を複製しないでください。
