# memoria.cls changelog

| Version | Change | Defect |
|---|---|---|
| 1.0.0 | Initial class: banner, footer, palette, title page, keybox | - |
| 1.0.1 | Title page spacing; footer and credit line as single LTR units | I-01, I-02 |
| 1.1.0 | `\Needspace` before sections and subsections; `lstset` without visible spaces; Libertinus Mono bold/italic fall back to regular | I-08 |
| 1.2.0 | `keybox` uses the standard tcolorbox skin (enhanced TikZ skin drew its frame off-page in RTL) | I-09 |
| 1.2.1 | `\emergencystretch` for narrow paragraphs and bibliography; PDF-string-safe `\en`/`\num` in bookmarks | overfull hboxes, hyperref warnings |
| 1.3.0 | Running header shows the section active at the top of the page (aux-based per-page marks, bibliography included); `tocdepth` 1 (compact TOC); `keeptogether` environment | I-15 |
| 1.3.1 | Column type `H`: tabularx `X` typeset as a right-to-left paragraph (all Hebrew table cells) | I-16 |
| 1.3.2 | `\tabcolsep` 9pt (default 6pt let a wrapped cell touch the next column) | I-17 |
| 1.3.3 | Header top-of-page test also requires that no float took space at the top (`\vsize`); bibliography heading marks before its heading | I-20 |
