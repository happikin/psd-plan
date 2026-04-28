#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash Tooling/run_backend.sh
#   bash Tooling/run_backend.sh --skip-tests
#   bash Tooling/run_backend.sh --no-install
#   bash Tooling/run_backend.sh --port 9000
#   bash Tooling/run_backend.sh --db postgres --database-url 'postgresql+psycopg://user:pass@localhost:5432/corehub'

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
PORT="8000"
RUN_TESTS="1"
INSTALL_DEPS="1"
DB_MODE="${DB_MODE:-sqlite}"
DATABASE_URL_OVERRIDE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-tests)
      RUN_TESTS="0"
      shift
      ;;
    --no-install)
      INSTALL_DEPS="0"
      shift
      ;;
    --port)
      PORT="${2:-8000}"
      shift 2
      ;;
    --db)
      DB_MODE="${2:-sqlite}"
      shift 2
      ;;
    --database-url)
      DATABASE_URL_OVERRIDE="${2:-}"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

cd "$ROOT_DIR"

if [[ -n "$DATABASE_URL_OVERRIDE" ]]; then
  export DATABASE_URL="$DATABASE_URL_OVERRIDE"
fi
export DB_MODE

if [[ "$DB_MODE" == "postgres" && -z "${DATABASE_URL:-}" ]]; then
  echo "Error: DB_MODE=postgres requires DATABASE_URL (or --database-url)."
  exit 1
fi

echo "[1/5] Ensuring virtual environment exists..."
if [[ ! -d "$VENV_DIR" ]]; then
  python3 -m venv "$VENV_DIR"
fi

echo "[2/5] Activating virtual environment..."
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

echo "[3/5] Installing dependencies..."
if [[ "$INSTALL_DEPS" == "1" ]]; then
  python -m pip install --upgrade pip setuptools wheel
  python -m pip install -e ".[dev]"
else
  echo "Skipped (--no-install)."
fi

echo "[4/5] Running tests..."
if [[ "$RUN_TESTS" == "1" ]]; then
  pytest -q
else
  echo "Skipped (--skip-tests)."
fi

echo "[5/5] Starting backend on port $PORT (DB_MODE=$DB_MODE)..."
exec uvicorn app:app --reload --app-dir src/backend --port "$PORT"
