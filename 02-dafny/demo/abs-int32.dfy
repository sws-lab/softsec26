newtype {:nativeType "int"} int32 = x | -0x8000_0000 <= x < 0x8000_0000

method Abs(i: int32) returns (r: int32)
requires i != -0x8000_0000
ensures 0 <= r
{   
    if 0 <= i {
        r := i;
    } else {
        r := -i;
    }
}