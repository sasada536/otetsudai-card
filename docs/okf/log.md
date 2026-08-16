# 更新履歴

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
