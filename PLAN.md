# PLAN — Memoria report

| Stage | Output | Owner (agent) | Gate |
|---|---|---|---|
| 0 | Repo, folders, PRD/PLAN/TODO | Lead | PRD approved by user |
| 1 | `memoria.cls` (banner, footer, colors, BiDi macros) + skeleton `main.tex` | Writer-CLS | empty skeleton compiles |
| 2 | `code/model.py` financial model + 5 figures | Analyst | figures render, numbers cross-checked |
| 3 | Chapters 1–8 (`chapters/*.tex`) | Writer | each chapter compiles alone |
| 4 | TikZ illustrations | Designer | `qa-img` passes |
| 5 | Detector run → Fixer run → Red-team → repeat | QA | `qa-super` zero blockers |
| 6 | Incident post-mortems (`docs/incidents.md`) | Lead + all | every human-found defect analysed |
| 7 | README with screenshots, prompt log, skills list | Lead | links resolve |
| 8 | Push to GitHub, share with rmisegal@gmail.com, self-grade, PDF form `biu-sk26-ex02.pdf` | Both partners | repo opens without login |

## Chapter outline (target 18–22 pages)
1. תקציר מנהלים / Executive Summary
2. הבעיה והזדמנות שוק / Problem & Market
3. השירות והתהליך הטכני / Service & AI pipeline (TikZ)
4. מודל עסקי ותמחור / Business model & Price quote (tables)
5. תחזית פיננסית / Financial forecast (Python graphs, break-even formula)
6. שיווק ותפעול / Go-to-market & operations
7. סיכונים ופרטיות / Risks, privacy (GDPR-style, consent)
8. סיכום והמלצות / Conclusion
Appendix: הצעת מחיר ללקוח (one-page quote), glossary, bibliography.

## Agent team (separate Claude Code windows, cross-session SendMessage)
`lead` (orchestrator) · `writer` · `analyst` · `detector` · `fixer`.
Lead hands tasks by SendMessage, Detector reports defects to Lead, Lead forwards to Fixer.
Red-team: Detector audits Fixer's changes before they are accepted.
