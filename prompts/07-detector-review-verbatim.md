# Independent detector review of commit 093cef5: task and report, verbatim

Source: the live log of the main session (`~/.claude/projects/C--BIU01-HW2/*.jsonl`), entries of 2026-11-27. The text is unchanged. Times are UTC. The same session later fixed the three minor findings; see `docs/qa-report.md` section 10.

## Task sent by the main session
Sent 2026-11-27T15:17:56.232Z to `detector-qa [4d0c68]`.

````
QA task for detector-qa: independent review of the qa-super run fixes, commit 093cef5 (main). Read-only. Do not edit, commit or push, and do not build inside C:\BIU01\HW2.
Follow skills/detector/SKILL.md and skills/qa-super/SKILL.md. The main session ran qa-super and fixed things itself; you are the independent confirmation (qa-super step 4).
Work on an immutable copy: extract the commit with git -C C:\BIU01\HW2 archive 093cef5 into a scratch folder outside the repo, and build there (powershell -File build.ps1 inside that folder). Do not trust docs/qa-report.md section 9; verify its claims yourself:
1. build.ps1 stops at the first failed Python, LuaLaTeX or Biber step and does not copy the final PDF (inject a failure in your own scratch copy for each tool, with a sentinel file standing in for Memoria-biu-sk26.pdf).
2. Orphan headings: render every page and check that no page ends with a heading; check the page fill, the running header, and that the quote and its signature line are on one page.
3. The 6 pt text rule: no \tiny left in chapters or generated figures; check the changed TikZ figures at 100 dpi for overlap or clipping (positioning map, pipeline, timeline axis, risk map, agent diagram).
4. Tables 4, 6 and 11 now use macros from code/model.py: confirm the printed values equal the model values and that the words of the PDF are otherwise unchanged against the PDF of commit 8d41a01.
5. CLS 1.3.4 (memoria.cls, docs/cls-changelog.md), code/lint_bidi.py, code/model.py (font discovery with kpsewhich): any regression, wrong claim or missed defect.
6. Anything in README.md, TODO.md, PLAN.md, docs/incidents.md, docs/qa-report.md that states something the repository does not support.
Report at most 8 findings, real ones only: id, severity (blocker, major, minor), location, evidence, suggested fix. Also say plainly what you verified and found correct. Send the report with SendMessage to the desktop session (copy the from address of this message).
````

## Report received from `detector-qa`
Received 2026-11-27T15:22:33.634Z.

````
Independent review of 093cef5: no blocker and no major defect; 3 minor findings. I checked everything in a scratch copy via git archive. I did not edit, commit or build inside C:\BIU01\HW2, and its git status is clean.

FINDINGS
| id | sev | location | evidence | suggested fix |
|---|---|---|---|---|
| N-1 | minor | README.md, "Pages" table (~lines 45-53) | The pipeline figure is on PDF page 5 in the rebuilt PDF; the README says "page 4". The other captions are correct: quality p6, break-even and revenue p9, risk map p13, agent diagram p14, quote p15. docs/screenshots/* is not in the 8d41a01..093cef5 diff, so the images predate the 6 pt and orphan-heading changes. Yet the text says "Screenshots rendered on 2026-11-25 from the current main.pdf". | Change "page 4" to "page 5". Either regenerate the screenshots from the current PDF, or reword to "rendered 2026-11-25 from the PDF of commit 6f2d7c6; layout has since changed slightly". |
| N-2 | minor | build.ps1, Invoke-Step failure branch | From reading the code, not executed: on any failed step it prints `Get-Content main.log -Tail 12`. If model.py, quality_demo or lint fails in a folder that already has an old main.log, those lines come from a previous LaTeX run and look like the cause. In my fresh copies there was no main.log, so I could not see it. | Print the log tail only for the lualatex and biber steps, or only if main.log is newer than the build start. |
| N-3 | minor | docs/qa-report.md 9.4 ("header line" row) vs skills/qa-BiDi/SKILL.md line 6 | The report records that the header line is not one `\en{}` unit, contrary to the skill, and says it was left unchanged. The skill still states a rule the class does not follow. | Reword the qa-BiDi rule to what the class does (it renders correctly), or fix the class. Do not leave a rule that is knowingly false. |

VERIFIED CORRECT (my own runs, not the report)
1. Build and failure injection. The build of 093cef5 exits 0 and gives 16 pages. main.pdf and Memoria-biu-sk26.pdf are byte-identical after the build, and the rebuilt PDF has the same words as the committed main.pdf. Using a sentinel text in place of Memoria-biu-sk26.pdf, I injected three failures: a syntax error in model.py, an undefined macro in chapter 8, and a broken bib/references.bib. Each exited 1 and the sentinel survived. The step errors were "Build step 'model.py' failed with exit code 1", "Build step 'lualatex pass 1' failed with exit code 1" and "Build step 'biber' failed with exit code 2". Each said the final PDF was not copied. I did not re-run the \tiny lint case or the "no tool installed" case.
2. Pages. I rendered all 16 pages (contact sheets at 100 dpi). No page ends with a heading. The headings that sit low on a page, such as chapters 3, 4, 5, 6, 7, 8, 9, "Production Process" and "Financial Forecast", are followed by body text, a table or a figure on the same page. The running header names the section active at the top of each page. The quote (Table 10) and its signature line "אישור: חתימת הלקוח / תאריך" are together on PDF page 15, followed by the glossary on 16. The TOC is one page and its numbers match the printed pages.
3. 6 pt rule. A grep finds no \tiny in chapters, figures or memoria.cls. Only lint_bidi.py mentions it, as a rule. A 130 dpi look at the Gantt (month axis) and agent diagram, and 100 dpi sheets for the positioning map, pipeline and risk map, show no clipping or overlap. Risk markers 1-6 are all visible, with 2/4 and 5/6 side by side.
4. Tables 4, 6 and 11. The macros in numbers.tex are PriceBasic 390, VarBasic 85, ShareBasic 55, PricePro 790, VarPro 190, SharePro 35, PriceHeritage 2,900, VarHeritage 780, ShareHeritage 10, FixedMin 48,000, FixedMax 66,000, StaffBefore 2, StaffAfter 3, OrdersStart 25 and the QuoteXUnit values; the printed values match them. A sorted word-multiset diff against the PDF of 8d41a01 shows only the CLS version (v1.3.3 to v1.3.4), the TOC page numbers (12 to 13 and 14 to 15), running-header words that moved with the repagination, and extraction-order noise. No printed value changed. The regenerated figures and numbers.tex, quality.tex, gantt.tex, riskmap.tex and model_excerpt.py are identical to the committed ones (all 8 figure PDFs rasterise the same).
5. CLS 1.3.4, lint and model. memoria.cls (\ProvidesClass and \memoriaversion) and docs/cls-changelog.md all say 1.3.4. The build log has no "Unused global option" and no float-specifier warnings; the only warnings are 5 Underfull \hbox plus the biblatex Hebrew one. In lint_bidi.py I saw no regression: the \tiny, [h] and float-after-heading rules look right, and the order model.py, then lint lets it check the generated figures/*.tex. The kpsewhich font discovery in model.py works here, and no Path.home() is left.
6. Documentation claims. The reported counts match what I measured: 28 commits (27 Katrina Reutova, 1 Alexandra Pirogan, so both partners have commits), no commit subject under 20 characters, 0 of 11 tables and 0 of 14 figures referenced (L-02), and \tiny uses of 9 in chapters plus 6 in riskmap.tex. In round 4, "8 findings, 3 major, 5 minor, 7 fixed, 1 open" matches the findings table. The PRD 6.2 wording is honest about the missing independent detector; this review does not close it for you, because I had no part in the fixes.

Not covered: I did not rebuild on a machine without TeX, and I did not inspect Q-05's claim about a clean `kpsewhich` fallback beyond reading the code.
````
