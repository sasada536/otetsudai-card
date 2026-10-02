---
type: Playbook
title: カードを更新して印刷する
description: Notionを編集してから紙を印刷するまでの日常運用フロー。
tags: [playbook, operations, routine]
status: stable
generated:
  by: claude-code
  at: 2026-08-16T21:00:00+09:00
---

# カードを更新して印刷する

所要時間はおよそ 2 分。iPhone だけでも完結する。

## 手順

1. **Notion でタスクを編集する**
   「おてつだいタスク一覧」のタスク名・タイプ・難易度・単価・備考を変更する。
   スキーマは [Notion データベース](../notion-database.md) を参照。

2. **GitHub でワークフローを実行する**
   Actions タブ →「おてつだいカード生成」→「Run workflow」。
   iPhone の GitHub アプリからも実行できる。

3. **1 分ほど待つ**
   ジョブが緑になれば公開完了。赤で止まった場合は下の「失敗したとき」へ。

4. **URL を開いて印刷する**
   `https://<ユーザー名>.github.io/<リポジトリ名>/` を開き、目的の紙のリンクを選んで
   「印刷する」ボタンを押す。URL はブックマークしておくとよい。

   - スタンプカード → A4 **横**（1 回の印刷で 2 部出る）
   - きほんポスター → A4 **縦**

## 失敗したとき

ジョブのログを開き、エラーメッセージを確認する。build と deploy のどちらが赤いかも見る
（build が緑で deploy だけ赤なら、カード自体は生成できている）。

| メッセージ | 原因と対処 |
| --- | --- |
| `NOTION_TOKEN が無効か、期限切れです` | Secrets の `NOTION_TOKEN` を再設定する |
| `データベースが見つかりません` | `NOTION_DATABASE_ID` の確認、または Notion 側でインテグレーションを「コネクト」する |
| `レート制限に達しました` | しばらく待って再実行する |
| `公開前チェックに失敗しました` | 出力に秘密情報が混入している。[公開ポリシー](../publication-policy.md) を確認する |
| `警告: タスクが1件も取得できませんでした` | [タスクが出てこないときの対応](./troubleshoot-missing-task.md) へ |
| deploy ジョブが `Failed to create deployment (status: 404)` で失敗 | Settings → Pages の Source を「GitHub Actions」にして再実行する。詳細は [公開ワークフロー](../publishing-workflow.md#pages-の公開元設定) |

## 補足

- 生成物には生成日時とコミット SHA が入る。印刷した紙がいつ時点のものか分からなくなったら、
  画面で開いて上部の注記を見る
- 毎月 1 日の 9 時ごろに自動で生成・公開される。月初の時点で Notion の編集が済んでいれば
  手順 2・3 は不要で、URL を開いて印刷するだけでよい。月の途中で Notion を編集したときは
  手動で実行する
- 長期間コードに変更がないと定期実行が自動で止まる。再開方法は
  [公開ワークフロー](../publishing-workflow.md#定期実行が止まる条件) を参照
