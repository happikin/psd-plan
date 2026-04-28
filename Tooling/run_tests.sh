#!/usr/bin/env bash
set -euo pipefail

# Usage examples:
#   bash Tooling/run_tests.sh
#   bash Tooling/run_tests.sh --suite all
#   bash Tooling/run_tests.sh --suite api
#   bash Tooling/run_tests.sh --suite dataset
#   bash Tooling/run_tests.sh --suite services
#   bash Tooling/run_tests.sh --suite repository
#   bash Tooling/run_tests.sh --file tests/test_api_contract.py
#   bash Tooling/run_tests.sh --k timeline
#   bash Tooling/run_tests.sh --suite api --k pagination

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="$ROOT_DIR/.venv"
SUITE="all"
FILE=""
K_EXPR=""
DB_ISOLATION="1"
TMP_DB_FILE=""
PYTEST_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --suite)
      SUITE="${2:-all}"
      shift 2
      ;;
    --file)
      FILE="${2:-}"
      shift 2
      ;;
    --k)
      K_EXPR="${2:-}"
      shift 2
      ;;
    --no-db-isolation)
      DB_ISOLATION="0"
      shift
      ;;
    --)
      shift
      PYTEST_ARGS+=("$@")
      break
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

cd "$ROOT_DIR"

if [[ ! -d "$VENV_DIR" ]]; then
  echo "Virtual environment not found at $VENV_DIR"
  echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -e '.[dev]'"
  exit 1
fi

# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Keep tests deterministic by default: avoid leaking data from persistent runtime DB.
if [[ "$DB_ISOLATION" == "1" ]]; then
  export DB_MODE="${DB_MODE:-sqlite}"
  if [[ -z "${DATABASE_URL:-}" ]]; then
    TMP_DB_FILE="$(mktemp /tmp/corehub_tests_${USER}_XXXXXX.db)"
    export DATABASE_URL="sqlite:///$TMP_DB_FILE"
    trap '[[ -n "$TMP_DB_FILE" && -f "$TMP_DB_FILE" ]] && rm -f "$TMP_DB_FILE"' EXIT
  fi
fi

TARGETS=()
if [[ -n "$FILE" ]]; then
  TARGETS+=("$FILE")
else
  case "$SUITE" in
    all)
      TARGETS+=("tests")
      ;;
    api)
      TARGETS+=("tests/test_api_contract.py")
      ;;
    dataset)
      TARGETS+=("tests/test_dataset_service.py")
      ;;
    services)
      TARGETS+=("tests/test_services.py")
      ;;
    repository)
      TARGETS+=("tests/test_repository_config.py")
      ;;
    *)
      echo "Unsupported suite: $SUITE"
      echo "Supported: all, api, dataset, services, repository"
      exit 1
      ;;
  esac
fi

CMD=(pytest -q)
if [[ -n "$K_EXPR" ]]; then
  CMD+=("-k" "$K_EXPR")
fi
CMD+=("${TARGETS[@]}")
if [[ ${#PYTEST_ARGS[@]} -gt 0 ]]; then
  CMD+=("${PYTEST_ARGS[@]}")
fi

echo "Running: ${CMD[*]}"
"${CMD[@]}"
