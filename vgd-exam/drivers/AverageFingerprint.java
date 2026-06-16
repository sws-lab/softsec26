package exam;

import average.Average;

// Q2 driver: run both average implementations on token-derived pairs
// (including forced overflow and rounding cases) and print
// "i:<average1>=<average2>=<floorReference>" per case.
//
// The floor reference is the specification value -- floor((a+b)/2) computed
// in 64-bit, immune to overflow. exam.py compares your two methods against
// each other AND against this reference, so a fix where both methods agree
// but are wrong the same way (e.g. truncating toward zero instead of
// flooring) is reported instead of silently passing. The recorded answer is
// just "i:<average1>=<average2>".
public final class AverageFingerprint {
    public static void main(String[] args) {
        String id = args[0];
        for (int i = 0; i < Derive.AVG_CASES; i++) {
            int[] p = Derive.averagePair(id, i);
            long a = p[0];
            long b = p[1];
            int ref = (int) Math.floorDiv(a + b, 2L);
            System.out.println(i + ":" + Average.average1(p[0], p[1])
                + "=" + Average.average2(p[0], p[1])
                + "=" + ref);
        }
    }
}
