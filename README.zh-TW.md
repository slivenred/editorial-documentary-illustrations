# Editorial Documentary Illustrations

<p align="center">
  <a href="README.md">English</a> ·
  <strong>繁體中文</strong> ·
  <a href="README.zh-CN.md">简体中文</a> ·
  <a href="README.ja.md">日本語</a> ·
  <a href="README.ko.md">한국어</a> ·
  <a href="README.es.md">Español</a>
</p>

> 一個 Skill Prompt，自動完成文章分析、標題導向精選圖、最佳數量文內圖、圖片 QA 與文章插入。

## Version 6：單一 Prompt SOP

`SKILL.md` 現在是一份完整、自足的單一提示詞。把文章網址、文章檔案或全文交給 Agent，即可完成：

1. 解析文章標題、摘要、核心機制、結果與限制。
2. 自動估算閱讀時間。
3. 自動決定精選圖與文內圖總數。
4. 找出最能提升理解的文內圖段落與插入位置。
5. 先生成標題導向精選圖，再以精選圖作為文內圖風格參考。
6. 使用 GPT Image 2 或可用的最高品質圖片工具實際生圖。
7. 檢查錯字、簡繁混用、裁切、遮擋、越界與跨圖一致性。
8. 將圖片自動插入 Markdown、MDX 或 HTML。

## 為什麼改成一個 Prompt

先前版本將大量分析、Visual Bible、QA 與負面限制重複塞進圖片 Prompt，容易造成 overprompt interference。新版把複雜分析留在 Agent 層，真正交給圖片模型的單張 Prompt 只保留：

- 圖片用途。
- 精確文字。
- 一個物理場景。
- 2–6 個必要物件。
- 一段固定精簡 Style Lock。
- 不得新增文字、遮擋或裁切的要求。

## 使用方式

```text
Use $editorial-documentary-illustrations

讀取下面的文章網址或文章檔案，自動生成一張精選圖片與最合適數量的文內圖。
完成圖片 QA，並把圖片插入原文章最適合的位置。

<文章網址、檔案路徑或全文>
```

完整執行規範位於 [`SKILL.md`](SKILL.md)。

## 核准風格參考圖

Skill 會優先讀取：

```text
assets/style-reference/approved-featured.png
assets/style-reference/approved-mechanism.png
assets/style-reference/approved-comparison.png
```

亦接受 `.jpg` 或 `.webp`。若檔案不存在但對話中附有三張參考圖，Agent 會保存後使用；若完全沒有參考圖，則依固定 Style Lock 繼續，不中斷工作。

## 授權

採用 [MIT License](LICENSE)。本專案與 Vox Media 無關，也不包含 Ian Xiaohei 的角色 IP 或範例素材。
