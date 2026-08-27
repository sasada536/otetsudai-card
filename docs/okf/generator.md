---
type: Script
title: generate.py
description: Notion取得・ドメイン変換・HTML生成の3層からなる単一スクリプト。外部依存なし。
tags: [python, generator, core]
resource: ../../generate.py
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# generate.py

システムの本体。3 層構造になっており、上から順に「取得」「変換」「生成」。

## 実行方法

```bash
# 通常（Notionから取得）
NOTION_TOKEN=ntn_... NOTION_DATABASE_ID=<32桁> python generate.py

# サンプルデータで実行（認証情報不要）
python generate.py --sample
```

`--sample` は**明示的なオプトイン**である。環境変数が無いときに自動でサンプルへ
フォールバックはしない。自動フォールバックにすると、CI で Secrets の設定漏れが起きた際に
ジョブが成功してしまい、架空のデータが公開されてしまうため。

## 第1層：Notion 取得

`notion_query_database(database_id)` が全ページを取得する。仕様は
[Notion データベース](./notion-database.md) を参照。

プロパティ抽出ヘルパー:

| 関数 | 対象型 | 値が無いとき |
| --- | --- | --- |
| `get_prop_text` | title / rich_text | `""` |
| `get_prop_select` | select | `""` |
| `get_prop_number` | number | `0` |

### エラーハンドリング

HTTP エラーは `fail_with_api_error()` が受け取り、原因の見当がつくメッセージを stderr に
出して `exit 1` する。トレースバックは出さない。

| ステータス | ヒント |
| --- | --- |
| 401 | トークンが無効か期限切れ |
| 403 | 読み取り権限がない |
| 404 | DB ID が違う、またはインテグレーション未接続 |
| 429 | レート制限 |

接続自体に失敗した場合（`URLError`）も同様にメッセージを出して終了する。

## 第2層：ドメイン変換

`load_tasks()` が Notion のページ配列を [タスクデータモデル](./task-model.md) の
2 つのリストへ振り分ける。`load_sample_tasks()` は同じ形をサンプルファイルから読む。

### 件数の警告

`warn_on_task_counts()` が異常を検知して stderr に**警告**を出す（`exit` はしない）。

| 条件 | 警告 |
| --- | --- |
| 両方 0 件 | プロパティ名・選択肢名の変更を疑うよう促す |
| 片方だけ 0 件 | 該当の紙が空になる旨 |
| 基本 > `BASIC_TASK_LIMIT`（8） | A4 縦に収まらない可能性 |
| チャレンジ > `CHALLENGE_TASK_LIMIT`（14） | A4 横に収まらない可能性 |

### 来歴

`build_provenance(source)` が、生成時刻（JST）・データ源（`notion` / `sample`）・
コミット SHA を持つ辞書を返す。SHA は `GITHUB_SHA` を優先し、無ければ
`git rev-parse --short HEAD`、それも失敗すれば空文字。

## 第3層：HTML 生成

| 関数 | 出力 |
| --- | --- |
| `build_stamp_print_html(challenge_tasks, prov)` | [スタンプカード](./output-stamp-card.md) |
| `build_basic_poster_html(basic_tasks, prov)` | [きほんポスター](./output-basic-poster.md) |
| `write_tasks_json(...)` | [タスクデータ (JSON)](./output-tasks-json.md) |

ビルダーはタスクリストと来歴のみに依存する**純粋関数**で、ネットワークにも
ファイルシステムにもアクセスしない。REPL から直接呼び出して確認できる。

```python
import generate as g
html = g.build_basic_poster_html(
    [{"name": "くつをそろえる", "note": "げんかんで"}],
    g.build_provenance("sample"),
)
```

f-string 内に CSS を直接書いているため、**リテラルの波括弧は `{{` `}}` と二重にする**。

### HTML エスケープ

Notion 由来の文字列は、埋め込む直前に必ず `esc()` を通す
（`html.escape(str(value), quote=True)` の薄いラッパ）。対象は `name` / `note` / `star`。
`price` は `int` 化済みのため対象外。

> **改修時の注意**：新しい値を差し込むときは必ず `esc()` で包むこと。包み忘れると、
> タスク名に `<` を含めただけでマークアップが壊れる（修正済みの既知不具合）。

## 主な定数

| 定数 | 値 | 意味 |
| --- | --- | --- |
| `FIXED_ALLOWANCE` | `500` | スタンプカードの「かならずもらえる」金額（円） |
| `BASIC_TASK_LIMIT` | `8` | 基本タスクの警告しきい値 |
| `CHALLENGE_TASK_LIMIT` | `14` | チャレンジタスクの警告しきい値 |
| `SAMPLE_DATA_PATH` | `data/sample_tasks.json` | サンプルデータの場所 |
