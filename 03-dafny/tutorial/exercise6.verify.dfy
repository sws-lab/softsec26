include "exercise6.dfy"

method VerifyFindMax(a: array<int>) returns (max: int)
	requires 0 < a.Length
	ensures forall k :: 0 <= k < a.Length ==> max >= a[k]
	ensures exists k :: 0 <= k < a.Length && max == a[k]
{
	max := FindMax(a);
}
