public class LastIndexOf {
    /**
     * Finds the last index of a specified element in an array.
     *
     * @param arr     The array in which to search for the element.
     * @param element The element to search for.
     * @return The last index of the element in the array, or -1 if the element is
     *         not found.
     */
    public static int lastIndexOf(int[] arr, int element) {
        for (int i = arr.length - 1; i >= 0; i--) {
            if (arr[i] == element) {
                return i;
            }
        }
        return -1; // Element not found
    }
}
