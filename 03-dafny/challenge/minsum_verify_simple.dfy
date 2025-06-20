include "minsum.dfy"
include "common.dfy"

method TeacherMinSum(a: seq<int>) returns (s: int)
requires 0 < |a|
ensures forall i,j :: 0 <= i < j <= |a| ==> s <= sum(a[i..j])
{
  s := MinSum(a);
}
