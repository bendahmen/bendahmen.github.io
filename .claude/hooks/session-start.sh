#!/bin/bash
# Installs what's needed to render and preview the site in Claude Code cloud sessions:
# Quarto (from PyPI, since GitHub release downloads are blocked), WeasyPrint for the
# CV PDF, and R with htmltools/rmarkdown/knitr for research/internships/index.qmd.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

if ! command -v quarto >/dev/null 2>&1; then
  pip install --quiet --root-user-action=ignore quarto-cli
fi

if ! command -v weasyprint >/dev/null 2>&1; then
  pip install --quiet --root-user-action=ignore weasyprint
fi

if ! Rscript -e 'library(htmltools); library(rmarkdown); library(knitr)' >/dev/null 2>&1; then
  apt-get update -qq
  DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
    r-base-core r-cran-htmltools r-cran-rmarkdown r-cran-knitr
fi

quarto --version
