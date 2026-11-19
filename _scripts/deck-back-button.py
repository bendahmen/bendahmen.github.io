# Post-render: inject a "back to all slides" link into every teaching deck in the output dir.
# Decks are self-contained HTML rendered elsewhere and only copied in as resources, so the
# link is added here rather than in each deck's source. New decks under teaching/ pick it up
# automatically. Idempotent: decks that already carry the marker are skipped.

import os
from pathlib import Path

MARKER = "deck-back-button"

SNIPPET = """
<!-- {marker}: injected by _scripts/deck-back-button.py -->
<style>
  #{marker} {{
    position: fixed; top: 12px; left: 12px; z-index: 9999;
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 12px; border-radius: 999px;
    font: 500 14px/1.2 system-ui, -apple-system, "Segoe UI", sans-serif;
    color: #222; background: rgba(255, 255, 255, 0.85);
    border: 1px solid rgba(0, 0, 0, 0.15); text-decoration: none;
    opacity: 0.5; transition: opacity 0.15s;
  }}
  #{marker}:hover, #{marker}:focus-visible {{ opacity: 1; }}
  @media print {{ #{marker} {{ display: none; }} }}
  html.print-pdf #{marker} {{ display: none; }}
</style>
<a id="{marker}" href="{href}" title="Back to all slide decks">&larr; All slides</a>
"""

out_dir = Path(os.environ.get("QUARTO_PROJECT_OUTPUT_DIR", "_site"))
overview = out_dir / "teaching" / "index.html"
course_dirs = [d for d in (out_dir / "teaching").iterdir() if d.is_dir()]

for deck in (p for d in course_dirs for p in d.rglob("*.html")):
    html = deck.read_text(encoding="utf-8")
    if MARKER in html:
        continue
    # Last </body>: decks embed other "</body>" strings inside inlined scripts.
    cut = html.rfind("</body>")
    if cut == -1:
        continue
    href = Path(os.path.relpath(overview, deck.parent)).as_posix()
    snippet = SNIPPET.format(marker=MARKER, href=href)
    deck.write_text(html[:cut] + snippet + html[cut:], encoding="utf-8")
    print(f"deck-back-button: {deck.relative_to(out_dir)}")
