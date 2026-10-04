#!/usr/bin/env python3
"""Turn a finished report (markdown) into a PDF under reports/pdf/, one file per report.

Markdown -> HTML with render_email.convert (standard library), HTML -> PDF with fpdf2
(`pip install fpdf2`, listed in requirements.txt). Links stay clickable.

Fonts: a Unicode font family when one is installed (DejaVu or Liberation on Linux, Arial on
macOS); otherwise the built-in Helvetica, with characters it cannot draw replaced by close
equivalents ("->" for an arrow), so a stray symbol never stops the PDF.

Usage:
  python render_pdf.py reports/daily/2026/10/2026-10-05.md          -> reports/pdf/2026-10-05.pdf
  python render_pdf.py reports/deep-dives/CRWD-2026-10-11.md        -> reports/pdf/deep-dive-CRWD-2026-10-11.pdf
  python render_pdf.py <report.md> --out <file.pdf>
"""
from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[3] / "scripts"))
import pilib  # noqa: E402
from render_email import convert  # noqa: E402

FONT_FAMILIES = [  # (regular, bold, italic, bold-italic)
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-BoldOblique.ttf"),
    ("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
     "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-BoldItalic.ttf"),
    ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
     "/System/Library/Fonts/Supplemental/Arial Italic.ttf", "/System/Library/Fonts/Supplemental/Arial Bold Italic.ttf"),
]
REPLACE = {"→": "->", "←": "<-", "↑": "up", "↓": "down", "↔": "<->", "−": "-",
           "–": "-", "—": " - ", "‘": "'", "’": "'", "“": '"', "”": '"',
           "…": "...", "•": "-", "≈": "~", "≤": "<=", "≥": ">=", "≠": "!=",
           "€": "EUR", "™": "(TM)", "✓": "yes", "✗": "no", " ": " "}


def to_latin1(text: str) -> str:
    """For the built-in font: keep Latin-1, swap common symbols, drop what cannot be drawn."""
    out = []
    for ch in text:
        if ord(ch) < 256:
            out.append(ch)
        elif ch in REPLACE:
            out.append(REPLACE[ch])
        else:
            base = unicodedata.normalize("NFKD", ch).encode("latin-1", "ignore").decode("latin-1")
            out.append(base or "?")
    return "".join(out)


def default_out(report: Path) -> Path:
    prefix = "deep-dive-" if report.parent.name == "deep-dives" else ""
    return pilib.ROOT / "reports" / "pdf" / f"{prefix}{report.stem}.pdf"


def build_pdf(md: str, title: str = "Portfolio report"):
    from fpdf import FPDF  # imported here so the rest of the toolbox never needs fpdf2
    from fpdf.fonts import TextStyle

    pdf = FPDF(format="A4")
    pdf.set_title(title)
    pdf.set_author("portfolio-intel")
    pdf.set_margins(16, 16, 16)
    pdf.set_auto_page_break(True, margin=16)
    family = "helvetica"
    for files in FONT_FAMILIES:
        if all(Path(f).exists() for f in files):
            for style, f in zip(("", "B", "I", "BI"), files):
                pdf.add_font("report", style, f)
            family = "report"
            break
    pdf.add_page()
    pdf.set_font(family, size=10.5)
    html = convert(md)
    # fpdf2 draws tables and quotes with its own styling; inline CSS from the email renderer is dropped
    html = re.sub(r'\sstyle="[^"]*"', "", html)
    for tag in ("p", "ul", "ol"):  # a little air between lines for reading
        html = html.replace(f"<{tag}>", f'<{tag} line-height="1.35">')
    if family == "helvetica":
        html = to_latin1(html)
    navy = (31, 56, 100)
    styles = {f"h{n}": TextStyle(font_style="B", font_size_pt=size, color=navy, t_margin=top, b_margin=2)
              for n, size, top in ((1, 18, 4), (2, 14, 6), (3, 12, 4), (4, 11, 3))}
    pdf.write_html(html, font_family=family, table_line_separators=True, tag_styles=styles,
                   li_prefix_color=(90, 90, 90))
    return pdf


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", type=Path)
    ap.add_argument("--out", type=Path)
    a = ap.parse_args(argv)
    md = a.report.read_text(encoding="utf-8")
    first = next((l[2:].strip() for l in md.splitlines() if l.startswith("# ")), a.report.stem)
    out = a.out or default_out(a.report.resolve())
    out.parent.mkdir(parents=True, exist_ok=True)
    build_pdf(md, first).output(str(out))
    print(f"PDF -> {out} ({out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
