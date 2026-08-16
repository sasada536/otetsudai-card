---
type: Reference
title: 用語集
description: 本プロジェクト内で使う日本語の用語と、その意味。
tags: [glossary, terminology]
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# 用語集

| 用語 | 意味 |
| --- | --- |
| 基本タスク | 毎日やる、報酬のないお手伝い。[きほんポスター](./output-basic-poster.md) に載る |
| チャレンジタスク | 回数に応じておこづかいが発生するお手伝い。[スタンプカード](./output-stamp-card.md) に載る |
| じゆうきにゅう | スタンプカードの空欄行。家庭で任意のタスクを手書きする |
| シート | スタンプカードの 1 ページ分。1 ファイルに 2 枚出力される |
| かならずもらえる | タスクの達成状況によらず支給される固定額（`FIXED_ALLOWANCE`、初期値 500 円） |
| サンプルモード | `--sample` を付けた実行。Notion に接続せず架空データで動かす |
| 来歴 / provenance | 生成物に埋め込む「いつ・何から・どのコミットで作られたか」の情報 |
| OKF | Open Knowledge Format。Google Cloud が 2026 年 6 月に公開した、組織のナレッジを YAML frontmatter 付き Markdown で表現するオープン仕様 |

## 文体の方針

出力される文字列・Notion のプロパティ名・コメント・ドキュメントはすべて日本語。
紙に載る文言は子どもが読む前提で、かな多めにする。
