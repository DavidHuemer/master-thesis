public class ExceptionTestIncorrect {
    /**
     * Returns the same integer as given.
     * If the integer is greater than 10, throws
     * an IllegalArgumentException.
     * 
     * @param a the integer to return
     * @return the integer
     * @throws IllegalArgumentException if the integer is greater than 10
     */
    public int test(int a) {
        if (a >= 10) {
            throw new IllegalArgumentException("a is too big");
        }

        return a;
    }
}