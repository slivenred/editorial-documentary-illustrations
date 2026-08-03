# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <a href="README.zh-TW.md">繁體中文</a> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <strong>Español</strong>
</p>

> Genera una imagen destacada guiada por el título y el número óptimo de imágenes internas según la longitud, el contexto y la mejora real de comprensión, todo dentro de un mismo sistema editorial de recortes sobre pergamino.

## Capacidades

- Una imagen destacada que responde directamente al título.
- Entre 0 y 6 imágenes internas realmente necesarias.
- Posición exacta de inserción para cada imagen.
- Imágenes finales 16:9 con texto explicativo integrado.
- Una Visual Bible compartida entre la portada y las imágenes internas.

## Sistema visual

Pergamino cálido envejecido, cuadrícula tenue, borde doble, títulos centrados, escena tridimensional de papel, 2–4 etiquetas breves y una cinta de conclusión opcional. Las personas son opcionales.

Las imágenes internas deben conservar el color del pergamino, el borde, la jerarquía tipográfica, la profundidad del papel, las sombras, la paleta, las tarjetas y la cinta de la imagen destacada. No se convierten en bocetos blancos, paneles de texto, PPT o diagramas vectoriales genéricos.

## Cantidad y colocación automáticas

El total incluye la imagen destacada. Se usa el menor valor entre la capacidad según tiempo de lectura y el número de anclas visuales valiosas y no redundantes. Cada imagen interna se coloca después del párrafo donde el concepto queda explicado por primera vez.

## Uso

```text
Use $editorial-documentary-illustrations
Genera la imagen destacada y la cantidad óptima de imágenes internas para el artículo.
La imagen destacada debe responder al título. Cada imagen interna debe heredar el sistema visual de la portada y explicar un solo núcleo contextual.
Decide automáticamente cantidad y posición, y revisa texto, recortes, superposiciones y continuidad visual.

<artículo>
```

Consulta [`SKILL.md`](SKILL.md) y [`templates/manifest.template.json`](templates/manifest.template.json). MIT License. No está afiliado a Vox Media y no incluye el personaje Xiaohei ni recursos de Ian.
