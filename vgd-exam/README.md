# Verification-Guided Development: Capstone Exam

This exam has four parts. Each part gives you a small broken program and a
mechanical check: a fuzzer, a differential test, or a verifier. In the first two
parts you use the check to *find* the mistake and record what it reveals — you
are not asked to hand in a corrected program. In the last two you prove a
property and then use the proven model to drive a fix. You record every answer
with `exam.py`.

The parts cover four related techniques:

| Technique | Checks | Main limitation |
|---|---|---|
| (Example tests) | selected inputs | only the cases you wrote down |
| Fuzzing | many generated inputs | usually only detects crashes or failed assertions |
| Differential testing | disagreement between implementations | needs a useful reference |
| Formal verification | a stated property for all inputs | requires a precise specification and proof work |

The examples focus on the kinds of edge cases that often matter in secure
software: malformed input, integer overflow, and boundary conditions. The final
part combines the last three techniques: a verified Dafny implementation is
translated to Java and used as an oracle in a fuzz test against a hand-written
Java implementation. This is the verification-guided development pattern used in
systems such as Cedar: prove a small model, then test production code against
that model on generated inputs.

**Solving this with AI.** This exam can be solved manually or with an AI coding
agent; optional prompt suggestions are included. Either way, the guardrails
increase trust in the fix. 
The future of software engineering may well be this kind of
[AI and verification workflow](https://cacm.acm.org/opinion/artificial-intelligence-for-software-engineering-from-probable-to-provable).
But if you use AI, make sure it changes the implementation and
does not weaken the specification, tests, or oracle.

## Grading Model

There are four questions, one per part. Parts A and B record only the finding
the check exposes — an exception class name, an overflow witness. Part C records
the verifier's verdict. Part D records your fixed search compared against a
verified oracle.

`exam.py` writes hashes to `answers.json`; the average overflow question also
stores the raw witness so the grader can validate it. The hashes are bound to
your personal exam token from Moodle, and the Part D test inputs are also derived
from that token. Copying another `answers.json` will not work.

## Setup

You need a JDK, Dafny 4.x, and Python 3. Gradle comes from the bundled wrapper
(`./gradlew`), so you do not need to install it separately.

### Option 1: container

Use Docker or Podman from this directory:

```sh
docker build -t vgd-exam .          # or: podman build -t vgd-exam .
docker run --rm -it -v "$PWD":/exam vgd-exam
```

The volume mount means edits and `answers.json` stay in this directory.

### Option 2: native install

On macOS:

```sh
brew install openjdk dafny python
```

On Debian/Ubuntu, install a JDK and Python with your package manager, and
install Dafny from https://github.com/dafny-lang/dafny/releases.

### Exam token

Save your Moodle exam token as a single line in `student_id.txt`, then check
your progress:

```sh
python3 exam.py status
```

The fuzzing targets print a short `PASS` or `FAIL` summary. The full Gradle and
Jazzer output is written under `.work/fuzz/`.

## Part A: Fuzzing

`src/main/java/calc/Calculator.java` evaluates integer arithmetic expressions:

```java
eval("(1+2)*3") == 9
```

Expression parsers are typical security-sensitive input handlers: they accept
attacker-controlled strings and must behave predictably on malformed input.
The parser already rejects malformed syntax with `CalcException`, but there
other things that can go wrong, so let's see if a fuzzer can find them.

Run:

```sh
make fuzz-calc
```

The fuzzer generates calculator inputs and treats any exception other than
`CalcException` as a finding. Notably, the test in
[`src/test/java/calc/CalculatorFuzzTest.java`](src/test/java/calc/CalculatorFuzzTest.java)
gives the fuzzer no grammar for expressions; it discovers the structure on its
own by mutating inputs to increase coverage.

It will usually find one issue quickly. Note the exception class, then guard
that case; that is, add a `catch` for the first exception and throw `CalcException` instead. Then, run the fuzzer again to find the next exception.
Record both exception names as Q1:

```sh
python3 exam.py q1 FirstException SecondException
```

Use the actual exception class names printed by the fuzzer. You may pass either
simple names or fully qualified names; `exam.py` records the simple class names.


## Part B: Differential Testing

`src/main/java/average/Average.java` contains two implementations of integer
average:

```java
static int average1(int a, int b) {
    return (int) Math.floorDiv((long) a + b, 2L);
}

static int average2(int a, int b) {
    return (a + b) / 2;
}
```

`average1` is the reference: it widens to `long`, so the sum cannot overflow.
`average2` is the common 32-bit attempt, but it is wrong when the non-negative
sum overflows.

Integer overflow is security-relevant when the value is later used as an index,
length, allocation size, or bounds check. Many divide-and-conquer algorithms use
integer averages to split a range in half; this caused a
[famous bug in binary search and merge sort](https://research.google/blog/extra-extra-read-all-about-it-nearly-all-binary-searches-and-mergesorts-are-broken/).
We want to replace it with an efficient non-overflowing version.

Run:

```sh
make fuzz-average
```

The fuzzer supplies pairs of integers. The test treats negative inputs as
outside the precondition, and asserts that the two methods agree on the
remaining non-negative pairs. A disagreement proves at least one implementation
is wrong. Here `average1` is the trusted reference.

Required behavior:

> Precondition: `a >= 0 && b >= 0`.
>
> Both methods return `floor((a + b) / 2)` over mathematical integers.

When `make fuzz-average` reports a finding, record the overflow witness:

```sh
python3 exam.py q2
```

`exam.py q2` reads `.work/fuzz/average.finding` or `.work/fuzz/average.log` and
only records a valid non-negative pair where the naive Java `int` sum overflows.
That witness is the graded answer for Part B.

If you want to confirm you have pinned down the bug, replace `average2` with the
standard non-overflowing `(a & b) + ((a ^ b) >> 1)`, leave `average1` alone, and
rerun `make fuzz-average`: it should now go the full duration with no findings.
This is optional and not recorded.


## Part C: Verification

One way to make sure we can trust the reference implementation is to prove it correct.
`dafny/BinarySearch.dfy` contains a lower-bound binary search with a full Dafny
contract. The method must return the first index containing `key`, or `-1` if
the key is absent.

The precondition says the sequence is sorted. The postconditions say:

```dafny
ensures 0 <= index ==>
          index < |a| && a[index] == key
          && forall k :: 0 <= k < index ==> a[k] < key
ensures index < 0 ==> key !in a
```

Run:

```sh
make verify
```

The code is functionally complete, but the loop is missing two invariants. The
loop maintains a search window `[lo, hi)`. To prove the postconditions, Dafny
needs the facts about the elements outside that window:

1. every index below `lo` contains a value less than `key`;
2. every index from `hi` onward contains a value at least `key`.

Add those invariants at the `// TODO` in `BinarySearch.dfy`. Do not edit
`BinarySearch.verify.dfy`, and do not use `assume`.

When verification succeeds, record Q3:

```sh
python3 exam.py q3
```

The expected clean result is `4 verified, 0 errors`.

Part D reuses this binary search as a trusted oracle. Because the method body is
already complete, that oracle is generated regardless of whether your proof goes
through, so even if you get stuck on the invariants here, you can still attempt
Part D.

## Part D: Verification-Guided Development

Part C proves a simple Dafny search implementation. Now we will use that verified
implementation as an oracle for a fuzz test against Java code.
This pattern is useful when the production implementation is too complicated or
costly to verify directly: a simpler verified model can still define the intended
behavior, and fuzzing can search for inputs where the production code disagrees
with that model.

The oracle is trusted under these assumptions:

1. Dafny's verifier and solver are sound.
2. `dafny translate java` preserves the behavior of the verified Dafny method.
3. `src/main/java/search/OracleAdapter.java` correctly converts Java `int[]`
   inputs to the oracle representation and only calls the oracle on sorted
   arrays.

`src/main/java/search/StudentSearch.java` is a standard binary search. It
returns immediately when it finds `key`. That is correct if keys are unique, but
the specification requires the first occurrence. On repeated values, returning
the first match encountered by binary search may return a later index.

Run:

```sh
make fuzz-search
```

This target first runs `make oracle`, which translates `BinarySearch.dfy` to
`src/main/java/Oracle/__default.java`. Translation uses the method body, which is
already complete, so it works even if you have not finished the Part C proof. 
We trust the oracle because I know this model *can* be proved correct, 
but in real workflow, the build should fail if the proof is missing.

The fuzz test generates sorted arrays with frequent duplicates, calls both
`StudentSearch.find` and the verified oracle, and compares their returned
indices.

Fix `StudentSearch.find` so it returns the first index of `key`, or `-1` if the
key is absent. The usual fix is to remember a matching index and continue
searching the left half (`hi = mid - 1`) instead of returning immediately.

When a full fuzz run reports no findings, record Q4:

```sh
python3 exam.py q4
```

## Summary

The parts build on each other:

| Part | Technique | What it demonstrates |
|---|---|---|
| A | Fuzzing | generated inputs can expose unhandled edge cases |
| B | Differential testing | comparing implementations can detect wrong results |
| C | Verification | a contract can be proved for all inputs |
| D | VGD | a verified model can serve as an oracle for fuzzing another implementation |

## Submitting

Check status:

```sh
python3 exam.py status
```

When all four questions show a hash, upload `answers.json` to Moodle. Do not
upload `student_id.txt`.
