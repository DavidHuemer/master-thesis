public class DigitRoot {
    /**
     * Calculates the digit root of a given number. The digit root is the result of
     * repeatedly summing the digits of a number until a single-digit value is obtained.
     *
     * @param number The input number for which to calculate the digit root. Must be a non-negative integer.
     * @return The single-digit result of the digit root calculation.
     * @throws IllegalArgumentException if the input number is negative.
     *
     * <p>Example usage:</p>
     * <pre>
     *     DigitRootCalculator.calculateDigitRoot(987); // Returns 6
     * </pre>
     */
    public int digitRoot(int number) {
        if (number < 0) {
            throw new IllegalArgumentException("Number must be non-negative.");
        }

        // Optimized calculation using modulo 9
        if (number == 0) {
            return 0;
        }

        int digitRoot = number % 9;
        return (digitRoot == 0) ? 9 : digitRoot;
    }
}