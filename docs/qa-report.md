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

## 9. Round 4: qa-super run (2026-11-27)

Method: the main session followed `skills/qa-super/SKILL.md`: a clean build, then `qa-infra`, `qa-cls-version`, `qa-typeset`, `qa-BiDi`, `qa-table`, `qa-code` and `qa-img`. Each check was done with a command or by looking at the rendered page; defects were fixed in the build script, the class, the generator or the lint, the project was rebuilt and the checks were repeated. Step 4 of `qa-super` (confirmation by `detector`, repair by `fixer`) was played by the main session: no separate agent confirmed the findings or the fixes. The `*-qa` agents of round 3 were not used. This is the main limit of this run.

### 9.1 Builds
| Run | Result |
|---|---|
| two consecutive builds before the fixes | exit 0, 16 pages, identical text |
| three builds after the fixes | exit 0, 16 pages, about 30 s each. The first build after the `float` package was added took 531 s, probably a package installation by MiKTeX (not verified) |
| copy of the tracked files without auxiliary files (control of the failure injection) | exit 0, 16 pages, the same PDF text as the project |

Log after the fixes: no `Overfull \hbox`, no `Underfull \vbox`, no missing glyph, no undefined reference or citation. Remaining entries: `Underfull \hbox` (5, in narrow table cells), biblatex "Language 'hebrew' not supported", pdf backend "duplicate destination page.1".

### 9.2 Failure injection of `build.ps1` (finding Q-01)
Every case ran in a throw-away copy; a sentinel text stood in place of `Memoria-biu-sk26.pdf`; the project folder was not touched.

| Case | Old script | New script |
|---|---|---|
| no failure (control) | exit 0, PDF replaced | exit 0, PDF replaced, 16 pages |
| syntax error in `code/model.py` | exit 0, PDF replaced | exit 1, PDF untouched ("Build step 'model.py' failed") |
| undefined macro in a chapter (LuaLaTeX) | exit 0, PDF replaced | exit 1, PDF untouched |
| corrupt `bib/references.bib` (Biber, exit code 2) | exit 0, PDF replaced | exit 1, PDF untouched |
| `\tiny` in a chapter (lint) | not run (the lint was new) | exit 1, PDF untouched |

### 9.3 Findings (record format of `qa-super`)
| id | skill | severity | location | evidence | root cause | status |
|---|---|---|---|---|---|---|
| Q-01 | qa-infra | major | `build.ps1` | table above: exit 0 and the final PDF overwritten after a failed Python, LuaLaTeX or Biber step, 3 of 3 cases | exit codes of native commands were ignored | fixed (I-22), verified |
| Q-02 | qa-typeset | major | PDF page 6, subsection 4.2 | rendering of every page: the last body line of page 6 was a heading, its table was on page 7. A second case, the glossary heading on page 15, appeared while fixing the first | a heading directly followed by a float | fixed (I-23); after the fix no page ends with a heading (checked on 15 pages) |
| Q-03 | qa-img | major | 9 uses of `\tiny` in 4 chapters and the code listing, 6 in the generated `riskmap.tex` | `\tiny` is 6 pt, the rule is 7 pt | rule not automated | fixed (I-24); lint added; the five figures that changed were inspected at 100 dpi |
| Q-04 | qa-cls-version | minor | `main.tex` | formatting commands around `\tableofcontents` | the fix of I-04 was put into `main.tex` | fixed (I-25) |
| Q-05 | qa-code | minor | `code/model.py`, `code/quality_demo.py` | font path built from the user's profile directory; unused import | machine-specific discovery | fixed (I-26); the rendered figures are identical to the committed ones |
| Q-06 | qa-table | minor | tables 4, 6 and 11 | tier prices, costs and shares, fixed-cost range, head counts, first-month orders, quote quantities and unit prices were typed | values never connected to the generator | fixed for model constants (I-27); the words of the PDF are unchanged |
| Q-07 | qa-table, qa-img | minor | all tables and figures | 0 of 11 tables and 0 of 14 figures are referenced in the text | captions and labels only | **open** (L-02) |
| Q-08 | qa-cls-version | minor | `memoria.cls` | LaTeX warning "Unused global option(s): twoside" | the option `twoside=false` is unknown to the article class | fixed (CLS 1.3.4) |

Observations that are not recorded as defects: the first column is on the right in 4 of 11 tables and on the left in 7 (a mix of directions alone is not a defect, see L-01); `Underfull \hbox` (5) in narrow table cells; the biblatex language and "duplicate destination" warnings, which no skill sets a threshold for.

### 9.4 Results per skill after the fixes
| Skill | Check | Result |
|---|---|---|
| qa-infra | required files and every chapter included by `main.tex` | all present |
| qa-infra | build from a copy of the tracked files | pass (exit 0, 16 pages) |
| qa-infra | `.gitignore` ignores auxiliary files, keeps `Memoria-biu-sk26.pdf` and `main.pdf` | pass |
| qa-infra | secrets and size | no match for key, token or password patterns in tracked text files; no credential-like file name; largest tracked file 497 KB |
| qa-infra | partners, messages, branch | both partners have commits; no commit subject shorter than 20 characters; one branch, `main` |
| qa-infra | build stops on failure; final PDF equals `main.pdf` | pass (9.2); pass |
| qa-cls-version | `\memoriaversion` = `\ProvidesClass` = last changelog row | 1.3.4 in all three |
| qa-cls-version | every commit that touched the class has a changelog row | pass (versions 1.0.0 to 1.3.3 in the history, 1.3.4 in the working tree) |
| qa-cls-version | no overrides in `main.tex` | pass after Q-04 |
| qa-typeset | `Overfull \hbox`, `Underfull \vbox` | 0, 0 |
| qa-typeset | page fill | 67.3 % at the lowest (page 15), 100 % at the highest; before the fixes the lowest was 30.9 % |
| qa-typeset | orphan headings | none after Q-02 |
| qa-typeset | `??` in the PDF text; undefined citations | 0; 0 |
| qa-typeset | page count | 16, inside 15 to 25 and equal to the previous run |
| qa-typeset | running header | the header of each of the 15 pages names the section active at its top; the glossary page shows "Glossary" because that section starts at its top |
| qa-typeset | table of contents; quote and signature line | chapters only, one page; the signature line is on the page of the quote |
| qa-BiDi | `lint_bidi.py`; `Missing character` | 0 violations; 0 |
| qa-BiDi | Latin words outside `\en{}`, `\code{}` and `\num{}` | 4 hits, all the dimensions of `\rule{4cm}{0.4pt}` (false positives) |
| qa-BiDi | rendered pages | pages 3, 8, 9 and 15 at 85 dpi, crops of pages 4 to 6 and 11 to 14: no reversed phrase seen |
| qa-BiDi | currency and percent | no currency symbol is used (amounts are written as a number followed by the word for shekels); 25 `\num{}\%` and 2 `\en{..\%}` forms |
| qa-BiDi | header line | `\en{Memoria}` and the section title are not one `\en{}` unit as the skill states; it renders correctly on every page (recorded, not changed) |
| qa-table | caption above the table; header rows; width | 11 of 11; 11 of 11; no overflow |
| qa-table | total rows bold; values from `model.py` | pass for the two tables with total rows; fixed for model constants (Q-06), other typed values remain (9.5) |
| qa-table | each table referenced in the text | 0 of 11, open |
| qa-code | generators from a copy of the tracked files | pass |
| qa-code | determinism | two runs give identical `numbers.tex`, `quality.tex`, `gantt.tex`, `riskmap.tex`, `model_excerpt.py` and identical rendered images of all 8 figures; they are also identical to the committed figures |
| qa-code | absolute or profile paths; unused imports; Hebrew labels | none; none; no Hebrew string in the code, so the figure labels are English |
| qa-code | excerpt generated from the source; listing fits the page | yes (`inspect.getsource`); yes, with the monospace font and a light box (page 11 viewed) |
| qa-img | figures are vector or TikZ; caption and label | 14 of 14; no raster or external image in the sources |
| qa-img | legibility | matplotlib text 7.6 to 9.3 pt; no `\tiny` left (lint) |
| qa-img | markers and legends at 100 dpi | all six risk markers visible; the legends of tier mix, break-even, revenue and quality curve do not cover data |
| qa-img | referenced in the text | 0 of 14, open |

### 9.5 Remaining issues
1. **L-02**: no table and no figure is referenced in the text. Not fixed; it changes the wording of the report.
2. Typed values that are not constants of `model.py`: package photo limits (10 and 50), the service targets of table 2, the channel months of table 7, the validity of the quote, the equation constants N-infinity and tau, and the numbers inside the prose of chapters 2, 4, 5, 6 and 8.
3. `qa-super` step 4 was not done with an independent detector (see the method above). Until a separate session confirms this run, the criterion of PRD 6.2 stays open in `TODO.md`.
4. The informational warnings listed above are unchanged.
5. Without a TeX installation `model.py` falls back to the default matplotlib font, so the figures would differ in typeface on such a machine.

## 10. Round 5: independent detector review and the resolution of L-02 (2026-11-27)

### 10.1 Independent review of commit 093cef5 (qa-super step 4)
`detector-qa` (a separate Claude Code session, not the main session) reviewed commit 093cef5 on an immutable copy made with `git archive`, built there, and did not touch the project folder. The task and the report, verbatim, are in `prompts/07-detector-review-verbatim.md`. Result: no blocker, no major finding, three minor findings.

| id | severity | finding | resolution |
|---|---|---|---|
| N-1 | minor | the README gave page 4 for the pipeline figure (it is on page 5); the screenshots predated the layout fixes although the text called them current | screenshots rendered again from the current PDF, captions corrected (I-29) |
| N-2 | minor | on a failed Python or lint step `build.ps1` could print the tail of an old `main.log` | the tail is printed only when `main.log` was written by this build; tested in two copies (I-30) |
| N-3 | minor | `qa-BiDi` demanded one `\en{}` unit for the header line, which the class does not do | the skill states what the class does (I-31) |

What the detector verified itself (from its report): the build of 093cef5 exits 0 with 16 pages and `main.pdf` equals the final PDF; failure injection for model.py, LuaLaTeX and Biber exits 1 with the sentinel untouched; no page ends with a heading; headers, quote and signature on one page; no `\tiny` left and the changed figures show no overlap at 100 and 130 dpi; the macro values of tables 4, 6 and 11 equal the printed values and the words of the PDF are otherwise unchanged against 8d41a01; the figures regenerate identically; the commit and finding counts in the documentation match. Not covered by the detector: a rebuild on a machine without TeX; the `\tiny` lint case and the "tool not installed" case were not re-run by it (the lint case was run by the main session, see 9.2).

### 10.2 L-02 resolved (finding Q-07)
Repair rule applied: the cause was that nothing in the toolchain asked for references, so the fix is in the class, the lint and the skills, followed by the text.
- Class 1.3.5: `\tabref{tab:..}` ("טבלה 4") and `\figref{fig:..}` ("איור 7"), so a reference reads correctly in a Hebrew sentence.
- `code/lint_bidi.py`: every `tab:` and `fig:` label must be referenced in the chapters, and every reference must point to a label. Negative test in a scratch copy: an unreferenced label and a reference to a missing label were both reported (exit 1).
- Skills `qa-table` and `qa-img` state the rule and the macros.
- Text: 25 references for 11 tables and 14 figures, each placed in the sentence that discusses the table or figure (for example "ההשוואה בין החלופות מוצגת בטבלה 1", "התוצאה מוצגת באיור 10"), or in one added sentence where the surrounding text had nothing to attach to. No caption was changed; no table or figure was moved.
- Recheck after the rebuild: exit 0, 16 pages, no `??` in the PDF text, no undefined reference or citation in the log; page fill 67.3 % at the lowest, no page ends with a heading; pages 3, 5, 9 and 10 were inspected at 85 dpi: the references read in the right order ("בטבלה 1", "(איור 8)", "איור 4, ואיור 5"). 25 labels, 25 references.
- Content change that comes with L-02: 14 sentences were added or extended in chapters 2 to 7, 9 and the quote appendix (the 25 references); nothing else in the chapters changed.

### 10.3 Status after this round
- The incident log is at I-31 and L-01 (observation only). L-02 is closed (I-28).
- Open: the typed values that are not constants of `model.py` (9.5 item 2) and the informational warnings (9.5 item 4); a rebuild without TeX was never tested.
- PRD 6.2: the independent detector confirmed round 4 (no blocker, no major). The L-02 changes and the three minor fixes of this round were made after that review; their confirmation is recorded in `TODO.md` once a second review of the current commit exists.
