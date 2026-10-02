# 更新履歴

## 2026-10-02

- 毎月 1 日 09:00 JST の定期実行を有効にした。60 日間活動がないと GitHub が定期実行を
  止める点と再開方法を [公開ワークフロー](./publishing-workflow.md) と README に記載

- [公開ワークフロー](./publishing-workflow.md) で使う Action を Node.js 24 対応版に更新
  （checkout v7 / setup-python v7 / upload-pages-artifact v5 / deploy-pages v5）。
  Node.js 20 非推奨の警告への対応
- Pages の Source が「GitHub Actions」から外れて deploy が 404 で落ちた件を受け、
  対処を [公開ワークフロー](./publishing-workflow.md)、
  [カードを更新して印刷する](./playbooks/run-generation.md)、README に追記

## 2026-08-30

- 実データ 14 件で、iPhone（Safari）と PC の両方で計算欄の改ページを確認。
  [スタンプカード](./output-stamp-card.md) の「Safari 未検証」の記述を更新した

## 2026-08-27

- チャレンジタスクが多いとき、[スタンプカード](./output-stamp-card.md) の計算欄を
  2 ページ目に送るようにした。12 件以下なら従来どおり 1 ページ
- 収まる件数の目安を実測に基づき 14 件から 12 件に修正
- 2 ページ目が用紙の上端で切れないよう、印刷時の上マージンを 5mm 確保した
- 「⭐ おてつだい合計」が折り返していたのを 1 行に収めた
- 改ページの判定をブラウザ任せから Python 側の件数判定に変更。iPhone の Safari でも
  同じ結果になるようにした

## 2026-08-16

- ナレッジバンドルを OKF v0.2 形式で新規作成。単一ファイルだった `docs/SPEC.md` を
  概念ごとの Markdown に分解し、frontmatter を付与した
- [公開ポリシー](./publication-policy.md) を新設。公開リポジトリとして
  個人情報・秘密情報を含めないという前提を明文化し、`scripts/check_public_output.py` と
  CI での検査を追加した
- [きほんポスター](./output-basic-poster.md) の色とアイコンを、並び順依存から
  タスク名依存に変更。タスクを追加しても他のタスクの見た目が変わらなくなった
- [生成スクリプト](./generator.md) に HTML エスケープ、API エラーハンドリング、
  件数警告、`--sample`、来歴の埋め込みを追加
- [タスクデータ (JSON)](./output-tasks-json.md) の出力を追加
- MIT License を設定
