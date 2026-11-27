"""qa-BiDi / qa-table lint for the LaTeX sources.

1. Adjacent LTR fragments: two \\en{..}/\\num{..} runs with only whitespace or punctuation between
   them are reordered by the bidi algorithm inside Hebrew paragraphs (incidents I-11, I-12).
   They must be merged into one unit or separated by a Hebrew word.
2. Tables: every tabularx needs an H column (CLS column type: X typeset as an RTL paragraph), no bare
   X, and no \\en in the column spec (it swallows the first token of each cell); otherwise
   the table is laid out differently from all the others (incident I-16).
3. Figure text size: `\tiny` is 6 pt at the 11 pt body size and breaks the 7 pt legibility rule of qa-img
   (incident I-24). Use `\scriptsize` (8 pt) or larger, also in the generated figures/*.tex.
4. Float placement: a table or figure that directly follows a heading must use [H] (float package), otherwise the
   heading can be left alone at the bottom of a page (incident I-23); `[h]` is not allowed anywhere, because LaTeX
   silently replaces it by `[ht]` and prints a warning.
Run: python code/lint_bidi.py   (exit code 1 when a violation is found)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARG = r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"          # braces nested up to 3 levels
CMD = r"\\(?:num|en|code)"
PAIR = re.compile(CMD + ARG + r"(?:\\%|%)?[\s,;:/.\-\u2013()]*" + CMD + ARG)
TABX = re.compile(r"\\begin\{tabularx\}\{[^{}]*\}\{(.*)\}\s*$", re.M)


def check_tables(f, text):
    bad = 0
    for m in TABX.finditer(text):
        spec = m.group(1)
        line = text.count("\n", 0, m.start()) + 1
        plain = re.sub(r"\\[A-Za-z]+", "", spec)
        if "H" not in plain:
            print(f"{f.relative_to(ROOT)}:{line}: tabularx without an H column")
            bad += 1
        if re.search(r"(?<![A-Za-z])X(?![A-Za-z])", plain):
            print(f"{f.relative_to(ROOT)}:{line}: bare X column, use H (right-to-left paragraph cell)")
            bad += 1
        if r"\en" in spec:
            print(f"{f.relative_to(ROOT)}:{line}: \\en inside a column spec")
            bad += 1
    return bad


HEAD_FLOAT = re.compile(r"\\(?:sub)?section\{[^\n]*\}\s*\n\s*\\begin\{(?:table|figure)\}(\[[^\]]*\])?")
ANY_FLOAT = re.compile(r"\\begin\{(?:table|figure)\}\[h\]")


def check_floats_and_sizes(f, text):
    bad = 0
    for m in re.finditer(r"\\tiny\b", text):
        print(f"{f.relative_to(ROOT)}:{text.count(chr(10), 0, m.start()) + 1}: \\tiny is 6 pt, below the 7 pt rule; use \\scriptsize")
        bad += 1
    if f.suffix == ".tex" and f.parent.name == "chapters":
        for m in HEAD_FLOAT.finditer(text):
            line = text.count(chr(10), 0, m.start()) + 1
            if m.group(1) != "[H]":
                print(f"{f.relative_to(ROOT)}:{line}: float directly after a heading must be [H]")
                bad += 1
            # [H] alone does not keep a chapter-level \section with its float (titlesec rule box): reserve the space
            if m.group(0).lstrip().startswith("\\section") and "\\Needspace" not in text[max(0, m.start() - 60):m.start()]:
                print(f"{f.relative_to(ROOT)}:{line}: \\section followed directly by a float needs \\Needspace*{{..}} in front of it")
                bad += 1
        for m in ANY_FLOAT.finditer(text):
            print(f"{f.relative_to(ROOT)}:{text.count(chr(10), 0, m.start()) + 1}: placement [h] is replaced by [ht] with a warning; use [ht] or [H]")
            bad += 1
    return bad


def main():
    bad = 0
    for f in sorted((ROOT / "figures").glob("*.tex")):
        bad += check_floats_and_sizes(f, f.read_text(encoding="utf-8"))
    for f in sorted((ROOT / "chapters").glob("*.tex")) + [ROOT / "main.tex"]:
        text = f.read_text(encoding="utf-8")
        bad += check_tables(f, text)
        bad += check_floats_and_sizes(f, text)
        for m in re.finditer(r"\\num\{\\pm|\\num\{[-+]", text):
            print(f"{f.relative_to(ROOT)}:{text.count(chr(10), 0, m.start()) + 1}: sign outside the unit, "
                  r"write \en{±20\%} so the sign stays on the number")
            bad += 1
        for m in PAIR.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            print(f"{f.relative_to(ROOT)}:{line}: adjacent LTR runs: {m.group(0)[:70]!r}")
            bad += 1
    print(f"lint_bidi: {bad} violation(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
