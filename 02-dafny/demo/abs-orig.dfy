method Abs(i: int) returns (r: int)
ensures 0 <= r
{   
    if 0 <= i {
        r := i;
    } else {
        r := -i;
    }
}