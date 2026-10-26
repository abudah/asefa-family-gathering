# Asefa Family Gathering Constitution

Trilingual (English, Amharic and Afaan Oromo) constitution and rules for the quarterly gathering of the grandchildren of Asefa.

- `index.html` – the designed web version (served by GitHub Pages)
- `Asefa-Family-Gathering-Constitution.pdf` – the designed, printable PDF
- `build_constitution.py` – holds all the text in the three languages
- `build_pdf.py` – lays out the PDF and prints it with Google Chrome
- `build_html.py` – builds the web page from the same text
- `fonts/` – local copies of the fonts (Fraunces, Source Serif 4, Noto Serif Ethiopic; SIL Open Font License)

To change the text, edit `build_constitution.py`, then run:

    python3 build_pdf.py
    python3 build_html.py

The PDF build needs Google Chrome installed on the Mac. No internet is needed.
