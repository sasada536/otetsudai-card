---
type: System
title: おてつだいカード自動生成
description: Notionのタスク一覧から印刷用HTMLと機械可読データを生成し、GitHub Pagesで公開する静的サイトジェネレータ。
tags: [overview, static-site, notion, github-pages]
resource: https://github.com/sasada536/otetsudai-card
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# システム概要

## 目的

家庭内の「おてつだい制度」を運用するため、Notion 上で管理しているタスク一覧から
**印刷して壁に貼る／記入する紙**を自動生成する。Notion を編集するだけで紙が更新される
状態を作り、手作業でのレイアウト修正を不要にすることが目的。

## データの流れ

```
Notion DB（非公開）
   │ Notion API
   ▼
generate.py（Python 3.11 / 標準ライブラリのみ）
   │
   ▼
output/（HTML 3ファイル + tasks.json）
   │ GitHub Actions
   ▼
GitHub Pages（公開）→ ブラウザで開いて印刷
```

詳細は [Notion データベース](./notion-database.md)、[生成スクリプト](./generator.md)、
[公開ワークフロー](./publishing-workflow.md) を参照。

## 構成要素

| パス | 役割 |
| --- | --- |
| `generate.py` | 取得・変換・生成のすべて |
| `scripts/check_public_output.py` | 公開前の秘密情報チェック |
| `data/sample_tasks.json` | 認証情報なしで動かすためのサンプル（架空の内容） |
| `.github/workflows/generate.yml` | 実行と Pages への公開 |
| `docs/okf/` | 本ナレッジバンドル |

## 設計上の性質

- **依存ゼロ** — Python 標準ライブラリのみ。`pip install` を必要としない
- **完全自己完結の出力** — CSS はインライン。外部参照は Google Fonts の 1 リンクのみ
- **印刷が主・画面は下見** — 寸法は `mm` / `pt` 指定。画面表示は確認用
- **ビルド・テストなし** — `--sample` での手動確認が唯一の検証手段

## ライセンス

| 対象 | ライセンス |
| --- | --- |
| コード（`generate.py`、`scripts/`、ワークフロー） | MIT License |
| ドキュメント（`README.md`、`docs/`） | CC BY 4.0 |

生成された HTML・JSON の著作権は、それを生成した主体（入力データの持ち主）に帰属する。
リポジトリのライセンスは生成物の内容には及ばない。
