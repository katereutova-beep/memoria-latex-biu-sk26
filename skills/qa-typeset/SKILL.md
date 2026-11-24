---
name: qa-typeset
description: Reads main.log for compilation warnings (hbox/vbox) and layout defects.
---
# qa-typeset
- Zero `Overfull \hbox` greater than 1pt; zero `Underfull \vbox` that leave a page more than 30% empty.
- No orphan section headings at page bottom; no empty or near-empty pages.
- No unresolved references (`??`), no `Citation undefined`.
- Page count within 15..25 and matches the previous run unless chapters changed.
