#!/usr/bin/env bash
set -u

usage() {
  cat <<'USAGE'
Usage: ./verify.sh [exercise-number | exerciseN.verify.dfy ...]

Examples:
  ./verify.sh        # verify all exercises
  ./verify.sh 3      # verify exercise3.verify.dfy
  ./verify.sh 2 5 9  # verify selected exercises

Set DAFNY=/path/to/dafny to use a non-default Dafny executable.
USAGE
}

dafny="${DAFNY:-dafny}"
status=0
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd -- "$script_dir"

if [[ $# -eq 0 ]]; then
  files=(exercise*.verify.dfy)
else
  files=()
  for arg in "$@"; do
    case "$arg" in
      -h|--help)
        usage
        exit 0
        ;;
      [0-9]|[1-9][0-9])
        files+=("exercise${arg}.verify.dfy")
        ;;
      exercise*.verify.dfy)
        files+=("$arg")
        ;;
      *)
        echo "Unknown argument: $arg" >&2
        usage >&2
        exit 2
        ;;
    esac
  done
fi

if [[ "${files[0]:-}" == "exercise*.verify.dfy" ]]; then
  echo "No verifier files found in this directory." >&2
  exit 1
fi

for file in "${files[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "Missing verifier file: $file" >&2
    status=1
    continue
  fi

  echo "==> $file"
  "$dafny" verify --verify-included-files --allow-deprecation "$file" || status=1
done

exit "$status"
