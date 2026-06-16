package exam;

import search.OracleAdapter;
import search.StudentSearch;

// Q4 driver: run the (fixed) student search AND the Dafny-verified oracle on
// token-derived sorted arrays and print "i:<student>=<oracle>" per case.
// Arrays contain duplicates, so "an index of key" is not enough: the oracle
// returns the FIRST occurrence, and the fixed search must match it exactly.
public final class SearchFingerprint {
    public static void main(String[] args) {
        String id = args[0];
        boolean diverged = false;
        for (int i = 0; i < Derive.SEARCH_CASES; i++) {
            int[] a = Derive.searchArray(id, i);
            int key = Derive.searchKey(id, i, a);
            int s = StudentSearch.find(a, key);
            int o = OracleAdapter.find(a, key);
            if (s != o) {
                diverged = true;
                System.err.println("case " + i + ": student=" + s + " oracle=" + o);
            }
            System.out.println(i + ":" + s + "=" + o);
        }
        if (diverged) {
            System.err.println("WARNING: StudentSearch disagrees with the verified oracle.");
            System.err.println("Fix src/main/java/search/StudentSearch.java and rerun.");
        }
    }
}
