---
name: qa-BiDi
description: Checks RTL/LTR correctness in mixed Hebrew-English text of the LaTeX project.
---
# qa-BiDi
Checks:
- Every Latin word, acronym, URL, number-with-unit inside Hebrew text is wrapped in `\en{}` or `\num{}`.
- No `Missing character` warnings in `main.log` (Hebrew or Latin glyphs).
- Parentheses and quotes adjacent to English fragments do not appear mirrored in the rendered PDF (render page to PNG and inspect).
- Header/footer/title-page lines containing both scripts are wrapped as a single `\en{}` unit.
- Currency (₪, $) and percentages keep the number first and the sign on the correct side.
Method: `grep` chapters for `[A-Za-z]{2,}` outside `\en{}`/`\code{}`/math, then visually verify 3 sample pages.
Severity: wrong order of a visible phrase = blocker.
- Two English fragments separated only by a comma or space must be merged into one `\en{}` unit, e.g. write `\en{A, B}` and not `\en{A}, \en{B}`: the neutral punctuation between separate LTR runs is reordered in an RTL paragraph (incident I-11).
- The same applies to `\num{A}, \num{B}` and to `\en{A} (\num{B}`: any two LTR runs separated only by whitespace/punctuation are reordered (incident I-12). `python code/lint_bidi.py` enforces this and is part of `build.ps1`; a hit fails the build. Fix by merging into one unit or placing a Hebrew word between the runs.
- A sign or percent belongs inside the LTR unit (`\en{±20\%}`), and `\num{A}\%. \num{B}` is the same adjacent-run defect as `\num{A}, \num{B}`; the lint covers `\%` and signs (incident I-19).
