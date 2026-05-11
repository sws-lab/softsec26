# Dafny Exercise Guide

Read "How to Work" and "Dafny Tools You Will Use" before starting,
then use the exercise notes as you work through the files in order.

Useful official references:

- [Getting Started with Dafny](https://dafny.org/latest/OnlineTutorial/guide)
- [Dafny Quick Reference](https://dafny.org/latest/QuickReference)
- [Dafny Reference Manual](https://dafny.org/dafny/DafnyRef/DafnyRef)

## How to Work

The exercises are ordered by increasing proof difficulty. Each new task reuses
ideas from the previous ones and adds one or two new Dafny constructs:

1. `exercise1.dfy`: postconditions for a maximum function.
2. `exercise2.dfy`: a first arithmetic loop invariant.
3. `exercise3.dfy`: a loop invariant tied to a recursive mathematical function.
4. `exercise4.dfy`: another arithmetic invariant, this time for square roots.
5. `exercise5.dfy`: array traversal with quantifiers.
6. `exercise6.dfy`: recursive binary search and termination.
7. `exercise7.dfy`: loop binary search and nullable arrays.
8. `exercise8.dfy`: array mutation, `old`, and slices.
9. `exercise9.dfy`: nested loops, sortedness, and multisets.

Work in the numbered `exerciseN.dfy` files. Some tasks also have a support file,
such as `exercise3.common.dfy`, which defines mathematical functions used in
specifications.

The `exerciseN.verify.dfy` files are local checking harnesses. 
Do not modify them: Moodle has the original version of these files,
so verification will fail if you change them.

You should work in VSCode with the Dafny extension,
which gives you real-time feedback on verification errors.
When you are done, you can check all tasks with:

```sh
./verify.sh
```

Check one task with:

```sh
./verify.sh 3
```

If you need a non-default Dafny executable, set `DAFNY`:

```sh
DAFNY=/path/to/dafny ./verify.sh 3
```

Do not use proof shortcuts such as `assume` to silence Dafny. The grading checks
are independent of the local checking files and audit submissions before
verification.

The basic workflow is:

1. Read the task and identify the intended input/output behavior.
2. Write or complete the contract: `requires` for assumptions, `ensures` for
   guarantees.
3. Implement the code.
4. Add invariants or decreases clauses only where Dafny needs a proof summary.
5. Interpret the errors before adding more annotations.


## Dafny Tools You Will Use

### Types and Expressions

Dafny has mathematical integers by default. `int` can be negative; `nat` is the
subset of integers satisfying `0 <= n`. Several exercises use `nat` when negative
inputs would not make sense.

Boolean formulas use the usual connectives:

```dafny
&&    // and
||    // or
!     // not
==>   // implication
```

In specifications, implication is common because many guarantees are
conditional. The next section shows how it appears in method contracts.

### Contracts

A method contract says what callers must provide and what the method guarantees:

```dafny
method M(x: int) returns (y: int)
  requires 0 <= x
  ensures y >= x
{
  ...
}
```

`requires` is a precondition. Callers must prove it before calling the method.
`ensures` is a postcondition. The method body must prove it before returning.

Several exercises use implication:

```dafny
ensures condition ==> property
```

Read this as "if `condition` holds, then `property` must hold." This is useful
when a method has different outcomes, such as "if the returned index is
non-negative, then it points to the value."

Try to make contracts precise but not implementation-specific. A caller should
be able to rely on the contract without knowing which loop or branch structure
you used. 
NB! In Dafny, *the contract is all*: calling functions do not see it!

### Functions and Predicates

Functions and predicates describe mathematical facts used in specifications.
They do not mutate state.

```dafny
function f(n: nat): nat {
  if n == 0 then 0 else 1 + f(n - 1)
}

predicate sorted(a: array<int>)
  reads a
{
  forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
}
```

The `reads a` clause is needed because the predicate looks at array contents.

Use functions and predicates to name concepts that would be awkward to repeat in
every contract, such as Fibonacci numbers or sortedness.

### Quantifiers

Most array specifications use `forall` or `exists`:

```dafny
forall k :: 0 <= k < a.Length ==> a[k] != value
exists k :: 0 <= k < a.Length && result == a[k]
```

Always guard array indexing with bounds in the quantifier range. Dafny must be
able to prove every `a[k]` access is in bounds.

For `forall`, the expression before `==>` usually acts as the range of values you
care about. For `exists`, use `&&` to combine the range with the property you
want some value to satisfy.

### Loops and Invariants

Dafny does not remember arbitrary facts from previous loop iterations. A loop
invariant is the summary that remains true before the loop starts, after every
iteration, and when the loop exits.

For a loop that counts from `0` to `n`, a typical bound invariant is:

```dafny
invariant 0 <= i <= n
```

Invariants are written between the `while` guard and the loop body:

```dafny
while i < n
  invariant 0 <= i <= n
{
  ...
}
```

You usually need at least two kinds of invariant:

- Bounds invariants, so Dafny can prove indexes and arithmetic are safe.
- Meaning invariants, so Dafny knows what partial result has been computed.

After the loop, Dafny combines the invariant with the fact that the loop guard is
false. For example, from `i < n` being false and `i <= n`, Dafny can conclude
`i == n`.

When debugging a loop proof, check the invariant in three places: before the
first iteration, after one arbitrary iteration, and at loop exit. If it is false
at the beginning, it is not an invariant. If it is true but too weak at the end,
strengthen it with the missing meaning of the loop.

### Termination and `decreases`

Dafny proves total correctness, so it also proves loops and recursion terminate.
It can often guess a termination measure for simple counter loops. For recursive
methods and some search loops, you may need to write one explicitly. A
`decreases` expression must get strictly smaller and stay bounded below.

For a loop or recursive search over a half-open range `[low, high)`, the natural
measure is the range length. For a counter that increases toward `n`, the natural
measure is the distance still left.

### Arrays, Nullability, and Slices

`array<int>` is a non-null array reference. `array?<int>` allows `null`.

Array indexes run from `0` to `a.Length - 1`. The range `[low, high)` includes
`low`, excludes `high`, and is empty when `low == high`.

Array slices such as `a[0..i]` are immutable sequences representing a snapshot of
part of the current array. They are useful in invariants about the prefix that
has not changed.

Arrays are mutable references; sequences and slices are values. That difference
is useful in specifications because a slice can describe a stable view of a part
of the array at a particular moment.

### `old` and Mutating Methods

In a postcondition or loop invariant, `old(e)` refers to the value of `e` at
method entry. This is essential when specifying array updates:

```dafny
ensures a[0] == old(a[a.Length - 1])
```

For methods that modify an array, include a frame:

```dafny
modifies a
```

`old` is not a replacement for saving a value that the implementation needs at
runtime. If an update will overwrite a value you later need, store it in a local
variable before the overwrite.

### Multisets

`multiset(a[..])` forgets order but keeps element counts. It is a compact way to
say a sorting algorithm permutes the original elements without losing or adding
values.

## Exercise Notes

### Exercise 1: Maximum of Two Integers

Goal: implement `Max(a, b)` and specify that it returns the larger input.

The key idea is the postcondition. Describe the result by cases: one case for
`a < b`, and one for `b <= a`. This avoids ambiguity when the two arguments are
equal.

Check that each branch returns a value that satisfies the matching
postcondition. No loop invariant is needed.

### Exercise 2: Sum of the First `n` Natural Numbers

Goal: compute `1 + 2 + ... + n`.

This is the first real loop proof. The postcondition gives the closed form for
the whole computation. The loop invariant should give the same kind of closed
form for the prefix already processed. Choose a counter convention first:
does `i` mean "we have summed through `i`" or "the next number to add is `i`"?
Then make the invariant match that convention.

Arithmetic invariants are easier when the update order mirrors the meaning of
the counter.

### Exercise 3: Fibonacci Loop

Goal: compute `fib(n)` iteratively while using the recursive `fib` function only
in the contract and invariants.

This exercise adds a mathematical specification function. The implementation
should be iterative, but the proof can still refer to the clean recursive
definition of Fibonacci numbers.

Use loop variables that represent neighboring Fibonacci numbers. Because the
update is simultaneous, the right-hand sides are evaluated before either
left-hand side is changed:

```dafny
a, b := b, a + b;
```

Your invariant should connect the loop counter to the mathematical meaning of
the current variables. Include a bound for the counter. If one variable
represents the predecessor of `b`, handle the initial `i == 0` case carefully.

### Exercise 4: Integer Square Root

Goal: return the largest `r` such that `r * r <= n`.

This is another arithmetic loop, but now the loop state has two related
variables. The variable `sqr` is intended to track the next square to test.
Compute a few iterations by hand:

- initially `r == 0` and `sqr == 1`;
- after increasing `r`, the next square can be updated by adding the next odd
  number.

The loop should continue while the next square still fits within `n`. The
invariant should relate `sqr` to `r`, and separately record that the current `r`
is still a valid lower approximation.

### Exercise 5: Maximum Value in an Array

Goal: scan a non-empty array and return a maximum value.

This is the first array traversal. The precondition should rule out the empty
array, because the usual implementation starts from `a[0]`.

The result must be at least every array element, and it must equal some element
of the array. That second condition prevents specifications that allow a made-up
large number.

A common loop shape is:

- initialize the current maximum from `a[0]`;
- scan with an index;
- update the current maximum when the scanned element is larger.

The invariant should say the current maximum is at least every element already
visited. You also need an existence fact saying the current maximum came from the
array. When the loop starts, the visited prefix may be empty, so make sure each
invariant is true at loop entry.

### Exercise 6: Recursive Binary Search

Goal: complete a recursive binary search over the range `[low, high)`.

This is the first task where the proof must track a shrinking search space.
The existing contracts already say that the array is sorted and that the range is
valid. The missing precondition should describe what is known about elements
outside the current candidate range. This is the recursive analogue of the
standard binary-search loop invariant: only `[low, high)` may still contain the
value.

The missing `decreases` clause should measure how much search space remains.
Check both recursive calls:

- when searching the upper half, the lower bound moves past `mid`;
- when searching the lower half, the upper bound becomes `mid`.

If the recursive calls fail to verify, check whether their new ranges still
satisfy the same "outside the range" fact required by the method. That fact is
the induction boundary for the recursive search.

### Exercise 7: Loop Binary Search with Nullable Arrays

Goal: implement loop-based binary search, but treat `null` as an empty array.

This exercise combines the search-space idea from Exercise 6 with a loop
invariant. It also introduces nullable arrays.

Start by deciding the method contract. For non-null arrays, it should match the
usual binary-search behavior. For `null`, the method should report that the value
was not found.

A helper predicate is useful for "the array is either null or sorted." Once the
method has checked `a == null` and returned, Dafny can reason about `a` as
non-null in the remaining code.

The main loop should maintain:

- valid bounds for `low` and `high`;
- the fact that no excluded index contains the value;
- a termination measure based on the current search range.

Do not forget that the lower update must skip `mid` after proving `a[mid]` is too
small. If Dafny complains about an array access after the null case, make sure
the code structure really exits on `null` before touching `a.Length` or `a[mid]`.

### Exercise 8: Circular Shift

Goal: shift every element one position to the right, with the old last element
moving to index `0`.

This is the first exercise where the array contents change. The specification
therefore has to relate the final array to the array as it was at method entry.

Because the method mutates the array, the contract must include `modifies a`.
The postconditions should relate the final array to the entry-state array using
`old(...)`.

A convenient implementation scans from right to left:

- save the old last element;
- copy `a[i - 1]` into `a[i]`;
- finally write the saved value into `a[0]`.

The loop invariant should distinguish the unchanged prefix from the shifted
suffix. Slices are helpful for the unchanged prefix; a quantifier is helpful for
the suffix that has already been shifted.

The empty-array case should return before reading the last element. This is both
normal defensive programming and part of what Dafny must prove for memory safety.

### Exercise 9: Insertion Sort Inner Invariant

Goal: fill the missing invariant in the inner loop of insertion sort.

This final exercise combines most of the earlier ideas: array predicates,
quantifiers, nested loops, mutation, and an invariant that is deliberately weaker
than full sortedness while the inner loop is running.

The outer loop says the prefix `arr[0..i)` is sorted before inserting position
`i`. During the inner loop, the current element is being moved left by swaps.
This temporarily breaks the simple sorted-prefix statement, so the missing
invariant has to describe the "almost sorted" state.

Think of `j` as the exceptional position. Most ordered pairs in the prefix still
have the right order; the comparisons involving the moving element are the ones
that may be temporarily unresolved.

The multiset invariant already states that swaps preserve the collection of
values. Your missing invariant should focus on order, not permutation.

This is the hardest exercise in the set. A good way to debug it is to ask: "Which
single comparison could currently be wrong because of the moving element?" Then
state sortedness for the rest of the prefix.
