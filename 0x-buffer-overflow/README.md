# Buffer overflows

This tutorial uses a deliberately unsafe password checker to illustrate how a
buffer overflow can be

1. found by manual inspection,
2. detected by runtime tooling,
3. rediscovered by fuzzing, and
4. exposed by symbolic analysis.

The main example is [`naive.c`](./naive.c). The later files
[`sneaky.c`](./sneaky.c) and [`symbolic.c`](./symbolic.c) reuse the same core
idea with small changes to show the strengths and weaknesses of different
analysis techniques.

Run the commands below from the `0x-buffer-overflow` directory.

**Note:** the `Dockerfile` is only needed for the fuzzing and symbolic-analysis
sections. You can start building it in parallel while working through the first
parts:

```bash
podman build -t bufover -f Dockerfile .
```

You may replace `podman` with `docker`.

## Manual discovery

On Linux, you can compile and run the vulnerable program as follows:

```bash
cc -O2 naive.c -o naive -g # Tested with gcc 14.2.0 and clang 22
echo -n qwerty1 > password.txt # Max 7 characters
./naive
```

First, confirm the intended behavior: the correct password grants access and an
incorrect password does not.

Then inspect [`naive.c`](./naive.c) carefully. The key questions are:

- Which function writes user-controlled bytes into memory? Which memory?
- What stops that function from writing more bytes?
- Does it check how large the destination buffer is?
- How string buffers might be stored relative to each other?
- What happens if the program writes input outside of destination buffer bounds?
- Can one exploit this behavior to manipulate the program state?
- Which input might be suitable for such manipulation to grant unauthorized
  access?

Two important caveats:

- This behavior is still undefined behavior in C. Once the overflow happens, the
  language standard makes no guarantees.
- The exercise relies on a memory layout that is common with the tested
  toolchains, but not guaranteed by the C standard.

## Automatic discovery

Modern compilers can instrument programs to catch many memory errors at runtime.
Compile the same program with AddressSanitizer:

```bash
cc -O2 naive.c -o sanitized -g -fsanitize=address # Tested with gcc 14.2.0 and clang 22
./sanitized
```

Try two kinds of input:

- the legitimate password,
- the input that triggered the bug during manual exploration.

When the overflow occurs, AddressSanitizer should abort the program and print a
report. Read that report closely:

- Which memory access failed?
- In which function did the invalid write occur?
- Which variable was overflowed?
- How large was the object, and how far past it did the write go?

This is a useful contrast with the manual analysis: before, you reasoned from
the source to the bug; now the tool points directly at the failing access.

## Sneaky program

[`sneaky.c`](./sneaky.c) demonstrates a limitation of runtime sanitizers. Compile
it as follows:

```bash
cc -O2 sneaky.c -o sneaky -fsanitize=address -g # Tested with gcc 14.2.0 and clang 22
./sneaky
```

Use the same problematic input as before. Does the sanitizer still trigger, or
can you once again gain unauthorized access?

The important change is that string buffers are no longer separate variables.
Instead, the program carves both objects out of one larger static pool through a
custom allocator.

That distinction matters for AddressSanitizer:

- it knows the bounds of the global allocation pool,
- but it does not automatically know the logical sub-allocation boundaries.

So an overwrite from one logical object into the next may stay inside the pool
and therefore avoid detection, even though it still corrupts program state. The
bug has not disappeared. Only the visibility of the bug to the runtime checker
has changed.

This is the broader lesson: runtime instrumentation is powerful, but it is not
the same as a proof of correctness. If a memory-management scheme is invisible
to the tool, some bugs may remain invisible too.

## Fuzzing

Fuzzing searches for bugs automatically by generating many inputs, mutating them,
and observing how the target behaves. When the program crashes, hangs, or hits a
sanitizer failure, the fuzzer keeps the interesting input for later inspection.

For this part, use the provided container environment:

```bash
podman build -t bufover -f Dockerfile .
podman run --rm -it bufover
```

Inside the container, run:

```bash
echo -n qwerty1 > password.txt # Max 7 characters
mkdir -p in
cp password.txt in/

afl-clang-lto -O2 naive.c -o naive
afl-fuzz -i in -o out-naive -- ./naive
```

The `in/` directory is the initial seed corpus. We start with a valid password
well-formed input to mutate, providing starting point to
[AFL++](https://github.com/AFLplusplus/AFLplusplus).

Inspect the AFL++ interface while it runs. On this example, crashes should
appear quickly. Once that happens, terminate the fuzzer with `Ctrl+C`.

Interesting inputs are stored under `out-naive/default/crashes`. A convenient
way to replay one of them is:

```bash
CRASH=$(find out-naive/default/crashes -type f ! -name README.txt | head -n 1)
./naive < "$CRASH"
```

You can inspect the bytes in the crashing input with:

```bash
xxd "$CRASH"
```

Some crash files will not be human-readable, which is normal. The useful point
is that the fuzzer can discover a bad input without understanding the program in
the way a human does.

## Symbolic analysis

Finally, try symbolic analysis. For this part, use [`symbolic.c`](./symbolic.c)
instead of `naive.c`.

The structure of the program is the same, but the input routine is different:
instead of reading concrete bytes with `fgetc`, it asks the verifier for
nondeterministic values. This lets the analyzer reason about many possible inputs
at once.

Use the same container environment as in the fuzzing section and run:

```bash
symbiotic --prp=memsafety --search-include-paths --witness=witness.yml --exit-on-error symbolic.c
```

The analyzer should finish relatively quickly and report a memory-safety error.
It also writes a witness to `witness.yml`.

Read that witness as a compact explanation of one path to failure:

- waypoint locations tell you which source lines matter,
- state information shows how execution reaches the fault,
- the final step corresponds to the out-of-bounds write.

One subtle but important point: the analyzer is proving a memory-safety problem,
not directly "unauthorized access." The witness shows how execution can reach the
unsafe write, and from there you can connect the result back to the exploit
behavior you observed earlier.
