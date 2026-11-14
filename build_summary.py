#!/usr/bin/env python3
"""Builds the short version of the constitution: the main points only,
one A4 page each in English, Amharic and Afaan Oromo.

Run:  python3 build_summary.py
Out:  Asefa-Family-Gathering-Constitution-Summary.pdf
Uses Google Chrome in headless mode and the local fonts in fonts/.
"""
import html
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "Asefa-Family-Gathering-Constitution-Summary.pdf")
TMP = os.path.join(HERE, "_summary.html")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGES = [
    {
        "lang": "en",
        "kicker": "Asefa Family Gathering",
        "title": "The Constitution in Brief",
        "sub": "The main points, for reading together at the gathering.",
        "points": [
            ("Who we are", "The grandchildren of Asefa aged 18 and over. Husbands and wives are welcome, may speak and may co-host, but do not pay or vote."),
            ("Our purpose", "To stay one family, let the cousins grow up together, support one another in joy and hardship, and honour the memory of Asefa."),
            ("When we meet", "Every three months, on the first Saturday, from 7:00 to 11:00. We start at 7:00 sharp. Nobody waits for anybody."),
            ("No rescheduling", "The program cannot be rescheduled without a probable cause. Only a death, a major holiday or a national event moves the date, announced two weeks ahead."),
            ("Hosting", "Married members host at home in the order drawn by lottery. A swap needs one month's notice. Hosting is not a competition."),
            ("The committee", "Leader, Deputy Leader, Secretary and Treasurer, elected for two years."),
            ("Contribution", "700 birr every month, paid by the 10th. More than 30 days late adds 100 birr a month. The fund is only for serious illness, a death in close family, emergency loans and family events."),
            ("Attendance", "Attending is a duty. If you cannot come, tell the Secretary three days before. Only sudden, serious events are excused. Only members living outside Ethiopia are excused from attending; they join by video."),
            ("Fines", None),
            ("Conduct", "We speak with respect: no insults, no shouting. Phones on silent. No political or religious debates. What is shared in confidence stays in the family."),
            ("Decisions", "Valid when more than half of the members are present. The majority decides. Changing money, fines or this constitution needs two-thirds."),
            ("Disputes", "1. Talk privately. 2. Tell the committee, in writing or by word of mouth. 3. The full Gathering. 4. A family elder, whose word is final. Taking it to social media or outsiders: 1,000 birr."),
        ],
        "fines_head": ("Situation", "Birr"),
        "fines": [
            ("Absent without notice", "2,000"),
            ("Absent, with notice 3 days before", "1,000"),
            ("Late by more than 30 minutes", "200"),
            ("Disturbing after a warning", "500"),
            ("Host cancelling with under a month's notice", "1,000"),
        ],
        "foot": "This is a summary. The full constitution is the official text.",
    },
    {
        "lang": "am",
        "kicker": "የአሰፋ ቤተሰብ ስብሰባ",
        "title": "መተዳደሪያ ደንቡ በአጭሩ",
        "sub": "በስብሰባው ላይ አብረን የምናነባቸው ዋና ዋና ነጥቦች።",
        "points": [
            ("እኛ ማን ነን", "ዕድሜያቸው 18 የሞላ የአሰፋ የልጅ ልጆች። ባል ወይም ሚስት እንኳን ደህና መጡ፤ ይናገራሉ፣ አብረው ያስተናግዳሉ፤ ግን መዋጮ አይከፍሉም፣ ድምፅ አይሰጡም።"),
            ("ዓላማችን", "አንድ ቤተሰብ ሆኖ መቆየት፣ የአጎትና የአክስት ልጆች አብረው እንዲያድጉ ማድረግ፣ በደስታም በችግርም መደጋገፍ፣ የአሰፋን መታሰቢያ ማክበር።"),
            ("መቼ እንገናኛለን", "በየሦስት ወሩ፣ የወሩ የመጀመሪያ ቅዳሜ፣ ከ7፡00 እስከ 11፡00። በ7፡00 በትክክል እንጀምራለን፤ ማንም ማንንም አይጠብቅም።"),
            ("ቀን አይቀየርም", "ፕሮግራሙ በቂና ተጨባጭ ምክንያት ሳይኖር ወደ ሌላ ቀን አይዛወርም። ቀኑ የሚቀየረው ለሞት፣ ለትልቅ በዓል ወይም ለአገራዊ ጉዳይ ብቻ ሲሆን ከሁለት ሳምንት በፊት ይነገራል።"),
            ("ማስተናገድ", "ያገቡ አባላት በዕጣ በወጣው ቅደም ተከተል በቤታቸው ያስተናግዳሉ። ተራ ለመለዋወጥ ከአንድ ወር በፊት ይነገራል። ማስተናገድ ውድድር አይደለም።"),
            ("ኮሚቴው", "መሪ፣ ምክትል መሪ፣ ጸሐፊ እና ገንዘብ ያዥ፤ ለሁለት ዓመት ይመረጣሉ።"),
            ("መዋጮ", "በየወሩ 700 ብር፣ እስከ ወሩ 10ኛ ቀን። ከ30 ቀን በላይ ከዘገየ በወር 100 ብር ይጨመራል። ገንዘቡ የሚውለው ለከባድ ሕመም፣ ለቅርብ ቤተሰብ ሞት፣ ለአስቸኳይ ብድር እና ለቤተሰብ ዝግጅት ብቻ ነው።"),
            ("መገኘት", "መገኘት ግዴታ ነው። መምጣት ካልቻሉ ከሦስት ቀን በፊት ለጸሐፊው ያሳውቁ። የሚታለፈው ድንገተኛና ከባድ ሁኔታ ብቻ ነው። ከመገኘት ነጻ የሆኑት ከኢትዮጵያ ውጭ የሚኖሩ አባላት ብቻ ናቸው፤ በቪዲዮ ይሳተፋሉ።"),
            ("ቅጣቶች", None),
            ("ሥነ ምግባር", "በአክብሮት እንነጋገራለን፤ ስድብና ጩኸት የለም። ስልኮች ድምፅ አልባ ይሆናሉ። የፖለቲካና የሃይማኖት ክርክር አይፈቀድም። በሚስጥር የተነገረ በቤተሰቡ ውስጥ ይቀራል።"),
            ("ውሳኔ", "ውሳኔ የሚጸናው ከአባላት ከግማሽ በላይ ሲገኙ ነው። አብላጫ ድምፅ ይወስናል። መዋጮን፣ ቅጣትን ወይም ይህን ደንብ ለመቀየር ሁለት ሦስተኛ ያስፈልጋል።"),
            ("አለመግባባት", "1. በግል መነጋገር። 2. ለኮሚቴው በጽሑፍ ወይም በቃል ማቅረብ። 3. ለሙሉ ስብሰባው። 4. ቃሉ የመጨረሻ ለሆነ የቤተሰብ ሽማግሌ። ጉዳዩን ወደ ማኅበራዊ ሚዲያ ወይም ወደ ውጭ ሰው መውሰድ 1,000 ብር ያስቀጣል።"),
        ],
        "fines_head": ("ሁኔታ", "ብር"),
        "fines": [
            ("ሳያሳውቁ መቅረት", "2,000"),
            ("ከ3 ቀን በፊት አሳውቆ መቅረት", "1,000"),
            ("ከ30 ደቂቃ በላይ መዘግየት", "200"),
            ("ከማስጠንቀቂያ በኋላ መረበሽ", "500"),
            ("አስተናጋጅ ከአንድ ወር ባነሰ ማስታወቂያ ተራውን መሰረዝ", "1,000"),
        ],
        "foot": "ይህ አጭር ማጠቃለያ ነው። ሙሉው መተዳደሪያ ደንብ ይፋዊው ጽሑፍ ነው።",
    },
    {
        "lang": "om",
        "kicker": "Walgahii Maatii Asefaa",
        "title": "Seera Ittiin Bulmaataa Gabaabinaan",
        "sub": "Qabxiilee ijoo walgahii irratti waliin dubbifnu.",
        "points": [
            ("Eenyu faana", "Ilmaan ijoollee Asefaa umuriin isaanii waggaa 18 guute. Abbaan manaa yookiin haati manaa ni simatamu, ni dubbatu, waliin ni keessummeessu; garuu buusii hin kaffalan, sagalee hin kennan."),
            ("Kaayyoo keenya", "Maatii tokko ta'anii turuu, ijoolleen obboleeyyanii waliin akka guddatan gochuu, yeroo gammachuu fi rakkinaa wal gargaaruu, yaadannoo Asefaa kabajuu."),
            ("Yoom walgahna", "Ji'a sadii sadiin, Sanbata jalqabaa ji'ichaa, 7:00 hanga 11:00. Sirriitti 7:00 jalqabna. Namni tokko illee nama biraa hin eegu."),
            ("Guyyaan hin jijjiiramu", "Sagantaan sababa ga'aa fi qabatamaa malee guyyaa biraatti hin jijjiiramu. Guyyaan kan jijjiiramu du'a, ayyaana guddaa yookiin dhimma biyyaaleessaa qofaaf, torban lama dura beeksifama."),
            ("Keessummeessuu", "Miseensonni fuudhanii fi heeruman tartiiba carraadhaan ba'een mana isaaniitti keessummeessu. Dabaree wal jijjiiruuf ji'a tokko dura beeksisu. Keessummeessuun dorgommii miti."),
            ("Koree", "Dura Taa'aa, Itti Aanaa Dura Taa'aa, Barreessaa fi Qabduu Maallaqaa; waggaa lamaaf filatamu."),
            ("Buusii", "Ji'a ji'aan Qarshii 700, hanga guyyaa 10ffaatti. Guyyaa 30 ol yoo ture ji'atti Qarshii 100 dabalama. Maallaqni dhukkuba cimaa, du'a maatii dhihoo, liqii hatattamaa fi sagantaa maatii qofaaf oola."),
            ("Argamuu", "Argamuun dirqama. Dhufuu yoo hin dandeenye guyyaa sadii dura barreessaaf beeksisi. Kan fudhatama qabu taatee tasaa fi cimaa qofa. Miseensota Itoophiyaa alaa jiraatan qofatu argamuu irraa bilisa; viidiyootiin hirmaatu."),
            ("Adabbii", None),
            ("Naamusa", "Kabajaan wal dubbifna; arrabsoo fi iyya hin jiru. Bilbilli sagalee malee ta'a. Falmiin siyaasaa fi amantii hin hayyamamu. Wanti iccitiidhaan qoodame maatii keessatti hafa."),
            ("Murtee", "Murteen kan raggaasifamu miseensota walakkaa ol yoo argaman. Sagaleen caalmaa murteessa. Buusii, adabbii yookiin seera kana jijjiiruuf sadii keessaa lama barbaachisa."),
            ("Wal-dhabdee", "1. Dhuunfaatti wal dubbachuu. 2. Koreef barreeffamaan yookiin afaaniin dhiheessuu. 3. Walgahii guutuu. 4. Jaarsa maatii, jechi isaa isa dhumaa. Gara miidiyaa hawaasummaa yookiin namoota alaatti geessuun Qarshii 1,000 adabsiisa."),
        ],
        "fines_head": ("Haala", "Qarshii"),
        "fines": [
            ("Osoo hin beeksisin hafuu", "2,000"),
            ("Guyyaa 3 dura beeksisee hafuu", "1,000"),
            ("Daqiiqaa 30 ol turuu", "200"),
            ("Akeekkachiisa booda jeequu", "500"),
            ("Keessummeessaan beeksisa ji'a tokkoo gadiin dabaree haquu", "1,000"),
        ],
        "foot": "Kun cuunfaa dha. Seerri ittiin bulmaataa guutuun barreeffama seeraa ti.",
    },
]

COLORS = ["#0e5245", "#c4202f", "#1b9aa0", "#b8296e", "#d99a1e", "#2e8b57"]

CSS = """
@import url("fonts/fonts.css");
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --green:#0e5245; --green-deep:#0b3d33; --gold:#f6c453; --red:#c4202f; --cream:#fff6e0; --paper:#fbf6ea; --ink:#1f2a27; --muted:#5f6762; }
body { font-family: "Source Serif 4", serif; color: var(--ink); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
[lang="am"], [lang="am"] * { font-family: "Noto Serif Ethiopic", serif !important; }
.page { width: 210mm; height: 297mm; overflow: hidden; position: relative; background: var(--paper); break-after: page; display: flex; flex-direction: column; }
.page:last-child { break-after: auto; }
.tibeb { height: 9mm; background: TIBEB repeat-x; background-size: auto 9mm; }
.tibeb.thin { height: 5mm; background-size: auto 5mm; }
header { background: radial-gradient(circle at 88% 30%, rgba(246,196,83,.35) 0 14mm, transparent 15mm), linear-gradient(160deg, var(--green) 0%, var(--green-deep) 100%); color: #fff6e0; padding: 9mm 16mm 8mm; position: relative; }
header .k { font-size: 9pt; letter-spacing: .18em; text-transform: uppercase; color: var(--gold); font-weight: 600; }
[lang="am"] header .k { letter-spacing: .04em; font-size: 10pt; }
header h1 { font-family: "Fraunces", serif; font-weight: 700; font-size: 30pt; line-height: 1.05; margin-top: 2mm; }
[lang="am"] header h1 { font-size: 26pt; line-height: 1.25; }
[lang="om"] header h1 { font-size: 22pt; max-width: 150mm; }
[lang="om"] .pt p { font-size: 9.1pt; line-height: 1.38; }
header p { margin-top: 2mm; font-size: 11pt; color: rgba(255,246,224,.85); font-style: italic; }
[lang="am"] header p { font-style: normal; }
header svg { position: absolute; right: 14mm; top: 7mm; width: 30mm; height: 30mm; }
main { flex: 1; padding: 7mm 13mm 0; display: grid; grid-template-columns: 1fr 1fr; grid-auto-rows: auto; gap: 3.6mm 4.5mm; align-content: start; }
.pt { background: #fff; border-radius: 3mm; padding: 3mm 4mm 3.4mm 4mm; border-left: 2.2mm solid var(--c); box-shadow: 0 .4mm 1.4mm rgba(14,82,69,.12); break-inside: avoid; }
.pt h2 { display: flex; align-items: center; gap: 2.4mm; font-family: "Fraunces", serif; font-size: 11.5pt; line-height: 1.2; color: var(--c); margin-bottom: 1.2mm; }
[lang="am"] .pt h2 { font-size: 11pt; }
.pt h2 .n { flex: none; width: 6mm; height: 6mm; display: grid; place-items: center; background: var(--c); color: #fff; font-size: 8.5pt; transform: rotate(45deg); border-radius: 1mm; }
.pt h2 .n span { transform: rotate(-45deg); font-family: "Fraunces", serif !important; }
.pt p { font-size: 9.4pt; line-height: 1.42; }
[lang="am"] .pt p { font-size: 9.9pt; line-height: 1.55; }
.pt.hl { background: var(--cream); }
table { width: 100%; border-collapse: collapse; font-size: 9pt; }
[lang="am"] table { font-size: 9.4pt; }
th { text-align: left; font-size: 7.5pt; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); font-weight: 600; padding-bottom: .8mm; }
td { padding: .9mm 0; border-top: .25mm solid #eadfc6; line-height: 1.3; }
td.b, th.b { text-align: right; white-space: nowrap; padding-left: 3mm; }
td.b { font-family: "Fraunces", serif !important; font-weight: 700; color: var(--red); }
footer { padding: 4mm 16mm 5mm; display: flex; justify-content: space-between; align-items: center; font-size: 8.5pt; color: var(--muted); }
footer b { color: var(--green); font-family: "Fraunces", serif; }
"""

SUN = ('<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="17" r="14" fill="#f6c453"/>'
       '<g fill="#3fa66b"><circle cx="11" cy="17" r="6"/><circle cx="20" cy="12" r="7.5"/><circle cx="29" cy="17" r="6"/>'
       '<circle cx="15.5" cy="19" r="6"/><circle cx="24.5" cy="19" r="6"/></g><circle cx="16" cy="13" r="1.5" fill="#c4202f"/>'
       '<circle cx="25" cy="16" r="1.5" fill="#b8296e"/><path d="M18.4 22h3.2v12h-3.2z" fill="#7a4a2a"/>'
       '<path d="M8 34.5h24" stroke="#f6c453" stroke-width="2.2" stroke-linecap="round"/></svg>')


def tibeb_uri():
    css = open(os.path.join(HERE, "assets", "site.css"), encoding="utf-8").read()
    start = css.index("--tibeb:") + len("--tibeb:")
    return css[start:css.index(";", css.index("svg%3E\")", start))].strip()


def page(p):
    e = html.escape
    cards = []
    for i, (h, body) in enumerate(p["points"]):
        c = COLORS[i % len(COLORS)]
        if body is None:
            rows = "".join(f'<tr><td>{e(a)}</td><td class="b">{e(b)}</td></tr>' for a, b in p["fines"])
            inner = (f'<table><tr><th>{e(p["fines_head"][0])}</th><th class="b">{e(p["fines_head"][1])}</th></tr>'
                     f'{rows}</table>')
            cls = "pt hl"
        else:
            inner = f"<p>{e(body)}</p>"
            cls = "pt hl" if i == 3 else "pt"
        cards.append(f'<section class="{cls}" style="--c:{c}"><h2><span class="n"><span>{i + 1}</span></span>'
                     f'{e(h)}</h2>{inner}</section>')
    return (f'<div class="page" lang="{p["lang"]}"><div class="tibeb"></div>'
            f'<header>{SUN}<div class="k">{e(p["kicker"])}</div><h1>{e(p["title"])}</h1><p>{e(p["sub"])}</p></header>'
            f'<main>{"".join(cards)}</main>'
            f'<footer><span>{e(p["foot"])}</span><b>abudah.github.io/asefa-family-gathering</b></footer>'
            f'<div class="tibeb thin"></div></div>')


def build():
    doc = ('<!doctype html><html><head><meta charset="utf-8"><title>Constitution in Brief</title>'
           f'<style>{CSS.replace("TIBEB", tibeb_uri())}</style></head><body>'
           + "".join(page(p) for p in PAGES) + "</body></html>")
    with open(TMP, "w", encoding="utf-8") as f:
        f.write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    "--virtual-time-budget=4000", f"--print-to-pdf={OUT}", "file://" + TMP],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(TMP)
    print("Wrote", OUT)


if __name__ == "__main__":
    build()
