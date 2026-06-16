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
