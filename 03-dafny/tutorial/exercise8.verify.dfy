include "exercise8.dfy"

method VerifySquareRoot (n: nat) returns (r: nat)
    ensures r * r <= n < (r + 1) * (r + 1)
{
    r := SquareRoot(n);
}
