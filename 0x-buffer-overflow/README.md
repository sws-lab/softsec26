# Buffer overflows

The provided file `naive.c` contains simple (and problematic) implementation of
a program granting access based on password which it prompts from the user.

**NOTE:** in parallel to working through the next few sections, run `podman
build -t bufover -f Dockerfile .` (you may replace `podman` with `docker`) to
build the environment for fuzzing section.

On Linux (you may use provided `Dockerfile` environment if you have it ready,
but this is not required), you can compile and run the program as follows:
```bash
cc -O2 naive.c -o naive -g # Tested with gcc 14.2.0 and clang 22
echo -n qwerty1 > password.txt # Max 7 characters
./naive
```
You may run the program and make sure that (naively) alternative passwords do
not grant the access.

However, the program is problematic in many respects, and in particular it
contains infamous buffer overflow vulnerability. To discover the vulnerability,
carefully inspect the source code. Consider which memory writes are performed by
the program, to which variables, whether the memory writes always stay in bounds
of their respective variables, and how these variables could be placed in memory
relative to each other. Ultimately, the goal would be finding the memory write
that inadvertently permits writes into the wrong variable under certain
conditions. Equipped with this, consider which inputs provided by the user may
trick the program to write into the wrong variable, and how this could be
exploited to gain access without knowing the contents of `password.txt` or
modifying program text.

## Automatic discovery

The modern compilers provide certain assistance in finding such class of bugs.
You may compile the program as follows:
```bash
cc -O2 naive.c -o sanitized -g -fsanitize=address # Tested with gcc 14.2.0 and clang 22
./sanitized
```
You may run the sanitized version and attempt to gain access, both using
legitimate password and the technique you discovered previously. In the latter
case, observe error trace printed by the program. Read the trace and correlate
with your understanding of the issue gained previously.

Can you modify the program to trick the sanitizer, bypassing these checks to
still admit problematic inputs? See below.

## Sneaky program

The sneaky version demonstrates limitations of sanitizer tooling. You may compile it as follows:
```bash
cc -O2 sneaky.c -o sneaky -fsanitize=address -g # Tested with gcc 14.2.0 and clang 22
./sneaky
```
Try to enter the same problematic input. Is the sanitizer triggered, or can you
once again gain unauthorized access? Read through the `sneaky.c` and consider
the pattern used there. This shows the limitations of runtime analysis tools for
C, which rely on knowing certain behaviors of the program (memory allocation
mechanism) in advance, so implementing custom memory allocator may still confuse
the sanitizer.

## Fuzzing

This kind of vulnerabilities can be identified in automatic manner by using
fuzzing. Fuzzers attempt many possible inputs, randomizing and mutating them
while observing program behaviors. Therefore, there is good probability to
arrive at the problematic input. Combined with sanitizers that abruptly fail
when the problem occurs, fuzzer can reasonably identify faulty programs.

To test fuzzing, you should use the provided `Dockerfile`
```bash
podman build -t bufover -f Dockerfile . # you may replace podman with docker
podman run --rm -it bufover
```
In the container, run
```bash
echo -n qwerty1 > password.txt # Max 7 characters
mkdir in
cp password.txt in

afl-clang-lto -O2 naive.c -o naive
afl-fuzz -i in -o out-naive -- ./naive
```

Inspect the user interface of
[AFL++](https://github.com/AFLplusplus/AFLplusplus) fuzzer. Once it finds some
crashes -- this should happen very quickly -- you may terminate it with ctrl+c.

Problematic inputs found by the fuzzer are located in
`out-naive/default/crashes` directory. You may run the program with these inputs:
```bash
./naive < out-naive/default/crashes/id\:000000\,sig\:06\,src\:000000\,time\:147\,execs\:200\,op\:havoc\,rep\:2 # File name will be different. Adjust!
```
You may also inspect particular inputs, however not all of them will be in printable form:
```bash
xxd out-naive/default/crashes/id\:000000\,sig\:06\,src\:000000\,time\:147\,execs\:200\,op\:havoc\,rep\:2
```

## Symbolic analysis

Finally, you may try using symbolic analysis to find the issue. For this
purpose, `symbolic.c` variant is prepared -- it is equivalent to the original
naive program except for password reading function. Inspect the source code to
make sure you understand the changes.

You should use the same container environment as in the fuzzing case:
```bash
symbiotic  --prp=memsafety --search-include-paths --witness=witness.yml --exit-on-error  symbolic.c
```
The analyzer should finish relatively quickly, reporting an error. It encodes
possible path to the fault in a form of a witness `witness.yml`. Read the
`witness.yml` file -- it contains a sequence of waypoints that show certain
program execution states that lead to the problem. Look at waypoint locations,
correlate these with the source code. What does the symbolic analyzer
communicate?