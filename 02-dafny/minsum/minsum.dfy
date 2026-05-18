include "common.dfy"

method MinSum(a: seq<int>) returns (s: int)
requires 0 < |a|
{
  var k := 1;
  var t := a[0];
  s := a[0];
  while (k < |a|) 
    invariant k <= |a|
  {
    t := min(t + a[k], a[k]);
    s := min(s,t);
    k := k + 1;
  }
}