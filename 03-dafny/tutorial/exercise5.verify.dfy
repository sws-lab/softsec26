include "exercise5.common.dfy"
include "exercise5.dfy"

method VerifyComputeFib(n: nat) returns (b: nat)
	ensures b == fib(n)
{
	b := ComputeFib(n);
}
