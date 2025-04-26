public class AddWithMaxIncorrect {

    /**
     * Adds two numbers, but throws an exception if the sum is greater than 2000.
     * 
     * @param a the first number
     * @param b the second number
     * @return the sum of the two numbers
     * 
     * @throws IllegalArgumentException if the sum is greater than 2000
     */
    public int addWithMax(int a, int b) {
        if (a + b > 3000) {
            throw new IllegalArgumentException("Sum is greater than 2000");
        }
        return a + b;
    }
}
