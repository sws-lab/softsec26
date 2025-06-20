// Exercise 8. Look at provided square root method for natural numbers. Fill in the loop condition and invariant to verify method correctness.
// You might want to manually compute few iterations of the loop to see how variables change.

method SquareRoot (n: nat) returns (r: nat)
    ensures r * r <= n < (r + 1) * (r + 1)
{
    r := 0;
    var sqr := 1;
    while // Fill in the condition and invariant
    {
        r := r + 1;
        sqr := sqr + 2 * r + 1;
    }
}
