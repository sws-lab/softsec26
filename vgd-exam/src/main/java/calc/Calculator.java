package calc;

// A tiny calculator for integer arithmetic expressions:
//
//   expr   := term  (('+' | '-') term)*
//   term   := factor (('*' | '/') factor)*
//   factor := number | '(' expr ')'
//
// Numbers are non-negative decimal literals; values are Java longs.
//
// Its author was careful about the malformed *syntax* they thought of: a
// stray character, a missing parenthesis, and input that ends mid-expression
// all raise CalcException. But "the cases I thought of" is exactly what
// fuzzing looks past - some inputs still make eval throw something other than
// CalcException, and Part A's fuzzer will hand them to you one at a time.
// Finding and fixing them (there is more than one) is the exercise.
//
// Contract after your fix: eval() either returns a value or throws
// CalcException. No other exception may escape.
public final class Calculator {

    public static long eval(String input) {
        return new Calculator(input).expr();
    }

    private final String s;
    private int pos;

    private Calculator(String s) {
        this.s = s;
    }

    private long expr() {
        long v = term();
        while (pos < s.length() && (s.charAt(pos) == '+' || s.charAt(pos) == '-')) {
            char op = s.charAt(pos);
            pos++;
            long r = term();
            v = (op == '+') ? v + r : v - r;
        }
        return v;
    }

    private long term() {
        long v = factor();
        while (pos < s.length() && (s.charAt(pos) == '*' || s.charAt(pos) == '/')) {
            char op = s.charAt(pos);
            pos++;
            long r = factor();
            if (op == '*') {
                v = v * r;
            } else {
                v = v / r;
            }
        }
        return v;
    }

    private long factor() {
        if (pos >= s.length()) {
            throw new CalcException("expected a number or '(' but reached end of input");
        }
        char c = s.charAt(pos);
        if (c == '(') {
            pos++;
            long v = expr();
            if (pos >= s.length() || s.charAt(pos) != ')') {
                throw new CalcException("missing ')'");
            }
            pos++;
            return v;
        }
        if (!Character.isDigit(c)) {
            throw new CalcException("unexpected character '" + c + "'");
        }
        int start = pos;
        while (pos < s.length() && Character.isDigit(s.charAt(pos))) {
            pos++;
        }
        return Long.parseLong(s.substring(start, pos));
    }
}
