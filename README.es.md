# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <strong>Español</strong>
</p>

> Convierte los juicios clave, procesos históricos, cadenas causales, mecanismos ocultos y cambios de escala de un artículo en una serie coherente de ilustraciones recortadas sobre pergamino, en formato 16:9 y con anotaciones legibles.

**Editorial Documentary Illustrations** es una Skill instalable para Codex y otros agentes de IA capaces de seguir flujos de trabajo definidos en `SKILL.md`. Lee un artículo, selecciona los fragmentos que realmente se benefician de una explicación visual, crea una Visual Bible compartida, genera imágenes base sin texto y añade anotaciones semánticas revisadas en el idioma del artículo o del público objetivo.

## Qué problema resuelve

Un único prompt largo suele fallar de formas previsibles:

1. Las imágenes de un mismo artículo terminan con estilos diferentes.
2. Las ideas abstractas se convierten en diapositivas con cajas y flechas, no en escenas narrativas.
3. Las imágenes son atractivas, pero no ayudan a comprender el texto.
4. Pedir al modelo de imagen que componga texto produce errores ortográficos, cifras falsas o caracteres ilegibles.
5. Las anotaciones quedan fijadas a un idioma que no coincide con el artículo o con sus lectores.

La Skill utiliza cinco capas de estabilidad:

- **Anclas cognitivas**: solo visualiza pasajes con mecanismos, contrastes, recorridos, cuellos de botella, cambios de escala o conclusiones relevantes.
- **Article Visual Bible**: fija pergamino, paleta, cámara, iluminación, proporciones de personajes, motivo recurrente y estilo de anotación para todo el artículo.
- **Immutable Style Lock**: repite las mismas restricciones visuales en cada prompt de imagen base.
- **Flujo de anotación sensible al idioma**: primero genera una imagen sin texto y después añade etiquetas revisadas mediante posproducción determinista.
- **QA y Retry Ladder**: evalúa por separado las imágenes base y las imágenes anotadas finales.

## Flujo de trabajo

```text
Artículo
  ↓
Article map y anclas cognitivas
  ↓
Article Visual Bible
  ↓
Version 3 shot manifest
  ↓
Calibration frame sin texto
  ↓
Resto de imágenes base con referencia de estilo
  ↓
Resolución del idioma y annotation plan
  ↓
Renderizado determinista de etiquetas de papel
  ↓
Base QA + Annotation QA
```

## Cómo se decide el idioma de las anotaciones

La prioridad es la siguiente:

1. El idioma solicitado explícitamente por el usuario.
2. Metadatos del artículo: frontmatter, locale o `lang`.
3. El idioma dominante del título, introducción, encabezados y cuerpo principal.
4. En artículos multilingües, el idioma mayoritario del texto explicativo; se ignoran código, URL, citas, referencias, marcas y nombres propios.
5. El idioma de la conversación solo cuando el artículo es demasiado corto o ambiguo.

El resultado debe guardarse como una etiqueta BCP 47 concreta, por ejemplo `es`, `en`, `zh-TW`, `ja` o `ko`. Los valores sin resolver, como `auto` y `und`, no están permitidos. `mul` se reserva para una salida multilingüe explícita a nivel de artículo, pero cada imagen debe seguir usando un idioma concreto.

Los nombres de productos, modelos, benchmarks, siglas, versiones, números, unidades y porcentajes se conservan tal como aparecen en la fuente, salvo indicación expresa del usuario.

## Salida predeterminada

- Ilustraciones horizontales 16:9 para insertar dentro de artículos.
- Normalmente 3–7 imágenes por artículo; hasta 9 para contenidos largos.
- Un titular de idea y 3–6 llamadas semánticas breves por imagen final.
- El modelo de imagen genera únicamente la base sin texto.
- Las anotaciones se renderizan de forma determinista con líneas de llamada y puntos de destino.
- `alt_text`, `caption` y anotaciones usan el mismo idioma objetivo.
- Los recursos originales y finales se guardan por separado:

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

## Instalación

Copia el repositorio al directorio de Skills de Codex:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
```

Instala la dependencia de anotación:

```bash
python3 -m pip install -r requirements-annotation.txt
```

El repositorio no incluye archivos de fuentes. El renderizador selecciona una fuente local compatible según `article.annotation_language`, o permite indicar una ruta local mediante `--font`.

## Uso

### Planificar sin generar imágenes

```text
Use $editorial-documentary-illustrations
Analiza el artículo siguiente y crea un version 3 shot manifest para cinco ilustraciones documentales recortadas. No generes imágenes todavía.
Detecta automáticamente el idioma principal de los lectores y redacta en ese idioma un titular de idea y entre 3 y 6 llamadas breves para cada imagen.

<artículo>
```

### Generar el conjunto completo anotado

```text
Use $editorial-documentary-illustrations
Crea cinco ilustraciones horizontales 16:9 de recortes sobre pergamino para el artículo siguiente.
Detecta automáticamente el idioma principal de los lectores, salvo que especifique otro idioma objetivo.
Genera primero las imágenes base sin texto; después inspecciona la composición real y añade un titular de idea y entre 3 y 6 etiquetas semánticas breves.
Cada etiqueta debe apuntar a un objeto visible, conservar la terminología de la fuente y superar una revisión factual y lingüística.

<artículo>
```

### Cambiar el idioma de las anotaciones

```text
Use $editorial-documentary-illustrations
El artículo original está en inglés, pero las ilustraciones son para lectores hispanohablantes. Usa español para las anotaciones, el alt text y los captions. Conserva nombres de modelos, siglas, benchmarks y números en su forma original.
```

### Crear un prompt de animación de exactamente 10 segundos

```text
Use $editorial-documentary-illustrations
Convierte la imagen 3 en un prompt de animación documental recortada de exactly 10 seconds y 24fps.
Sin voz en off ni texto superpuesto. Usa únicamente sonido ambiente y una escena time-lapse continua.
```

## Validación, generación de prompts y anotación

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

Para indicar una fuente local:

```bash
python3 scripts/annotate_images.py \
  path/to/manifest.json \
  --input path/to/images/raw \
  --output path/to/images \
  --font /path/to/local-font.ttf \
  --force
```

## Elementos esenciales del manifest version 3

```json
{
  "version": 3,
  "article": {
    "title": "Artículo de ejemplo",
    "slug": "example-article",
    "language": "es",
    "annotation_language": "es",
    "summary": "Un resumen breve y el argumento central del artículo.",
    "target_count": 5
  },
  "shots": [
    {
      "id": "01",
      "filename": "01-specialist-model.png",
      "alt_text": "Un modelo especializado procesa la mayoría del trabajo y solo deriva los casos difíciles a un modelo mayor.",
      "caption": "Las tareas rutinarias permanecen en la ruta eficiente; solo los casos difíciles se escalan.",
      "annotation": {
        "enabled": true,
        "language": "es",
        "layout_status": "draft",
        "headline": {
          "text": "Mantén el trabajo rutinario en la ruta eficiente",
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

Consulta [`templates/manifest.template.json`](templates/manifest.template.json) y [`schemas/shot-manifest.schema.json`](schemas/shot-manifest.schema.json) para ver la estructura completa.

## Estructura del repositorio

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

## Principios de diseño

- Una imagen comunica una sola idea central.
- La imagen final debe explicar el artículo, no limitarse a decorarlo.
- El modelo de imagen crea el mundo visual; la posproducción determinista gestiona el texto.
- El idioma de las anotaciones sigue al artículo o a una audiencia definida explícitamente.
- Cada etiqueta debe apuntar a un objeto visible y aportar valor cognitivo.
- Si la imagen base es correcta y solo falla la anotación, se corrige el annotation plan sin volver a generar la imagen.
- Los nombres de estilos de marca son atajos descriptivos, no permisos para copiar composiciones o identidades existentes.

## Atribución y licencia

- Publicado bajo la [Licencia MIT](LICENSE).
- El flujo de trabajo por etapas está inspirado y adaptado a partir de [`ian-xiaohei-illustrations`](https://github.com/helloianneo/ian-xiaohei-illustrations) de Ian; consulta [`NOTICE.md`](NOTICE.md).
- Este repositorio no incluye el personaje Xiaohei original, imágenes de ejemplo, prompts copiados literalmente ni archivos de fuentes.
- Este proyecto no está afiliado, respaldado ni producido por Vox Media. No copies fotogramas, logotipos, tarjetas de título, tipografías ni recursos de marca específicos.
