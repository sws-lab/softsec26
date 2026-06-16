package average;

// "The average of two ints", twice: a trusted 64-bit reference (average1) and
// an efficient 32-bit version under test (average2). Differential fuzzing
// compares them, so your job is to make the fast one agree with the reference.
//
// Contract: both methods return the floor of (a + b) / 2 computed over
// mathematical integers (no overflow, rounding toward negative infinity), for
// ALL int inputs. average1 already meets it; average2 does not yet.
public final class Average {
    private Average() {}

    // The trusted reference: widen to long so a + b cannot overflow, then floor.
    // It is the specification in code form -- leave it alone.
    public static int average1(int a, int b) {
        return (int) Math.floorDiv((long) a + b, 2L);
    }

    // The efficient version under test: it should compute the same floor using
    // only 32-bit int arithmetic, but this naive attempt overflows once a + b
    // passes Integer.MAX_VALUE and truncates toward zero instead of flooring.
    public static int average2(int a, int b) {
        return (a + b) / 2;
    }

    // A few interesting inputs to look at by hand: `make demo-average`.
    public static void main(String[] args) {
        int[][] pairs = {
            {2_000_000_000, 2_000_000_000},
            {-2_000_000_000, 2_000_000_000},
            {-7, 0},
        };
        for (int[] p : pairs) {
            System.out.println("average1(" + p[0] + ", " + p[1] + ") = "
                + average1(p[0], p[1]));
            System.out.println("average2(" + p[0] + ", " + p[1] + ") = "
                + average2(p[0], p[1]));
        }
    }
}
