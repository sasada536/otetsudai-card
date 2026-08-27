---
okf_version: "0.2"
---

# おてつだいカード自動生成 — ナレッジバンドル

Notion の「おてつだいタスク一覧」から、印刷用の紙（スタンプカード・ポスター）と
機械可読データを生成し、GitHub Pages で公開する仕組みについてのナレッジ。

このディレクトリは [Open Knowledge Format (OKF) v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
に従って構成している。各ファイルが 1 つの概念を表し、YAML frontmatter に構造化フィールド、
本文に説明を置く。人間が GitHub 上でそのまま読めると同時に、AI エージェントが
翻訳なしに読み取れることを意図している。

## 全体像

- [システム概要](./system.md) — 何を作る仕組みか、構成要素は何か

## 入力

- [Notion データベース](./notion-database.md) — 入力元のスキーマと採否ルール
- [タスクデータモデル](./task-model.md) — 変換後の内部表現とサンプルデータ

## 処理

- [生成スクリプト](./generator.md) — `generate.py` の 3 層構造と各関数

## 出力

- [スタンプカード](./output-stamp-card.md) — A4 横・チャレンジタスク用
- [きほんポスター](./output-basic-poster.md) — A4 縦・基本タスク用
- [タスクデータ (JSON)](./output-tasks-json.md) — 機械可読な出力

## 運用

- [公開ワークフロー](./publishing-workflow.md) — GitHub Actions と Pages
- [公開ポリシー](./publication-policy.md) — 公開してよいもの・いけないもの
- [手順書](playbooks/index.md) — 日常運用とトラブル対応

## 参照

- [既知の制約](./constraints.md) — 仕様上の限界と設計判断
- [用語集](./glossary.md)
- [更新履歴](./log.md)
