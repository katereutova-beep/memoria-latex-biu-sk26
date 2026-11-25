# TODO

Status as verified on 2026-11-25 against commit `6f2d7c6`. `[x]` means done and checked in the repository or the PDF; `[ ]` means open. Evidence in parentheses.

## Done
- [x] Repo, folders, git init (`4ff1796`)
- [x] PRD.md, PLAN.md, TODO.md (`4ff1796`)
- [x] `memoria.cls` and `main.tex` skeleton compile (`1ecb2a4`); class now v1.3.3
- [x] `code/model.py` and generated figures (`27f2981`); `code/quality_demo.py`, `code/lint_bidi.py`
- [x] Chapters 1-8 plus chapter 9 (production process) and appendices (quote, glossary); 16 pages in `Memoria-biu-sk26.pdf`
- [x] TikZ illustrations: pipeline, positioning map, personas, timeline (Gantt), risk map, agent diagram
- [x] Ten skills written (`skills/`)
- [x] Agent windows opened and PING/PONG run by `lead` (`docs/mesh-check.md`); lead-to-peer links only
- [x] QA round 1 by the main session (incidents I-01 to I-11)
- [x] QA round 2: detector report, 11 fixer commits, detector re-review (`docs/qa-report.md`, incidents I-12 to I-21, L-01)
- [x] README with screenshots, regenerated from the current PDF on 2026-11-25
- [x] Prompts saved: summaries `prompts/01-03`, verbatim user prompts `04`, verbatim agent messages `05`
- [x] Repository public on GitHub: https://github.com/katereutova-beep/memoria-latex-biu-sk26 (public, so no sharing step is needed for the lecturer)
- [x] Clean-clone build verified (16 pages, `lint_bidi` 0 violations)

## Open: required by the assignment or the PRD
- [ ] Lecturer approves the topic (the assignment requires approval in advance)
- [ ] Both partners commit, push and pull (all 21 commits up to `6f2d7c6` are from one git identity)
- [ ] Self-assessed grade chosen and recorded in `docs/self-assessment.md` (PRD 6.4; not written)
- [ ] Fill the Word form and save `biu-sk26-ex02.pdf` (do not submit Word); each partner submits separately in Moodle
- [ ] PRD 6.2: a `qa-super` run with zero blocking findings; none is recorded (`docs/qa-report.md`, section 7)
- [ ] PRD FR1 target 18-22 pages; the document has 16 (minimum 15 is met, margin is one page, and the count includes cover, table of contents and bibliography)

## Open: quality and evidence
- [ ] Table column order is inconsistent: Tables 1, 5, 8 and 10 have the first column on the right, Tables 2, 3, 4, 6, 7, 9 and 11 on the left; cause not established; recorded accurately in `docs/incidents.md` L-01 (corrected 2026-11-25)
- [ ] Typed numbers outside the model remain in chapters 2, 4 and 8 (`docs/qa-report.md`, section 6)
- [ ] Percent-sign placement in the Monte Carlo paragraph not independently verified
- [ ] No second-agent verification of the final PDF after the last fix
- [ ] No real screenshot of the agent windows (only `docs/screenshots/mesh.png`, rendered from `docs/mesh-check.md`)
- [ ] Peer-to-peer links in the mesh check were never tested
- [ ] Duplicate agent sessions (four started before the check; origin not established) not closed
- [ ] `start-agents.ps1` opens windows without initial prompts, `agent.ps1` starts one with its prompt; `docs/agent-windows.md` describes only the former
