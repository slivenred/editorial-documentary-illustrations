# Article Visual Bible

## 為什麼需要

同篇文章最常見的失敗不是單張不好看，而是每張圖像不同專案。Visual Bible 是文章級別的鎖，所有 shot 都必須繼承它，包括底圖風格與最終標註系統。

## 必填欄位

### `world_summary`

用 1–2 句描述整篇文章的視覺世界，不重述全文。

### `background`

固定羊皮紙主色、網格／地圖線強度、摺痕數量與方向，以及是否有海岸線、街區、桌面邊界或空白地形。

### `palette`

選 4–6 個具名顏色並指定用途。同篇文章不得突然加入高飽和色。

### `camera`

固定 `top-down-map-15deg`、`flat-orthographic` 或 `soft-isometric`。沒有強理由時優先 `top-down-map-15deg`。

### `lighting`

固定光源方向、色溫、落影方向與長度。

### `character_system`

固定人物剪紙比例、臉部簡化程度、服裝色、群眾 cluster 方式與職業辨識物。

### `recurring_motif`

全篇只選一個貫穿意象，例如赭黃色路徑、逐漸增加的證據紙片或一條連接不同地點的紅線。

### `annotation_language`

由 `article.annotation_language` 決定。必須是具體 BCP 47 tag，不得是 `auto`。同篇文章預設不切換語言；專有名詞與數字保留原文。

### `annotation_style`

固定標籤紙片、字級層級、accent 色語意、連線樣式、target dot、陰影方向與字型策略。字型來自本機，不隨 repo 分發。

### `continuity_rules`

至少包含：背景與色盤不變、鏡頭不變、人物比例不變、陰影方向不變、底圖無模型文字、recurring motif 延續、最終標註語言與樣式一致。

## Calibration Frame

第一張選擇能同時測試紙張、剪紙人物、一個主物件、一條路徑、3–5 個顏色、低至中密度與後製標註留白的 shot。

第一張合格後，支援 image reference 時用它鎖定材質、色盤、人物比例與陰影；不支援時，每張 prompt 原封不動重複 visual bible 與 style lock。

## 密度曲線

建議：`low → medium → medium → high → resolved-medium`。高密度使用群眾剪影、前中後景分層與重複形狀，不要求大量清楚臉孔。

## 每張可變與不可變

不可變：紙張世界、鏡頭、光線、剪紙邊緣、人物比例、色盤、recurring motif、annotation language、標籤紙片與色彩語意。

可變：主體、路徑方向、密度、場景物件、人物數量、構圖類型與各段落主色權重。
