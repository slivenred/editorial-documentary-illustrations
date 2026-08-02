# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <strong>Español</strong>
</p>

> Elige automáticamente la cantidad y la posición óptimas de las imágenes según la longitud y el contenido del artículo, y genera escenas recortadas sobre pergamino, inspiradas en el periodismo visual, con texto explicativo integrado.

La jerarquía final es estable:

```text
antetítulo → conclusión → explicación breve → visual recortado → 2–4 tarjetas explicativas
```

La versión 5 evita dos extremos: obligar a una imagen sin texto a contener toda la precisión técnica, y rescatar una imagen genérica de IA con muchas etiquetas dispersas.

## Cantidad automática

| Tiempo de lectura | Máximo de imágenes |
|---|---:|
| 1–2 min | 1 |
| 3–4 min | 3 |
| 5–6 min | 4 |
| 7–9 min | 5 |
| 10–12 min | 6 |
| 13–16 min | 7 |
| 17+ min | 8 |

La cantidad final es el menor valor entre la capacidad por tiempo de lectura y el número de anclas visuales valiosas y no redundantes. La imagen hero cuenta dentro del total.

## Posición automática

- Hero: después del título.
- Imagen interna: después del párrafo que completa la primera explicación útil del concepto.
- Al menos dos párrafos entre imágenes internas.
- No añadir imágenes decorativas tras FAQ, referencias o al final del artículo.

## Seis diseños

`hero-explainer`, `mechanism-focus`, `process-strip`, `comparison-split`, `timeline-route`, `result-board`.

## Instalación

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
cp -R ./editorial-documentary-illustrations \
  "${CODEX_HOME:-$HOME/.codex}/skills/"
python3 -m pip install -r requirements-annotation.txt
```

## Uso

```text
Use $editorial-documentary-illustrations
Analiza el artículo y decide automáticamente la mejor cantidad y posición de imágenes.
Cada imagen debe corresponder directamente a su sección e incluir una escena de recortes sobre pergamino, un headline, un subheadline y entre 2 y 4 tarjetas explicativas.
No generes cinco imágenes por defecto.

<artículo>
```

## Comandos

```bash
python3 scripts/recommend_image_count.py --reading-minutes 4 --anchors 4 --sections 5 --include-hero
python3 scripts/validate_manifest.py path/to/manifest.json
python3 scripts/render_prompts.py path/to/manifest.json --mode still --output path/to/prompts
python3 scripts/annotate_images.py path/to/manifest.json --input path/to/images/raw --output path/to/images --force
```

Consulta [`templates/manifest.template.json`](templates/manifest.template.json) para ver el formato completo.

Publicado bajo MIT License y sin afiliación con Vox Media. No incluye fuentes de terceros ni recursos de personajes originales.
