#!/bin/bash
# Installs what's needed to render and preview the site in Claude Code cloud sessions:
# Quarto (from PyPI, since GitHub release downloads are blocked) and WeasyPrint for the CV PDF.
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

quarto --version
