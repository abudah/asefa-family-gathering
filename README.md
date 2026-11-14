# Asefa Family Gathering Constitution

Trilingual (English, Amharic and Afaan Oromo) constitution and rules for the quarterly gathering of the grandchildren of Asefa.

- `index.html` – home page: choose a language, then go to the constitution, meetups or games
- `constitution.html` – the constitution (built by `build_html.py`)
- `meetups.html` – each round's date, hosts, schedule and photo album
- `Games/` – the family games: Enkulal (egg) and Tekula (wolves and doctor)
- `assets/` – the shared design (`site.css`), language choice, header and footer (`site.js`), and artwork
- `Asefa-Family-Gathering-Constitution.pdf` – the designed, printable PDF
- `build_constitution.py` – holds all the constitution text in the three languages
- `build_pdf.py` – lays out the PDF and prints it with Google Chrome
- `build_html.py` – builds `constitution.html` from the same text
- `fonts/` – local copies of the fonts (Fraunces, Source Serif 4, Noto Serif Ethiopic; SIL Open Font License)

To change the text, edit `build_constitution.py`, then run:

    python3 build_pdf.py
    python3 build_html.py

The PDF build needs Google Chrome installed on the Mac. No internet is needed.
