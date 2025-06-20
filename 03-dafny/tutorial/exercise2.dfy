// Exercise 2: Complete the recursive binary search implementation by filling in the missing precondition and termination measure.
// For precondition, consider what are binary search expectations for array values outside of [low..high) range.
// For termination measure, consider which values might be used to ensure that recursion eventually terminates.

predicate sorted(a: array<int>)
	reads a
{
	forall j, k :: 0 <= j < k < a.Length ==> a[j] <= a[k]
}

method BinarySearchRec(a: array<int>, value: int, low: int, high: int) returns (index: int)
    requires sorted(a)
    requires 0 <= low <= high <= a.Length
    requires /* Fill in the missing precondition */
	ensures 0 <= index ==> index < a.Length && a[index] == value
	ensures index < 0 ==> forall k :: 0 <= k < a.Length ==> a[k] != value
    decreases /* Fill in the missing temination measure */
{
    if low == high {
        return -1;
    }

    var mid := (low + high) / 2;
    if a[mid] < value
    {
        index := BinarySearchRec(a, value, mid + 1, high);
    }
    else if value < a[mid]
    {
        index := BinarySearchRec(a, value, low, mid);
    }
    else
    {
        return mid;
    }
}
