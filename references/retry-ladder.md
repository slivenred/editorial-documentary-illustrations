# Retry Ladder

## 1. Context Reset

症狀：圖片漂亮但像任何 AI 文章都能用。

修正：重寫 `visual_story`，只保留該段落中的人物、物件、機制與結果；刪除泛用科技裝飾。

## 2. Simplify Scene

症狀：畫面太技術、太滿或像論文架構圖。

修正：把關鍵物件降到 2–4 類，只呈現一個關係；把精確名稱、比例與數字移到解釋卡。

## 3. Layout Reset

症狀：文字遮住畫面或卡片太亂。

修正：換固定 layout，不手動散放標籤；優先使用 header + bottom cards 或 header + right cards。

## 4. Text Rewrite

症狀：文字像段落摘要、太長或沒有判斷。

修正：headline 改成一句結論；每張卡只保留名稱／數字和一句解釋。

## 5. Card Reduction

症狀：手機縮小後不可讀。

修正：由 4 張卡降為 3 張，再降為 2 張；不要縮小到難讀。

## 6. Style Restore

症狀：羊皮紙、剪紙、色盤、鏡頭或陰影漂移。

修正：使用 calibration frame 鎖材質，不複製構圖。

## 7. Image Merge

症狀：兩張圖內容相似。

修正：合併成一張更清楚的圖，降低整篇圖片總數。
