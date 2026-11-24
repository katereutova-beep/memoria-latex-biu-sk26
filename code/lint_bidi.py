"""qa-BiDi lint: adjacent LTR fragments separated only by neutral characters.

Two \\en{..}/\\num{..} runs with only whitespace or punctuation between them are reordered
by the bidi algorithm inside Hebrew paragraphs (incidents I-11, I-12). They must be merged
into one unit or separated by a Hebrew word.
Run: python code/lint_bidi.py   (exit code 1 when a violation is found)
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARG = r"\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}"          # braces nested up to 3 levels
CMD = r"\\(?:num|en|code)"
PAIR = re.compile(CMD + ARG + r"[\s,;:/.\-–()]*" + CMD + ARG)


def main():
    bad = 0
    for f in sorted((ROOT / "chapters").glob("*.tex")) + [ROOT / "main.tex"]:
        text = f.read_text(encoding="utf-8")
        for m in PAIR.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            print(f"{f.relative_to(ROOT)}:{line}: adjacent LTR runs: {m.group(0)[:70]!r}")
            bad += 1
    print(f"lint_bidi: {bad} violation(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
