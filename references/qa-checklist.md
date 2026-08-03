# QA Checklist

## A. 全篇規劃 QA

- 圖片總數符合閱讀時間與高價值錨點數。
- 精選圖計入總數。
- 沒有為每個小節平均配圖。
- 文內圖之間沒有高語意重複。
- 插入位置在概念完整解釋之後。
- 兩張文內圖通常至少間隔兩個正文段落。

## B. 精選圖 QA

硬性失敗：

- Headline 沒有直接回應文章標題主張。
- 沒有呈現 Title Contract 的 `claim`。
- `key_result`、`mechanism` 都沒有進入畫面。
- 圖片只解釋一個次要小節。
- 場景是泛用 AI 圖，換標題就能套到其他文章。

## C. 文內圖 QA

硬性失敗：

- 與對應段落無關。
- 和精選圖重複同一完整構圖。
- 看起來不像同一套專題。
- 降級成白底簡圖、左右文字面板、普通向量圖、PPT 或論文架構圖。
- 人物只是裝飾，或硬塞人物使畫面更亂。

## D. 風格與版面 QA

- 16:9。
- 暖色羊皮紙、淡網格、雙線邊框與角飾一致。
- 上方置中標題階層清楚。
- 主場景位於中下方，沒有超出邊框。
- 所有重要內容距離畫布邊緣至少約 72 px。
- 沒有文字、物件、路徑或旗幟被裁切。
- 標註卡沒有遮住核心物件。
- 引線短而無交叉。
- 縮至 600 px 寬仍看得懂 headline、主要數字與主場景。

## E. 文字 QA

- 所有字串和 manifest 完全一致。
- 沒有錯字、簡繁混用、亂碼或額外文字。
- Headline 是判斷，不是圖表類型。
- Subheadline 不重複 headline。
- Labels 為 2–4 個且有用。
- 數字、百分比、單位與模型名稱和文章一致。
- Caveat 只在必要時出現。

## F. 評分

- Title / context alignment：25
- Comprehension gain：20
- Scene clarity：15
- Cross-image continuity：15
- Text accuracy and hierarchy：10
- Safe layout：10
- Craft quality：5

交付門檻：

- 無硬性失敗。
- 總分至少 88。
- Title / context alignment 至少 22／25。
- Safe layout 至少 9／10。
