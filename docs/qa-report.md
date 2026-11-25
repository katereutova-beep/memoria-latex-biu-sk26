# QA report

Prepared 2026-11-25 from the repository history, `docs/incidents.md`, and the exported session log. It records what the QA process actually produced. It does not replace the acceptance criterion in `PRD.md` section 6.2, which is still open (see "Status against PRD 6.2").

## 1. Who did what

| Activity | Done by | Evidence |
|---|---|---|
| All authoring (chapters, `code/*.py`, `memoria.cls`, skills), build, and QA round 1 | The main desktop session, acting as writer, detector and fixer in one session. No separate agents were involved in round 1 | git history up to `007fa59`; incidents I-01 to I-11 |
| Mesh check (PING/PONG), lead to every other session | `lead [c8d412]`, started by the main session | `docs/mesh-check.md` |
| QA round 2: defect finding | `detector [72ab50]` | report below (received 2026-11-24T20:52:34Z) |
| QA round 2: fixes | `fixer [35005a]`, instructed by the main session | commits `44767dd` to `8c4acc4` (the commits carry the shared git identity, so authorship by session cannot be read from git) |
| QA round 2: red-team re-review | `detector [72ab50]` | text read from the agent terminal, quoted in section 4 |
| `writer` and `analyst` agents | Started, answered the PING with PONG, and did no other recorded work | agent terminals; mesh check |

`qa-super` was not run as a standalone skill and no `qa-super` output exists. The checks of the other `qa-*` skills were applied by hand by the detector.

## 2. Round 1 (main session, I-01 to I-11)
Contact-sheet review of every page after the first full build. Eleven incidents, each with root cause, why it was not detected earlier, and a fix at CLS, skill or generator level: see `docs/incidents.md`.

## 3. Round 2: detector report (verbatim)
Received by the main session as a cross-session message, 2026-11-24T20:52:34Z, from `detector`. Reproduced unchanged.

> Detector report, red-team round 2: 6 defects found, no files edited.
> Method: ran build.ps1 (17 pages, no Overfull or Undefined warnings, memoriaversion 1.2.1 matches the changelog). Rendered all 17 pages at 55 dpi and zoomed pages 4, 9, 10 and 14.
> Page numbers below are PDF pages; the printed footer is PDF page minus 1 from page 4 on.
>
> | id | sev | page | evidence | likely root cause | why not caught earlier |
> |---|---|---|---|---|---|
> | D-01 | blocker | 10 (Table 6, row "צוות") | Renders "עד חודש 312 , משם והלאה 2". Source chapters/05-financials.tex:17 is `\num{2} עד חודש \num{12}, \num{3} משם והלאה`. Digits merge into 312 and the order flips, so the visible phrase is wrong. | Two `\num{}` runs separated only by a comma in an RTL cell, the same mechanism as I-11. The qa-BiDi merge rule names only `\en{A}, \en{B}`, so `\num` is not covered. | No grep for `\num{..}, \num{..}` and no rule for it. The visual check samples only 3 pages, and this cell is small on page 10. |
> | D-02 | major | 14 (Fig 13 risk map) | Markers 2 and 5 are hidden under 4 and 6. The `\foreach` list in 07-risks-privacy.tex:32 has duplicate coordinates (3/4/2 and 3/4/4; 2/3/5 and 2/3/6). The caption says the numbers match the table rows, but 2 of 6 are unreadable. | Marker coordinates are hard-coded and collide. There is no offset or jitter logic for equal (p,i) pairs. | qa-img checks "text over shapes" by eye only. A TikZ figure produces no overfull warning (I-06 pattern), and nothing compares figure content to the table. |
> | D-03 | major | 13 (Fig 12 Gantt); also chapters 05 and 06 | Gantt says "Archive subscriptions" runs months 24–36 and "Third hire, paid ads" runs 12–24. code/model.py applies hosting attach from month 1 (HOSTING_ATTACH in `run()`), and the third hire at t>=13 (`fixed_costs`). Chapter 6 table says paid ads start in month 7 (line 19), and Ch 5 and 6 say the hire is in month 13. So Gantt contradicts both the model and the text. | Gantt bars are hand-typed numbers inside the TikZ source, not macros from numbers.tex or model.py. | The I-07 rule ("every numeric claim is a macro") was applied to prose and tables, not to figure source. There is no cross-check between figures and text. |
> | D-04 | major | 3, 4, 17 | TOC spills 2 lines (appendix entries 10 and 11) onto page 3, which is about 95% empty. Page 4: the running header says "Problem & Market" on the page where chapter 1 starts. Page 17 (printed 16): the quote's signature line "אישור: חתימת הלקוח / תאריך" is orphaned at the top of the glossary page, away from the quote (p16). | TOC is just over one page. The header uses the last section mark on the page. The quote is not forced onto a single page (no `\Needspace` or `\samepage`). | qa-typeset only counts pages (17 is within 15..25) and greps the log. It has no per-page fill measurement, no header-vs-first-heading check, and nothing treats the appendix quote as a unit. |
> | D-05 | minor | 10 (Table 5), 17 (Table 11 glossary) | Both read left-to-right (Package or Term at the left, columns in LTR order). Tables 1–4 and 6–10 are RTL with the first column on the right. Table 5 values (390/85/305/78% etc.) are retyped in 04-pricing.tex:62-64 instead of generated from model.py. The same is true of Table 4, Table 6 and the quote. | Tables 5 and 11 use `>{\bfseries\en}l` without an RTL tabular wrapper. There is no `figures/*.tex` snippet generator for these tables. | qa-table says "values from model.py snippets", but model.py only emits the 16 scalar macros, so there was nothing to check against. The column-order rule is read by eye. |
> | D-06 | minor | 9 (Fig 6 tier_mix) | The legend ("Revenue per average order / Contribution margin") overlaps the Pro and Heritage bars and hides their tops. The Table 4 "מה כולל" cell for Pro also runs into the price column with no padding. | In `fig_mix()` the legend uses the default location with no headroom (`plt.legend(frameon=False)`). The Pro cell is wrapped by `X` with no column gap. | qa-img "no text over shapes" is manual, and the figure PDF is not rasterised and inspected. |
>
> Numeric audit: I recomputed with code/model.py and all 16 macros in figures/numbers.tex match (781, 191, 590, month 6, month 20, 82, 187, 841,894, 1,900,074, 661,665, 856,005, 91%, 49,257, 1,680,053, 920,599).
> These numbers are hard-typed in chapters and not macros. They all agree with the code, but each is a drift risk:
> - Ch 2: 3.5 million households, 0.5%, 17,500 customers, 13.7M ILS potential, "<15%"
> - Ch 4: margins 78/76/73%, 305/600/2,120, "almost 2x"
> - Ch 5: N0=25, Ninf=200, tau=14, fixed costs 48,000–66,000, sigma 6% and 18%, 2000 runs
> - Ch 6 and 8: 30 families, 30% attach, 2% churn
> - Ch 1: "2000 scenarios"
> Real disagreements are only D-03 and the policy mismatch below.
> Policy mismatch: the Ch 4 volume discount applies only above 3 orders per family per year, but the Appendix quote applies a 10% family discount (-290) to a first order.
>
> Housekeeping: running build.ps1 modified tracked figures/*.pdf and main.pdf (regenerated binaries), and code/__pycache__/ is untracked. I changed no source files.

The task that produced it is in `prompts/05-agent-messages-verbatim.md` (B2).

## 4. Round 2: fixes and re-review

Mapping of the detector's findings to incidents (from `docs/incidents.md`): D-01 = I-12, D-02 = I-13, D-03 = I-14, D-04 = I-15, D-05 = I-16, D-06 = I-17, quote-policy mismatch = I-18. Findings labelled N-1, N-1b, N-2 and N-3 appear in the commit messages and map to I-19, I-20 and I-21; the messages in which they were raised were exchanged between the detector and fixer sessions and are not in the main session's log.

Commits made by the fixer session (and the final rebuild commit):

| Commit | Time | Subject |
|---|---|---|
| `44767dd` | 2026-11-24T22:55:48+02:00 | fix(qa-BiDi): D-01 flag and remove adjacent LTR runs (num, num), add lint to build |
| `d8bd847` | 2026-11-24T22:56:44+02:00 | fix(qa-img): D-02 generate risk map markers from one register with collision spreading |
| `fed39fb` | 2026-11-24T22:57:51+02:00 | fix(qa-table): D-03 generate Gantt and month macros from model.py constants |
| `3235f7a` | 2026-11-24T23:08:48+02:00 | fix(qa-typeset): D-04 compact TOC, top-of-page header marks, keep quote signature together (CLS 1.3.0) |
| `aaf363b` | 2026-11-25T12:18:05+02:00 | fix(qa-table): D-05 consistent RTL table cells via column type H (CLS 1.3.1), table 5 generated from model.py |
| `cd58ded` | 2026-11-25T12:19:05+02:00 | fix(qa-img): D-06 headroom for tier_mix legend, wider table column padding (CLS 1.3.2) |
| `7ab653b` | 2026-11-25T12:20:46+02:00 | fix(qa-table): quote-policy remove first-order family discount, generate quote and policy numbers from model.py |
| `39e78f6` | 2026-11-25T12:24:34+02:00 | fix(qa-BiDi): N-1 N-1b adjacent runs across percent sign and signs outside the unit, extend lint |
| `2d0ed5f` | 2026-11-25T12:25:52+02:00 | fix(qa-typeset): N-2 header on float-first pages and bibliography page (CLS 1.3.3) |
| `9d0c002` | 2026-11-25T12:26:36+02:00 | fix(qa-infra): N-3 build copies main.pdf to the final PDF; commit rebuilt PDFs and figures |
| `8c4acc4` | 2026-11-25T12:28:23+02:00 | docs: record table column-order limitation (L-01) |

Final rebuild commit (not a fix): `6f2d7c6`, made by the main session after the round, committing regenerated PDFs and figures.

Detector re-review, as read from the detector's terminal (lines visible on screen at that time; earlier lines of the review were not visible and are not quoted):

```
- N-1 and N-1b, accepted:
  - The Monte Carlo paragraph on page 9 now reads "18%. תוציר 2000 לוכה ךסב" instead of the merged "200018 %".
  - The sensitivity text reads "±20% ±40%-ו", with the sign on the correct side.
  - I judged these by eye on the rendered page. Whether the % sign and following comma sit on exactly the right side
    in the Monte Carlo line is the one thing I couldn't settle at that zoom.
- N-2, accepted: the header text of all 16 pages matches the content at the top of each page. Page 13 now says "Risks
  & Privacy" instead of "Conclusion", and the bibliography page no longer says "Glossary".
- N-3, accepted: Memoria-biu-sk26.pdf is byte-identical to main.pdf.
- D-05, still open: all tables lay out columns left to right, so column order is not mirrored in any table. I asked
  the fixer to record this as a known limitation in docs/incidents.md or the README. I found no new defects.
```

Fixer's terminal, same time: "The detector accepted N-1, N-1b, N-2 and N-3 and found no new defects. L-01 is the one remaining caveat: all tables still run left to right."

## 5. Checks made independently on 2026-11-25 (main session)

| Check | Result |
|---|---|
| Clean clone of `origin/main` at `6f2d7c6`, then `build.ps1` | Builds; `lint_bidi: 0 violation(s)`; 16 pages |
| Warnings in the clean-clone `main.log` | No `Overfull \hbox`, no `Missing character`, no undefined references. Present: `Underfull \hbox (badness 10000)` (5 places), `'h' float specifier changed to 'ht'` (13), `Package biblatex Warning: Language 'hebrew' not supported`, `pdf backend: ignoring duplicate destination page.1`, `Unused global option(s)` |
| `Memoria-biu-sk26.pdf` equals `main.pdf` | Yes |
| CLS version vs changelog | `memoria.cls` 1.3.3; `docs/cls-changelog.md` last entry 1.3.3 |
| Incident count | I-01 to I-21 (21) plus L-01 (known limitation, open) |
| Table column direction (header row of every table located in the final PDF) | **Not consistent.** First column on the right (RTL order): Tables 1 (page 3), 5 (page 8), 8 (page 12), 10 (page 15). First column on the left (LTR order): Tables 2 (page 5), 3 and 4 (page 7), 6 (page 8), 7 (page 11), 9 (page 14), 11 (page 15). This contradicts both the detector's round 1 statement (Tables 1 to 4 and 6 to 10 RTL) and its re-review (all tables LTR). Open |

## 6. Open items

1. **Table column order** is inconsistent (section 5). Not fixed. L-01 in `docs/incidents.md` was corrected on 2026-11-25 to match the measurement in section 5; the cause is not established.
2. **Typed numbers in the chapters** that are not macros, listed by the detector (market size, margins, schedule parameters, discount thresholds). At the time of this report three of the listed text locations still contain typed values: `chapters/02-problem-market.tex:26`, `chapters/04-pricing.tex:51`, `chapters/08-conclusion.tex:7`. The detector found them consistent with `code/model.py`; they remain a drift risk.
3. **Percent sign placement** in the Monte Carlo paragraph: the detector said it could not settle this at the zoom used. Not independently verified.
4. **No independent verification of the final PDF after the last fix** by a second agent. Commit `6f2d7c6` only added regenerated binaries.
5. **`qa-super` was never executed as a skill**, so there is no single orchestrated run recording zero blocking findings.

## 7. Status against PRD 6.2
"`qa-super` reports zero blocking findings; the incident log lists every defect found by humans with root cause and why it was missed."

- Incident log: present, 21 incidents plus L-01, with root cause and why-not-detected columns.
- "Zero blocking findings": the last detector re-review found no new defects and no open blocker. But no `qa-super` run is recorded, and an inconsistency in the detector's statements about table direction was found afterwards (section 5). **Criterion stays open.**

## 8. Round 3: documentation audit with four new agents (2026-11-25)

Agents: `lead-qa`, `writer-qa`, `detector-qa`, `fixer-qa`, started in terminal tabs in `C:\BIU01\HW2`. The older sessions with the same role names were not used or touched. Scope: documentation, skill and prompt files only (`README.md`, `TODO.md`, `PLAN.md`, `docs/*.md`, `prompts/*.md`, `skills/*/SKILL.md`). No PDF, code, class, chapter or figure was to be changed. Every message is in `prompts/06-qa-cycle-verbatim.md`.

| id | severity | file | finding (by `detector-qa`) | result |
|---|---|---|---|---|
| F1 | major | `skills/qa-BiDi/SKILL.md` | the file was corrupted: an escape sequence had swallowed `\num`, so the rule behind I-12 was unreadable | fixed by `fixer-qa`, accepted by `detector-qa` and `writer-qa` |
| F2 | major | `prompts/agent-roles.md` | claimed skill files were injected automatically; the scripts do not do that | reworded to say what the scripts do; wording softened to "presumed hand-pasted" after the writer's note |
| F3 | major | `docs/agent-windows.md` | no mention of `agent.ps1`; claimed a window screenshot for `mesh.png`, 20 links, and a lead-forwards flow, none of which matches the record | corrected; the flow marked as plan, 9 lead-to-peer links explained |
| F4 | minor | `skills/qa-table`, `skills/qa-infra` | rules stated as met although L-01 and the one-author history show they are not | marked "not met in 7 of 11 tables, see L-01" and "open, see TODO" |

Other outcomes: `writer-qa` proofread the changed text and raised four minor points, all applied and re-checked; a fifth nit on the TODO wording was applied afterwards. `lead-qa` reported a scope gate PASS (only allowed files changed, no untracked files after the stray temporary file was removed by `fixer-qa`, `git log -1` still `b64ad4c`). The detector's real audit report is reproduced in `prompts/06-qa-cycle-verbatim.md`.

Limits of this round:
- `detector-qa` accepted F1 to F4 before the later wording and header edits; it did not re-review those. `writer-qa` checked them.
- `writer-qa` did not send its proofread to `lead-qa`; `lead-qa` said so and did not guess.
- The round covers documentation only. It does not address L-01 (table order), the typed numbers, or the PDF.
- The edits are uncommitted at the time of writing; commit and push need approval.
