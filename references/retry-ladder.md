# Retry Ladder

不要看到失敗就加更多形容詞。先判斷是底圖問題還是標註問題，再採最小修正。

## A. 底圖修正

### 1. Style Reset

症狀：背景變寫實、剪紙感消失、色盤漂移、變成向量插畫或遊戲式 3D。

```text
Regenerate from scratch. Preserve the shot's core idea, but reset the visual execution to the immutable style lock. Match the article visual bible exactly: warm parchment, faint map grid, hand-drawn paper cutouts, short soft shadows in the same direction, the locked earthy palette, and the locked top-down camera. Do not preserve the previous rendering style.
```

### 2. Prompt Compression

症狀：畫面太滿、焦點不明、多餘物件、忽略主要動作、無處放標註。

順序：

1. supporting elements 降到 3–5。
2. 人物數減半。
3. 次路徑全部刪除。
4. 只留一個動作。
5. 把 `high` 改為 `medium`。
6. 明確保留 3–6 個安靜羊皮紙區。

```text
Simplify aggressively. Keep only the main subject, one core action, one route, and at most five supporting object types. Remove all decorative objects and secondary stories. Preserve several calm parchment pockets for later semantic annotations.
```

### 3. Anatomy Simplification

症狀：手指、手臂或群眾臉孔畸形。

```text
Replace detailed human gestures with simple paper-cutout silhouettes. Show the action through body direction, object position, route lines, and staggered poses. Do not show fingers or close-up hands. Convert distant people into layered crowd clusters.
```

### 4. De-PPT Rewrite

症狀：方框、節點、標題、箭頭很多，看起來像流程圖。

```text
Reinvent the composition as one physical documentary scene on parchment. Replace boxes and diagram arrows with a real paper-cutout setting such as a market, workbench, road, archive room, kitchen, port, or machine. Express flow through physical movement and routes. Do not render any text or placeholder labels in the base image.
```

### 5. Motion Clarification

症狀：靜態擺拍、沒有 time-lapse 感、路徑與角色無關。

```text
Freeze the scene at the decisive middle moment of a smooth time-lapse. Show partial assembly, staggered positions, a growing queue, converging routes, or repeated shapes that clearly reveal what has just happened and what is about to happen.
```

### 6. Continuity Restore

症狀：和前面圖片不像同篇文章。

```text
Match the calibration frame only for material, parchment tone, palette, cutout edge, shadow direction, camera angle, recurring character proportions, recurring motif, and empty-space rhythm. Do not copy its composition. Rebuild this shot inside the same article world.
```

### 7. Composition Swap

同一修正策略重試 2 次仍失敗：

- 保留 `core_idea`。
- 換另一個 composition pattern。
- 重新決定主物件。
- 降低人物數與 supporting elements。
- 不再沿用失敗 prompt 的句子。

例：

- `route-network` 太像流程圖 → 改 `physical-metaphor`。
- `scale-up-crowd` 人物一直畸形 → 改成物件與群眾 cluster 的 `ecosystem-tableau`。
- `cutaway-mechanism` 太技術 → 改成低科技工作台的 `process-station`。

### 8. Base Local Edit

只在主體與風格都正確、錯誤很局部時使用：

- 去除模型誤生的文字或符號。
- 修單一多餘物件。
- 清除一隻畸形手。
- 延伸羊皮紙邊緣以利裁切。

不要用局部編輯挽救整體構圖錯誤。

## B. 標註修正

底圖正確時，以下問題只改 annotation plan，不重生成底圖。

### 9. Semantic Rewrite

症狀：headline 太泛、labels 沒有文章價值、只是在命名物件。

處理：

1. 回到對應原文段落。
2. headline 改成判斷、對比、因果或限制。
3. 保留最有價值的名稱、數字與轉折。
4. 刪除 `流程`、`結果`、`重點` 等泛用詞。
5. 確認每個 label 都有可見 target。

### 10. Fact Correction

症狀：模型名稱、百分比、數字、單位、階段或繁簡字錯誤。

處理：

- 直接以原文與可信來源校對。
- 不修改視覺底圖。
- 重新渲染最終圖。
- 若底圖中的物件數量與正確數字矛盾，才回到 Base QA。

### 11. Collision and Occlusion Fix

症狀：文字遮住主體、人物、路徑或互相碰撞。

順序：

1. 移動 label 到較近的安靜區。
2. 縮短 callout line。
3. 改變 label angle 但維持 ±4° 內。
4. 刪除最低價值 label。
5. 最後才小幅降低字級；不要小於可讀門檻。

### 12. Callout Target Fix

症狀：線指錯物件、落在空白處、線條交叉過多。

處理：

- 重新查看底圖並更新 `target_x/target_y`。
- 每條線只指一個物件。
- 優先使用短直達路徑。
- 若 3 條以上互相交叉，改變標籤區域或減少 labels。

### 13. De-PPT Annotation Rewrite

症狀：標籤排列太整齊、像投影片或資訊圖表。

處理：

- headline 保留一個。
- labels 減到 3–5 個。
- 不使用等寬欄位、節點框、編號圓點或表格。
- 讓標籤靠近實際物件，保留輕微不規則角度。
- 場景仍要是主要內容，文字只是導讀層。

### 14. Mobile Readability Fix

症狀：桌面可讀，但縮到 360–420px 寬後看不清。

處理：

- 優先縮短文字，不是直接縮小字體。
- headline 保留，labels 減量。
- 把最重要 labels 移到高對比安靜區。
- 確保文字與紙片有足夠對比。
