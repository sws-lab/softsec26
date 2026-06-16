package calc;

// The one exception Calculator.eval is allowed to throw: malformed input,
// division by zero, or input too deeply nested. Anything else escaping
// eval() is a bug.
public class CalcException extends RuntimeException {
    public CalcException(String message) {
        super(message);
    }
}
