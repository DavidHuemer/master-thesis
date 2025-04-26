public class CompareIntIncorrect {
    /**
     * Compares two integers.
     * 
     * @param a the first integer
     * @param b the second integer
     * @return 0 if the integers are equal, a positive number if the first integer
     *         is greater, and a negative number if the second integer is greater
     */
    public int compareInt(int a, int b) {
        if (a == b) {
            return 0;
        } else if (a > b) {
            return -1;
        } else {
            return 1;
        }
    }
}
