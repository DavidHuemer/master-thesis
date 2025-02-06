public class RandomInt {
    /**
     * Generates a random integer between the given minimum and maximum values.
     * 
     * @param min the minimum value of the random integer
     * @param max the maximum value of the random integer
     * @return a random integer between the minimum and maximum values
     * 
     * @throws IllegalArgumentException if {@code min > max}
     */
    public int randomInt(int min, int max) {
        if (min > max) {
            throw new IllegalArgumentException("min(" + min + ") > max(" + max + ")");
        }

        return min + (int) (Math.random() * ((max - min) + 1));
    }
}
