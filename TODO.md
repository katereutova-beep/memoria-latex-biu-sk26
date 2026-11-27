# TODO

Status as verified on 2026-11-25 against commit `6f2d7c6`; `b64ad4c` is a later documentation-only commit. The collaboration items were updated on 2026-11-27 against `origin/main` at `01d97bb`. The QA, build and class items were updated on 2026-11-27 after the `qa-super` run. `[x]` means done and checked in the repository or the PDF; `[ ]` means open. Evidence in parentheses.

## Done
- [x] Repo, folders, git init (`4ff1796`)
- [x] PRD.md, PLAN.md, TODO.md (`4ff1796`)
- [x] `memoria.cls` and `main.tex` skeleton compile (`1ecb2a4`); class now v1.3.5
- [x] `code/model.py` and generated figures (`27f2981`); `code/quality_demo.py`, `code/lint_bidi.py`
- [x] Chapters 1-8 plus chapter 9 (production process) and appendices (quote, glossary); 16 pages in `Memoria-biu-sk26.pdf`
- [x] TikZ illustrations: pipeline, positioning map, personas, timeline (Gantt), risk map, agent diagram
- [x] Ten skills written (`skills/`)
- [x] `docs/agent-windows.md` and `prompts/agent-roles.md` corrected to describe `agent.ps1` and the role prompts (presumed hand-pasted) (doc audit after `b64ad4c`)
- [x] Agent windows opened and PING/PONG run by `lead` (`docs/mesh-check.md`); lead-to-peer links only
- [x] QA round 1 by the main session (incidents I-01 to I-11)
- [x] QA round 2: detector report, 11 fixer commits, detector re-review (`docs/qa-report.md`, incidents I-12 to I-21, L-01)
- [x] QA round 3 (documentation audit) with four new agents `lead-qa`, `writer-qa`, `detector-qa`, `fixer-qa`: findings F1 to F4 fixed in docs, skills and prompts, re-reviewed, scope gate passed; all messages in `prompts/06-qa-cycle-verbatim.md`, record in `docs/qa-report.md` section 8
- [x] `qa-super` run on 2026-11-27 by the main session (`docs/qa-report.md` section 9): 8 findings, 7 fixed (incidents I-22 to I-27 and one class warning), L-02 open at that time and closed in round 5 (I-28)
- [x] `build.ps1` stops at the first failed Python, LuaLaTeX or Biber step and does not copy the final PDF; verified by failure injection in throw-away copies (4 failure cases exit 1 with the PDF untouched, the control copies it); rule added to `qa-infra`
- [x] Independent review of the qa-super fixes (commit 093cef5) by `detector-qa`: no blocker, no major, 3 minor findings (N-1 to N-3), all fixed (`docs/qa-report.md` section 10.1)
- [x] L-02 resolved: 25 references to the 11 tables and 14 figures, `\tabref`/`\figref` in class 1.3.5, lint for unreferenced labels, skills updated (incident I-28)
- [x] Screenshots in `docs/screenshots` rendered again from the current PDF (2026-11-27)
- [x] Second independent review (commit b7a3028) by `detector-qa`: no blocker, no major, three minor findings (M-1 to M-3), fixed (incidents I-32 to I-34)
- [x] Third independent review (commit 61942d1) by `detector-qa`: M-1 to M-3 confirmed, no blocker or major, two minor documentation findings (P-1, P-2) fixed (`docs/qa-report.md` section 10.5)
- [x] PRD 6.2 (`qa-super` with zero blocking findings; incident log with root causes): met on commit 61942d1, caveats: the pass is split over several sessions (the main session ran the checks and fixes, `detector-qa` confirmed them in three reviews) and not one run of the orchestrating skill; the typed values that are not constants of `model.py` remain (`docs/qa-report.md` 9.5 item 2); the mixed table direction (L-01) stays an observation; no rebuild was tried on a machine without TeX (`docs/qa-report.md` section 10.5)
- [x] Real captures of the four new agents added to the README (`docs/screenshots/agent-*.png`)
- [x] README with screenshots, regenerated from the current PDF on 2026-11-25
- [x] Prompts saved: summaries `prompts/01-03`, verbatim user prompts `04`, verbatim agent messages `05`
- [x] Repository public on GitHub: https://github.com/katereutova-beep/memoria-latex-biu-sk26 (public, so no sharing step is needed for the lecturer)
- [x] Topic selected independently from the assignment's suggested categories (a business plan with a detailed price quote). The students confirm that the lecturer allowed independent topic selection (relayed by the user on 2026-11-27); explicit lecturer approval is not claimed.
- [x] Clean-clone build verified (16 pages, `lint_bidi` 0 violations); repeated on 2026-11-27 on a copy of the tracked files
- [x] Partner commit and push verified on 2026-11-27 at `ced6645`: 24 commits, 23 by Katrina Reutova (`katereutova-beep`) and 1 by Alexandra Pirogan (`ced6645`, `PLAN.md`, 2026-11-25T21:29:00+02:00; GitHub links it to `sspirogan`, a collaborator with push permission; GitHub lists a push by `sspirogan` at 2026-11-25T19:31:07Z). Earlier stage: up to `6f2d7c6` all 21 commits carried one git identity.
- [x] Pull by Katrina verified on 2026-11-27: local `main` was fast-forwarded from `f537091` to `ced6645` at 15:44:31+02:00 (`git reflog`: "merge origin/main: Fast-forward"; no local commit was lost).
- [x] Pull by Alexandra, confirmed on 2026-11-27: she reported that she ran `git pull --ff-only` on her Mac, `ced6645` to `01d97bb`, working tree clean. This rests on that confirmation (relayed by the user on 2026-11-27); git and GitHub do not record pulls. Consistent with it: the parent of `ced6645` is `f537091`.
- [x] Both partners have now committed, pushed and pulled. Basis: commits and pushes are visible in git and GitHub (`ced6645` and the push by `sspirogan`, Katrina's commits and pushes); Katrina's pull is in `git reflog`; Alexandra's pull rests on her confirmation.

## Open: required by the assignment or the PRD
- [ ] Self-assessed grade chosen and recorded (PRD 6.4; not written)
- [ ] Fill the Word form and save `biu-sk26-ex02.pdf` (do not submit Word); each partner submits separately in Moodle
- [ ] PRD FR1 target 18-22 pages; the document has 16 (minimum 15 is met, margin is one page, and the count includes cover, table of contents and bibliography)

## Open: quality and evidence
- [ ] Table column order is mixed (first column on the right in Tables 1, 5, 8 and 10, on the left in the other seven; cause not established; `docs/incidents.md` L-01). A mix alone is not recorded as a defect; kept as an observation
- [ ] Typed numbers that are not constants of `model.py` remain (package photo limits, service targets, channel months, equation constants, prose in chapters 2, 4, 5, 6 and 8); tables 4, 6 and 11 now use macros (I-27) (`docs/qa-report.md` section 9.5)

- [ ] Percent-sign placement in the Monte Carlo paragraph not independently verified
- [ ] No rebuild was tried on a machine without TeX (the figure font falls back to the matplotlib default there)
- [ ] Peer-to-peer links were not tested by the mesh check (they were exercised in round 3 messages, but there was no dedicated test)
- [ ] Duplicate agent sessions (four started before the check; origin not established) not closed
