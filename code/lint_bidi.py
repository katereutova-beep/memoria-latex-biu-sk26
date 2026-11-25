"""qa-BiDi / qa-table lint for the LaTeX sources.

1. Adjacent LTR fragments: two \\en{..}/\\num{..} runs with only whitespace or punctuation between
   them are reordered by the bidi algorithm inside Hebrew paragraphs (incidents I-11, I-12).
   They must be merged into one unit or separated by a Hebrew word.
2. Tables: every tabularx needs an H column (CLS column type: X typeset as an RTL paragraph), no bare
   X, and no \\en in the column spec (it swallows the first token of each cell); otherwise
   the table is laid out differently from all the others (incident I-16).
Run: python code/lint_bidi.py   (exit code 1 when a violation is found)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARG = r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"          # braces nested up to 3 levels
CMD = r"\\(?:num|en|code)"
PAIR = re.compile(CMD + ARG + r"[\s,;:/.\-\u2013()]*" + CMD + ARG)
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


def main():
    bad = 0
    for f in sorted((ROOT / "chapters").glob("*.tex")) + [ROOT / "main.tex"]:
        text = f.read_text(encoding="utf-8")
        bad += check_tables(f, text)
        for m in PAIR.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            print(f"{f.relative_to(ROOT)}:{line}: adjacent LTR runs: {m.group(0)[:70]!r}")
            bad += 1
    print(f"lint_bidi: {bad} violation(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
