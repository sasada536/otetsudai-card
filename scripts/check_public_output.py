"""公開前チェック：output/ に秘密情報が混入していないか検査する。

このリポジトリはGitHub上で公開運用しているため、output/ の中身はそのまま
全世界に公開される。トークンやデータベースIDが誤って埋め込まれた状態で
公開されるのを防ぐための最後の関門。

問題を見つけたら exit 1 する。CIではPagesへのアップロード前に実行する。

  python scripts/check_public_output.py
"""

import os
import re
import sys

OUTPUT_DIR = "output"

# 値そのものが出力に現れてはいけない環境変数
FORBIDDEN_ENV_VARS = ["NOTION_TOKEN", "NOTION_DATABASE_ID"]

# 秘密情報によくある形。値を知らなくても検出できるようにするための保険。
SECRET_PATTERNS = [
    (r"ntn_[A-Za-z0-9]{20,}", "Notion Integration Secret らしき文字列"),
    (r"secret_[A-Za-z0-9]{20,}", "Notion Integration Secret（旧形式）らしき文字列"),
    (r"ghp_[A-Za-z0-9]{20,}", "GitHub Personal Access Token らしき文字列"),
    (r"gh[opsu]_[A-Za-z0-9]{20,}", "GitHub Token らしき文字列"),
    (r"Bearer\s+[A-Za-z0-9\-._~+/]{20,}", "Authorization ヘッダらしき文字列"),
    (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "メールアドレス"),
]


def iter_output_files():
    for root, _, files in os.walk(OUTPUT_DIR):
        for name in files:
            yield os.path.join(root, name)


def main():
    if not os.path.isdir(OUTPUT_DIR):
        print(f"エラー: {OUTPUT_DIR}/ がありません。先に generate.py を実行してください。", file=sys.stderr)
        sys.exit(1)

    problems = []
    checked = 0

    for path in iter_output_files():
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        checked += 1

        for var in FORBIDDEN_ENV_VARS:
            value = os.environ.get(var, "")
            # 空や極端に短い値で誤検知しないようにする
            if len(value) >= 8 and value in text:
                problems.append(f"{path}: 環境変数 {var} の値がそのまま含まれています")

        for pattern, label in SECRET_PATTERNS:
            match = re.search(pattern, text)
            if match:
                problems.append(f"{path}: {label} を検出しました（{match.group()[:12]}...）")

    if problems:
        print("公開前チェックに失敗しました。以下を解消するまで公開できません:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        sys.exit(1)

    print(f"公開前チェック OK: {checked}ファイルを検査し、秘密情報は検出されませんでした")


if __name__ == "__main__":
    main()
