# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 応答言語（最優先ルール / TOP PRIORITY）

**このリポジトリでの応答・解説・要約・質問はすべて日本語で書くこと。**
ユーザーが英語で書いてきた場合や、コード・ログ・エラーメッセージが英語の場合でも、
Claude の地の文（説明部分）は必ず日本語にする。英語で返答してはならない。

Always respond in Japanese in this repository — every explanation, summary, plan, and
question. This applies regardless of the language of the user's message, the code, or any
tool output. Do not answer in English.

例外は、リポジトリに書き込む成果物そのもの（コミットメッセージ、PR タイトル／本文、
コード内のコメント）のうち、既存の慣習が英語であるもののみ。チャットでの説明は常に日本語。

## 公開リポジトリの原則（最優先ルール / TOP PRIORITY）

**このリポジトリは GitHub 上で公開運用している。コミット・プッシュする内容はすべて、
全世界から永続的に閲覧できる前提で扱うこと。** git の履歴は後から消しにくいため、
「入れてしまってから消す」ではなく「最初から入れない」で守る。

This repository is public. Everything committed is world-readable and effectively permanent.
Never commit personal information or anything security-sensitive.

### 絶対にコミットしてはいけないもの

- `NOTION_TOKEN`、API キー、各種シークレット（GitHub Actions Secrets 経由でのみ渡す）
- `NOTION_DATABASE_ID`（データベースを特定できる識別子。生成物にも埋め込まない）
- 実在の家族の氏名・学校名・住所・写真・生活パターンが推測できる情報
- `output/` の生成物（実データを含むため。`.gitignore` 済み）
- 上記が写り込んだスクリーンショットやログの貼り付け

### 守るべきこと

- サンプルデータ（`data/sample_tasks.json`）は**架空の内容のみ**。実在のタスクをコピーしない
- 新しい出力項目・新しいファイルを追加するときは、**公開して問題ないかを必ず確認してから**追加する
- 迷ったら入れない。判断がつかない場合はユーザーに確認する
- 公開前チェック `scripts/check_public_output.py` を弱めたり、迂回したりしない

なお、コミットのメタデータ（author の氏名・メールアドレス）も公開される。これは GitHub
アカウントの設定に属するため本リポジトリの管理外だが、変更したい場合は GitHub の
noreply アドレス設定を使う。

## Knowledge bundle: docs/okf/

Detailed specifications, playbooks, and design rationale live in `docs/okf/`, an
[OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
bundle — one concept per Markdown file, `type` in YAML frontmatter, interlinked with relative
links. Start at `docs/okf/index.md`. **Read the relevant concept file before changing the thing
it describes**, and update it in the same commit when behavior changes.

When adding a concept file: give it a non-empty `type` (that is the only required field), plus
`title` / `description` / `tags`. Reserved names `index.md` and `log.md` carry no frontmatter —
the sole exception is the bundle-root `index.md`, which holds `okf_version`. Record notable
changes in `docs/okf/log.md`.

## What this is

A single-script static site generator: it reads a Notion database (「おてつだいタスク一覧」 — a kids' chore list) and emits three self-contained print-oriented HTML files into `output/`, which GitHub Actions publishes to GitHub Pages. The whole project is `generate.py` plus one workflow; there are no dependencies (stdlib `urllib` only), no build step, no tests, and no package manifest.

## Running it

```bash
NOTION_TOKEN=ntn_... NOTION_DATABASE_ID=<32 hex chars, no hyphens> python generate.py
```

Both env vars are required; the script exits 1 without them. Output goes to `output/` (gitignored, regenerated each run). Open `output/index.html` in a browser to preview; use the browser's print preview to check page layout, since almost all styling only matters on paper.

**To iterate without Notion credentials, use sample mode** — this is the normal way to work on layout:

```bash
python generate.py --sample   # reads data/sample_tasks.json
```

Sample mode is opt-in by design: missing credentials without `--sample` still exit 1, so a misconfigured CI run fails loudly instead of silently publishing sample data. The HTML builders are pure functions of the task lists plus a provenance dict, so they can also be called directly from a REPL.

CI: `.github/workflows/generate.yml` runs the same command on Python 3.11 via `workflow_dispatch` (a monthly cron is present but commented out), then uploads `output/` as the Pages artifact and deploys. Secrets `NOTION_TOKEN` / `NOTION_DATABASE_ID` are configured at the repo level.

## Architecture

`generate.py` has three layers, in order:

1. **Notion fetch** — `notion_query_database()` POSTs to the `/v1/databases/{id}/query` endpoint with `Notion-Version: 2022-06-28`, paging through `has_more`/`next_cursor`. The `get_prop_*` helpers flatten Notion's property shapes into plain values.
2. **Domain mapping** — `load_tasks()` splits pages into two lists by the 「タイプ」 select: 「基本」 → basic tasks (name + note only) and 「チャレンジ」 → challenge tasks (also 難易度 star and 単価（円） price). Rows with an empty 「タスク名」 and rows with any other type are silently dropped. **The Japanese property names are hardcoded here** — renaming a column in Notion silently produces empty output, so this function is the first place to look when a task disappears.
3. **HTML builders** — `build_stamp_print_html()` (challenge tasks → A4 landscape stamp card) and `build_basic_poster_html()` (basic tasks → A4 portrait poster) take `(tasks, prov)` and return complete standalone documents from f-strings with doubled braces (`{{`) for literal CSS. `main()` writes them, plus a hand-written `index.html` link page and `tasks.json`.

`main()` also calls `warn_on_task_counts()`, which prints warnings (not errors) when a task list is empty — the usual symptom of a renamed Notion property — or when counts exceed what fits on the page (`BASIC_TASK_LIMIT` 8, `CHALLENGE_TASK_LIMIT` 14).

## Editing the templates

- Everything is inline: CSS lives in the f-string, no external assets except the Google Fonts link. Keep pages self-contained so they work as static Pages files.
- Layout is print-first — dimensions are in `mm`/`pt` and each page has an `@media print` block with `@page { size: A4 landscape|portrait; margin: 0 }`. Screen rendering exists only as a preview; the `.print-controls` button block is hidden when printing.
- The stamp card is a fixed 31-column grid (days 1–31) built from `dates`, with `free_rows = 3` blank write-in rows. Column widths are declared in `<colgroup>` and the matching `col.col-*` CSS rules; the section-label row's `colspan` is computed as `3 + len(dates) + 2`, so changing the column set means updating all three places together. Each sheet is emitted twice (`sheet() + sheet()`) so one print gives two copies.
- **Always wrap Notion-derived text in `esc()`** when adding a new interpolation. Every existing one already is; forgetting it reintroduces the HTML-injection bug that `<`, `>`, and `&` in task names used to cause.
- Poster cards cycle through fixed `colors` (6) and `icons` (10) lists by index, so a task's color/icon depends on its position in the Notion query order, not on its content. Adding one task shifts every later task's color and icon.
- Every page carries provenance `<meta>` tags built by `provenance_meta(prov)`, and a screen-only note from `provenance_note(prov)`. New pages should include both.

## Conventions

All user-facing strings, Notion property names, comments, and the README are in Japanese; the README documents the end-user setup and daily operation flow. Keep new output text in Japanese and kid-readable (kana-heavy) to match the existing copy.
