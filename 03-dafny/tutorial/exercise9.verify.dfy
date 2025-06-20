include "exercise9.dfy"

method VerifyCircularShift(a: array<bool>)
    modifies a
    ensures a.Length > 0 ==> a[0] == old(a[a.Length - 1])
    ensures forall j :: 0 < j < a.Length ==> a[j] == old(a[j - 1])
{
    CircularShift(a);
}
