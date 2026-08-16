---
type: Document Template
title: スタンプカード (stamp_print.html)
description: チャレンジタスク用のA4横スタンプカード。31日分の記入欄とおこづかい計算欄を持ち、1ファイルに2部出力される。
tags: [output, print, a4-landscape]
resource: ./generator.md
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# スタンプカード (stamp_print.html)

[チャレンジタスク](./task-model.md) を載せる A4 横の記入用紙。
`build_stamp_print_html(challenge_tasks, prov)` が生成する。

## 構成

1 枚のシートは「ヘッダー」「メインテーブル」「計算セクション」の 3 ブロック。
**同一のシートを 2 回出力する**（`sheet() + sheet()`）ため、1 回の印刷で 2 部得られる。
1 枚目には `page-break-after: always`、最後のシートには `page-break-after: avoid` が効く。

### ヘッダー

タイトル「⭐ おてつだいスタンプカード」と、記入欄「なまえ」（30mm）「年」（13mm）「月」（9mm）。

### メインテーブル

固定 36 列（3 + 31 + 2）。

| 列 | CSS クラス | 幅 | 内容 |
| --- | --- | --- | --- |
| 1 | `col-task` | 36mm | おてつだい（タスク名＋備考） |
| 2 | `col-star` | 7mm | むず（難易度） |
| 3 | `col-price` | 10mm | 1かい（単価） |
| 4〜34 | `col-date` | 6.5mm × 31 | 日付 1〜31 のスタンプ欄 |
| 35 | `col-count` | 9mm | かい数 |
| 36 | `col-earn` | 12mm | ごうけい |

行は「タスク行 × タスク数」→「セクションラベル行」→「自由記入行 × 3」（`free_rows = 3`）。

> **改修時の注意（3 か所連動）**
> 列構成を変える場合、以下を必ず同時に修正すること。
> 1. `<colgroup>` 内の `<col>` 要素
> 2. `col.col-*` の CSS 幅指定
> 3. セクションラベル行の `colspan="{3 + len(dates) + 2}"`

列幅の合計は 275.5mm。印刷時のシート内幅は A4 横 297mm − 左右パディング 8mm × 2 = 281mm
なので収まる。一方**画面表示時は 263mm しかないため、ブラウザが圧縮して表示する**。
画面で列が詰まって見えるのは仕様どおりで、確認は印刷プレビューで行う。

### 計算セクション

- 左：タスクごとに「タスク名 / 単価円 × □ = □ 円」を 2 列グリッドで配置（自由記入 3 行を含む）
- 右：「🔒 かならずもらえる **500円**」（`FIXED_ALLOWANCE` 定数）、「⭐ おてつだい合計」、「合計」

## 印刷設定

`@media print` 内で `@page { size: A4 landscape; margin: 0 }`。
`.print-controls`（印刷ボタンと来歴注記）は印刷時に非表示になる。
