method Abs(i: int) returns (r: int)
ensures 0 <= r
{   
    if 0 <= i {
        assert 0 <= i;
        r := i;
        assert 0 <= r;
    } else {
        assert i < 0;
        assert 0 <= -i;
        r := -i;
        assert 0 <= r;
    }
    assert 0 <= r;
}