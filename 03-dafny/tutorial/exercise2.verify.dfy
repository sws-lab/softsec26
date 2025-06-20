include "exercise2.dfy"

predicate verify_sorted(a: array<int>)
	reads a
{
	forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
}

method VerifyBinarySearch(a: array<int>, value: int) returns (index: int)
    requires sorted(a)
	ensures 0 <= index ==> index < a.Length && a[index] == value
	ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != value
{
    index := BinarySearchRec(a, value, 0, a.Length);
}
