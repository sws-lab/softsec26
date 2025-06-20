include "exercise4.dfy"

predicate verify_sorted(a: array?<int>)
	requires a != null
	reads a
{
	forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
}

method VerifyInsertionSort(a: array<int>)
	ensures verify_sorted(a)
	ensures multiset(a[..]) == multiset(old(a[..]))
	modifies a
{
	insertion_sort(a);
}
