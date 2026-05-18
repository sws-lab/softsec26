function min(a: int, b: int): int
{
  if a <= b then a else b
}

function sum(a: seq<int>): int
{
  if |a| == 0 then 0 else a[0] + sum(a[1..])
}