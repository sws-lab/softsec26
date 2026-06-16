package exam;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;

// Deterministic test-input derivation from the student's exam token.
//
// Everything is derived from SHA-256 digests, byte for byte, with no PRNG.
// The instructor-side grader (grading/grade.py) re-implements exactly the
// same derivation in Python; any change here must be mirrored there.
public final class Derive {
    private Derive() {}

    public static final int CALC_CASES = 24;
    public static final int AVG_CASES = 16;
    public static final int SEARCH_CASES = 16;

    // 64 deterministic bytes per (token, tag, case).
    public static byte[] bytes64(String id, String tag, int i) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] d1 = md.digest((id + "|" + tag + "|" + i + "|a").getBytes(StandardCharsets.UTF_8));
            byte[] d2 = md.digest((id + "|" + tag + "|" + i + "|b").getBytes(StandardCharsets.UTF_8));
            byte[] out = new byte[64];
            System.arraycopy(d1, 0, out, 0, 32);
            System.arraycopy(d2, 0, out, 32, 32);
            return out;
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }

    private static int u(byte b) {
        return b & 0xFF;
    }

    private static int int32(byte[] d, int off) {
        return (u(d[off]) << 24) | (u(d[off + 1]) << 16) | (u(d[off + 2]) << 8) | u(d[off + 3]);
    }

    // ---- Q1: arithmetic expression for case i, fully parenthesized -------
    // Tree grammar (cursor walks the digest): at depth 3 or when the next
    // byte is divisible by 3, emit a literal 0..99; otherwise emit a binary
    // node with operator "+-*/"[byte % 4]. Values stay well inside long
    // range (at most 8 literals of at most 2 digits).
    public static String calcExpression(String id, int i) {
        if (i == 0) {
            // A fixed probe case, identical for every student; the other 23
            // are token-derived below. (Rationale in AGENTS.md, not shipped.)
            return "99999999999999999999";
        }
        byte[] d = bytes64(id, "q1", i);
        int[] cursor = {0};
        return gen(d, cursor, 0);
    }

    private static String gen(byte[] d, int[] cursor, int depth) {
        int b = u(d[cursor[0]++]);
        if (depth == 3 || b % 3 == 0) {
            return Integer.toString(u(d[cursor[0]++]) % 100);
        }
        char op = "+-*/".charAt(u(d[cursor[0]++]) % 4);
        String left = gen(d, cursor, depth + 1);
        String right = gen(d, cursor, depth + 1);
        return "(" + left + op + right + ")";
    }

    // ---- Q2: int pair for case i ------------------------------------------
    // Every fourth case forces near-MAX pairs (overflow in (a+b)/2), every
    // fourth forces a near-MIN/small pair (overflow in b-a), every fourth
    // forces small negatives (rounding direction).
    public static int[] averagePair(String id, int i) {
        byte[] d = bytes64(id, "q2", i);
        int a = int32(d, 0);
        int b = int32(d, 4);
        if (i % 4 == 1) {
            a = Integer.MAX_VALUE - u(d[8]) % 5;
            b = Integer.MAX_VALUE - u(d[9]) % 5;
        } else if (i % 4 == 2) {
            a = Integer.MIN_VALUE + u(d[8]) % 5;
            b = u(d[9]) % 50;
        } else if (i % 4 == 3) {
            a = -(u(d[8]) % 9) - 1;
            b = u(d[9]) % 9;
        }
        return new int[] {a, b};
    }

    // ---- Q4: sorted array + key for case i --------------------------------
    // Non-decreasing values with frequent REPEATS (each step adds 0, 1, or 2),
    // so a key can occur several times. The spec wants the FIRST occurrence, so
    // a search that returns just any matching index disagrees with the oracle.
    public static int[] searchArray(String id, int i) {
        byte[] d = bytes64(id, "q4", i);
        int n = u(d[0]) % 8;
        int[] a = new int[n];
        if (n > 0) {
            a[0] = u(d[1]) % 10 - 5;
            for (int j = 1; j < n; j++) {
                a[j] = a[j - 1] + u(d[2 + j]) % 3;
            }
        }
        return a;
    }

    public static int searchKey(String id, int i, int[] a) {
        byte[] d = bytes64(id, "q4", i);
        int k = u(d[10]);
        if (a.length == 0) {
            return 7;                       // absent -> -1
        }
        if (i % 4 == 0) {
            return a[a.length - 1] + 1;     // absent (just above the max) -> -1
        }
        return a[k % a.length];             // present; often inside a run of duplicates
    }
}
