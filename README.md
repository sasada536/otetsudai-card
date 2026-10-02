# おてつだいカード自動生成

Notionの「おてつだいタスク一覧」DBから、印刷用HTML（スタンプカード・基本タスクポスター）を
自動生成し、iPhoneからいつでも見られるWebページとして公開する仕組みです。

日常の運用は「Notionを編集 → GitHubでボタンを1回押す（or 自動）→ iPhoneでURLを開いて印刷」だけです。

---

## 動作をすぐ試したい場合（Notionの設定なし）

サンプルデータが同梱されているので、Notionのアカウントやトークンがなくても動かせます。

```bash
python generate.py --sample
```

`output/` に3つのHTMLと `tasks.json` が生成されるので、`output/index.html` をブラウザで開いてください。
必要なのはPython 3.11以降だけで、`pip install` は不要です（標準ライブラリのみを使用）。

---

## セットアップ手順（最初の1回だけ）

### ① Notion Integration（APIキー）を作る

1. https://www.notion.so/my-integrations を開く
2. 「+ New integration」
3. 名前は何でもいい（例：おてつだいカード）
4. ワークスペースを選んで「Submit」
5. 表示された **Internal Integration Secret**（`ntn_...` から始まる文字列）をコピーしておく

### ② Notionのデータベースにインテグレーションを接続する

1. Notionで「おてつだいタスク一覧」のデータベースを開く
2. 右上の「...」→「コネクト」→ ①で作ったインテグレーション名を選択
3. これで①のキーがこのDBを読めるようになる

### ③ データベースIDを控える

データベースを開いたときのURLがこの形式：
```
https://www.notion.so/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx?v=...
```
`xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx` の32文字（ハイフンなし）が Database ID。

### ④ GitHubリポジトリを作る

1. https://github.com にログイン（アカウントがなければ作成、無料）
2. 「New repository」→ 名前は任意（例：otetsudai-card）
3. **Public**（無料枠が一番広い。金額は表示されるだけで実害はないので基本Publicで問題なし。
   気になる場合はPrivateでもOK、月2,000分の無料枠内で足りる）
4. このフォルダの中身（`generate.py`、`.github/workflows/generate.yml`、`README.md`）を
   そのままリポジトリにアップロードする（GitHubの「Add file」→「Upload files」でドラッグ&ドロップでOK）

### ⑤ GitHubにNotionの情報を安全に登録する（Secrets）

1. 作ったリポジトリの「Settings」タブ
2. 左メニュー「Secrets and variables」→「Actions」
3. 「New repository secret」を2回行う：
   - 名前：`NOTION_TOKEN` / 値：①でコピーしたキー
   - 名前：`NOTION_DATABASE_ID` / 値：③で控えたID

### ⑥ GitHub Pagesを有効にする

1. リポジトリの「Settings」→「Pages」
2. 「Source」を **GitHub Actions** に設定

### ⑦ 初回実行

1. リポジトリの「Actions」タブ
2. 左の「おてつだいカード生成」をクリック
3. 「Run workflow」ボタンを押す
4. 1分ほどで完了。「Settings」→「Pages」に表示されるURL
   （`https://ユーザー名.github.io/リポジトリ名/`）にアクセスすると印刷ページが見られる

---

## 日常の運用

1. Notionでタスクを編集する
2. GitHubの「Actions」タブ →「Run workflow」を押す（iPhoneのGitHubアプリからも可能）
3. 1分待ってから、さっきのURLをブラウザで開く
4. 「印刷する」ボタンを押す

URLはブックマークしておくと毎回探さなくて済みます。

### うまくいかないとき

- **`deploy` だけ赤くなり、ログに `Failed to create deployment (status: 404)` と出る**
  → 「Settings」→「Pages」の「Source」が **GitHub Actions** になっているか確認し、
  なっていなければ直して「Run workflow」をやり直す（⑥の設定が外れている状態）。
  すでに GitHub Actions になっている場合は、一度別の値に切り替えてから戻すと直ることがある
- そのほかのエラーは [`docs/okf/playbooks/run-generation.md`](docs/okf/playbooks/run-generation.md)
  の「失敗したとき」を参照

---

## 補足

- 費用は完全無料（GitHub Actions・Pages・Notion APIすべて無料枠内）
- タスクの追加・削除・単価変更はすべてNotion側の編集だけで反映される
- レイアウト自体（列数やデザイン）を変えたいときはこれまで通りClaudeに相談してOK。
  その場合は `generate.py` 内のHTMLテンプレート部分を書き換える
- 「かならずもらえる」金額は `generate.py` の `FIXED_ALLOWANCE`（初期値500円）で変更する
- 詳しい仕様・手順書は [`docs/okf/`](docs/okf/index.md) を参照
  （[OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
  形式のナレッジバンドル。人間も AI エージェントもそのまま読める）

---

## 出力されるファイル

| ファイル | 内容 |
| --- | --- |
| `index.html` | 印刷ページへのリンク集 |
| `stamp_print.html` | チャレンジタスクのスタンプカード（A4横・2部） |
| `basic_tasks_poster.html` | 基本タスクのポスター（A4縦） |
| `tasks.json` | タスクデータ（機械可読・再利用向け） |

---

## 公開範囲とライセンス

このリポジトリで**オープンにしているのはツールと生成物であって、入力データではありません**。

- Notionのデータベース（各家庭のタスク内容）は非公開で、閲覧にはトークンが必要です
- GitHub Pages に公開されるのは、生成されたHTMLと `tasks.json` だけです
- 動作確認用の `data/sample_tasks.json` は実在の家庭のデータではなく、すべて架空の内容です

ライセンスは用途ごとに分かれています。

| 対象 | ライセンス |
| --- | --- |
| コード（`generate.py`、ワークフロー等） | [MIT License](LICENSE) |
| ドキュメント（`README.md`、`docs/`） | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.ja) |

生成されたHTML・JSONの著作権は、それを生成した人（＝入力データの持ち主）に帰属します。
