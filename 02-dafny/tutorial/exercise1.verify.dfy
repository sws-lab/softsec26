include "exercise1.dfy"

method VerifyMax(a: int, b:int) returns (c: int)
	ensures a < b  ==> c == b
	ensures b <= a ==> c == a
{
	c := Max(a, b);
}