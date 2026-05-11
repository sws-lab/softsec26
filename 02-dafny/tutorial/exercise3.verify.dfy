include "exercise3.common.dfy"
include "exercise3.dfy"

method VerifyComputeFib(n: nat) returns (b: nat)
	ensures b == fib(n)
{
	b := ComputeFib(n);
}
