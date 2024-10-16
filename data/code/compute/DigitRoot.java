public class DigitRoot {
    /**
     * Calculates the digit root of a given positive number. The number root is the result
     * the repeated calculation of the cross sum of a number until the result is
     * only one digit.
     * 
     * @param num The number
     * @return The digit root of the number
     */
    public int digitRoot(int num) {
        while (num >= 10) {
            int sum = 0;
            while (num > 0) {
                sum += num % 10;
                num /= 10;
            }
            num = sum;
        }
        return num;
    }
}