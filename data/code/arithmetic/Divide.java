public class Divide {

    /**
     * Divides two integers.
     * 
     * @param a the dividend
     * @param b the divisor
     * @return the quotient
     * 
     * @throws ArithmeticException if the divisor is zero
     */
    public int divide(int a, int b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }

        return a / b;
    }
}
