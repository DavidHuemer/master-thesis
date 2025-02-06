public class DivideIncorrect {

    /**
     * Divides two integers.
     * 
     * @param a the dividend
     * @param b the divisor
     * @return the quotient
     * 
     * @throws IllegalArgumentException if the divisor is zero
     */
    public int divide(int a, int b) {
        if (b == 0) {
            throw new IllegalArgumentException("Cannot divide by zero");
        }

        return b / a;
    }
}
