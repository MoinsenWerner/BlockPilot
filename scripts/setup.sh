#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${PROJECT_ROOT}/.venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required" >&2
  exit 1
fi

python3 -m venv "${VENV_PATH}"
# shellcheck disable=SC1090
source "${VENV_PATH}/bin/activate"

pip install --upgrade pip
pip install -r "${PROJECT_ROOT}/backend/requirements.txt"

mkdir -p "${PROJECT_ROOT}/backend/data"

cat <<CONFIG > "${PROJECT_ROOT}/backend/.env"
DB_URL=sqlite:///./data/app.db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=$(openssl rand -hex 32)
PANEL_PORT=8444
CONFIG

echo "Environment prepared. Activate with: source ${VENV_PATH}/bin/activate"
