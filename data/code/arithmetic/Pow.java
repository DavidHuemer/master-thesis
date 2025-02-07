public class Pow {
    /**
     * Returns the result of raising a number to a power.
     * If b is 0, the result is 1.
     * 
     * @param a the base
     * @param b the exponent
     * @return the result of raising a to the power of b
     *
     * @throws IllegalArgumentException if a is negative or b is negative
     * @throws IllegalArgumentException if a or b is greater than 10
     */
    public int pow(int a, int b) {
        if (a < 0 || b < 0) {
            throw new IllegalArgumentException("a and b must be non-negative");
        }

        if (a > 10 || b > 10) {
            throw new IllegalArgumentException("a and b must be less than or equal to 10");
        }

        int result = 1;

        for (int i = 0; i < b; i++) {
            result *= a;
        }

        return result;
    }
}
