---
name: qa-table
description: Checks table alignment, column order in RTL, widths, captions and overflow.
---
# qa-table
- Column order reads right-to-left in Hebrew tables; numeric columns right-aligned digits in LTR cells (`\num{}`).
- Table fits text width (no `Overfull \hbox` from tabularx/longtable); caption above table; each table referenced in text.
- Header row uses `\theadrow` + `\thead{}`; total rows are bold.
- Values in tables come from `code/model.py` output (`figures/*.tex` snippets), never retyped.
- Month numbers and schedules (hire month, ad start, subscription start, Gantt bars) come from the constants in `code/model.py` (`HIRE3_MONTH`, `ADS_MONTH`, `HOSTING_MONTH`, `GANTT`) as macros or generated TikZ; a figure or sentence that retypes them is a defect (incident I-14).
- Table cells with Hebrew text use the CLS column type `H` (RTL paragraph), never bare `X`, `l`, `r` or `\en` in the column spec: in those cells the paragraph direction is LTR, so leading numbers, final punctuation and ranges (`1--6`) land on the wrong side. `l`/`r`/`c` are for pure numbers or Latin words only. `code/lint_bidi.py` enforces the spec rules. Numbers of derived tables (unit economics) come from `model.py` macros (incident I-16).
- A sample quote or price example must be derived from the stated policy in `model.py` (`quote()`), never typed: the appendix quote once applied a family discount that chapter 4 grants only above 3 orders a year (incident I-18).
