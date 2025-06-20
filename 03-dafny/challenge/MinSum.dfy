function min(a: int, b: int): int
{
  if a <= b then a else b
}

function sum(a: seq<int>): int
{
  if |a| == 0 then 0 else a[0] + sum(a[1..])
}

method MinSum(a: seq<int>) returns (s: int)
requires 0 < |a|;
ensures forall i,j :: 0 <= i < j <= |a| ==> s <= sum(a[i..j])
{
  var k := 1;
  var t := a[0];
  s := a[0];
  while (k < |a|) 
  {
    t := min(t + a[k], a[k]);
    s := min(s,t);
    k := k + 1;
  }
}
