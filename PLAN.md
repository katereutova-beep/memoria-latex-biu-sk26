# PLAN — Memoria report

Original plan with the status verified on 2026-11-25 (commit `6f2d7c6`). The "Executed by" column records who actually did the work, from the session log and git history.

| Stage | Output | Planned owner | Executed by | Gate | Status |
|---|---|---|---|---|---|
| 0 | Repo, folders, PRD/PLAN/TODO | Lead | Main session | PRD approved by user | Done; user approved ("אשר, התחל") |
| 1 | `memoria.cls` and skeleton `main.tex` | Writer-CLS | Main session | skeleton compiles | Done; class now v1.3.3 |
| 2 | `code/model.py` and figures | Analyst | Main session | figures render, numbers cross-checked | Done; detector recomputed the 16 scalar macros and found them equal to the code |
| 3 | Chapters (`chapters/*.tex`) | Writer | Main session | each chapter compiles alone | Done; 9 chapters plus 2 appendices. Not tested chapter by chapter, only through `main.tex` |
| 4 | TikZ illustrations | Designer | Main session | `qa-img` passes | Done; checked by eye, no standalone `qa-img` run |
| 5 | Detector run, Fixer run, red team, repeat | Detector, Fixer | Round 1: main session. Round 2: `detector [72ab50]` and `fixer [35005a]` | `qa-super` zero blockers | Round 1 and 2 done; no `qa-super` run recorded, gate not met as written (`docs/qa-report.md`) |
| 6 | Incident post-mortems (`docs/incidents.md`) | Lead and all | Main session and fixer | every human-found defect analysed | Done for I-01 to I-21; L-01 open and inaccurately worded |
| 7 | README with screenshots, prompt log, skills list | Lead | Main session | links resolve | Done and links checked 2026-11-25; agent-window screenshot missing |
| 8 | Push to GitHub, share with the lecturer, self-grade, form `biu-sk26-ex02.pdf` | Both partners | Push by main session; the rest not done | repo opens without login | Repo is public and pushed. Lecturer topic approval, partner commits, self-grade, form and Moodle submissions are open (see `TODO.md`) |

## Chapter outline as built (16 pages, original target 18-22 not met)
1. תקציר מנהלים / Executive Summary
2. הבעיה והזדמנות שוק / Problem & Market (alternatives table, personas, positioning map)
3. השירות ותהליך העבודה / Service & AI Pipeline (TikZ pipeline, quality metrics, journey table)
4. מודל עסקי ותמחור / Business Model & Pricing (tiers table, unit economics)
5. תחזית פיננסית / Financial Forecast (Python figures, break-even, sensitivity, Monte Carlo)
6. שיווק ותפעול / Go-to-Market & Operations
7. סיכונים ופרטיות / Risks & Privacy
8. סיכום והמלצות / Conclusion
9. תהליך ההפקה / Production Process (agent team, incidents)

Appendices: customer quote, glossary. Bibliography (IEEE, biber).

## Agent team (separate Claude Code windows, cross-session SendMessage)
Planned: `lead` (orchestrator), `writer`, `analyst`, `detector`, `fixer`. Lead hands out tasks by SendMessage, the detector reports defects, the fixer repairs, the detector red-teams the fixes.

What actually ran: all five windows were started and answered the PING/PONG check. Only `detector` and `fixer` did recorded work (QA round 2). `lead` ran the mesh check only. `writer` and `analyst` did no other recorded work. In round 2 the main session relayed the detector's report to the fixer; the fixer's and detector's later messages went to each other and not to the main session. See `docs/qa-report.md` and `prompts/05-agent-messages-verbatim.md`.
