# Article Visual Bible

## 為什麼需要

同篇文章最常見的失敗不是單張不好看，而是每張圖像不同專案。Visual Bible 是文章級別的鎖，所有底圖與最終標註圖都必須繼承它。

## 必填欄位

### `world_summary`

用 1–2 句描述整篇文章的視覺世界，不重述全文。

### `background`

固定：

- 羊皮紙主色。
- 網格／地圖線強度。
- 摺痕數量與方向。
- 是否有海岸線、街區、桌面邊界或空白地形。

### `palette`

4–7 個具名顏色與用途。例如：

- dark ink brown：輪廓與主要結構。
- terracotta：核心行動者。
- mustard ochre：主流程與移動路徑。
- sage：驗證、修補、安全結果。
- dusty indigo：對照組、基礎設施或次要系統。
- brick red：風險、攻擊、警告或升級案件。

同篇文章不得突然新增高飽和色。標註 accent 必須沿用同一色彩語意。

### `camera`

固定一種：

- `top-down-map-15deg`
- `flat-orthographic`
- `soft-isometric`

若沒有強理由，優先 `top-down-map-15deg`。

### `lighting`

固定光源方向、色溫、落影方向與長度。標籤紙片的陰影方向也必須相同。

### `character_system`

描述：

- 主角人物的剪紙比例。
- 臉部簡化程度。
- 服裝色。
- 群眾如何 cluster 化。
- 是否有特定職業辨識物，但避免複雜服裝。

### `recurring_motif`

全篇只選一個貫穿意象，例如：

- 一條赭黃色彎曲路徑。
- 一組逐漸增加的紙片證據。
- 一條紅線連接不同地點。
- 從小到大的圓形印章。
- 一個持續展開的攤位頂棚。

motif 可以改變位置與大小，但不能每張換新符號。

### `continuity_rules`

至少列出：

- 背景與色盤不變。
- 鏡頭不變。
- 人物比例不變。
- 陰影方向不變。
- 邊緣樣式不變。
- 底圖不含模型生成文字。
- recurring motif 必須出現或被合理延續。
- 最終標註使用相同紙片、字級階層、連線與色彩語意。

## Annotation Continuity

即使每張 label 的內容不同，下列項目不可任意改變：

- headline 與 label 的字級階層。
- 標籤紙片材質與不規則邊緣。
- 紙膠帶、accent 底線與 callout line 的樣式。
- callout line 粗細與 target dot 大小。
- 同一 accent 的概念用途。
- 使用的 CJK 字型或字型家族。
- 文字與主體之間的留白比例。

## Calibration Frame

第一張底圖要能同時測試：

- 紙張。
- 剪紙人物。
- 1 個主物件。
- 1 條路徑。
- 3–5 個顏色。
- 低至中密度。
- 至少 3 個可供後製標註的安靜區。

第一張底圖合格後：

- 支援 image reference：後續使用它做 style reference。
- 不支援 image reference：把 visual bible 與 style lock 原封不動重複在每張 prompt。

第一張不合格時不得繼續批量生成。

第一張標註圖完成後，也要作為後續標註排版的校準：字級、紙片厚度、陰影、accent 與線條風格都跟著它。

## 密度曲線

建議：

```text
low → medium → medium → high → resolved-medium
```

`high` 不代表畫 30 張清楚人臉，而是使用：

- 3–5 組群眾剪影。
- 前中後景分層。
- 重複形狀與色塊。
- 隊伍、餐桌、攤位或建築群的聚集。

高密度圖也必須留下可讀標註所需的空白，不可把整張塞滿。

## 每張可變與不可變

不可變：

- 紙張世界。
- 鏡頭。
- 光線。
- 剪紙邊緣與陰影。
- 人物比例。
- 色盤。
- recurring motif。
- 標註紙片、字級階層、連線與色彩語意。

可變：

- 主體。
- 路徑方向。
- 密度。
- 場景物件。
- 人物數量。
- 構圖類型。
- 文章段落的主色權重。
- 標註內容與具體位置。
