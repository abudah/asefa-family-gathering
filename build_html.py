#!/usr/bin/env python3
"""Build the designed HTML version of the Asefa Family Gathering Constitution.

Run:  python3 build_html.py
Output: Asefa-Family-Gathering-Constitution.html in the same folder.

The text comes from build_constitution.py (CONTENT_EN / CONTENT_AM), so edit it there
and re-run both scripts. This file only holds the page design.
"""

import html
import os
import re

from build_constitution import CONTENT_EN, CONTENT_AM, DATE_EN, DATE_AM

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Asefa-Family-Gathering-Constitution.html")

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
            m = re.match(r"^(?:Article|አንቀጽ)\s+(\d+)\.\s*(.*)$", item[1])
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
    out = [f'<div class="col {lang}" lang="{lang}">']
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
    pre_en, arts_en, sig_en = split(CONTENT_EN)
    pre_am, arts_am, sig_am = split(CONTENT_AM)
    assert len(arts_en) == len(arts_am) == 12

    toc = []
    for (n, t_en, _), (_, t_am, _) in zip(arts_en, arts_am):
        toc.append(
            f'<li><a href="#article-{n}"><span class="toc-num">{n}</span>'
            f'<span class="toc-en en">{esc(t_en)}</span>'
            f'<span class="toc-am am" lang="am">{esc(t_am)}</span></a></li>'
        )

    articles = []
    for (n, t_en, it_en), (_, t_am, it_am) in zip(arts_en, arts_am):
        articles.append(f"""
<section class="article" id="article-{n}">
  <div class="gutter"><span class="num">{n}</span><span class="geez" lang="am">{GEEZ[n - 1]}</span></div>
  <div class="col en" lang="en">
    <h2><span class="eyebrow">Article {n}</span>{esc(t_en)}</h2>
    {items_html(it_en)}
  </div>
  <div class="col am" lang="am">
    <h2><span class="eyebrow">አንቀጽ {GEEZ[n - 1]}</span>{esc(t_am)}</h2>
    {items_html(it_am)}
  </div>
</section>""")

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Asefa Family Gathering Constitution</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=Noto+Serif+Ethiopic:wght@400;600;700&display=swap">
<style>
/* Layout: a bound bilingual charter. Article number in the gutter, English and Amharic
   as parallel columns, one language at a time on a phone or by the switch. */
:root {{
  --paper: #fbfaf6;
  --ink: #1b201d;
  --muted: #5f6762;
  --line: #d6dbd4;
  --tint: #edf3ee;
  --accent: #1e5a3a;
  --brass: #a4761e;
  --display: "Fraunces", "Iowan Old Style", Georgia, serif;
  --body: "Source Serif 4", "Iowan Old Style", Georgia, serif;
  --ethiopic: "Noto Serif Ethiopic", "Kefa", "Abyssinica SIL", "Nyala", serif;
  color-scheme: light;
}}
@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
    --paper: #131614; --ink: #e9e7df; --muted: #a2aaa4; --line: #2b322d;
    --tint: #1a241e; --accent: #7fc69c; --brass: #d8ab4f; color-scheme: dark;
  }}
}}
:root[data-theme="dark"] {{
  --paper: #131614; --ink: #e9e7df; --muted: #a2aaa4; --line: #2b322d;
  --tint: #1a241e; --accent: #7fc69c; --brass: #d8ab4f; color-scheme: dark;
}}

* {{ box-sizing: border-box; }}
html {{ -webkit-text-size-adjust: 100%; }}
body {{
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font-family: var(--body);
  font-size: 1.0625rem;
  line-height: 1.6;
  padding-left: max(16px, env(safe-area-inset-left, 0px));
  padding-right: max(16px, env(safe-area-inset-right, 0px));
  padding-block: 0 4rem;
}}
[lang="am"], .am {{ font-family: var(--ethiopic); line-height: 1.75; }}
h1, h2, h3, h4 {{ font-family: var(--display); font-weight: 600; text-wrap: balance; margin: 0; }}
h2[lang="am"], .am h2, .am h3, .am h4 {{ font-family: var(--ethiopic); }}
a {{ color: var(--accent); }}
:focus-visible {{ outline: 2px solid var(--brass); outline-offset: 3px; }}

/* ---- toolbar with the language switch */
.toolbar {{
  position: sticky; top: env(safe-area-inset-top, 0px); z-index: 5;
  display: flex; align-items: center; justify-content: space-between; gap: 1rem; flex-wrap: wrap;
  margin: 0 calc(-1 * max(16px, env(safe-area-inset-left, 0px))) 0 calc(-1 * max(16px, env(safe-area-inset-right, 0px)));
  padding: .6rem max(16px, env(safe-area-inset-right, 0px)) .6rem max(16px, env(safe-area-inset-left, 0px));
  background: color-mix(in srgb, var(--paper) 88%, transparent);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid var(--line);
}}
.brand {{ font-family: var(--display); font-size: .95rem; letter-spacing: .01em; color: var(--muted); }}
.switch {{ display: inline-flex; border: 1px solid var(--line); border-radius: 999px; padding: 3px; gap: 2px; }}
.switch button {{
  font: inherit; font-size: .85rem; border: 0; background: transparent; color: var(--muted);
  padding: .3rem .85rem; border-radius: 999px; cursor: pointer;
}}
.switch button[lang="am"] {{ font-family: var(--ethiopic); }}
.switch button[aria-pressed="true"] {{ background: var(--accent); color: var(--paper); }}

main {{ max-width: 72rem; margin: 0 auto; }}

/* ---- cover */
.cover {{ padding: 4rem 0 2.5rem; border-bottom: 1px solid var(--line); }}
.cover .eyebrow {{ display: block; font-size: .8rem; letter-spacing: .14em; text-transform: uppercase; color: var(--brass); margin-bottom: 1rem; }}
.cover h1 {{ font-size: clamp(2.4rem, 6vw, 4.25rem); line-height: 1.02; font-weight: 700; font-variation-settings: "opsz" 144; letter-spacing: -.01em; }}
.cover .am-title {{ font-family: var(--ethiopic); font-size: clamp(1.6rem, 4vw, 2.6rem); line-height: 1.25; margin-top: .75rem; color: var(--accent); }}
.cover .sub {{ color: var(--muted); margin-top: 1.5rem; font-size: 1rem; }}
.cover .sub [lang="am"] {{ display: block; }}
.rule {{ height: 3px; width: 5.5rem; background: var(--brass); margin: 1.75rem 0 0; position: relative; }}
.rule::after {{ content: ""; position: absolute; left: 0; right: 0; top: 6px; height: 1px; background: var(--brass); }}

.facts {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(10rem, 1fr)); gap: 1rem 2rem; margin: 2.5rem 0 0; padding: 0; list-style: none; }}
.facts li {{ border-top: 1px solid var(--line); padding-top: .6rem; }}
.facts .k {{ display: block; font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }}
.facts .v {{ font-family: var(--display); font-size: 1.35rem; font-weight: 600; font-variant-numeric: tabular-nums; }}
.facts .v [lang="am"] {{ font-size: 1rem; font-weight: 400; color: var(--muted); display: block; }}

/* ---- contents */
.toc {{ padding: 2.5rem 0; border-bottom: 1px solid var(--line); }}
.toc h2 {{ font-size: .8rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); font-family: var(--body); font-weight: 600; margin-bottom: 1rem; }}
.toc ol {{ list-style: none; margin: 0; padding: 0; display: grid; grid-template-columns: repeat(auto-fill, minmax(18rem, 1fr)); gap: .2rem 2.5rem; }}
.toc a {{ display: grid; grid-template-columns: 2rem 1fr; column-gap: .5rem; align-items: baseline; text-decoration: none; color: var(--ink); padding: .45rem 0; border-bottom: 1px solid var(--line); }}
.toc a:hover .toc-en, .toc a:hover .toc-am {{ color: var(--accent); }}
.toc-num {{ font-family: var(--display); color: var(--brass); font-variant-numeric: tabular-nums; }}
.toc-am {{ grid-column: 2; display: block; font-size: .95rem; color: var(--muted); }}

/* ---- articles: gutter | en | am */
.article, .preamble, .signatures {{
  display: grid; grid-template-columns: 3.5rem minmax(0, 1fr); gap: 1rem 2.5rem;
  padding: 2.5rem 0; border-bottom: 1px solid var(--line);
}}
.article .col, .preamble .col, .signatures .col {{ grid-column: 2; min-width: 0; max-width: 42rem; }}
.gutter {{ grid-column: 1; grid-row: 1 / span 2; display: flex; flex-direction: column; align-items: flex-start; gap: .1rem; }}
.gutter .num {{ font-family: var(--display); font-size: 2.6rem; line-height: 1; font-weight: 700; color: var(--brass); font-variation-settings: "opsz" 144; }}
.gutter .geez {{ font-size: 1.1rem; color: var(--muted); }}
.preamble .col p {{ font-size: 1.15rem; line-height: 1.55; }}
.preamble .col[lang="am"] p {{ font-size: 1.1rem; line-height: 1.75; }}

.article h2 {{ font-size: 1.55rem; line-height: 1.2; margin-bottom: 1rem; }}
.article h2 .eyebrow {{ display: block; font-family: var(--body); font-size: .75rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); font-weight: 600; margin-bottom: .35rem; }}
.article h2[lang="am"] .eyebrow, .am h2 .eyebrow {{ font-family: var(--ethiopic); letter-spacing: .04em; text-transform: none; }}

ol.clauses {{ list-style: none; margin: 0; padding: 0; counter-reset: clause; display: flex; flex-direction: column; gap: .55rem; }}
ol.clauses > li {{ counter-increment: clause; position: relative; padding-left: 2.1rem; }}
ol.clauses > li::before {{ content: counter(clause); position: absolute; left: 0; top: .05em; font-family: var(--display); font-weight: 600; color: var(--brass); font-variant-numeric: tabular-nums; }}
ol.clauses p {{ margin: 0; }}
ul.sub {{ margin: .4rem 0 .2rem; padding: 0 0 0 1.1rem; list-style: none; display: flex; flex-direction: column; gap: .3rem; }}
ul.sub li {{ position: relative; padding-left: .9rem; }}
ul.sub li::before {{ content: ""; position: absolute; left: 0; top: .72em; width: 5px; height: 5px; background: var(--accent); }}

.tablewrap {{ overflow-x: auto; margin: .8rem 0 .4rem; }}
table {{ border-collapse: collapse; width: 100%; font-size: .95rem; }}
th, td {{ text-align: left; padding: .5rem .7rem; border-bottom: 1px solid var(--line); vertical-align: top; }}
thead th {{ background: var(--tint); font-weight: 600; font-size: .8rem; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); border-bottom: 2px solid var(--accent); }}
[lang="am"] thead th {{ text-transform: none; letter-spacing: .02em; font-size: .9rem; }}
td.num {{ font-variant-numeric: tabular-nums; text-align: right; white-space: nowrap; }}
td.blank {{ min-width: 8rem; background: repeating-linear-gradient(to right, transparent 0 6px, var(--line) 6px 9px) bottom / 100% 1px no-repeat; }}

/* ---- signatures */
.signatures h3 {{ font-size: 1.35rem; margin-bottom: .5rem; }}
.signatures .adopted {{ color: var(--muted); }}
.posts {{ display: flex; flex-direction: column; gap: 1.2rem; margin: 1.5rem 0 2rem; }}
.post {{ display: grid; grid-template-columns: 8rem 1fr 1fr; gap: 1rem; align-items: end; }}
.post-name {{ font-weight: 600; }}
.line {{ border-bottom: 1px solid var(--ink); min-height: 1.8rem; display: flex; align-items: flex-end; }}
.line small {{ font-size: .7rem; color: var(--muted); letter-spacing: .08em; text-transform: uppercase; }}
[lang="am"] .line small {{ text-transform: none; letter-spacing: 0; }}
.signatures h4 {{ font-size: 1rem; margin-bottom: .6rem; }}
ol.members {{ margin: 0; padding: 0 0 0 1.6rem; columns: 2; column-gap: 2.5rem; }}
ol.members li {{ border-bottom: 1px solid var(--line); height: 2rem; break-inside: avoid; color: var(--muted); font-variant-numeric: tabular-nums; }}

footer {{ color: var(--muted); font-size: .85rem; padding-top: 2rem; max-width: 72rem; margin: 0 auto; }}

/* ---- two-column mode on wide screens, when both languages are shown */
@media (min-width: 64rem) {{
  body[data-lang="both"] .article, body[data-lang="both"] .preamble, body[data-lang="both"] .signatures {{
    grid-template-columns: 3.5rem minmax(0, 1fr) minmax(0, 1fr);
  }}
  body[data-lang="both"] .col.en {{ grid-column: 2; }}
  body[data-lang="both"] .col.am {{ grid-column: 3; }}
  body[data-lang="both"] .gutter {{ grid-row: 1; }}
}}
body[data-lang="en"] .am, body[data-lang="en"] .toc-am {{ display: none; }}
body[data-lang="am"] .en, body[data-lang="am"] .toc-en {{ display: none; }}
body[data-lang="am"] .toc-am {{ grid-column: 2; color: var(--ink); font-size: 1.05rem; }}
@media (max-width: 40rem) {{
  .gutter {{ flex-direction: row; align-items: baseline; gap: .6rem; grid-row: auto; grid-column: 1 / -1; }}
  .article, .preamble, .signatures {{ grid-template-columns: 1fr; gap: .5rem; }}
  .article .col, .preamble .col, .signatures .col {{ grid-column: 1; }}
  .post {{ grid-template-columns: 1fr; gap: .4rem; }}
  ol.members {{ columns: 1; }}
  .cover {{ padding-top: 2.5rem; }}
  .facts {{ grid-template-columns: 1fr 1fr; gap: 1rem 1.25rem; }}
  .facts .v {{ font-size: 1.15rem; }}
}}
@media (prefers-reduced-motion: no-preference) {{
  html {{ scroll-behavior: smooth; }}
}}
@media print {{
  .toolbar {{ display: none; }}
  body {{ font-size: 10.5pt; padding: 0; background: #fff; color: #111; }}
  .cover {{ page-break-after: always; border: 0; padding-top: 30vh; }}
  .article {{ break-inside: avoid; }}
  .signatures {{ page-break-before: always; }}
  a {{ color: inherit; text-decoration: none; }}
}}
</style>
</head>
<body data-lang="both">

<header class="toolbar">
  <span class="brand">Asefa Family Gathering &middot; <span lang="am">የአሰፋ ቤተሰብ ስብሰባ</span></span>
  <div class="switch" role="group" aria-label="Language">
    <button type="button" id="lang-both" data-lang="both" aria-pressed="true">Both</button>
    <button type="button" id="lang-en" data-lang="en" aria-pressed="false">English</button>
    <button type="button" id="lang-am" data-lang="am" lang="am" aria-pressed="false">አማርኛ</button>
  </div>
</header>

<main>
<section class="cover">
  <span class="eyebrow">Constitution and Rules &middot; <span lang="am">መተዳደሪያ ደንብ</span></span>
  <h1>Asefa Family Gathering</h1>
  <div class="am-title" lang="am">የአሰፋ ቤተሰብ ስብሰባ</div>
  <div class="rule"></div>
  <p class="sub">Draft for adoption &middot; {esc(DATE_EN)}<span lang="am">ለማጽደቅ የቀረበ ረቂቅ &middot; {esc(DATE_AM)}</span></p>
  <ul class="facts">
    <li><span class="k">Meets</span><span class="v">Every 3 months <span lang="am">በየሦስት ወሩ</span></span></li>
    <li><span class="k">Day</span><span class="v">First Saturday <span lang="am">የመጀመሪያ ቅዳሜ</span></span></li>
    <li><span class="k">Program</span><span class="v">7:00 to 11:00 <span lang="am">ከ7፡00 እስከ 11፡00</span></span></li>
    <li><span class="k">Contribution</span><span class="v">700 birr / month <span lang="am">በወር 700 ብር</span></span></li>
  </ul>
</section>

<nav class="toc" aria-label="Contents">
  <h2>Contents &middot; <span lang="am">ማውጫ</span></h2>
  <ol>{"".join(toc)}</ol>
</nav>

<section class="preamble">
  <div class="gutter" aria-hidden="true"></div>
  <div class="col en" lang="en">{items_html(pre_en)}</div>
  <div class="col am" lang="am">{items_html(pre_am)}</div>
</section>
{"".join(articles)}

<section class="signatures" id="signatures">
  <div class="gutter" aria-hidden="true"></div>
  {sig_html(sig_en, "en")}
  {sig_html(sig_am, "am")}
</section>
</main>

<footer>
  <p>Asefa Family Gathering &middot; Constitution and Rules &middot; Draft, {esc(DATE_EN)}. Amendments follow Article 12.</p>
</footer>

<script>
(function () {{
  var body = document.body;
  var buttons = document.querySelectorAll('.switch button');
  function apply(lang) {{
    body.setAttribute('data-lang', lang);
    buttons.forEach(function (b) {{ b.setAttribute('aria-pressed', String(b.dataset.lang === lang)); }});
    try {{ localStorage.setItem('asefa-lang', lang); }} catch (e) {{}}
  }}
  buttons.forEach(function (b) {{ b.addEventListener('click', function () {{ apply(b.dataset.lang); }}); }});
  var saved = null;
  try {{ saved = localStorage.getItem('asefa-lang'); }} catch (e) {{}}
  if (saved === 'en' || saved === 'am' || saved === 'both') apply(saved);
}})();
</script>
</body>
</html>
"""
    # Same page twice: the named file, and index.html for GitHub Pages.
    for path in (OUT, os.path.join(HERE, "index.html")):
        with open(path, "w", encoding="utf-8") as f:
            f.write(page)
        print("Wrote", path)


if __name__ == "__main__":
    build()
