---
type: Data Model
title: タスクデータモデル
description: Notionから変換された後の内部表現。基本タスクとチャレンジタスクの2種類がある。
tags: [model, schema]
resource: ../../data/sample_tasks.json
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# タスクデータモデル

[Notion データベース](./notion-database.md) から取り出した後、システム内部で扱う形。
[生成スクリプト](./generator.md) の HTML ビルダーはこの形だけに依存する。

## 基本タスク

毎日やる、報酬のないお手伝い。[きほんポスター](./output-basic-poster.md) に載る。

```python
{"name": str, "note": str}
```

## チャレンジタスク

回数に応じておこづかいが発生するお手伝い。[スタンプカード](./output-stamp-card.md) に載る。

```python
{"name": str, "note": str, "star": str, "price": int}
```

- `price` は `int()` で整数化されるため、小数は**切り捨て**られる
- `star` は空文字なら `"★"` にフォールバックする

## サンプルデータ

`data/sample_tasks.json` が同じ構造をそのまま保持する。Notion の認証情報がなくても
動作を再現できるようにするためのもので、**内容はすべて架空**。

```json
{
  "basic_tasks":     [{ "name": "...", "note": "..." }],
  "challenge_tasks": [{ "name": "...", "note": "...", "star": "★★", "price": 50 }]
}
```

`python generate.py --sample` で使われる。実在のタスクをここにコピーしてはいけない
（[公開ポリシー](./publication-policy.md)）。
