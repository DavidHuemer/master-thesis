public class FindFirstZero {
    /**
     * Finds the first zero in the given array.
     * 
     * @param arr The array to search
     * 
     * @return The index of the first zero in the array, or -1 if no zero is found
     */
    public int findFirstZero(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == 0) {
                return i;
            }
        }
        return -1;
    }
}
