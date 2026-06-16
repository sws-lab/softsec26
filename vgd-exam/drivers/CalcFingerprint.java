package exam;

import calc.CalcException;
import calc.Calculator;

// Q1 driver: evaluate token-derived expressions with the (fixed) calculator
// and print one line per case. CalcException renders as "ERR" (the
// documented contract); any other throwable renders as "EXC:<name>", which
// never matches the expected vector - so unfixed code cannot pass.
public final class CalcFingerprint {
    public static void main(String[] args) {
        String id = args[0];
        for (int i = 0; i < Derive.CALC_CASES; i++) {
            String expr = Derive.calcExpression(id, i);
            String res;
            try {
                res = Long.toString(Calculator.eval(expr));
            } catch (CalcException e) {
                res = "ERR";
            } catch (Throwable t) {
                res = "EXC:" + t.getClass().getSimpleName();
            }
            System.out.println(i + ":" + res);
        }
    }
}
