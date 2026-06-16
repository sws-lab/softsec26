package calc;

import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;

class CalculatorFuzzTest {

    @FuzzTest(maxDuration = "30s")
    void eval(FuzzedDataProvider data) {
        // Bound the length: this exercise is about how eval handles the
        // *content* of an expression, not how deep recursion can go, so we
        // keep inputs short enough that nesting can't exhaust the stack.
        String expr = data.consumeAsciiString(100);
        try {
            Calculator.eval(expr);
        } catch (CalcException expected) {
            // Allowed by the contract. Anything else escaping is a finding.
        } catch (Throwable finding) {
            // Maven's Jazzer runner does not echo the crashing input, so we
            // print it here: this exact string is what made eval throw a
            // forbidden exception. Then rethrow so Jazzer records the finding.
            System.err.println("\n>>> FUZZ FINDING: eval(\"" + display(expr)
                    + "\") threw " + finding.getClass().getName() + "\n");
            throw finding;
        }
    }

    // Render the fuzzer's bytes readably: printable ASCII as-is, everything
    // else as \xNN so control characters don't scramble the terminal.
    private static String display(String s) {
        StringBuilder b = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '\\') {
                b.append("\\\\");
            } else if (c == '"') {
                b.append("\\\"");
            } else if (c >= 0x20 && c < 0x7f) {
                b.append(c);
            } else {
                b.append(String.format("\\x%02x", (int) c));
            }
        }
        return b.toString();
    }
}
