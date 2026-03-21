#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT_DIR="/tmp/htmlcov"

python -m pytest "$SCRIPT_DIR/tests" \
    --cov="$SCRIPT_DIR/src/longevity" \
    --cov-report=html:"$REPORT_DIR" \
    --cov-report=term-missing \
    "$@"

xdg-open "$REPORT_DIR/index.html" >/dev/null 2>&1 &
