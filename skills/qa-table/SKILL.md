---
name: qa-table
description: Checks table alignment, column order in RTL, widths, captions and overflow.
---
# qa-table
- Column order reads right-to-left in Hebrew tables; numeric columns right-aligned digits in LTR cells (`\num{}`).
- Table fits text width (no `Overfull \hbox` from tabularx/longtable); caption above table; each table referenced in text.
- Header row uses `\theadrow` + `\thead{}`; total rows are bold.
- Values in tables come from `code/model.py` output (`figures/*.tex` snippets), never retyped.
