---
name: qa-code
description: Checks Python code listings, background code and pythonbox-style overflow.
---
# qa-code
- Python in `code/` runs from a clean checkout (`python code/model.py`) and regenerates every figure deterministically (fixed seed).
- Code shown in the PDF fits the page width (no overflow past margins), uses the monospace font, and has a light background box.
- No hard-coded absolute paths; no unused imports.
- Hebrew labels in matplotlib render without tofu boxes (font fallback verified).
- Code excerpts in the report are generated from the source (`inspect.getsource` in `model.py` writes `figures/model_excerpt.py`), never included by absolute line numbers: editing the generator must not change what the report shows (incident I-15).
- The figure font comes from the TeX installation through `kpsewhich` (`libertinus_sans()` in `model.py`), never from a path under the user's profile; without TeX matplotlib keeps its default font (incident I-26). Two consecutive generator runs must give identical `figures/*.tex` files and identical rendered figures (compare rendered pages, not PDF bytes: the PDF files carry a creation date).
