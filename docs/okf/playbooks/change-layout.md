---
type: Playbook
title: レイアウトを変更する
description: 紙のデザインに手を入れるときの作業手順と、壊しやすい箇所。
tags: [playbook, development, layout]
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# レイアウトを変更する

## 作業の流れ

1. **サンプルモードで回す**（Notion の認証情報は不要）

   ```bash
   python generate.py --sample
   ```

2. **印刷プレビューで確認する**
   `output/` の HTML をブラウザで開き、**必ず印刷プレビュー**で見る。
   画面表示は下見であり、実際の紙とは一致しない
   （[スタンプカード](../output-stamp-card.md) の列幅の説明を参照）。

3. **1 と 2 を繰り返す**

4. コミットする前に、`output/` を含めていないことを確認する（`.gitignore` 済み）

## 壊しやすい箇所

### f-string の波括弧

CSS は f-string の中にある。**リテラルの `{` `}` は `{{` `}}` と二重にする。**
忘れると `KeyError` か、CSS が壊れた HTML が出る。

### スタンプカードの列（3 か所連動）

列構成を変えるときは以下を必ず同時に直す。

1. `<colgroup>` 内の `<col>` 要素
2. `col.col-*` の CSS 幅指定
3. セクションラベル行の `colspan="{3 + len(dates) + 2}"`

### HTML エスケープ

Notion 由来の値を新しく差し込むときは、**必ず `esc()` で包む**。
包み忘れると、タスク名に `<` を含めただけでマークアップが壊れる。

### アイコン規則の順序

`ICON_RULES` は上から順に評価される。かな表記が重なる語があるため、
**具体的な語を先に**置く（`くつした` は `くつ` より前、`テーブル` は `ふく` より前）。
詳細は [きほんポスター](../output-basic-poster.md)。

## よくある変更

| やりたいこと | 触る場所 |
| --- | --- |
| 「かならずもらえる」金額を変える | `FIXED_ALLOWANCE` 定数 |
| ポスターの色を増やす | `POSTER_COLORS` に CSS クラスを追加し、`.task-card.cN` の定義も足す |
| アイコンを追加・変更する | `ICON_RULES`（順序に注意）、`FALLBACK_ICONS` |
| 自由記入行の数を変える | `build_stamp_print_html()` 内の `free_rows` |
| 警告のしきい値を変える | `BASIC_TASK_LIMIT` / `CHALLENGE_TASK_LIMIT` |

## 注意

外部アセットを増やさないこと。生成物は GitHub Pages 上の静的ファイルとして
単体で成立している必要がある（外部参照は Google Fonts の 1 リンクのみ）。
