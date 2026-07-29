# Retry Ladder

不要看到失敗就加更多形容詞。先判斷是哪一類問題，再採最小修正。

## 1. Style Reset

症狀：背景變寫實、剪紙感消失、色盤漂移、變成向量插畫或 3D。

```text
Regenerate from scratch. Preserve the shot's core idea, but reset the visual execution to the immutable style lock. Match the article visual bible exactly: warm parchment, faint map grid, hand-drawn paper cutouts, short soft shadows in the same direction, the locked earthy palette, and the locked top-down camera. Do not preserve the previous rendering style.
```

## 2. Prompt Compression

症狀：畫面太滿、焦點不明、多餘物件、忽略主要動作。

順序：

1. supporting elements 降到 3–5。
2. 人物數減半。
3. 次路徑全部刪除。
4. 只留一個動作。
5. 把 `high` 改為 `medium`。

```text
Simplify aggressively. Keep only the main subject, one core action, one route, and at most five supporting object types. Remove all decorative objects and secondary stories.
```

## 3. Anatomy Simplification

症狀：手指、手臂或群眾臉孔畸形。

```text
Replace detailed human gestures with simple paper-cutout silhouettes. Show the action through body direction, object position, route lines, and staggered poses. Do not show fingers or close-up hands. Convert distant people into layered crowd clusters.
```

## 4. De-PPT Rewrite

症狀：方框、節點、標題、箭頭很多，看起來像流程圖。

```text
Reinvent the composition as one physical documentary scene on parchment. Replace boxes and diagram arrows with a real paper-cutout setting such as a market, workbench, road, archive room, kitchen, port, or machine. Express flow through physical movement and routes. No labels.
```

## 5. Motion Clarification

症狀：靜態擺拍、沒有 time-lapse 感、路徑與角色無關。

```text
Freeze the scene at the decisive middle moment of a smooth time-lapse. Show partial assembly, staggered positions, a growing queue, converging routes, or repeated shapes that clearly reveal what has just happened and what is about to happen.
```

## 6. Continuity Restore

症狀：和前面圖片不像同篇文章。

```text
Match the calibration frame only for material, parchment tone, palette, cutout edge, shadow direction, camera angle, recurring character proportions, and recurring motif. Do not copy its composition. Rebuild this shot inside the same article world.
```

## 7. Composition Swap

同一修正策略重試 2 次仍失敗：

- 保留 `core_idea`。
- 換另一個 composition pattern。
- 重新決定主物件。
- 降低人物數與 supporting elements。
- 不再沿用失敗 prompt 的句子。

例：

- `route-network` 太像流程圖 → 改 `physical-metaphor`。
- `scale-up-crowd` 人物一直畸形 → 改成攤位、桌子、盤子與群眾 cluster 的 `ecosystem-tableau`。
- `cutaway-mechanism` 太技術 → 改成低科技工作台的 `process-station`。

## 8. Local Edit

只在主體與風格都正確、錯誤很局部時使用：

- 去文字。
- 修單一多餘物件。
- 清除一隻畸形手。
- 延伸羊皮紙邊緣以利裁切。

不要用局部編輯挽救整體構圖錯誤。
