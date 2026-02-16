method Abs(i: int) returns (r: int)
ensures 0 <= r
ensures r == i || r == -i
{   
    r := i;
    if r < 0 {
         r := -1 * r;
    }
}