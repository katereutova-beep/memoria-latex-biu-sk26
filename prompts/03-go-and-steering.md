# Prompts 03-05 — Go-ahead and steering (user -> lead agent)

| # | Real prompt (translated) | Effect |
|---|---|---|
| 03 | "Approve, start." | Lead wrote PRD.md (expert committee), PLAN.md, TODO.md and committed them |
| 04 | "Yes, continue." | Lead built `memoria.cls`, `main.tex`, skeleton chapters, ten QA skills; stopped to ask permission before `pip install` |
| 05 | "Yes, install." | Lead installed matplotlib/numpy, built `code/model.py`, figures, chapters 1-9, ran QA round 1 |

Engineering notes:
- Permission-gated actions (downloads, pushes) were always confirmed with the user first.
- QA round 1 was run by the lead acting as Detector (contact-sheet review of every page); it found incidents I-01..I-11, each fixed at CLS / skill / generator level (see `docs/incidents.md`).
- A bug in the lead's own change (keybox regex replacing nothing while the changelog already claimed 1.2.0) was caught on the next render and corrected; the changelog was made true only after the fix was verified.
