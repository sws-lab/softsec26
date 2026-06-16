package search;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;
import java.util.Arrays;

class SearchOracleFuzzTest {

    @FuzzTest(maxDuration = "30s")
    void matchesOracle(FuzzedDataProvider data) {
        int n = data.consumeInt(0, 16);
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            // A small value range so the sorted array frequently REPEATS values
            // -- the only situation in which the leftmost-occurrence bug shows.
            a[i] = data.consumeInt(-10, 10);
        }
        Arrays.sort(a); // establish the oracle's precondition
        int key = data.consumeInt(-10, 10);

        int s = StudentSearch.find(a, key);
        int o = OracleAdapter.find(a, key);

        // The spec asks for the index of the FIRST occurrence of key, which is
        // unique, so we compare the indices directly against the verified
        // oracle. Both must return the same index (or both -1); any difference
        // is, by construction, a bug in StudentSearch.
        if (s != o) {
            throw new AssertionError("disagreement on " + Arrays.toString(a)
                + " key=" + key + ": student=" + s + " oracle=" + o);
        }
    }
}
