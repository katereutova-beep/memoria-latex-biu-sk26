# User prompts, verbatim from the session log

Source: the exported transcript of the working session (`transcript.jsonl`, entries of type `user` with origin `human`), extracted by script on 2026-11-25. Times are UTC as recorded in the log. Nothing is paraphrased or translated in the third column (P01 is linked to its own file because of its length); the fourth column is a factual pointer to what the repository history or the log shows happened next.

`prompts/01-kickoff.md`, `02-decisions.md` and `03-go-and-steering.md` are earlier summaries (translated) of P01 to P05. This file is the verbatim record and supersedes them where they differ in wording. The answers given through the question cards (topic delegated, partner confirmed, group code `biu-sk26`, mixed Hebrew and English, 15+ pages, SendMessage windows) are tool results in the log, not typed prompts; `02-decisions.md` records them.

| # | Time (UTC) | Prompt | What followed |
|---|---|---|---|
| P01 | 2026-11-24T19:15:38.491Z | Full text, including the pasted brief and the three attachment references: [P01-kickoff-verbatim.md](P01-kickoff-verbatim.md). The user's own sentence: אם יש לך שאלות , תשאל אותי אל תליט על דעת עצמך | Read the three PDFs, asked four questions (topic, language/length, group code, agent method) before creating files |
| P02 | 2026-11-24T19:18:43.133Z | 1. תחליט אתה איזה נושא של המסמך , לפי הנחיות של המרצה  2. כן  3. C:\BIU01\HW2 | Created C:\BIU01\HW2, checked lualatex, biber, python, git, gh |
| P03 | 2026-11-24T19:19:56.756Z | אשר, התחל | Commit 4ff1796 (PRD.md, PLAN.md, TODO.md) |
| P04 | 2026-11-24T19:22:54.424Z | כן, המשך | Commits 1ecb2a4 (class and skeleton), 6030c9c (QA skills); stopped to ask before pip install |
| P05 | 2026-11-24T19:27:04.560Z | כן, התקן | Installed matplotlib and numpy; commits 27f2981, 7cb0653, 007fa59, e2ad9d7 (model, chapters, QA round 1, README) |
| P06 | 2026-11-24T19:52:46.393Z | כן, צור ודחף | Created the public GitHub repository and pushed main |
| P07 | 2026-11-24T20:37:39.700Z | כן, הכן | Commit f2c7423 (start-agents.ps1, docs/agent-windows.md) |
| P08 | 2026-11-24T20:38:55.064Z | כן, דחוף | Pushed f2c7423 |
| P09 | 2026-11-24T20:40:04.931Z | להריץ את start-agents.ps1 ואת בדיקת PING/PONG, לצלם ולהוסיף ל-README.  אתה לא יכול לעשות זאת ? | Opened five agent terminals, ran the PING/PONG check, commit c7f615e (agent.ps1, docs/mesh-check.md, README section) |
| P10 | 2026-11-24T20:43:27.897Z | כן, דחוף | Pushed c7f615e |
| P11 | 2026-11-24T20:45:00.704Z | בשביל מה לנקות סשנים כפולים ? | Answer only, no file changes |
| P12 | 2026-11-24T20:48:28.555Z | זה משפיעה על הציון של מטלה ? | Answer only, no file changes |
| P13 | 2026-11-24T20:49:02.609Z | להמשיך לסבב הצוות האדום | Sent the round 2 task to detector [72ab50] (log: SendMessage 2026-11-24T20:49:11Z) |
| P14 | 2026-11-24T20:50:16.086Z | אז מה עושים עכשיו ? | Answer only; read the detector terminal |
| P15 | 2026-11-25T17:05:41.595Z | הכל כבר בתוך הגיט? | Checked git status and log: 11 fixer commits local, binaries modified |
| P16 | 2026-11-25T17:07:00.372Z | כן | Rebuilt, committed 6f2d7c6 (rebuilt PDF and figures) and pushed |
| P17 | 2026-11-25T17:09:11.628Z | שלח לי קישור לגיט | Answer only: repository link |
| P18 | 2026-11-25T17:13:35.579Z | אוקיי ,  אתה עדיין עובד? או שסיימת את העבודה ? | Answer only: status |
| P19 | 2026-11-25T17:14:25.895Z | תסגור את הטרמינלים אם כבר סיימת לעבוד | Closed terminal tabs c5 to c9 |
| P20 | 2026-11-25T17:30:12.027Z | Audit README.md, TODO.md, PLAN.md and PRD.md against the current repository and final PDF. Check page count, CLS version, incident count, screenshots, missing files, completed tasks and outstanding requirements. Report exact discrepancies and proposed changes. Do not modify files until I approve. Do not fabricate completed work or evidence. | Read-only audit of README, TODO, PLAN, PRD |
| P21 | 2026-11-25T17:34:53.496Z | Approve documentation fixes only. Update README, TODO and PLAN with verified facts. Regenerate screenshots from the latest PDF. Create qa-report.md and recover the missing numbered prompts using actual session logs only. Verify all internal links. Do not lower PRD acceptance criteria, change the PDF, create a self-assessment, or fabricate agent activity. Keep unmet requirements open. Show me all changes before committing and pushing. | This documentation update (uncommitted until approved) |
