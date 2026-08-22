# Compiling `cycle-survival.tex`

**Status: compiled successfully.** `pdflatex` was not available when
this package was first built; a minimal TeX Live install
(`texlive-latex-base texlive-latex-recommended texlive-fonts-recommended
texlive-bibtex-extra`) was added, and `cycle-survival.pdf` was produced
with the standard `pdflatex` -> `bibtex` -> `pdflatex` -> `pdflatex`
sequence below: zero errors, zero undefined references, zero undefined
citations (all 12 bibliography entries resolved). The only warnings are
harmless `hyperref` "Token not allowed in a PDF string" notices from
math mode inside section-heading bookmarks -- cosmetic, does not affect
the visible typeset output -- plus one pre-existing overfull `\hbox` in
the size-biasing remark of \S2 (a few points too wide, present since the
original build), likewise cosmetic. `cycle-survival.pdf` in this
directory is that build's output (currently 9 pages, after the update
adding the $K=3,4,5$ bridge results); auxiliary files (`.aux`/`.log`/
`.bbl`/etc.) were removed after the build and are not tracked.

## To compile

```bash
cd paper/
pdflatex cycle-survival.tex
bibtex cycle-survival
pdflatex cycle-survival.tex
pdflatex cycle-survival.tex   # second pass to resolve references
```

or, with [Tectonic](https://tectonic-typesetting.github.io/) (no
separate `bibtex` step needed, and no manual package install required):

```bash
cd paper/
tectonic cycle-survival.tex
```

Either produces `cycle-survival.pdf`. Three `pdflatex` passes (plus the
`bibtex` run in between) are needed because the document uses
cross-references (`\ref`, `\eqref`) and a bibliography; a single pass
will show "undefined reference" / missing citation warnings that resolve
on the second and third pass.

## If a package is reported missing

All five packages used are part of any standard TeX Live installation
(`texlive-latex-base` + `texlive-latex-recommended` is sufficient; no
`texlive-full` needed). On a minimal/custom install:

```bash
tlmgr install amsmath amsfonts geometry hyperref
```

(`amsthm` ships with `amsmath`/base LaTeX in essentially all
distributions.)

## Verifying the result independently

The paper's numeric claims are not just typeset text -- every number in
it is reproduced by the scripts in `../simulations/` (see the package
`README.md`, "Reproducing every figure and number"). If the PDF and the
script output ever disagree, trust the scripts and file it as a bug in
the `.tex` source, not the other way around.
