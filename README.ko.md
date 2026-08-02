# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>한국어</strong> ·
  <a href="README.es.md">Español</a>
</p>

> 글의 길이와 내용을 바탕으로 최적의 이미지 수와 삽입 위치를 자동으로 정하고, 문맥에 맞는 VOX-inspired 양피지 컷아웃 장면과 설명 텍스트를 생성합니다.

완성 이미지의 정보 순서는 다음과 같습니다.

```text
eyebrow → 핵심 판단 → 한 줄 설명 → 컷아웃 주 시각 → 2~4개 설명 카드
```

Version 5는 텍스트 없는 이미지에 모든 기술 세부 정보를 억지로 넣지 않으며, 범용 AI 이미지를 많은 라벨로 사후 설명하는 방식도 피합니다.

## 이미지 수 자동 결정

| 읽기 시간 | 최대 이미지 수 |
|---|---:|
| 1~2분 | 1 |
| 3~4분 | 3 |
| 5~6분 | 4 |
| 7~9분 | 5 |
| 10~12분 | 6 |
| 13~16분 | 7 |
| 17분 이상 | 8 |

최종 수량은 읽기 시간 용량과 중복되지 않는 고가치 시각 앵커 수 중 작은 값입니다. Hero도 총수에 포함됩니다.

## 자동 배치

- Hero는 글 제목 뒤에 배치합니다.
- 본문 이미지는 개념이 처음 충분히 설명된 문단 뒤에 배치합니다.
- 본문 이미지 사이에는 최소 두 문단을 둡니다.
- FAQ, 참고문헌, 글 끝에 장식용으로 억지 삽입하지 않습니다.

## 6가지 레이아웃

`hero-explainer`, `mechanism-focus`, `process-strip`, `comparison-split`, `timeline-route`, `result-board`.

## 설치

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

## 사용

```text
Use $editorial-documentary-illustrations
글을 분석하고 최적의 이미지 수와 삽입 위치를 자동으로 결정해 주세요.
각 이미지는 해당 문단과 직접 연결된 VOX-inspired 양피지 컷아웃 장면, headline, subheadline, 2~4개의 설명 카드를 포함해야 합니다.
5장으로 고정하지 마세요.

<글 본문>
```

## 명령

```bash
python3 scripts/recommend_image_count.py --reading-minutes 4 --anchors 4 --sections 5 --include-hero
python3 scripts/validate_manifest.py path/to/manifest.json
python3 scripts/render_prompts.py path/to/manifest.json --mode still --output path/to/prompts
python3 scripts/annotate_images.py path/to/manifest.json --input path/to/images/raw --output path/to/images --force
```

전체 형식은 [`templates/manifest.template.json`](templates/manifest.template.json)을 참고하세요.

MIT License로 배포되며 Vox Media와 관련이 없습니다. 타사 폰트나 원본 캐릭터 소재는 포함하지 않습니다.
