---
name: qa-typeset
description: Reads main.log for compilation warnings (hbox/vbox) and layout defects.
---
# qa-typeset
- Zero `Overfull \hbox` greater than 1pt; zero `Underfull \vbox` that leave a page more than 30% empty.
- No orphan section headings at page bottom; no empty or near-empty pages.
- No unresolved references (`??`), no `Citation undefined`.
- Page count within 15..25 and matches the previous run unless chapters changed.
- Running header: every page's header names the section active at the top of the page (a section starting at the very top, else the one carried over); check pages where a new chapter starts mid-page (incident I-15). The TOC lists chapters only (`tocdepth` 1) and must not spill onto its own near-empty page.
- Short closing blocks (terms + signature line, caption + figure) are wrapped in `keeptogether`; a signature line alone at the top of a page is a defect.
- Check the header on pages that open with a float or a table: it must name the chapter the page opened in, not the chapter that starts lower down.
- A table or figure that directly follows a heading uses `[H]` (the class loads `float`), and a `\section` followed directly by a float also needs `\Needspace*{..}` in front of it, because `[H]` alone did not keep a chapter heading with its float. `[h]` is not allowed (LaTeX turns it into `[ht]` with a warning). `code/lint_bidi.py` enforces all three (incident I-23).
- Per-page check by rendering every page: body fill of at least 30 %, and the last body line of a page is not a heading. Do not rely on the log for this; the log has no warning for an orphaned heading.
