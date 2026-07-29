# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <strong>한국어</strong> ·
  <a href="README.es.md">Español</a>
</p>

> 글의 핵심 판단, 역사적 흐름, 인과관계, 숨은 메커니즘, 규모 변화를 일관된 스타일과 읽기 쉬운 주석을 갖춘 16:9 양피지 컷아웃 본문 이미지로 변환합니다.

**Editorial Documentary Illustrations**는 Codex 및 `SKILL.md` 워크플로를 실행할 수 있는 AI Agent에 설치하는 Skill입니다. 글을 읽고 실제로 시각화할 가치가 있는 부분을 선택한 뒤, 글 전체가 공유하는 Visual Bible을 만들고 텍스트 없는 기본 이미지를 생성합니다. 이후 원문 또는 대상 독자에게 가장 적합한 언어로 검수된 의미 주석을 추가합니다.

## 이 Skill이 해결하는 문제

하나의 긴 이미지 프롬프트만으로 작업하면 다음 문제가 자주 발생합니다.

1. 같은 글의 이미지들이 서로 다른 스타일로 생성됩니다.
2. 추상적인 개념이 서사적 장면이 아니라 PPT 박스와 화살표로 바뀝니다.
3. 이미지는 예쁘지만 글을 이해하는 데 도움이 되지 않습니다.
4. 이미지 모델에 글자 배치를 맡기면 오탈자, 가짜 숫자, 읽을 수 없는 텍스트가 생깁니다.
5. 주석 언어가 하나로 고정되어 원문이나 대상 독자와 맞지 않습니다.

이 Skill은 다섯 단계로 안정성을 확보합니다.

- **인지 앵커**: 메커니즘, 대비, 경로, 병목, 규모 변화, 결론이 있는 문단만 시각화합니다.
- **Article Visual Bible**: 양피지, 색상, 카메라, 조명, 인물 비율, 반복 모티프, 주석 스타일을 글 단위로 고정합니다.
- **Immutable Style Lock**: 모든 기본 이미지 프롬프트에 동일한 시각 제약을 반복합니다.
- **언어 인식 주석 파이프라인**: 먼저 텍스트 없는 이미지를 만들고, 결정론적 후처리로 검수된 텍스트를 추가합니다.
- **QA 및 Retry Ladder**: 기본 이미지와 최종 주석 이미지를 별도로 검수합니다.

## 워크플로

```text
글
  ↓
Article map 및 인지 앵커
  ↓
Article Visual Bible
  ↓
Version 3 shot manifest
  ↓
텍스트 없는 calibration frame
  ↓
스타일 참조를 사용한 나머지 기본 이미지
  ↓
주석 언어 결정 및 annotation plan
  ↓
종이 태그 주석 렌더링
  ↓
Base QA + Annotation QA
```

## 주석 언어 결정 방식

다음 우선순위로 결정합니다.

1. 사용자가 명시한 언어.
2. frontmatter, locale, `lang` 등 글의 메타데이터.
3. 제목, 도입부, 소제목, 본문의 주된 언어.
4. 혼합 언어 글에서는 설명 본문의 다수 언어. 코드, URL, 인용문, 참고문헌, 브랜드명, 고유명사는 제외합니다.
5. 글이 너무 짧거나 판별할 수 없을 때만 현재 대화 언어를 사용합니다.

최종 값은 `ko`, `en`, `zh-TW`, `ja`, `es`와 같은 구체적인 BCP 47 태그여야 합니다. `auto`와 `und`는 최종 설정에서 허용되지 않습니다. `mul`은 명시적인 다국어 글 설정에만 사용하며, 각 이미지에는 여전히 구체적인 언어가 필요합니다.

제품명, 모델명, 벤치마크명, 약어, 버전, 숫자, 단위, 백분율은 사용자가 별도로 요청하지 않는 한 원문 표기를 유지합니다.

## 기본 출력

- 16:9 가로형 본문 이미지.
- 보통 글 하나당 3~7장, 긴 글은 최대 9장.
- 각 최종 이미지에 핵심 판단 1개와 짧은 주석 3~6개.
- 이미지 모델은 텍스트 없는 기본 이미지만 생성.
- 콜아웃 라인과 대상 점을 포함한 결정론적 주석 렌더링.
- `alt_text`, `caption`, 이미지 주석은 동일한 대상 언어 사용.
- 원본과 최종 이미지를 분리 저장:

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

## 설치

Codex Skills 디렉터리에 복사합니다.

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

주석 렌더링 의존성을 설치합니다.

```bash
python3 -m pip install -r requirements-annotation.txt
```

폰트 파일은 포함하지 않습니다. 렌더러는 `article.annotation_language`에 맞는 로컬 폰트를 선택하며, 필요하면 `--font`로 직접 지정할 수 있습니다.

## 사용 예시

### 이미지 생성 없이 계획만 작성

```text
Use $editorial-documentary-illustrations
아래 글을 분석하고 다큐멘터리 컷아웃 본문 이미지 5장을 위한 version 3 shot manifest를 작성해 주세요. 아직 이미지는 생성하지 마세요.
주요 독자 언어를 자동으로 판별하고, 그 언어로 각 이미지의 핵심 판단 1개와 짧은 주석 3~6개를 작성해 주세요.

<글 본문>
```

### 주석이 포함된 최종 세트 생성

```text
Use $editorial-documentary-illustrations
아래 글을 위해 16:9 양피지 컷아웃 본문 이미지 5장을 생성해 주세요.
다른 대상 언어를 지정하지 않으면 주요 독자 언어를 자동으로 판별해 주세요.
먼저 텍스트 없는 기본 이미지를 생성하고, 실제 구도를 확인한 뒤 핵심 판단 1개와 짧은 주석 3~6개를 추가해 주세요.
모든 주석은 화면에 보이는 대상을 가리키고, 원문의 고유 용어를 유지하며, 사실 및 언어 검수를 통과해야 합니다.

<글 본문>
```

### 주석 언어 변경

```text
Use $editorial-documentary-illustrations
원문은 영어지만 한국 독자를 위한 이미지입니다. 주석, alt text, caption은 한국어로 작성하고, 모델명, 약어, 벤치마크명, 숫자는 원문 표기를 유지해 주세요.
```

### 정확히 10초짜리 영상 프롬프트 생성

```text
Use $editorial-documentary-illustrations
3번 이미지를 exactly 10 seconds, 24fps 다큐멘터리 컷아웃 애니메이션 프롬프트로 변환해 주세요.
내레이션과 텍스트 오버레이는 사용하지 말고, 환경음과 하나의 연속된 time-lapse 장면만 사용해 주세요.
```

## 검증, 프롬프트 생성, 주석 처리

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

로컬 폰트를 지정하려면:

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/local-font.ttf \
  --force
```

## Version 3 manifest 핵심

```json
{
  "version": 3,
  "article": {
    "title": "예시 글",
    "slug": "example-article",
    "language": "ko",
    "annotation_language": "ko",
    "summary": "글의 짧은 요약과 핵심 주장입니다.",
    "target_count": 5
  },
  "shots": [
    {
      "id": "01",
      "filename": "01-specialist-model.png",
      "alt_text": "전문 모델이 대부분의 작업을 처리하고 어려운 사례만 대형 모델로 전달한다.",
      "caption": "일상적인 작업은 효율적인 경로에 남기고 어려운 사례만 상위 모델로 보낸다.",
      "annotation": {
        "enabled": true,
        "language": "ko",
        "layout_status": "draft",
        "headline": {
          "text": "일상 작업은 효율적인 경로에 남긴다",
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

전체 형식은 [`templates/manifest.template.json`](templates/manifest.template.json)과 [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json)을 참고하세요.

## 저장소 구조

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

## 설계 원칙

- 이미지 한 장은 하나의 핵심 인지만 전달합니다.
- 최종 이미지는 장식이 아니라 글의 이해를 도와야 합니다.
- 이미지 모델은 시각 세계를 만들고, 결정론적 후처리가 텍스트를 담당합니다.
- 주석 언어는 글 또는 명시된 대상 독자에 맞춥니다.
- 모든 주석은 보이는 대상을 가리키고 인지적 가치를 추가해야 합니다.
- 기본 이미지가 맞고 주석만 틀린 경우 이미지를 다시 생성하지 않고 annotation plan만 수정합니다.
- 브랜드 스타일 이름은 설명을 위한 축약일 뿐, 기존 화면이나 브랜드 자산을 복제할 수 있다는 뜻이 아닙니다.

## 출처 및 라이선스

- [MIT License](LICENSE)로 배포됩니다.
- 다단계 워크플로는 Ian의 [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations)를 참고해 재설계했습니다. 자세한 내용은 [`NOTICE.md`](NOTICE.md)를 확인하세요.
- 원 프로젝트의 Xiaohei 캐릭터 IP, 예시 이미지, 프롬프트 원문, 폰트 파일은 포함하지 않습니다.
- 본 프로젝트는 Vox Media와 관련이 없으며, 해당 회사의 승인이나 후원을 받지 않았습니다. 특정 영상 프레임, 로고, 타이틀 카드, 서체 또는 브랜드 자산을 복제하지 마세요.
