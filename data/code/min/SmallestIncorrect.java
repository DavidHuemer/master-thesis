public class SmallestIncorrect {
    /**
     * Returns the smallest element in the given array.
     * If the array is empty, returns -1.
     * 
     * @param a the array of integers
     * @return the smallest element in the array, or -1 if the array is empty
     */
    public int smallest(int[] a) {
        if (a.length == 0)
            return -1;

        int smallest = a[0];

        for (int i = 1; i < a.length; i++) {
            if (a[i] > smallest) {
                smallest = a[i];
            }
        }

        return smallest;
    }
}