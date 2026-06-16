#!/usr/bin/env bash
set -u

if [ "$#" -ne 2 ]; then
  echo "usage: scripts/fuzz.sh <name> <JUnitTestClass>" >&2
  exit 2
fi

name="$1"
test_class="$2"
log_dir=".work/fuzz"
log="$log_dir/${name}.log"

mkdir -p "$log_dir"
rm -f "$log"

echo "FUZZ $name: running for up to 30 seconds"
echo "  full log: $log"

./gradlew -Pfuzz test --tests "*${test_class}" --console=plain >"$log" 2>&1
rc="$?"

if [ "$rc" -eq 0 ]; then
  summary="$(awk '/^Done [0-9]+ runs in [0-9]+ second/ { line = $0 } END { print line }' "$log")"
  if [ -n "$summary" ]; then
    echo "PASS $name: no findings ($summary)"
  else
    echo "PASS $name: no findings"
  fi
  exit 0
fi

echo "FAIL $name: finding or build error"
echo

# Gradle indents test output and reports a finding as a bare exception line
# (the "Caused by:" sits on its own line), so we match a whitespace-stripped
# copy of each line and accept the exception with or without that prefix.
awk '
  { t = $0; sub(/^[[:space:]]+/, "", t) }
  t ~ /^>>> FUZZ FINDING/ && !finding {
    print t
    finding = 1
    next
  }
  t ~ /^(Caused by: )?java\.lang\.AssertionError:/ && !assertion {
    sub(/^Caused by: /, "", t)
    print t
    assertion = 1
    next
  }
  t ~ /^(Caused by: )?java\.[A-Za-z.]+:/ && !cause {
    sub(/^Caused by: /, "", t)
    print t
    cause = 1
    next
  }
  END {
    if (!finding && !assertion && !cause) {
      exit 1
    }
  }
' "$log"

if [ "$?" -ne 0 ]; then
  echo "No concise finding was recognized; last log lines:"
  tail -n 25 "$log"
fi

echo
echo "See $log for the full Gradle/Jazzer output and stack trace."
exit "$rc"
