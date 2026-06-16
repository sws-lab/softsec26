#!/usr/bin/env python3
"""VGD home exam helper.

Records answers into answers.json. Every answer is
sha256(token | question | observed_value), so the file is bound to your
personal exam token: copying someone else's answers.json cannot work.

Usage:
    python3 exam.py status
    python3 exam.py q1     # calculator: fix until `make fuzz-calc` is clean
    python3 exam.py q2     # averages: fix until they meet the floor spec
    python3 exam.py q3     # dafny: add invariants until `make verify` passes
    python3 exam.py q4     # search: fix until `make fuzz-search` is clean

Each question records the result of running the tool on YOUR fixed code; it
only grades as correct once the guardrail (the fuzzer or the verifier) is
satisfied. There is nothing to record by hand.

Requires: a recent JDK (javac/java), Dafny 4.x on PATH (q3), Python 3.
"""

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

EXAM_DIR = Path(__file__).resolve().parent
WORK_DIR = EXAM_DIR / ".work"
ANSWERS_FILE = EXAM_DIR / "answers.json"
ID_FILE = EXAM_DIR / "student_id.txt"
EXAM_NAME = "vgd-exam"

QUESTIONS = ["q1", "q2", "q3", "q4"]

SRC = EXAM_DIR / "src" / "main" / "java"
DRIVERS = EXAM_DIR / "drivers"
DAFNY_RUNTIME = EXAM_DIR / "lib" / "DafnyRuntime.jar"


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def student_id():
    if not ID_FILE.exists():
        fail(
            "student_id.txt not found.\n"
            "Copy your personal exam token from Moodle and save it as\n"
            f"  {ID_FILE}\n"
            "(a single line, nothing else)."
        )
    sid = ID_FILE.read_text(encoding="utf-8").strip()
    if not sid:
        fail("student_id.txt is empty.")
    return sid


def id_fingerprint(sid):
    return hashlib.sha256(sid.encode("utf-8")).hexdigest()[:12]


def answer_hash(sid, qid, canonical):
    payload = sid + "|" + qid + "|" + canonical
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def load_answers(sid):
    fp = id_fingerprint(sid)
    if ANSWERS_FILE.exists():
        data = json.loads(ANSWERS_FILE.read_text(encoding="utf-8"))
        if data.get("id_fingerprint") == fp:
            return data
        print("note: existing answers.json belongs to a different exam token;"
              " starting fresh.")
    return {"exam": EXAM_NAME, "id_fingerprint": fp, "answers": {}}


def record(sid, qid, canonical):
    data = load_answers(sid)
    data["answers"][qid] = answer_hash(sid, qid, canonical)
    ANSWERS_FILE.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"recorded {qid} -> {data['answers'][qid]}")


def run(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def need_tool(name, probe):
    try:
        subprocess.run(probe, capture_output=True)
    except FileNotFoundError:
        fail(f"`{name}` not found on PATH. See the Setup section of README.md.")


def compile_java(out_name, sources, classpath=None):
    need_tool("javac", ["javac", "-version"])
    out = WORK_DIR / out_name
    out.mkdir(parents=True, exist_ok=True)
    cmd = ["javac", "-d", str(out)]
    if classpath:
        cmd += ["-cp", classpath]
    cmd += [str(s) for s in sources]
    r = run(cmd)
    if r.returncode != 0:
        print(r.stderr, file=sys.stderr)
        fail("compilation failed (see messages above).")
    return out


def run_driver(classes, main_class, sid, classpath_extra=None):
    cp = str(classes)
    if classpath_extra:
        cp += os.pathsep + classpath_extra
    r = run(["java", "-cp", cp, main_class, sid])
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)
    if r.returncode != 0:
        fail("driver run failed.")
    return "\n".join(line.rstrip() for line in r.stdout.strip().splitlines())


# ---------------------------------------------------------------- questions

def q1(sid, args):
    # Part A -- the calculator, fixed until `make fuzz-calc` is clean.
    classes = compile_java("q1", sorted((SRC / "calc").glob("*.java")) + [
        DRIVERS / "Derive.java",
        DRIVERS / "CalcFingerprint.java",
    ])
    vector = run_driver(classes, "exam.CalcFingerprint", sid)
    if "EXC:" in vector:
        print("warning: your calculator still lets an exception other than"
              " CalcException escape, so this will not grade as correct. Keep"
              " fixing until a full `make fuzz-calc` run finds nothing, then"
              " record again.")
    record(sid, "q1", vector)


def q2(sid, args):
    # Part B -- both averages, fixed until they meet the floor spec.
    classes = compile_java("q2", sorted((SRC / "average").glob("*.java")) + [
        DRIVERS / "Derive.java",
        DRIVERS / "AverageFingerprint.java",
    ])
    # The driver prints "i:avg1=avg2=floorReference" per case.
    raw = run_driver(classes, "exam.AverageFingerprint", sid)
    canon = []
    disagree = 0
    spec_violation = 0
    for ln in raw.splitlines():
        idx, rest = ln.split(":", 1)
        a1, a2, ref = rest.split("=")
        canon.append(f"{idx}:{a1}={a2}")
        if a1 != a2:
            disagree += 1
        elif a1 != ref:
            spec_violation += 1
    total = len(canon)
    if disagree:
        print(f"warning: average2 still DISAGREES with the average1 reference on"
              f" {disagree} of {total} cases. Make the efficient average2 match"
              f" the reference before recording.")
    if spec_violation:
        print(f"warning: average1 and average2 agree with each other but do NOT"
              f" match the floor specification on {spec_violation} of {total}"
              f" cases (floor rounds toward negative infinity; e.g. the average"
              f" of -7 and 0 is -4, not -3). You appear to have changed the"
              f" reference -- leave average1 as 64-bit floorDiv and only fix"
              f" average2.")
    record(sid, "q2", "\n".join(canon))


def q3(sid, args):
    # Part C -- the Dafny proof, recorded once `make verify` is clean.
    need_tool("dafny", ["dafny", "--version"])
    r = run(["dafny", "verify", "--verify-included-files",
             "BinarySearch.verify.dfy"], cwd=EXAM_DIR / "dafny")
    out = r.stdout + r.stderr
    m = re.search(r"finished with (\d+) verified, (\d+) error", out)
    if not m:
        print(out, file=sys.stderr)
        fail("could not parse Dafny output.")
    verified, errors = int(m.group(1)), int(m.group(2))
    src = (EXAM_DIR / "dafny" / "BinarySearch.dfy").read_text(encoding="utf-8")
    dirty = any(tok in src for tok in ("assume", ":axiom", "assert false"))
    audit = "dirty" if dirty else "clean"
    print(f"dafny: {verified} verified, {errors} errors, audit {audit}")
    if errors:
        print("warning: the proof does not go through yet; add the missing"
              " invariants and rerun.")
    record(sid, "q3", f"bs-verify:{verified}:{errors}:{audit}")


def q4(sid, args):
    # Part D -- the student search, fixed until it agrees with the oracle.
    if not DAFNY_RUNTIME.exists():
        fail(f"missing {DAFNY_RUNTIME}")
    oracle_java = SRC / "Oracle" / "__default.java"
    if not oracle_java.exists():
        fail(
            "generated oracle not found.\n"
            "Run `make fuzz-search` after completing Q3; it first runs"
            " `make oracle`, which verifies dafny/BinarySearch.dfy and"
            " generates src/main/java/Oracle/__default.java."
        )
    classes = compile_java(
        "q4",
        sorted((SRC / "Oracle").glob("*.java"))
        + sorted((SRC / "search").glob("*.java"))
        + [DRIVERS / "Derive.java", DRIVERS / "SearchFingerprint.java"],
        classpath=str(DAFNY_RUNTIME),
    )
    vector = run_driver(classes, "exam.SearchFingerprint", sid,
                        classpath_extra=str(DAFNY_RUNTIME))
    record(sid, "q4", vector)


def status(sid, args):
    data = load_answers(sid)
    print(f"exam: {data['exam']}   token fingerprint: {data['id_fingerprint']}")
    for q in QUESTIONS:
        mark = data["answers"].get(q, "-")
        print(f"  {q}: {mark}")
    missing = [q for q in QUESTIONS if q not in data["answers"]]
    if missing:
        print("missing: " + ", ".join(missing))
    else:
        print("all questions answered; upload answers.json to Moodle.")


COMMANDS = {"status": status, "q1": q1, "q2": q2, "q3": q3, "q4": q4}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    sid = student_id()
    COMMANDS[sys.argv[1]](sid, sys.argv[2:])


if __name__ == "__main__":
    main()
