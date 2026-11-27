---
name: qa-table
description: Checks table alignment, column order in RTL, widths, captions and overflow.
---
# qa-table
- Column order reads right-to-left in Hebrew tables. Observed on 2026-11-27: the first column is on the right in 4 of 11 tables and on the left in 7 (L-01 in `docs/incidents.md`); a mix of directions alone is not recorded as a defect. Numeric columns right-aligned digits in LTR cells (`\num{}`).
- Table fits text width (no `Overfull \hbox` from tabularx/longtable); caption above table; each table referenced in text. Every table is referenced in the text with `\tabref{tab:..}` (11 of 11 on 2026-11-27, a reference reads "בטבלה 4" or "(ראו טבלה 4)"); `code/lint_bidi.py` rejects an unreferenced table label and a reference to a missing label (incidents L-02 and I-28).
- Header row uses `\theadrow` + `\thead{}`; total rows are bold.
- Values in tables come from `code/model.py` output (`figures/*.tex` snippets), never retyped. Tier prices, costs and shares, the fixed-cost range, head counts, the first-month orders and the quote quantities and unit prices are macros from `model.py` (incident I-27). Typed values that are not model constants (package photo limits, service targets, channel months) remain; see `docs/qa-report.md`.
- Month numbers and schedules (hire month, ad start, subscription start, Gantt bars) come from the constants in `code/model.py` (`HIRE3_MONTH`, `ADS_MONTH`, `HOSTING_MONTH`, `GANTT`) as macros or generated TikZ; a figure or sentence that retypes them is a defect (incident I-14).
- Table cells with Hebrew text use the CLS column type `H` (RTL paragraph), never bare `X`, `l`, `r` or `\en` in the column spec: in those cells the paragraph direction is LTR, so leading numbers, final punctuation and ranges (`1--6`) land on the wrong side. `l`/`r`/`c` are for pure numbers or Latin words only. `code/lint_bidi.py` enforces the spec rules. Numbers of derived tables (unit economics) come from `model.py` macros (incident I-16).
- A sample quote or price example must be derived from the stated policy in `model.py` (`quote()`), never typed: the appendix quote once applied a family discount that chapter 4 grants only above 3 orders a year (incident I-18).
