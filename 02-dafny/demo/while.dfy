method id(x: int) returns (r: int)
requires x >= 0
ensures x == r
{
    var i := 0;
    while i < x
        invariant i <= x // this is needed (and would fail if we do i := i + 2)
    {
        i := i + 1;
    }
    assert i == x;
    r := i;
}