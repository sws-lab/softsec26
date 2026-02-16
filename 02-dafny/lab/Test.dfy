method Abs(n: int) returns (result: int)
    ensures result >= 0
    ensures result == n || result == -n
{
    if n < 0 {
        result := -n;
    } else {
        result := n;
    }
}

method {:main} TestAbs()
{
    var x := Abs(-3);
    assert x == 3;
    print x, "\n";
}