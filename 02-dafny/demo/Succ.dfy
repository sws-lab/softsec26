method Succ(x: int) returns (y: int)
   ensures y == x + 1
{
    assert (x + 1 == 1 ==> x == 0) && (x + 1 != 1 ==> x + 1 == x + 1); // <-- Verification Condition
    var a := x + 1;
    assert (a == 1 ==> x == 0) && (a != 1 ==> a == x + 1);
    if (a-1 == 0)
    { 
        assert x == 0;
        y := 1; 
    }
    else
    { 
        assert a == x + 1;
        y := a; 
    }
    assert y == x + 1;
}
