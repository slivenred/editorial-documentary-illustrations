# Prompt Assembly (v5 — lean)

## 原則

**Lean prompt，豐富場景。** 圖中文字與主場景一起生成，但提示詞必須**短而啟發式**：一段豐富、有觸感、會說故事的場景描述 + 精確文字清單 + 一行濃縮風格。不要把所有安全/版面/材質限制預先倒進 prompt——過度約束會讓模型產出**安全但平面、圖表化**的圖（v4 的 ~1,100 字 prompt 即如此）；精簡 prompt 讓模型有空間渲染**豐富、有深度、紙雕敘事場景**（已實驗驗證）。

實測對比（同一模型）：1,100 字 prompt → 圖表化（色塊、輸送帶、堆疊）；334 字 prompt → 豐富 3D 場景（機器、路徑、旗子、寫實紋理）。

## Prompt 順序（5 段，~300-350 字）

1. 一句開場：16:9、暖色羊皮紙、淡網格、雙線邊框、角飾。
2. Context：精選圖 Title Contract（claim/key_result/mechanism）或文內圖 Article Context（section/core_idea ＋ 以精選圖為 style reference）。
3. 主場景：manifest 的 `scene` 段落（豐富敘事）＋ 一句輕材質提示（紙雕、無金屬/玻璃/螢幕）。
4. 精確文字清單（逐字，不加其他文字）：eyebrow/headline/subheadline/labels/bottom_takeaway/caveat。
5. 一行濃縮風格：色盤（含概念對應，如 terracotta=KDA）＋ 標題階層位置 ＋ 光線 ＋ 安全邊界（outer_margin_px）。

## 精選圖 Prompt 範本

```text
Create one original 16:9 featured / hero editorial illustration on warm aged parchment
with a faint grid, a fine double-line ink border, and small corner ornaments.

TITLE CONTRACT
Claim: {claim}
Key result: {key_result}
Mechanism: {mechanism}
The featured image must visibly answer the article title.

{scene} Build it as a dimensional handcrafted paper-craft tableau — layered cardstock,
parchment, corrugated paper and balsa wood with ink detailing and soft paper shadows;
no metal, no glass, no screens, no robot silhouettes.

{EXACT TEXT — RENDER VERBATIM AND ADD NO OTHER TEXT}

STYLE
Palette: {palette}. A centered editorial title hierarchy (small eyebrow, large headline,
concise subheadline) sits at the top; the paper-craft tableau occupies the middle and
lower canvas; an optional bottom takeaway ribbon closes the composition. Soft warm
upper-left light with short consistent lower-right shadows. Keep every word and object
fully inside the border with at least {outer_margin_px}px of clear margin.
```

## 文內圖 Prompt 範本

```text
Create one original 16:9 inline article editorial illustration on warm aged parchment ...

ARTICLE CONTEXT
Section: {section_heading}
Core idea: {core_idea}
Use the approved featured image only as a style reference. Match its parchment tone,
fine double-line border, corner ornaments, centered title hierarchy, paper-crafted
depth, shadow direction, and accent colors. Do not copy its composition.

{scene} Build it as a dimensional handcrafted paper-craft tableau ...

{EXACT TEXT — RENDER VERBATIM AND ADD NO OTHER TEXT}

STYLE
Palette: {palette}. ...
```

## 寫 scene 段落的要點（lean 下，scene 是品質樞紐）

- **描述你要的，而非禁你要的**：用正向、具體、有觸感的詞描述物件與動作（「三道低矮的紙雕閘板，token 卡片從細縫穿過」），優於負向約束（「不要畫成門」）。必要時一句輕材質提示即可。
- **會說故事的物理場景**：機器、路徑、推車、旗子、堆疊、轉化——讓物件互動、有深度、有紋理，而非抽象色塊。
- **避免 1,100 字的 v4 習慣**：不要倒 MATERIAL LOCK / VERTICAL COMPOSITION BANDS / GLYPH CLAMP / LAYOUT 條列 / SELF-CHECK。這些是 v4 的過度工程，會把模型推向圖表化。

## 修字 Prompt（文字錯才用，不重產場景）

```text
Edit the provided image without changing the composition, paper-craft objects, colors,
border, or lighting. Replace only the incorrect text "{wrong}" with the exact text
"{correct}". Keep every other pixel and every other string unchanged.
```

## 美學生成 vs 文字修復（預設工作流）

1. 用 lean prompt 生成豐富場景（信任模型）。
2. 只在「某個字串錯」時，用修字 prompt 做針對性編輯——**不要**為了防字錯而預載一堆文字安全限制（那正是 v4 過度約束的成因）。
3. 只在「場景與上下文不符」時，才重產整張場景。
