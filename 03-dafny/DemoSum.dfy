function sumto(n: nat): nat
{
  if (n == 0) then 0 else n + sumto(n-1)
}

lemma Gauss(n: nat)
ensures sumto(n) == n * (n+1) / 2
{ }

method SumTo(n : nat) returns (s: nat)
ensures s == sumto(n)
{
  Gauss(n);
  assert sumto(n) == n * (n+1) / 2;
  return n * (n+1) / 2;
}
