"""
Notionの「おてつだいタスク一覧」DBを読み込んで、
印刷用スタンプカードHTML（stamp_print.html）と
基本タスクポスター（basic_tasks_poster.html）を自動生成するスクリプト。

必要な環境変数:
  NOTION_TOKEN        Notion Internal Integration Secret
  NOTION_DATABASE_ID  「おてつだいタスク一覧」データベースのID
"""

import os
import sys
import json
import urllib.request

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
NOTION_VERSION = "2022-06-28"

OUTPUT_DIR = "output"


def notion_query_database(database_id):
    """Notion DBの全ページを取得する（ページネーション対応）"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    results = []
    payload = {"page_size": 100}
    while True:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {NOTION_TOKEN}",
                "Notion-Version": NOTION_VERSION,
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            data = json.loads(res.read().decode("utf-8"))
        results.extend(data.get("results", []))
        if data.get("has_more"):
            payload["start_cursor"] = data["next_cursor"]
        else:
            break
    return results


def get_prop_text(props, name):
    """title または rich_text プロパティからプレーンテキストを取り出す"""
    prop = props.get(name)
    if not prop:
        return ""
    ptype = prop.get("type")
    arr = prop.get(ptype, [])
    if not arr:
        return ""
    return "".join([t.get("plain_text", "") for t in arr])


def get_prop_select(props, name):
    prop = props.get(name)
    if not prop:
        return ""
    sel = prop.get("select")
    return sel.get("name") if sel else ""


def get_prop_number(props, name):
    prop = props.get(name)
    if not prop:
        return 0
    return prop.get("number") or 0


def load_tasks():
    pages = notion_query_database(NOTION_DATABASE_ID)
    basic_tasks = []
    challenge_tasks = []

    for page in pages:
        props = page.get("properties", {})
        name = get_prop_text(props, "タスク名")
        if not name:
            continue
        task_type = get_prop_select(props, "タイプ")
        star = get_prop_select(props, "難易度")
        price = get_prop_number(props, "単価（円）")
        note = get_prop_text(props, "備考")

        if task_type == "基本":
            basic_tasks.append({"name": name, "note": note})
        elif task_type == "チャレンジ":
            challenge_tasks.append(
                {"name": name, "note": note, "star": star or "★", "price": int(price)}
            )

    return basic_tasks, challenge_tasks


# ============================================================
# HTML テンプレート（印刷用スタンプカード：チャレンジタスク）
# ============================================================
def build_stamp_print_html(challenge_tasks):
    dates = list(range(1, 32))
    free_rows = 3

    def task_row(t):
        note_html = f'<div class="task-note">{t["note"]}</div>' if t["note"] else ""
        date_cells = "".join('<td class="td-date"></td>' for _ in dates)
        return f"""
    <tr>
      <td class="td-task">
        <div class="task-name">{t['name']}</div>
        {note_html}
      </td>
      <td class="td-star">{t['star']}</td>
      <td class="td-price">{t['price']}<span style="font-size:5pt;">円</span></td>
      {date_cells}
      <td class="td-count">　かい</td>
      <td class="td-earn">　　円</td>
    </tr>"""

    def free_row():
        date_cells = "".join('<td class="td-date"></td>' for _ in dates)
        return f"""
    <tr>
      <td class="td-task free"><div class="task-name free">（じゆうきにゅう）</div></td>
      <td class="td-star free">★</td>
      <td class="td-price free">　円</td>
      {date_cells}
      <td class="td-count">　かい</td>
      <td class="td-earn">　　円</td>
    </tr>"""

    def calc_row(t):
        return f"""
      <div class="calc-row">
        <span class="c-name">{t['name']}</span>
        <span class="c-price">{t['price']}円</span>
        <span class="c-x">×</span>
        <span class="c-box"></span>
        <span class="c-eq">=</span>
        <span class="c-res"></span>
        <span class="c-yen">円</span>
      </div>"""

    def free_calc_row():
        return """
      <div class="calc-row">
        <span class="c-free"></span>
        <span class="c-price" style="color:#ccc;">　円</span>
        <span class="c-x">×</span>
        <span class="c-box"></span>
        <span class="c-eq">=</span>
        <span class="c-res"></span>
        <span class="c-yen">円</span>
      </div>"""

    task_rows_html = "".join(task_row(t) for t in challenge_tasks)
    free_rows_html = "".join(free_row() for _ in range(free_rows))
    calc_rows_html = "".join(calc_row(t) for t in challenge_tasks) + "".join(
        free_calc_row() for _ in range(free_rows)
    )
    date_headers = "".join(f"<th>{d}</th>" for d in dates)
    date_cols = "".join('<col class="col-date">' for _ in dates)

    def sheet():
        return f"""
    <div class="sheet">
      <div class="sheet-header">
        <div class="sheet-title">⭐ おてつだいスタンプカード</div>
        <div class="header-fields">
          <div class="field-group">
            <span class="field-label">なまえ</span>
            <span class="field-line name"></span>
          </div>
          <div class="field-group">
            <span class="field-line year"></span><span class="field-unit">年</span>
            <span class="field-line month"></span><span class="field-unit">月</span>
          </div>
        </div>
      </div>

      <table class="main-table">
        <colgroup>
          <col class="col-task">
          <col class="col-star">
          <col class="col-price">
          {date_cols}
          <col class="col-count">
          <col class="col-earn">
        </colgroup>
        <thead>
          <tr>
            <th class="th-task">おてつだい</th>
            <th>むず</th>
            <th>1かい</th>
            {date_headers}
            <th>かい数</th>
            <th>ごうけい</th>
          </tr>
        </thead>
        <tbody>
          {task_rows_html}
          <tr class="section-label">
            <td colspan="{3 + len(dates) + 2}">✏️ じゆうきにゅう（おうちのひとといっしょにきめよう）</td>
          </tr>
          {free_rows_html}
        </tbody>
      </table>

      <div class="calc-section">
        <div class="calc-title">💰 今月のおこづかい計算（かい数 × 1かいのきんがく = ごうけい）</div>
        <div class="calc-body">
          <div class="calc-tasks">{calc_rows_html}</div>
          <div class="calc-right">
            <div class="cr-row">
              <span class="cr-label">🔒 かならずもらえる</span>
              <span class="cr-fixed">500円</span>
            </div>
            <div class="cr-row">
              <span class="cr-label">⭐ おてつだい合計</span>
              <div style="display:flex;align-items:flex-end;gap:1mm;">
                <span class="cr-line"></span><span class="cr-yen">円</span>
              </div>
            </div>
            <hr class="cr-divider">
            <div class="cr-total">
              <span>合計</span>
              <div style="display:flex;align-items:flex-end;gap:1mm;">
                <span class="cr-total-line"></span><span style="font-size:9pt;">円</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>"""

    sheets_html = sheet() + sheet()

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>おてつだいスタンプカード（印刷用）</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Sans JP', sans-serif;
    background: #e8e8e8;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 16px;
  }}
  .print-controls {{ text-align: center; }}
  .print-btn {{
    font-family: 'Noto Sans JP', sans-serif;
    background: #1c1c1e; color: #fff;
    border: none; border-radius: 12px;
    padding: 12px 32px; font-size: 15px; font-weight: 700;
    cursor: pointer;
  }}
  .print-btn:hover {{ background: #333; }}
  .screen-note {{ font-size: 12px; color: #888; margin-top: 6px; }}
  .sheet {{
    width: 277mm;
    background: #fff;
    padding: 6mm 7mm 5mm;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  }}
  .sheet-header {{ display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: 3mm; }}
  .sheet-title {{ font-size: 14pt; font-weight: 900; white-space: nowrap; }}
  .header-fields {{ display: flex; align-items: flex-end; gap: 7mm; }}
  .field-group {{ display: flex; align-items: flex-end; gap: 1.5mm; }}
  .field-label {{ font-size: 8pt; color: #666; padding-bottom: 0.5mm; }}
  .field-line {{ border-bottom: 1.5px solid #333; display: inline-block; }}
  .field-line.year {{ width: 13mm; }}
  .field-line.month {{ width: 9mm; }}
  .field-line.name {{ width: 30mm; }}
  .field-unit {{ font-size: 8pt; color: #444; padding-bottom: 0.5mm; }}
  .main-table {{ width: 100%; border-collapse: collapse; table-layout: fixed; }}
  col.col-task {{ width: 36mm; }}
  col.col-star {{ width: 7mm; }}
  col.col-price {{ width: 10mm; }}
  col.col-date {{ width: 6.5mm; }}
  col.col-count {{ width: 9mm; }}
  col.col-earn {{ width: 12mm; }}
  .main-table thead th {{
    font-size: 6.5pt; font-weight: 700; text-align: center; vertical-align: middle;
    padding: 1mm 0; background: #1c1c1e; color: #fff; height: 6.5mm; border: 0.5px solid #000;
  }}
  .main-table thead th.th-task {{ text-align: left; padding-left: 2mm; font-size: 7pt; }}
  .main-table tbody tr td {{ border: 0.5px solid #ccc; height: 7.5mm; vertical-align: middle; }}
  .main-table tbody tr:nth-child(odd) td {{ background: #fafafa; }}
  .main-table tbody tr:nth-child(even) td {{ background: #fff; }}
  .td-task {{ padding: 0.5mm 1.5mm; border-left: 2px solid #333 !important; }}
  .task-name {{ font-size: 6.5pt; font-weight: 700; line-height: 1.3; }}
  .task-note {{ font-size: 5pt; color: #999; line-height: 1.2; margin-top: 0.5mm; }}
  .td-star {{ text-align: center; font-size: 6.5pt; color: #d97706; font-weight: 700; }}
  .td-price {{ text-align: center; font-size: 7pt; font-weight: 900; color: #059669; border-right: 2px solid #333 !important; }}
  .td-date {{ border: 0.5px solid #ccc !important; }}
  .td-count, .td-earn {{
    text-align: center; font-size: 6pt; color: #aaa; vertical-align: bottom;
    padding-bottom: 1mm; border-bottom: 1px solid #888 !important;
  }}
  .td-count {{ border-left: 2px solid #333 !important; }}
  .td-earn {{ border-right: 2px solid #333 !important; font-size: 5.5pt; }}
  .td-task.free {{ vertical-align: bottom; padding-bottom: 1mm; border-bottom: 1px solid #aaa !important; }}
  .task-name.free {{ color: #ccc; font-weight: 400; font-size: 6pt; }}
  .td-star.free {{ color: #ddd; font-size: 6pt; }}
  .td-price.free {{
    color: #ccc; font-weight: 400; font-size: 6pt; vertical-align: bottom;
    padding-bottom: 1mm; border-bottom: 1px solid #aaa !important;
  }}
  tr.section-label td {{
    background: #f0f0f0 !important; border: 0.5px solid #bbb; font-size: 6.5pt;
    font-weight: 700; color: #555; padding: 0.8mm 2mm; height: 4.5mm;
  }}
  .calc-section {{ margin-top: 3mm; border: 1.5px solid #333; border-radius: 2mm; overflow: hidden; }}
  .calc-title {{ background: #1c1c1e; color: #fff; font-size: 8pt; font-weight: 700; padding: 1.2mm 3mm; }}
  .calc-body {{ padding: 2.5mm 3mm; display: flex; gap: 4mm; align-items: flex-start; }}
  .calc-tasks {{ flex: 1; display: grid; grid-template-columns: repeat(2, 1fr); gap: 1.5mm 5mm; }}
  .calc-row {{ display: flex; align-items: flex-end; gap: 1.5mm; font-size: 6.5pt; }}
  .c-name {{ flex: 1; color: #333; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding-bottom: 0.5mm; }}
  .c-price {{ color: #059669; font-weight: 700; white-space: nowrap; padding-bottom: 0.5mm; }}
  .c-x {{ color: #999; padding-bottom: 0.5mm; }}
  .c-box {{ width: 8mm; border-bottom: 1px solid #666; flex-shrink: 0; height: 3.5mm; }}
  .c-eq {{ color: #999; padding-bottom: 0.5mm; }}
  .c-res {{ width: 10mm; border-bottom: 1px solid #666; flex-shrink: 0; height: 3.5mm; }}
  .c-yen {{ color: #888; font-size: 5.5pt; padding-bottom: 0.5mm; }}
  .c-free {{ flex: 1; border-bottom: 1px solid #ddd; height: 3.5mm; }}
  .calc-right {{
    width: 46mm; flex-shrink: 0; border-left: 1px dashed #ccc; padding-left: 4mm;
    display: flex; flex-direction: column; gap: 2.5mm; justify-content: center;
  }}
  .cr-row {{ display: flex; justify-content: space-between; align-items: flex-end; font-size: 7.5pt; }}
  .cr-label {{ color: #555; }}
  .cr-fixed {{ font-weight: 700; color: #1c1c1e; }}
  .cr-line {{ width: 16mm; border-bottom: 1px solid #666; height: 4mm; }}
  .cr-yen {{ font-size: 6.5pt; color: #555; margin-left: 1mm; }}
  .cr-divider {{ border: none; border-top: 1.5px solid #333; }}
  .cr-total {{ display: flex; justify-content: space-between; align-items: flex-end; font-size: 10pt; font-weight: 900; }}
  .cr-total-line {{ width: 18mm; border-bottom: 2px solid #333; height: 5mm; }}
  @media print {{
    @page {{ size: A4 landscape; margin: 0; }}
    body {{ background: none; padding: 0; gap: 0; }}
    .print-controls {{ display: none !important; }}
    .sheet {{ box-shadow: none; width: 100%; padding: 7mm 8mm 6mm; page-break-after: always; }}
    .sheet:last-child {{ page-break-after: avoid; }}
  }}
</style>
</head>
<body>
<div class="print-controls">
  <button class="print-btn" onclick="window.print()">🖨️ 印刷する（A4・横向き）</button>
  <p class="screen-note">Notionのデータから自動生成されました</p>
</div>
<div id="sheets">{sheets_html}</div>
</body>
</html>"""


# ============================================================
# HTML テンプレート（基本タスクポスター：A4縦）
# ============================================================
def build_basic_poster_html(basic_tasks):
    colors = ["c1", "c2", "c3", "c4", "c5", "c6"]
    icons = ["🧹", "👕", "🧺", "🍽️", "🥢", "🗑️", "🧴", "🧽", "📚", "🪥"]

    def task_card(t, i):
        color = colors[i % len(colors)]
        icon = icons[i % len(icons)]
        note_html = f'<div class="task-note">{t["note"]}</div>' if t["note"] else ""
        return f"""
    <div class="task-card {color}">
      <div class="task-icon">{icon}</div>
      <div class="task-body">
        <div class="task-name">{t['name']}</div>
        {note_html}
      </div>
    </div>"""

    cards_html = "".join(task_card(t, i) for i, t in enumerate(basic_tasks))

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>きほんおてつだいリスト</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Sans JP', sans-serif; background: #e0e0e0; padding: 20px;
    display: flex; flex-direction: column; align-items: center; gap: 16px;
  }}
  .print-controls {{ text-align: center; }}
  .print-btn {{
    font-family: 'Noto Sans JP', sans-serif; background: #1c1c1e; color: #fff;
    border: none; border-radius: 12px; padding: 12px 32px; font-size: 15px; font-weight: 700; cursor: pointer;
  }}
  .print-btn:hover {{ background: #333; }}
  .screen-note {{ font-size: 12px; color: #888; margin-top: 6px; }}
  .poster {{
    width: 190mm; min-height: 270mm; background: #fff; padding: 10mm 10mm 8mm;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15); display: flex; flex-direction: column; gap: 6mm;
  }}
  .poster-header {{ text-align: center; background: #1c1c1e; border-radius: 5mm; padding: 6mm 4mm; color: #fff; }}
  .poster-header .emoji {{ font-size: 36pt; display: block; margin-bottom: 3mm; }}
  .poster-header h1 {{ font-size: 22pt; font-weight: 900; line-height: 1.3; margin-bottom: 3mm; }}
  .poster-header p {{ font-size: 10pt; color: #aaa; line-height: 1.6; }}
  .name-field {{ display: flex; align-items: center; justify-content: center; gap: 3mm; padding: 3mm 0; border-bottom: 1.5px dashed #ddd; }}
  .name-label {{ font-size: 10pt; color: #888; }}
  .name-line {{ width: 50mm; border-bottom: 2px solid #333; height: 6mm; }}
  .task-list {{ display: flex; flex-direction: column; gap: 4mm; flex: 1; }}
  .task-card {{ display: flex; align-items: center; gap: 4mm; border-radius: 4mm; padding: 4mm 5mm; border-left: 5px solid; }}
  .task-card.c1 {{ background: #fff7ed; border-color: #fb923c; }}
  .task-card.c2 {{ background: #fdf4ff; border-color: #c084fc; }}
  .task-card.c3 {{ background: #f0fdf4; border-color: #4ade80; }}
  .task-card.c4 {{ background: #eff6ff; border-color: #60a5fa; }}
  .task-card.c5 {{ background: #fff1f2; border-color: #fb7185; }}
  .task-card.c6 {{ background: #fefce8; border-color: #facc15; }}
  .task-icon {{ font-size: 28pt; flex-shrink: 0; width: 14mm; text-align: center; line-height: 1; }}
  .task-body {{ flex: 1; }}
  .task-name {{ font-size: 14pt; font-weight: 900; color: #1c1c1e; line-height: 1.4; margin-bottom: 1.5mm; }}
  .task-note {{ font-size: 8.5pt; color: #888; line-height: 1.5; }}
  .poster-footer {{ text-align: center; padding-top: 4mm; border-top: 1.5px dashed #eee; }}
  .footer-text {{ font-size: 9pt; color: #aaa; line-height: 1.6; }}
  .footer-star {{ font-size: 14pt; }}
  @media print {{
    @page {{ size: A4 portrait; margin: 0; }}
    body {{ background: none; padding: 0; gap: 0; }}
    .print-controls {{ display: none !important; }}
    .poster {{ box-shadow: none; width: 100%; min-height: 100vh; padding: 12mm 12mm 10mm; }}
  }}
</style>
</head>
<body>
<div class="print-controls">
  <button class="print-btn" onclick="window.print()">🖨️ 印刷する（A4・縦向き）</button>
  <p class="screen-note">Notionのデータから自動生成されました</p>
</div>
<div class="poster">
  <div class="poster-header">
    <span class="emoji">🏠</span>
    <h1>きほんのお手伝い</h1>
    <p>これは毎日やること。家族の一員としての大事なしごと。</p>
  </div>
  <div class="name-field">
    <span class="name-label">なまえ</span>
    <span class="name-line"></span>
  </div>
  <div class="task-list">{cards_html}
  </div>
  <div class="poster-footer">
    <div class="footer-star">⭐ ⭐ ⭐</div>
    <p class="footer-text">
      これができたら、チャレンジおてつだいにもちょうせんしてみよう！<br>
      チャレンジは回数分のおこづかいがもらえるよ。
    </p>
  </div>
</div>
</body>
</html>"""


def main():
    if not NOTION_TOKEN or not NOTION_DATABASE_ID:
        print("エラー: NOTION_TOKEN / NOTION_DATABASE_ID が設定されていません", file=sys.stderr)
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    basic_tasks, challenge_tasks = load_tasks()
    print(f"基本タスク: {len(basic_tasks)}件, チャレンジタスク: {len(challenge_tasks)}件")

    stamp_html = build_stamp_print_html(challenge_tasks)
    with open(os.path.join(OUTPUT_DIR, "stamp_print.html"), "w", encoding="utf-8") as f:
        f.write(stamp_html)

    poster_html = build_basic_poster_html(basic_tasks)
    with open(os.path.join(OUTPUT_DIR, "basic_tasks_poster.html"), "w", encoding="utf-8") as f:
        f.write(poster_html)

    # シンプルな index.html（iPhoneから開いたときのリンク集）
    index_html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>おてつだい制度</title>
<style>
  body {{ font-family: sans-serif; background:#f5f5f0; padding:40px 20px; text-align:center; }}
  h1 {{ font-size: 20px; margin-bottom: 24px; }}
  a {{
    display:block; max-width:320px; margin:0 auto 16px; padding:16px;
    background:#1c1c1e; color:#fff; text-decoration:none; border-radius:12px; font-weight:bold;
  }}
  p.updated {{ color:#999; font-size:12px; margin-top:24px; }}
</style>
</head>
<body>
  <h1>⭐ おてつだい制度 印刷ページ</h1>
  <a href="stamp_print.html">📋 チャレンジタスク スタンプカード（A4横）</a>
  <a href="basic_tasks_poster.html">🏠 きほんタスク ポスター（A4縦）</a>
  <p class="updated">Notionのデータから自動生成されています</p>
</body>
</html>"""
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)

    print("生成完了: output/index.html, stamp_print.html, basic_tasks_poster.html")


if __name__ == "__main__":
    main()
