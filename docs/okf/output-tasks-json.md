---
type: Dataset
title: タスクデータ (tasks.json)
description: 印刷用HTMLと同時に出力される機械可読なタスクデータ。GitHub Pages上で公開される。
tags: [output, data, machine-readable]
resource: ./generator.md
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# タスクデータ (tasks.json)

印刷用 HTML と同じ `output/` に出力される機械可読データ。HTML をスクレイピングせずに
中身を再利用できるようにするためのもの。`write_tasks_json()` が生成する。

## 構造

```json
{
  "generated_at": "2026-08-16T21:30:00+09:00",
  "source": "notion",
  "commit": "2160986",
  "counts": { "basic": 6, "challenge": 7 },
  "basic_tasks":     [{ "name": "...", "note": "..." }],
  "challenge_tasks": [{ "name": "...", "note": "...", "star": "★★", "price": 50 }]
}
```

| フィールド | 内容 |
| --- | --- |
| `generated_at` | 生成時刻（JST・ISO 8601） |
| `source` | `notion` または `sample` |
| `commit` | 生成元のコミット SHA（取得できなければ空文字） |
| `counts` | 種別ごとの件数 |
| `basic_tasks` / `challenge_tasks` | [タスクデータモデル](./task-model.md) と同じ形 |

`ensure_ascii=False` / `indent=2` で出力するため、日本語がそのまま読める。

## 含めないもの

**`NOTION_DATABASE_ID` は意図的に含めていない。** このファイルは GitHub Pages 上で
公開されるため、データベースの識別子を出さない方針とする
（[公開ポリシー](./publication-policy.md)）。

## 注意

このファイルには**実際の家庭のタスク内容がそのまま入る**。公開してよい範囲かどうかは、
Notion に何を書くかの段階で判断すること。
