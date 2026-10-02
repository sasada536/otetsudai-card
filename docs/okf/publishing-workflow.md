---
type: Workflow
title: 公開ワークフロー (GitHub Actions)
description: 手動トリガでgenerate.pyを実行し、秘密情報チェックを通してからGitHub Pagesへ公開する。
tags: [ci, github-actions, github-pages, deployment]
resource: ../../.github/workflows/generate.yml
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# 公開ワークフロー (GitHub Actions)

## 設定

| 項目 | 内容 |
| --- | --- |
| ワークフロー名 | おてつだいカード生成 |
| トリガー | `workflow_dispatch`（手動）と `schedule`（定期実行） |
| 定期実行 | 毎月 1 日 09:00 JST（cron `0 0 1 * *`、UTC 表記）。GitHub 側の混雑で遅れることがある |
| ランナー | `ubuntu-latest` / Python 3.11 |
| 権限 | `contents: read` / `pages: write` / `id-token: write` |
| 同時実行制御 | `group: "pages"`、`cancel-in-progress: false` |

## ジョブ構成

**build**

1. チェックアウト（`actions/checkout@v7`）
2. Python 3.11 セットアップ（`actions/setup-python@v7`）
3. `python generate.py`（Secrets を環境変数に注入）
4. `python scripts/check_public_output.py` — **公開前の秘密情報チェック**
5. `output/` を `actions/upload-pages-artifact@v5` でアップロード

**deploy**（`needs: build`）

6. `actions/deploy-pages@v5` で GitHub Pages へ公開

使用する Action はすべて Node.js 24 ランタイムのメジャーバージョンにそろえている
（Node.js 20 は GitHub Actions で非推奨）。上げるときはこの表記も合わせて更新する。

## 定期実行が止まる条件

GitHub は、公開リポジトリで **60 日間コミットなどの活動がない**と、定期実行のワークフローを
自動で無効にする（事前にメールで通知が来る）。月 1 回の実行そのものは「活動」に数えられない
ため、コードを触らない月が続くと 2〜3 か月後に止まる。

止まったら Actions タブの「おてつだいカード生成」に出る「Enable workflow」を押せば再開する。
定期実行の失敗・停止は GitHub からメールで届くので、それを見落とさないことが前提になる。

## Pages の公開元設定

deploy ジョブは、リポジトリの Settings → Pages →「Build and deployment」の **Source が
「GitHub Actions」** になっていることを前提にしている。「Deploy from a branch」になっていると
build は成功するのに deploy だけが次のエラーで落ちる。

```
Failed to create deployment (status: 404) ... Ensure GitHub Pages has been enabled
```

対処は Source を「GitHub Actions」に戻して再実行するだけ。すでに「GitHub Actions」に
なっている場合は、一度別の値に切り替えてから戻すと直ることがある。

## 公開前チェック

手順 4 が失敗するとアップロードに進まない。検査対象は `output/` 配下の全テキストファイルで、
以下を検出したら `exit 1` する。

- `NOTION_TOKEN` / `NOTION_DATABASE_ID` の値そのもの（8 文字未満の値は誤検知防止のため無視）
- トークンらしき文字列（`ntn_` / `secret_` / `ghp_` / `gh[opsu]_` / `Bearer ...`）
- メールアドレス

意図は [公開ポリシー](./publication-policy.md) を参照。ローカルでも実行できる。

```bash
python generate.py --sample && python scripts/check_public_output.py
```

## 必要な Secrets

リポジトリの Actions Secrets に以下を設定しておく。

- `NOTION_TOKEN`
- `NOTION_DATABASE_ID`

これらをコードやドキュメントに書いてはいけない。
