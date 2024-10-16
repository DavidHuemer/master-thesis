public class IsCommonFactor {
    /**
     * Returns whether the factor is a common factor of the two numbers.
     * 
     * @param a:      The first number
     * @param b:      The second number
     * @param factor: The number that is checked whether it is a common factor of
     *                the two numbers
     * 
     * @return True when the factor is the common factor of the two numbers, false
     *         otherwise.
     */
    public boolean isCommonFactor(int a, int b, int factor) {
        return a % factor == 0 && b % factor == 0;
    }
}