#!/usr/bin/env python3
"""Build the designed HTML version of the Asefa Family Gathering Constitution (EN, AM, OM).

Run:  python3 build_html.py
Output: Asefa-Family-Gathering-Constitution.html in the same folder.

The text comes from build_constitution.py (CONTENT_EN / CONTENT_AM), so edit it there
and re-run both scripts. This file only holds the page design.
"""

import html
import os
import re

from build_constitution import CONTENT_EN, CONTENT_AM, CONTENT_OM, DATE_EN, DATE_AM, DATE_OM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "constitution.html")

GEEZ = ["፩", "፪", "፫", "፬", "፭", "፮", "፯", "፰", "፱", "፲", "፲፩", "፲፪"]


def esc(s):
    return html.escape(s, quote=False)


# ---------------------------------------------------------------- parsing
def split(content):
    """Return (preamble_items, [(number, title, items)...], sig_spec)."""
    preamble, articles, sig = [], [], None
    current = None
    for item in content:
        kind = item[0]
        if kind == "h1":
            m = re.match(r"^(?:Article|አንቀጽ|Keewwata)\s+(\d+)\.\s*(.*)$", item[1])
            current = (int(m.group(1)), m.group(2), [])
            articles.append(current)
        elif kind == "sig":
            sig = item[1]
        elif current is None:
            preamble.append(item)
        else:
            current[2].append(item)
    return preamble, articles, sig


# ---------------------------------------------------------------- rendering
def table_html(rows, fill_in):
    head, body = rows[0], rows[1:]
    out = ['<div class="tablewrap"><table>', "<thead><tr>"]
    out += [f"<th>{esc(c)}</th>" for c in head]
    out.append("</tr></thead><tbody>")
    for r in body:
        out.append("<tr>")
        for i, c in enumerate(r):
            cls = ' class="num"' if re.fullmatch(r"[\d,]+", c) else ""
            if c == "" and fill_in:
                cls = ' class="blank"'
            out.append(f"<td{cls}>{esc(c)}</td>")
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def items_html(items):
    out = []
    ol = li = ul = False

    def close_ul():
        nonlocal ul
        if ul:
            out.append("</ul>")
            ul = False

    def close_li():
        nonlocal li
        close_ul()
        if li:
            out.append("</li>")
            li = False

    def close_all():
        nonlocal ol
        close_li()
        if ol:
            out.append("</ol>")
            ol = False

    for item in items:
        kind = item[0]
        if kind == "p":
            close_all()
            out.append(f"<p>{esc(item[1])}</p>")
        elif kind == "n":
            close_li()
            if not ol:
                out.append('<ol class="clauses">')
                ol = True
            out.append(f"<li><p>{esc(item[2])}</p>")
            li = True
        elif kind == "b":
            if not ul:
                out.append('<ul class="sub">')
                ul = True
            out.append(f"<li>{esc(item[1])}</li>")
        elif kind == "t":
            close_ul()
            rows = item[1]
            fill_in = all(r[-1] == "" for r in rows[1:])
            out.append(table_html(rows, fill_in))
    close_all()
    return "".join(out)


def sig_html(spec, lang):
    out = [f'<div class="t" lang="{lang}">']
    out.append(f'<h3>{esc(spec["title"])}</h3>')
    out.append(f'<p class="adopted">{esc(spec["line"])}</p>')
    out.append('<div class="posts">')
    for p in spec["posts"]:
        out.append(
            f'<div class="post"><span class="post-name">{esc(p)}</span>'
            f'<span class="line"><small>{esc(spec["cols"][1])}</small></span>'
            f'<span class="line"><small>{esc(spec["cols"][2])}</small></span></div>'
        )
    out.append("</div>")
    out.append(f'<h4>{esc(spec["members"])}</h4><ol class="members">')
    out += ["<li></li>"] * 20
    out.append("</ol></div>")
    return "".join(out)


def build():
    langs = [("en", CONTENT_EN), ("am", CONTENT_AM), ("om", CONTENT_OM)]
    parsed = {l: split(c) for l, c in langs}
    for l in parsed:
        assert len(parsed[l][1]) == 12, l
    COLORS = ["#0e5245", "#c4202f", "#1b9aa0", "#b8296e", "#c98f1c"]
    ARTICLE = {"en": lambda n: f"Article {n}", "am": lambda n: f"አንቀጽ {GEEZ[n - 1]}", "om": lambda n: f"Keewwata {n}"}

    def t3(en, am, om, tag="span"):
        return (f'<{tag} class="t" lang="en">{en}</{tag}><{tag} class="t" lang="am">{am}</{tag}>'
                f'<{tag} class="t" lang="om">{om}</{tag}>')

    toc = []
    for i in range(12):
        n = parsed["en"][1][i][0]
        titles = [esc(parsed[l][1][i][1]) for l in ("en", "am", "om")]
        toc.append(f'<li><a href="#article-{n}"><span class="dia" style="--c:{COLORS[i % 5]}"><b>{n}</b></span>'
                   f'<span>{t3(*titles)}</span></a></li>')

    arts = []
    for i in range(12):
        n = parsed["en"][1][i][0]
        cols = []
        for l in ("en", "am", "om"):
            _, title, items = parsed[l][1][i]
            cols.append(f'<div class="t" lang="{l}"><h2><span class="kicker">{esc(ARTICLE[l](n))}</span>{esc(title)}</h2>{items_html(items)}</div>')
        arts.append(f'<article class="card art" id="article-{n}"><div class="dia big" style="--c:{COLORS[i % 5]}"><b>{n}</b></div>'
                    f'<div class="art-body">{"".join(cols)}</div></article>')

    preamble = "".join(f'<div class="t" lang="{l}">{items_html(parsed[l][0])}</div>' for l in ("en", "am", "om"))
    signs = "".join(sig_html(parsed[l][2], l) for l in ("en", "am", "om"))

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0b3d33">
<title>Asefa Family Constitution</title>
<link rel="stylesheet" href="assets/site.css">
<script src="assets/site.js" data-root="./" data-page="constitution"></script>
<style>
.facts {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 1.8rem 0 0; padding: 0; list-style: none; }}
.facts li {{ background: rgba(255, 246, 224, .08); border: 1px solid rgba(246, 196, 83, .35); border-radius: 14px; padding: 12px 14px; }}
.facts .k {{ display: block; font-size: .74rem; letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }}
html[data-lang="am"] .facts .k {{ letter-spacing: .03em; font-size: .85rem; }}
.facts .v {{ display: block; font-family: var(--head); font-weight: 700; font-size: 1.2rem; margin-top: 2px; }}
@media (max-width: 46rem) {{ .facts {{ grid-template-columns: 1fr 1fr; }} }}
.hero-actions {{ margin-top: 1.4rem; display: flex; gap: 10px; flex-wrap: wrap; }}
.draft {{ margin-top: .7rem; color: rgba(255, 246, 224, .75); font-size: .95rem; }}

.layout {{ display: grid; grid-template-columns: 17rem minmax(0, 1fr); gap: 22px; align-items: start; }}
.layout > * {{ min-width: 0; }}
@media (max-width: 60rem) {{ .layout {{ grid-template-columns: minmax(0, 1fr); }} }}
.toc {{ padding: 18px; position: sticky; top: 14px; }}
@media (max-width: 60rem) {{ .toc {{ position: static; }} }}
.toc ol {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 2px; }}
.toc a {{ display: flex; align-items: center; gap: 10px; text-decoration: none; color: var(--ink) !important; padding: 6px 6px; border-radius: 10px; line-height: 1.3; font-size: .98rem; }}
.toc a:hover {{ background: var(--cream); }}

.dia {{ --c: var(--green); width: 28px; height: 28px; flex: none; display: grid; place-items: center; position: relative; }}
.dia::before {{ content: ""; position: absolute; inset: 4px; background: var(--c); transform: rotate(45deg); border-radius: 3px; }}
.dia b {{ position: relative; color: #fff; font-family: var(--display); font-size: .8rem; font-weight: 700; }}
.dia.big {{ width: 58px; height: 58px; }}
.dia.big::before {{ inset: 8px; border-radius: 6px; box-shadow: 0 0 0 4px var(--cream), 0 0 0 5.5px var(--c); }}
.dia.big b {{ font-size: 1.35rem; }}

.main-col {{ display: grid; gap: 16px; }}
.preamble {{ padding: 22px 24px; background: var(--cream); border-color: #eadbb8; font-size: 1.12rem; }}
.preamble p {{ margin: 0; }}
.art {{ display: grid; grid-template-columns: 58px minmax(0, 1fr); gap: 18px; padding: 22px 24px; scroll-margin-top: 16px; }}
.art-body {{ min-width: 0; }}
@media (max-width: 34rem) {{ .art {{ grid-template-columns: minmax(0, 1fr); gap: 6px; padding: 18px; }} }}
.art h2 {{ margin: 4px 0 12px; font-family: var(--head); font-weight: 700; font-size: 1.45rem; line-height: 1.25; color: var(--green); }}
.kicker {{ display: block; font-family: var(--text); font-size: .76rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); font-weight: 600; }}
html[data-lang="am"] .kicker {{ letter-spacing: .03em; font-size: .88rem; }}
ol.clauses {{ list-style: none; margin: 0; padding: 0; counter-reset: c; display: grid; gap: 9px; }}
ol.clauses > li {{ counter-increment: c; position: relative; padding-left: 2.1rem; }}
ol.clauses > li::before {{ content: counter(c); position: absolute; left: 0; top: .1em; width: 1.5rem; height: 1.5rem; border-radius: 50%; background: var(--cream); color: var(--gold-deep); font-family: var(--display); font-weight: 700; font-size: .85rem; display: grid; place-items: center; }}
ol.clauses p {{ margin: 0; }}
ul.sub {{ list-style: none; margin: .45rem 0 .2rem; padding: 0; display: grid; gap: 5px; }}
ul.sub li {{ position: relative; padding-left: 1.1rem; }}
ul.sub li::before {{ content: ""; position: absolute; left: 0; top: .62em; width: 7px; height: 7px; background: var(--teal); transform: rotate(45deg); }}
ul.sub li:nth-child(4n+2)::before {{ background: var(--red); }} ul.sub li:nth-child(4n+3)::before {{ background: var(--gold-deep); }} ul.sub li:nth-child(4n)::before {{ background: var(--magenta); }}
.tablewrap {{ overflow-x: auto; margin: .8rem 0 .4rem; border-radius: 12px; border: 1px solid var(--line); }}
table {{ border-collapse: collapse; width: 100%; font-size: .97rem; }}
th, td {{ text-align: left; padding: .55rem .8rem; vertical-align: top; }}
thead th {{ background: var(--green); color: var(--cream); font-weight: 600; font-size: .85rem; border-bottom: 3px solid var(--gold); }}
tbody tr:nth-child(even) td {{ background: #fdf9ef; }}
td {{ border-top: 1px solid var(--line); }}
td.num {{ text-align: right; font-family: var(--display); font-weight: 700; color: var(--red); white-space: nowrap; font-variant-numeric: tabular-nums; }}
td.blank {{ min-width: 8rem; }}

.signs {{ padding: 24px; }}
.signs h3 {{ margin: 0 0 6px; font-family: var(--head); font-size: 1.4rem; color: var(--green); }}
.signs .adopted {{ color: var(--muted); }}
.posts {{ display: grid; gap: 16px; margin: 18px 0 24px; }}
.post {{ display: grid; grid-template-columns: 9rem 1fr 1fr; gap: 14px; align-items: end; }}
@media (max-width: 34rem) {{ .post {{ grid-template-columns: 1fr; gap: 6px; }} }}
.post-name {{ font-weight: 700; }}
.line {{ border-bottom: 1.5px solid var(--ink); min-height: 2rem; display: flex; align-items: flex-end; }}
.line small {{ font-size: .7rem; color: var(--muted); letter-spacing: .1em; text-transform: uppercase; }}
.signs h4 {{ margin: 0 0 8px; }}
ol.members {{ margin: 0; padding-left: 1.6rem; columns: 2; column-gap: 2rem; }}
@media (max-width: 34rem) {{ ol.members {{ columns: 1; }} }}
ol.members li {{ border-bottom: 1px solid var(--line); height: 2.1rem; break-inside: avoid; color: var(--muted); }}
@media print {{ .layout {{ display: block; }} .toc {{ display: none; }} .art {{ break-inside: avoid; box-shadow: none; }} }}
</style>
</head>
<body class="site">
<div id="site-head"></div>

<section class="hero">
  <div class="wrap">
    <div class="eyebrow">{t3("Constitution and rules", "መተዳደሪያ ደንብ", "Seera ittiin bulmaataa")}</div>
    <h1>{t3("Asefa Family Gathering", "የአሰፋ ቤተሰብ ስብሰባ", "Walgahii Maatii Asefaa")}</h1>
    <div class="draft">{t3("Draft for adoption · " + esc(DATE_EN), "ለማጽደቅ የቀረበ ረቂቅ · " + esc(DATE_AM), "Wixinee raggaasisuuf dhihaate · " + esc(DATE_OM))}</div>
    <ul class="facts">
      <li><span class="k">{t3("Meets", "ስብሰባ", "Walgahii")}</span><span class="v">{t3("Every 3 months", "በየሦስት ወሩ", "Ji'a sadii sadiin")}</span></li>
      <li><span class="k">{t3("Day", "ቀን", "Guyyaa")}</span><span class="v">{t3("First Saturday", "የመጀመሪያ ቅዳሜ", "Sanbata jalqabaa")}</span></li>
      <li><span class="k">{t3("Program", "መርሐ ግብር", "Sagantaa")}</span><span class="v">{t3("7:00 to 11:00", "ከ7፡00 እስከ 11፡00", "7:00 hanga 11:00")}</span></li>
      <li><span class="k">{t3("Contribution", "መዋጮ", "Buusii")}</span><span class="v">{t3("700 birr a month", "በወር 700 ብር", "Ji'atti Qarshii 700")}</span></li>
    </ul>
    <div class="hero-actions no-print"><a class="btn gold" href="Asefa-Family-Gathering-Constitution.pdf"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14"/></svg>{t3("Download the PDF", "PDF ያውርዱ", "PDF buusi")}</a></div>
  </div>
</section>
<div class="tibeb"></div>

<main class="section">
  <div class="wrap layout">
    <nav class="card toc" aria-label="Contents">
      <p class="label">{t3("Contents", "ማውጫ", "Qabiyyee")}</p>
      <ol>{"".join(toc)}</ol>
    </nav>
    <div class="main-col">
      <section class="card preamble">{preamble}</section>
      {"".join(arts)}
      <section class="card signs" id="signatures">{signs}</section>
    </div>
  </div>
</main>

<div id="site-foot"></div>
</body>
</html>
"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
