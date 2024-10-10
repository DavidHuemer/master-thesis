public class Biggest {
    /**
     * Returns the biggest element in the given array.
     * If the array is empty, returns -1.
     * 
     * @param a the array of integers
     * @return the biggest element in the array, or -1 if the array is empty
     */
    public int biggest(int[] a) {
        if (a.length == 0)
            return -1;

        int biggest = a[0];

        for (int i = 1; i < a.length; i++) {
            if (a[i] > biggest) {
                biggest = a[i];
            }
        }

        return biggest;
    }
}