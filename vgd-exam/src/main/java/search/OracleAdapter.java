package search;

import dafny.DafnySequence;
import dafny.TypeDescriptor;
import java.lang.reflect.Method;
import java.math.BigInteger;

// Bridges Java's int[] to the verified search in src/main/java/Oracle/,
// which was generated from dafny/BinarySearch.dfy by `dafny translate java`.
//
// Trust boundary, stated explicitly: the oracle is correct modulo
//  (1) Dafny's verifier,
//  (2) the Dafny-to-Java translator,
//  (3) this adapter (it must pass a sorted array - the oracle's
//      precondition - and convert values faithfully).
public final class OracleAdapter {
    private OracleAdapter() {}

    public static int find(int[] a, int key) {
        BigInteger[] seq = new BigInteger[a.length];
        for (int i = 0; i < a.length; i++) {
            seq[i] = BigInteger.valueOf(a[i]);
        }
        DafnySequence<BigInteger> s =
            DafnySequence.of(TypeDescriptor.BIG_INTEGER, seq);
        try {
            Class<?> oracle = Class.forName("Oracle.__default");
            Method find = oracle.getMethod(
                "Find", DafnySequence.class, BigInteger.class);
            Object result = find.invoke(null, s, BigInteger.valueOf(key));
            return ((BigInteger) result).intValueExact();
        } catch (ClassNotFoundException e) {
            throw new IllegalStateException(
                "generated oracle missing; run `make oracle` after Q3 verifies", e);
        } catch (ReflectiveOperationException e) {
            throw new IllegalStateException("generated oracle could not be called", e);
        }
    }
}
