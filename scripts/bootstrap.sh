#!/usr/bin/env bash
# Create the local Python environment for /go (once), then keep it up to date. Safe to rerun.
set -euo pipefail
cd "$(dirname "$0")/.."
[ -x .venv/bin/python ] || python3 -m venv .venv
.venv/bin/python -m pip install -q --disable-pip-version-check -r requirements.txt
.venv/bin/python -c "import sys; print('python ready:', sys.version.split()[0], '-> .venv/bin/python')"
