#!/usr/bin/env python3
"""Build the designed PDF of the Asefa Family Gathering Constitution.

Run:  python3 build_pdf.py
Output: Asefa-Family-Gathering-Constitution.pdf in the same folder.

The text comes from build_constitution.py (CONTENT_EN / CONTENT_AM / CONTENT_OM).
This script lays it out as a print page (fonts from the local fonts/ folder) and
prints it to PDF with Google Chrome in headless mode, so no internet is needed.
"""

import os
import subprocess
import sys

from build_constitution import CONTENT_EN, CONTENT_AM, CONTENT_OM, DATE_EN, DATE_AM, DATE_OM
from build_html import split, items_html, esc, GEEZ

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Asefa-Family-Gathering-Constitution.pdf")
PRINT_HTML = os.path.join(HERE, "_print.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

LANGS = [
    {
        "code": "en", "content": CONTENT_EN, "letter": "A", "kicker": "Part A",
        "name": "English", "contents": "Contents",
        "article": lambda n: f"Article {n}",
    },
    {
        "code": "am", "content": CONTENT_AM, "letter": "ለ", "kicker": "ክፍል ለ",
        "name": "አማርኛ", "contents": "ማውጫ",
        "article": lambda n: f"አንቀጽ {GEEZ[n - 1]}",
    },
    {
        "code": "om", "content": CONTENT_OM, "letter": "C", "kicker": "Kutaa C",
        "name": "Afaan Oromoo", "contents": "Qabiyyee",
        "article": lambda n: f"Keewwata {n}",
    },
]


def family_tree_svg():
    """Three generations: Asefa, our parents, the grandchildren who gather."""
    W, x0 = 300, 150
    mids = [40, 95, 150, 205, 260]
    kids = [18 + i * 24.4 for i in range(12)]
    parts = [f'<svg class="tree" viewBox="0 0 {W} 150" role="img" aria-label="Three generations of the Asefa family">']
    parts.append('<g stroke="currentColor" stroke-width="0.9" fill="none" opacity="0.7">')
    for m in mids:
        parts.append(f'<path d="M{x0} 22 V40 H{m} V58"/>')
    for i, k in enumerate(kids):
        m = mids[min(i * 5 // 12, 4)]
        parts.append(f'<path d="M{m} 66 V84 H{k:.1f} V102"/>')
    parts.append("</g>")
    parts.append(f'<circle cx="{x0}" cy="14" r="8" fill="currentColor"/>')
    for m in mids:
        parts.append(f'<circle cx="{m}" cy="62" r="5" fill="currentColor" opacity="0.85"/>')
    for k in kids:
        parts.append(f'<circle cx="{k:.1f}" cy="106" r="3.6" fill="currentColor" opacity="0.7"/>')
    parts.append('<text x="150" y="134" text-anchor="middle" class="tree-label">'
                 'Asefa &middot; our parents &middot; us, the grandchildren</text>')
    parts.append("</svg>")
    return "".join(parts)


def part_html(lang):
    pre, arts, sig = split(lang["content"])
    code = lang["code"]
    toc = "".join(
        f'<li><span class="toc-n">{n}</span><span class="toc-t">{esc(t)}</span></li>'
        for n, t, _ in arts
    )
    body = []
    for n, title, items in arts:
        body.append(f"""
<article class="art">
  <header class="art-head">
    <div class="art-num"><span class="n">{n}</span><span class="g" lang="am">{GEEZ[n - 1]}</span></div>
    <h2><span class="eyebrow">{esc(lang["article"](n))}</span>{esc(title)}</h2>
  </header>
  <div class="art-body">{items_html(items)}</div>
</article>""")

    posts = "".join(
        f'<div class="post"><span class="post-name">{esc(p)}</span>'
        f'<span class="line"><small>{esc(sig["cols"][1])}</small></span>'
        f'<span class="line"><small>{esc(sig["cols"][2])}</small></span></div>'
        for p in sig["posts"]
    )
    members = "".join(f"<li><span>{i}</span></li>" for i in range(1, 21))

    return f"""
<section class="part part-{code}" lang="{code}">
  <header class="opener">
    <div class="kicker">{esc(lang["kicker"])}</div>
    <div class="letter">{esc(lang["letter"])}</div>
    <h1 class="part-name">{esc(lang["name"])}</h1>
    <div class="rule"></div>
    <h3 class="toc-h">{esc(lang["contents"])}</h3>
    <ol class="toc">{toc}</ol>
  </header>
  <div class="preamble">{items_html(pre)}</div>
  {"".join(body)}
  <section class="sign">
    <h2 class="sign-h">{esc(sig["title"])}</h2>
    <p class="adopted">{esc(sig["line"])}</p>
    <div class="posts">{posts}</div>
    <h3 class="members-h">{esc(sig["members"])}</h3>
    <ol class="members">{members}</ol>
  </section>
</section>"""


CSS = r"""
/* Print layout: a bound family charter. Full-colour cover, one part per language,
   article numbers hung in the left margin, brass for numbering, green for structure. */
:root {
  --ink: #1b201d;
  --muted: #5f6762;
  --line: #d9ddd6;
  --tint: #eef3ef;
  --green: #1e5a3a;
  --green-deep: #173f2a;
  --brass: #a4761e;
  --brass-light: #dcb468;
  --cream: #f5efdf;
  --display: "Fraunces", Georgia, serif;
  --body: "Source Serif 4", Georgia, serif;
  --ethiopic: "Noto Serif Ethiopic", "Kefa", serif;
}
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; padding: 0; background: #fff; color: var(--ink); }
body { font-family: var(--body); font-size: 10pt; line-height: 1.5; font-variant-numeric: lining-nums; }
[lang="am"] { font-family: var(--ethiopic); }
h1, h2, h3 { margin: 0; font-weight: 600; }

@page {
  size: A4;
  margin: 20mm 18mm 22mm 18mm;
  @bottom-left { content: "Asefa Family Gathering"; font-family: "Source Serif 4", serif; font-size: 7.5pt; color: #5f6762; vertical-align: top; padding-top: 6mm; }
  @bottom-right { content: counter(page); font-family: "Fraunces", serif; font-weight: 600; font-size: 9pt; color: #a4761e; vertical-align: top; padding-top: 5.6mm; }
}
@page cover { margin: 0; @bottom-left { content: none; } @bottom-right { content: none; } }
@page opener { @bottom-left { content: none; } @bottom-right { content: none; } }
@page en { @bottom-left { content: "Asefa Family Gathering  ·  Constitution and Rules"; } }
@page am { @bottom-left { content: "የአሰፋ ቤተሰብ ስብሰባ  ·  መተዳደሪያ ደንብ"; font-family: "Noto Serif Ethiopic", serif; } }
@page om { @bottom-left { content: "Walgahii Maatii Asefaa  ·  Seera Ittiin Bulmaataa"; } }

/* ---------- cover */
.cover {
  page: cover;
  width: 210mm; height: 296.6mm; overflow: hidden;
  position: relative;
  background: var(--green);
  background-image: radial-gradient(120% 70% at 85% 0%, #24704a 0%, transparent 60%);
  color: var(--cream);
  padding: 30mm 24mm 26mm;
  display: flex; flex-direction: column;
  break-after: page;
}
.cover::before { content: ""; position: absolute; inset: 9mm; border: 0.6pt solid rgba(220, 180, 104, .55); pointer-events: none; }
.cover::after { content: ""; position: absolute; inset: 10.4mm; border: 0.3pt solid rgba(220, 180, 104, .3); pointer-events: none; }
.cover .eyebrow { font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; color: var(--brass-light); }
.cover .eyebrow span { letter-spacing: .05em; text-transform: none; }
.cover .titles { margin-top: 26mm; }
.cover h1 { font-family: var(--display); font-weight: 700; font-size: 50pt; line-height: .98; letter-spacing: -.012em; font-variation-settings: "opsz" 144; max-width: 150mm; }
.cover .t-am { font-family: var(--ethiopic); font-size: 27pt; line-height: 1.3; margin-top: 6mm; color: var(--brass-light); font-weight: 600; }
.cover .t-om { font-family: var(--display); font-style: italic; font-size: 20pt; margin-top: 1.5mm; color: rgba(245, 239, 223, .82); }
.cover .double { width: 26mm; height: 4.2pt; border-top: 2pt solid var(--brass-light); border-bottom: .6pt solid var(--brass-light); margin: 9mm 0 0; }
.cover .tree { width: 92mm; color: var(--brass-light); margin: auto 0 0 auto; display: block; }
.cover .tree-label { font-family: var(--body); font-size: 7.4px; fill: rgba(245, 239, 223, .75); letter-spacing: .04em; }
.cover .facts { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0 6mm; margin-top: 12mm; padding-top: 4mm; border-top: .5pt solid rgba(245, 239, 223, .35); list-style: none; padding-left: 0; }
.cover .facts .k { display: block; font-size: 6.8pt; letter-spacing: .16em; text-transform: uppercase; color: var(--brass-light); }
.cover .facts .v { display: block; font-family: var(--display); font-size: 12.5pt; font-weight: 600; margin-top: 1mm; }
.cover .facts .s { display: block; font-size: 8pt; color: rgba(245, 239, 223, .75); line-height: 1.45; }
.cover .facts .s[lang="om"] { font-style: italic; }
.cover .draft { margin-top: 8mm; font-size: 8pt; color: rgba(245, 239, 223, .75); line-height: 1.6; }

/* ---------- part opener */
.part-en { page: en; } .part-am { page: am; } .part-om { page: om; }
.opener { page: opener; break-before: page; break-after: page; padding-top: 22mm; }
.opener .kicker { font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); }
.part-am .opener .kicker { letter-spacing: .04em; }
.opener .letter { font-family: var(--display); font-size: 96pt; line-height: 1; font-weight: 700; color: var(--brass); margin-top: 4mm; font-variation-settings: "opsz" 144; }
.part-am .opener .letter { font-family: var(--ethiopic); font-size: 80pt; }
.opener .part-name { font-family: var(--display); font-size: 30pt; line-height: 1.1; margin-top: 2mm; color: var(--green); }
.part-am .opener .part-name { font-family: var(--ethiopic); }
.opener .rule { width: 26mm; height: 4.2pt; border-top: 2pt solid var(--brass); border-bottom: .6pt solid var(--brass); margin: 8mm 0 14mm; }
.opener .toc-h { font-family: var(--body); font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); font-weight: 600; margin-bottom: 4mm; }
.part-am .opener .toc-h { font-family: var(--ethiopic); letter-spacing: .04em; font-size: 9pt; }
.toc { list-style: none; margin: 0; padding: 0; columns: 2; column-gap: 12mm; }
.toc li { display: grid; grid-template-columns: 9mm 1fr; align-items: baseline; padding: 2.4mm 0; border-bottom: .5pt solid var(--line); break-inside: avoid; font-size: 10.5pt; }
.toc-n { font-family: var(--display); font-weight: 600; color: var(--brass); }

/* ---------- body */
.preamble { font-size: 11.2pt; line-height: 1.55; padding: 0 0 6mm 20mm; border-bottom: .5pt solid var(--line); }
.preamble p { margin: 0; }
.preamble::first-line { font-variant: small-caps; letter-spacing: .03em; }
.part-am .preamble { font-size: 10.6pt; line-height: 1.75; }
.part-am .preamble::first-line { font-variant: normal; letter-spacing: 0; }

.art { padding: 6mm 0 5mm; border-bottom: .5pt solid var(--line); }
.art-head { display: grid; grid-template-columns: 14mm 1fr; column-gap: 6mm; align-items: start; break-inside: avoid; break-after: avoid; page-break-after: avoid; }
.art-body { padding-left: 20mm; }
.art-body > ol.clauses > li:first-child { break-before: avoid; }
.art-num { display: flex; flex-direction: column; align-items: flex-start; }
.art-num .n { font-family: var(--display); font-weight: 700; font-size: 26pt; line-height: .95; color: var(--brass); font-variation-settings: "opsz" 144; }
.art-num .g { font-family: var(--ethiopic); font-size: 10pt; color: var(--muted); margin-top: 1mm; }
.art h2 { font-family: var(--display); font-size: 14.5pt; line-height: 1.2; color: var(--ink); margin-bottom: 3mm; break-after: avoid; }
.part-am .art h2 { font-family: var(--ethiopic); font-size: 13.5pt; }
.art h2 .eyebrow { display: block; font-family: var(--body); font-size: 7pt; letter-spacing: .18em; text-transform: uppercase; color: var(--muted); font-weight: 600; margin-bottom: 1mm; }
.part-am .art h2 .eyebrow { font-family: var(--ethiopic); letter-spacing: .04em; font-size: 8pt; }

ol.clauses { list-style: none; margin: 0; padding: 0; counter-reset: c; }
ol.clauses > li { counter-increment: c; position: relative; padding-left: 6.5mm; margin: 0 0 1.8mm; break-inside: avoid; }
ol.clauses > li::before { content: counter(c); position: absolute; left: 0; top: 0; font-family: var(--display); font-weight: 600; color: var(--brass); font-size: 9.5pt; }
ol.clauses p { margin: 0; }
.part-am ol.clauses > li { line-height: 1.72; font-size: 9.6pt; }
ul.sub { list-style: none; margin: 1.2mm 0 .4mm; padding: 0; }
ul.sub li { position: relative; padding-left: 4.2mm; margin-bottom: 1mm; }
ul.sub li::before { content: ""; position: absolute; left: .4mm; top: .62em; width: 1.6mm; height: 1.6mm; background: var(--green); }
.part-am ul.sub li::before { top: .8em; }

.tablewrap { margin: 2.5mm 0 3mm; break-inside: avoid; }
table { width: 100%; border-collapse: collapse; font-size: 9pt; line-height: 1.38; }
thead th { text-align: left; background: var(--tint); color: var(--green); font-weight: 600; font-size: 7.4pt; letter-spacing: .12em; text-transform: uppercase; padding: 2mm 2.4mm; border-bottom: 1.1pt solid var(--green); }
.part-am thead th { letter-spacing: .02em; text-transform: none; font-size: 8.6pt; }
td { padding: 1.7mm 2.4mm; border-bottom: .5pt solid var(--line); vertical-align: top; }
td:first-child { font-variant-numeric: tabular-nums; }
td.num { text-align: right; font-family: var(--display); font-weight: 600; font-variant-numeric: tabular-nums; white-space: nowrap; color: var(--green); }
td.blank { min-width: 34mm; }
tr > td:nth-child(2):last-child:not(.blank) { text-align: right; }
td.blank::after { content: ""; display: block; border-bottom: .6pt dotted var(--muted); height: 3.6mm; }

/* ---------- signatures */
.sign { break-before: page; }
.sign-h { font-family: var(--display); font-size: 22pt; color: var(--green); }
.part-am .sign-h { font-family: var(--ethiopic); font-size: 19pt; }
.adopted { color: var(--muted); margin: 3mm 0 10mm; }
.posts { display: grid; gap: 7mm; margin-bottom: 12mm; }
.post { display: grid; grid-template-columns: 40mm 1fr 1fr; gap: 6mm; align-items: end; }
.post-name { font-weight: 600; font-family: var(--display); font-size: 11pt; }
.part-am .post-name { font-family: var(--ethiopic); font-size: 10.5pt; }
.line { border-bottom: .7pt solid var(--ink); height: 9mm; position: relative; }
.line small { position: absolute; left: 0; top: calc(100% + 1mm); font-size: 6.6pt; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.part-am .line small { letter-spacing: 0; font-size: 7.4pt; }
.members-h { font-family: var(--body); font-size: 8pt; letter-spacing: .2em; text-transform: uppercase; color: var(--muted); margin-bottom: 2mm; }
.part-am .members-h { font-family: var(--ethiopic); letter-spacing: .04em; font-size: 9pt; }
ol.members { list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 12mm; }
ol.members li { height: 9.6mm; border-bottom: .5pt solid var(--line); display: flex; align-items: flex-end; padding-bottom: 1mm; break-inside: avoid; }
ol.members li span { font-family: var(--display); font-size: 8.5pt; color: var(--brass); width: 7mm; }
"""


def build():
    cover = f"""
<section class="cover">
  <div class="eyebrow">Constitution and Rules &nbsp;·&nbsp; <span lang="am">መተዳደሪያ ደንብ</span> &nbsp;·&nbsp; Seera Ittiin Bulmaataa</div>
  <div class="titles">
    <h1>Asefa Family Gathering</h1>
    <div class="t-am" lang="am">የአሰፋ ቤተሰብ ስብሰባ</div>
    <div class="t-om" lang="om">Walgahii Maatii Asefaa</div>
    <div class="double"></div>
  </div>
  {family_tree_svg()}
  <ul class="facts">
    <li><span class="k">Meets</span><span class="v">Every 3 months</span><span class="s" lang="am">በየሦስት ወሩ</span><span class="s" lang="om">Ji'a sadii sadiin</span></li>
    <li><span class="k">Day</span><span class="v">First Saturday</span><span class="s" lang="am">የመጀመሪያ ቅዳሜ</span><span class="s" lang="om">Sanbata jalqabaa</span></li>
    <li><span class="k">Program</span><span class="v">7:00 to 11:00</span><span class="s" lang="am">ከ7፡00 እስከ 11፡00</span><span class="s" lang="om">7:00 hanga 11:00</span></li>
    <li><span class="k">Contribution</span><span class="v">700 birr a month</span><span class="s" lang="am">በወር 700 ብር</span><span class="s" lang="om">Ji'atti Qarshii 700</span></li>
  </ul>
  <div class="draft">
    Draft for adoption &middot; {esc(DATE_EN)}<br>
    <span lang="am">ለማጽደቅ የቀረበ ረቂቅ &middot; {esc(DATE_AM)}</span><br>
    <span lang="om">Wixinee raggaasisuuf dhihaate &middot; {esc(DATE_OM)}</span>
  </div>
</section>"""

    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Asefa Family Gathering Constitution</title>
<link rel="stylesheet" href="fonts/fonts.css">
<style>{CSS}</style>
</head>
<body>
{cover}
{"".join(part_html(l) for l in LANGS)}
</body>
</html>
"""
    with open(PRINT_HTML, "w", encoding="utf-8") as f:
        f.write(page)

    if not os.path.exists(CHROME):
        sys.exit("Google Chrome was not found at " + CHROME)
    subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
         "--virtual-time-budget=15000", "--run-all-compositor-stages-before-draw",
         f"--print-to-pdf={OUT}", "file://" + PRINT_HTML],
        check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    os.remove(PRINT_HTML)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
