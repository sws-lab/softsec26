method FindMin(a: seq<int>) returns (s: int)
  requires 0 < |a|
  ensures forall i :: 0 <= i < |a| ==> s <= a[i]
  ensures exists i :: 0 <= i < |a| && s == a[i]
{
  s := a[0];
  var k := 1;
  while k < |a|
    invariant k <= |a|
    invariant forall i :: 0 <= i < k ==> s <= a[i]
    invariant exists i :: 0 <= i < |a| && s == a[i]
  {
    if a[k] < s
    { s := a[k]; }
    k := k + 1;
  }
  assert k == |a|;
  assert forall i :: 0 <= i < |a| ==> s <= a[i];
}
