#!/usr/bin/env bash
# Install the locked dependencies, with the dev group, for CI (labinacan-ci.yml).
# A project whose dependencies need a CPU-only index, such as torch's, changes this file.
set -euo pipefail

VENV_DIR="${VENV_DIR:-.venv}"
UV_PROJECT_ENVIRONMENT="$VENV_DIR" uv sync --quiet --frozen --group dev
"$VENV_DIR/bin/python" -c "import labinacan; print(f'labinacan {labinacan.__version__}')"
