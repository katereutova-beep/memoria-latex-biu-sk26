# Independent detector reviews of commits 093cef5 and b7a3028: tasks and reports, verbatim

Source: the live log of the main session (`~/.claude/projects/C--BIU01-HW2/*.jsonl`), entries of 2026-11-27. The text is unchanged. Times are UTC. The main session fixed the findings afterwards; see `docs/qa-report.md` section 10.

## Review 1: commit 093cef5 (the qa-super run)

### Task sent by the main session
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

### Report received from `detector-qa`
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

## Review 2: commit b7a3028 (L-02 and the fixes of review 1)

### Task sent by the main session
Sent 2026-11-27T15:27:18.207Z to `detector-qa [4d0c68]`.

````
Second task for detector-qa: independent review of local commit b7a3028 (main, not pushed). Read-only again: do not edit, commit or push, and do not build inside C:\BIU01\HW2. Work on an immutable copy made with git -C C:\BIU01\HW2 archive b7a3028 into a scratch folder outside the repo, and build there.
The commit resolves L-02 and fixes your three minor findings (N-1 to N-3). Verify yourself, do not trust docs/qa-report.md section 10:
1. L-02: every table and figure is referenced in the text (25 labels, 25 references). For each reference check that the target is right (the number printed belongs to the table or figure the sentence talks about), that the sentence is meaningful and that it reads in the right order in the rendered PDF (Hebrew prefix plus macro, for example "בטבלה 1", "(איור 8)", "ו-איור 5"). Look at the rendered pages at 100 dpi, not only at the text extraction. Check that no caption, table or figure changed and that nothing but these references changed in the chapter text (compare the words with the PDF of 093cef5).
2. memoria.cls 1.3.5 (tabref, figref) and docs/cls-changelog.md; code/lint_bidi.py: run it, and try to break the new reference check in your scratch copy (unreferenced label, reference to a missing label, a label referenced only inside a comment, a reference spelled with a different macro).
3. N-1: the eight screenshots in docs/screenshots match the current PDF pages (compare each with a fresh render) and the page numbers in the README captions are right. N-2: build.ps1 prints the main.log tail only when the log belongs to the failed build (test a python failure with an old main.log present, and a LuaLaTeX failure). N-3: skills/qa-BiDi/SKILL.md now states what the class does.
4. Rebuild: exit 0, page count, no ?? in the text, headings and page fill, headers. Any regression.
5. README.md, TODO.md, PLAN.md, docs/incidents.md, docs/qa-report.md and prompts/04 and prompts/07: any statement the repository does not support, and any unmet criterion marked as met (PRD 6.2 must stay open unless you find the conditions met; tell me what you think).
Report at most 8 findings, real ones only: id, severity (blocker, major, minor), location, evidence, suggested fix; and say plainly what you verified and found correct. Send the report with SendMessage to the desktop session (copy the from address of this message).
````

### Report received from `detector-qa`
Received 2026-11-27T15:31:36.612Z.

````
Independent review of b7a3028: no blocker, no major, 3 minor findings. I worked in scratch copies made with git archive. I did not edit, commit or build inside C:\BIU01\HW2.

FINDINGS
| id | sev | location | evidence | suggested fix |
|---|---|---|---|---|
| M-1 | minor | chapters/07-risks-privacy.tex, the sentence added after the risk map | It prints "הטבלה בטבלה 8 מפרטת" ("the table in table 8 lists"). The table is named twice. The rendered page 12 confirms it. | Drop "הטבלה": write "\tabref{tab:risks} מפרטת את הסיכונים ... ו\figref{fig:riskmap} ממקם אותם ..." so it reads "טבלה 8 מפרטת ..., ואיור 13 ממקם ...". Then rebuild. |
| M-2 | minor | code/lint_bidi.py `check_references` | It does not strip TeX comments, so a reference or label inside a `%` comment counts. In my scratch copy I commented out the only reference to fig:timeline (`% \figref{fig:timeline}`). The lint printed 0 violations and exited 0, yet the figure would be unreferenced in the PDF. The same applies to a commented-out `\label`. The negative tests in qa-report 10.2 did not cover this. | Strip comments (`(?<!\\)%.*` per line) before the regexes. Add the commented-reference case to the negative tests in 10.2. |
| M-3 | minor | docs/agent-windows.md line 40 | It says "A screenshot of the windows ... has not been taken yet (open item in TODO.md)". That is now false. README "New agents at work" shows four real captures (docs/screenshots/agent-*.png), and TODO.md no longer has that open item (TODO.md lines 22-23 mark it done). | Reword to point at the README section and the four agent-*.png captures. Keep the note that mesh.png is rendered, not a screenshot. |

VERIFIED CORRECT (my own runs)
1. L-02, targets. There are 25 labels and 25 references, one per label. From main.aux I took the number each label prints and checked it against the sentence in the PDF text and the rendered pages. Every reference points at the table or figure its sentence discusses. These match: tab:alternatives=1, fig:personas=1, fig:positioning=2, fig:pipeline=3, tab:sla=2, fig:qdemo=4, fig:qcurve=5, tab:journey=3, tab:tiers=4, fig:tiermix=6, tab:unit=5, tab:assumptions=6, fig:breakeven=7, fig:revcost=8, fig:cash=9, fig:sens=10, fig:mc=11, tab:channels=7, fig:timeline=12, tab:risks=8, fig:riskmap=13, fig:agents=14, tab:incidents=9, tab:quote=10, tab:glossary=11.
2. L-02, reading order. In the rendered text and the pages the prefixes read in the right order ("בטבלה 1", "(ראו איור 2)", "באיור 4, ואיור 5", "(טבלה 4)", "(איור 8)", "ואיור 13"). tab:glossary is the appendix table 11. Apart from M-1, the sentences are meaningful.
3. L-02, nothing else changed. A sorted word-multiset comparison of this PDF against the PDF of 093cef5 shows only the version number (v1.3.5) and the added reference words and sentences, plus punctuation attachment. No caption, table or figure text changed. One of the added sentences is new factual content, not a bare reference: "המחירים בטבלה 10 אינם כוללים מע״מ". It is consistent with the quote's row "סה״כ לפני מע״מ" and the Table 4 caption, so I count it as supported.
4. memoria.cls and changelog. `\ProvidesClass` and `\memoriaversion` both say 1.3.5, and docs/cls-changelog.md has the 1.3.5 row. `\tabref`, `\figref` and the lint behave as stated.
5. Lint negative tests. Unreferenced label: exit 1, "label tab:ghost is never referenced". Reference to a missing fig: or tab: label: exit 1. `\hyperref[..]` as the only use of a label: flagged as unreferenced (a conservative false positive). The comment-only case passed (M-2). A `\cref` to a missing label is not caught, which does not matter because it would fail LuaLaTeX anyway.
6. N-1. The eight page screenshots (title, toc, pipeline, quality, financials, risks, process, quote) are pixel-identical (mean difference 0.0) to a fresh 80 dpi render of PDF pages 1, 2, 5, 6, 9, 13, 14 and 15. The README captions match: pipeline p5, quality p6, financials p9, risks p13, process p14, quote p15, TOC p2. The four agent-*.png captures show only terminal text, with no e-mail or personal data visible.
7. N-2. In scratch copies with a stale main.log (dated 2026-11-20): a Python failure prints no log tail and the stale text never appears, exit 1. A LuaLaTeX failure prints the new log tail, exit 1. Both stop before the copy.
8. N-3. skills/qa-BiDi/SKILL.md now states what the class does for footer, credit line and running header.
9. Rebuild of b7a3028. Exit 0, 16 pages, and main.pdf equals Memoria-biu-sk26.pdf. No "??" in the text, and the log has no Overfull, undefined reference or citation (only 5 Underfull, the biblatex Hebrew line and the duplicate-destination note). No page ends with a heading in the bottom crops of all 16 pages, and the headers name the right sections. The page count and the quote with its signature line on p15 are unchanged.
10. Documentation counts. `docs/incidents.md` has 31 incidents (I-01 to I-31). The 25 labels and 25 references match qa-report 10.2. The statements about the minor fixes in 10.1 are supported. prompts/07 reproduces my previous report. The prompts/04 diff is only the P36 line added.

PRD 6.2: I agree it must stay open for now. The conditions are almost met. After 093cef5 I have confirmed this commit's changes (L-02, N-1 to N-3) as above. What is still missing is a `qa-super` pass on the final tree with this report as step 4. Fix M-1 and M-2 (both are in this commit's scope), rebuild, and then show that pass in the report. After that I would not object to marking it met, with the typed-values issue (9.5 item 2) kept as a listed open item. Marking it met is your call, not mine. I did not check prompts/06 in detail or the 43-message claim in PLAN.md.
````
