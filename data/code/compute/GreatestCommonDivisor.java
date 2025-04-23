public class GreatestCommonDivisor {
    /**
     * Calculates the Greatest Common Divisor (GCD) of two positive integers using
     * the recursive subtraction-based Euclidean algorithm.
     *
     * @param y1 the first positive integer
     * @param y2 the second positive integer
     * @return the greatest common divisor of y1 and y2;
     *         returns 0 if either input is less than or equal to zero
     */
    public int getGreatestCommonDivisor(int y1, int y2) {
        if (y1 <= 0 || y2 <= 0) {
          return 0;
        }
        if (y1 == y2) {
          return y1;
        }
        if (y1 > y2) {
          return getGreatestCommonDivisor(y1 - y2, y2);
        }
        return getGreatestCommonDivisor(y1, y2 - y1);
    }
}