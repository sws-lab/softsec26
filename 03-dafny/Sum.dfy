function sum(a: seq<int>): int
{
   if |a| == 0 then 0 else a[0] + sum(a[1..])
}

lemma SumLemma(a: seq<int>, b: seq<int>)
ensures sum(a + b) == sum(a) + sum(b)
{
  if (a == []) {
    assert a + b == b;
  }
  else { 
    // assert a == [a[0]] + a[1..];
    // assert a[0] + sum(a[1..]) == sum(a);
    // SumLemma(a[1..], b);
    // assert sum(a[1..]) + sum(b) == sum(a[1..] + b);
    // assert ([a[0]] + (a[1..] + b) == ([a[0]] + a[1..]) + b);
    assert ([a[0]] + (a[1..] + b) == a + b);
    // assert sum(a + b) == sum(a) + sum(b);
  }
}


method SumIter(a: seq<int>) returns (s: int) 
ensures s == sum(a)
{
  s := 0;
  var i := 0;
  while (i < |a|)
    invariant i <= |a|
    invariant s == sum(a[0..i])
  {
    SumLemma(a[0..i], [a[i]]);
    assert a[0..i] + [a[i]] == a[0..(i+1)];
    // assert sum(a[0..i]) + a[i] == sum(a[0..(i + 1)]);
    // assert s + a[i] == sum(a[0..(i + 1)]);
    s := s + a[i];
    // assert s == sum(a[0..(i + 1)]);
    i := i + 1;
    // assert s == sum(a[0..i]);
  }
  //assert i == |a|;
  assert a[0..|a|] == a;
  assert s == sum(a);
}
