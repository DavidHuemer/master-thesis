public class FactorialIncorrect {

    /**
     * Returns the factorial of a number.
     * For example, the factorial of 5 is 5 * 4 * 3 * 2 * 1 = 120.
     * The factorial of 0 is 1.
     * 
     * @param n the number to calculate the factorial
     * @return the factorial of the number
     * 
     * @throws IllegalArgumentException if n is negative
     * @throws IllegalArgumentException if n is greater than 10
     */
    public int factorial(int n) {
        if (n < 0) {
            throw new IllegalArgumentException("Factorial is not defined for negative numbers");
        }

        if (n > 10) {
            throw new IllegalArgumentException("Factorial is not defined for numbers greater than 10");
        }

        int result = 2;
        for (int i = 1; i <= n; i++) {
            result *= i;
        }
        return result;
    }
}
