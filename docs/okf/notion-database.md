---
type: Data Source
title: Notion データベース「おてつだいタスク一覧」
description: 本システムの唯一の入力元。日本語のプロパティ名がコードにハードコードされている。
tags: [input, notion, schema]
resource: https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# Notion データベース「おてつだいタスク一覧」

家庭で手入力・編集するタスクの一覧。**非公開**であり、閲覧には Integration Token が必要。
公開してよい範囲については [公開ポリシー](./publication-policy.md) を参照。

## 接続情報

| 項目 | 内容 |
| --- | --- |
| エンドポイント | `POST https://api.notion.com/v1/databases/{id}/query` |
| API バージョン | `Notion-Version: 2022-06-28`（固定） |
| 認証 | `Authorization: Bearer {NOTION_TOKEN}` |
| ページサイズ | 100（`has_more` / `next_cursor` でページング） |

必要な環境変数は 2 つ。いずれも未設定なら `exit 1` する。

| 変数名 | 内容 |
| --- | --- |
| `NOTION_TOKEN` | Internal Integration Secret（`ntn_` 始まり） |
| `NOTION_DATABASE_ID` | データベース ID（ハイフンなし 32 桁） |

## スキーマ

参照するプロパティは 5 つ。**プロパティ名（日本語）はコードにハードコードされている。**

| プロパティ名 | Notion 型 | 必須 | 用途 |
| --- | --- | --- | --- |
| `タスク名` | title / rich_text | ○ | タスクの名称 |
| `タイプ` | select | ○ | `基本` または `チャレンジ` |
| `難易度` | select | — | 星の表示（例 `★★`）。空なら `★` |
| `単価（円）` | number | — | 1 回あたりの金額。空なら `0` |
| `備考` | rich_text | — | 補足説明 |

`難易度` と `単価（円）` はチャレンジタスクでのみ使う。

## 行の採否ルール

| 条件 | 結果 |
| --- | --- |
| `タスク名` が空 | 破棄 |
| `タイプ` = `基本` | 基本タスクとして採用 |
| `タイプ` = `チャレンジ` | チャレンジタスクとして採用 |
| `タイプ` がそれ以外・空 | 破棄 |

**破棄は無言で行われる。** そのため Notion 側で列名や選択肢名を変更すると、エラーではなく
「出力が空になる」という形で現れる。0 件になった場合は警告が出る（[生成スクリプト](./generator.md)）。
調査手順は [タスクが出てこないときの対応](playbooks/troubleshoot-missing-task.md) を参照。

## 並び順

`sorts` を指定していないため、Notion 側のデフォルト順をそのまま使う。
この順序は出力の見た目には影響しない（色・アイコンはタスク名から決まるため）。
