# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A single-script static site generator: it reads a Notion database (「おてつだいタスク一覧」 — a kids' chore list) and emits three self-contained print-oriented HTML files into `output/`, which GitHub Actions publishes to GitHub Pages. The whole project is `generate.py` plus one workflow; there are no dependencies (stdlib `urllib` only), no build step, no tests, and no package manifest.

## Running it

```bash
NOTION_TOKEN=ntn_... NOTION_DATABASE_ID=<32 hex chars, no hyphens> python generate.py
```

Both env vars are required; the script exits 1 without them. Output goes to `output/` (untracked, regenerated each run). Open `output/index.html` in a browser to preview; use the browser's print preview to check page layout, since almost all styling only matters on paper.

To iterate on layout without Notion credentials, temporarily stub `load_tasks()` to return literal task lists — the HTML builders are pure functions of those lists.

CI: `.github/workflows/generate.yml` runs the same command on Python 3.11 via `workflow_dispatch` (a monthly cron is present but commented out), then uploads `output/` as the Pages artifact and deploys. Secrets `NOTION_TOKEN` / `NOTION_DATABASE_ID` are configured at the repo level.

## Architecture

`generate.py` has three layers, in order:

1. **Notion fetch** — `notion_query_database()` POSTs to the `/v1/databases/{id}/query` endpoint with `Notion-Version: 2022-06-28`, paging through `has_more`/`next_cursor`. The `get_prop_*` helpers flatten Notion's property shapes into plain values.
2. **Domain mapping** — `load_tasks()` splits pages into two lists by the 「タイプ」 select: 「基本」 → basic tasks (name + note only) and 「チャレンジ」 → challenge tasks (also 難易度 star and 単価（円） price). Rows with an empty 「タスク名」 and rows with any other type are silently dropped. **The Japanese property names are hardcoded here** — renaming a column in Notion silently produces empty output, so this function is the first place to look when a task disappears.
3. **HTML builders** — `build_stamp_print_html()` (challenge tasks → A4 landscape stamp card) and `build_basic_poster_html()` (basic tasks → A4 portrait poster) return complete standalone documents from f-strings with doubled braces (`{{`) for literal CSS. `main()` writes them plus a hand-written `index.html` link page.

## Editing the templates

- Everything is inline: CSS lives in the f-string, no external assets except the Google Fonts link. Keep pages self-contained so they work as static Pages files.
- Layout is print-first — dimensions are in `mm`/`pt` and each page has an `@media print` block with `@page { size: A4 landscape|portrait; margin: 0 }`. Screen rendering exists only as a preview; the `.print-controls` button block is hidden when printing.
- The stamp card is a fixed 31-column grid (days 1–31) built from `dates`, with `free_rows = 3` blank write-in rows. Column widths are declared in `<colgroup>` and the matching `col.col-*` CSS rules; the section-label row's `colspan` is computed as `3 + len(dates) + 2`, so changing the column set means updating all three places together. Each sheet is emitted twice (`sheet() + sheet()`) so one print gives two copies.
- Task text from Notion is interpolated into HTML unescaped; names and notes containing `<`, `>`, or `&` will break the markup.
- Poster cards cycle through fixed `colors` (6) and `icons` (10) lists by index, so a task's color/icon depends on its position in the Notion query order, not on its content.

## Conventions

All user-facing strings, Notion property names, comments, and the README are in Japanese; the README documents the end-user setup and daily operation flow. Keep new output text in Japanese and kid-readable (kana-heavy) to match the existing copy.
