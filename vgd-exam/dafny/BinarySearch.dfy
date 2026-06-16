module Oracle {

method Find(a: seq<int>, key: int) returns (index: int)
  requires forall i, j :: 0 <= i < j < |a| ==> a[i] <= a[j]
  ensures 0 <= index ==> index < |a| && a[index] == key
                         && forall k :: 0 <= k < index ==> a[k] < key
  ensures index < 0 ==> key !in a
{
  var lo, hi := 0, |a|;
  while lo < hi
    invariant 0 <= lo <= hi <= |a|
    // TODO: add the missing loop invariants here
  {
    var mid := (lo + hi) / 2;
    if a[mid] < key {
      lo := mid + 1;
    } else {
      hi := mid;
    }
  }
  if lo < |a| && a[lo] == key {
    return lo;
  }
  return -1;
}

}
