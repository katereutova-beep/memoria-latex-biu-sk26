%% memoria.cls -- custom class for the Memoria business plan (Assignment 02, biu-sk26)
%% Requires LuaLaTeX. Hebrew (RTL) + English (LTR) with one OpenType family.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{memoria}[2026/11/24 v1.2.1 Memoria bilingual report class]
\newcommand{\memoriaversion}{1.2.1}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt,a4paper,twoside=false]{article}

\RequirePackage{iftex}
\ifluatex\else\ClassError{memoria}{LuaLaTeX is required}{Compile with lualatex.}\fi

\RequirePackage[a4paper,top=3.2cm,bottom=2.8cm,inner=2.6cm,outer=2.6cm,headheight=28pt]{geometry}
\RequirePackage{fontspec}
\RequirePackage{polyglossia}
\setmainlanguage{hebrew}
\setotherlanguage{english}
\setmainfont{Libertinus Serif}
\setsansfont{Libertinus Sans}
\setmonofont{Libertinus Mono}[Scale=0.9,BoldFont={Libertinus Mono},ItalicFont={Libertinus Mono}]
\newfontfamily\hebrewfont{Libertinus Serif}
\newfontfamily\hebrewfontsf{Libertinus Sans}
\newfontfamily\hebrewfonttt{Libertinus Mono}[Scale=0.9]

\RequirePackage{xcolor}
\definecolor{mteal}{HTML}{0B5563}
\definecolor{mtealdark}{HTML}{073B45}
\definecolor{mamber}{HTML}{E0A030}
\definecolor{msepia}{HTML}{8A6A4B}
\definecolor{mpaper}{HTML}{FBF6EC}
\definecolor{mink}{HTML}{1F2A30}
\definecolor{mgrey}{HTML}{6B7780}

\RequirePackage{microtype}
\RequirePackage{graphicx}
\RequirePackage{booktabs,tabularx,array,multirow}
\RequirePackage{amsmath,amssymb}
\RequirePackage{enumitem}
\RequirePackage{caption}
\RequirePackage[most]{tcolorbox}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,calc,fit,backgrounds}
\RequirePackage{fancyhdr}
\RequirePackage{titlesec}
\RequirePackage{etoc}
\RequirePackage{needspace}
\RequirePackage{etoolbox}
\RequirePackage[backend=biber,style=ieee,sorting=none]{biblatex}
\RequirePackage[hidelinks,colorlinks=true,linkcolor=mteal,urlcolor=mteal,citecolor=mteal]{hyperref}

%% ---- language helpers ----------------------------------------------------
\newcommand{\en}[1]{\textenglish{#1}}          % inline English inside Hebrew
\newcommand{\num}[1]{\en{#1}}
\setlength{\emergencystretch}{3em}
\pdfstringdefDisableCommands{\def\en#1{#1}\def\num#1{#1}\def\code#1{#1}}                  % numbers/units stay LTR
\newcommand{\code}[1]{\en{\texttt{#1}}}

%% ---- headings --------------------------------------------------------------
\titleformat{\section}{\Large\bfseries\color{mteal}\sffamily}{\thesection}{0.7em}{}[{\color{mamber}\titlerule[1.2pt]}]
\titleformat{\subsection}{\large\bfseries\color{mtealdark}\sffamily}{\thesubsection}{0.6em}{}
\titlespacing*{\section}{0pt}{1.6em}{0.9em}
\titlespacing*{\subsection}{0pt}{1.2em}{0.5em}
\pretocmd{\section}{\Needspace*{9\baselineskip}}{}{}
\pretocmd{\subsection}{\Needspace*{5\baselineskip}}{}{}
\lstset{showstringspaces=false,columns=fullflexible,keepspaces=true}

%% ---- header banner and footer ---------------------------------------------
\newcommand{\memoriagroup}{biu-sk26}
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\fancyhead[C]{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[mteal] ([yshift=-0.9cm]current page.north west) rectangle ([yshift=-0.0cm]current page.north east);
    \fill[mamber] ([yshift=-1.0cm]current page.north west) rectangle ([yshift=-0.9cm]current page.north east);
    \node[anchor=east,text=white,font=\sffamily\small\bfseries] at ([xshift=-1.8cm,yshift=-0.45cm]current page.north east) {\en{Memoria}~\textbullet~\leftmark};
    \node[anchor=west,text=white,font=\sffamily\footnotesize] at ([xshift=1.8cm,yshift=-0.45cm]current page.north west) {\en{Business Plan \& Quote}};
  \end{tikzpicture}}
\fancyfoot[C]{%
  \begin{tikzpicture}[remember picture,overlay]
    \draw[mamber,line width=0.6pt] ([xshift=2cm,yshift=1.5cm]current page.south west) -- ([xshift=-2cm,yshift=1.5cm]current page.south east);
  \end{tikzpicture}%
  {\sffamily\footnotesize\color{mgrey}\en{\memoriagroup\ \textbullet\ Assignment 02\ \textbullet\ \thepage}}}

\renewcommand{\sectionmark}[1]{\markboth{#1}{}}

%% ---- boxes -------------------------------------------------------------------
% The tcolorbox title bar renders as a detached block in RTL, so the title is typeset
% inside the box body instead (class v1.2.0, incident I-09).
\pgfkeys{/memoria/.cd,title/.store in=\keyboxtitle,title/.default=}
% tcolorbox frames are only drawn correctly in an LTR context, so the box is built inside
% `english` and its content is switched back to Hebrew.
\newtcolorbox{keyboxinner}[1][]{colback=mpaper,colframe=mteal,
  boxrule=0.6pt,leftrule=3.5pt,arc=0pt,left=8pt,right=8pt,top=6pt,bottom=6pt,
  before upper={\begin{hebrew}\def\keyboxtitle{}\pgfkeys{/memoria/.cd,#1}%
    \ifx\keyboxtitle\empty\else{\sffamily\bfseries\color{mteal}\keyboxtitle\par}\smallskip\fi},
  after upper={\end{hebrew}}}
\newenvironment{keybox}[1][]{\begin{english}\begin{keyboxinner}[#1]}{\end{keyboxinner}\end{english}}

%% ---- tables --------------------------------------------------------------------
\renewcommand{\arraystretch}{1.25}
\newcommand{\thead}[1]{\textbf{\sffamily\color{white}#1}}
\newcommand{\theadrow}{\rowcolor{mteal}}
\RequirePackage{colortbl}
\captionsetup{font={small,sf},labelfont={bf,color=mteal}}

%% ---- title page --------------------------------------------------------------
\newcommand{\memoriatitlepage}[3]{% #1 title (Hebrew), #2 subtitle, #3 date
  \begin{titlepage}
  \thispagestyle{empty}
  \begin{tikzpicture}[remember picture,overlay]
    \fill[mpaper] (current page.south west) rectangle (current page.north east);
    \fill[mteal] ([yshift=-11cm]current page.north west) rectangle (current page.north east);
    \fill[mamber] ([yshift=-11.25cm]current page.north west) rectangle ([yshift=-11cm]current page.north east);
    % abstract "photo frames" drawn in TikZ
    \foreach \x/\y/\a/\c in {2/-3.2/-8/mpaper,4.6/-4.4/5/mamber,15.5/-3.4/7/mpaper,17.8/-5.6/-5/mamber}{
      \begin{scope}[shift={([xshift=\x cm,yshift=\y cm]current page.north west)},rotate=\a]
        \filldraw[fill=\c,draw=white,line width=2pt,opacity=0.9] (-0.9,-0.7) rectangle (0.9,0.7);
        \filldraw[fill=mtealdark!60,draw=none] (-0.7,-0.5) rectangle (0.7,0.5);
      \end{scope}}
  \end{tikzpicture}
  \vspace*{2.6cm}
  \begin{center}
    {\sffamily\bfseries\fontsize{40}{46}\selectfont\color{white} #1\par}
    \vspace{0.7cm}
    {\sffamily\Large\color{mpaper}\linespread{1.15}\selectfont #2\par}
  \end{center}
  \vfill
  \begin{center}
    {\sffamily\large\color{mtealdark} #3\par}
    \vspace{0.4cm}
    {\sffamily\small\color{mgrey}\en{Group \memoriagroup\ \textbullet\ LuaLaTeX\ \textbullet\ class memoria v\memoriaversion}\par}
  \end{center}
  \vspace*{1.2cm}
  \end{titlepage}}

\endinput
