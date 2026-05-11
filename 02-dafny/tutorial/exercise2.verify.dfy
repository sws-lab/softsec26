include "exercise2.dfy"

method VerifySum(n: nat) returns (s: nat)
    ensures s == n * (n + 1) / 2 {
    s := sum(n);
}
