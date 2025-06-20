// Exercise 4. Fill in the missing invariant of insertion sort inner loop.
// Consider how elements in range a[0..i] compare among themselves, and what is special about element a[j].

predicate sorted_slice(a: array<int>, begin: int, end: int)
    requires 0 <= begin <= end <= a.Length
    reads a {
    forall i, j :: begin <= i <= j < end ==> a[i] <= a[j]
}

method insertion_sort(arr: array<int>)
    modifies arr
    ensures sorted_slice(arr, 0, arr.Length)
    ensures multiset(arr[..]) == multiset(old(arr[..]))
{
    if arr.Length < 2 {
        return;
    }

    var i := 1;
    while i < arr.Length
        invariant 1 <= i <= arr.Length
        invariant sorted_slice(arr, 0, i)
        invariant multiset(arr[..]) == multiset(old(arr[..]))
    {
        var j := i;
        while j >= 1 && arr[j - 1] > arr[j]
            invariant 0 <= j <= i
            invariant // Fill in the missing invariant here
            invariant multiset(arr[..]) == multiset(old(arr[..]))
        {
            arr[j - 1], arr[j] := arr[j], arr[j - 1];
            j := j - 1;
        }

        i := i + 1;
    }
}
