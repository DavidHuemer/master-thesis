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
     * 
     * @throws IllegalArgumentException when the factor is less than 1
     */
    public boolean isCommonFactor(int a, int b, int factor) {
        if (factor < 1) {
            throw new IllegalArgumentException("The factor must be greater than 0.");
        }

        return a % factor == 0 && b % factor == 0;
    }
}