include "BinarySearch.dfy"

import opened Oracle

method VerifyFind(a: seq<int>, key: int) returns (index: int)
  requires forall i, j :: 0 <= i < j < |a| ==> a[i] <= a[j]
  ensures 0 <= index ==> index < |a| && a[index] == key
                         && forall k :: 0 <= k < index ==> a[k] < key
  ensures index < 0 ==> key !in a
{
  index := Find(a, key);
}
