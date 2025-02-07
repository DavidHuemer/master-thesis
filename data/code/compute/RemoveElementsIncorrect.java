public class RemoveElementsIncorrect {
    /**
     * Returns a new array with all occurrences of an element removed.
     * The original array is not modified.
     * The new array may be shorter than the original array.
     *
     * @param arr the array from which the returning array is built (without the element to remove)
     * @param b   the element to remove
     * @return the new array with the element removed (may be shorter than the original array)
     */
    public int[] removeElement(int[] arr, int b) {
        int count = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] != b) {
                count++;
            }
        }

        int[] result = new int[count];

        for (int i = 0, j = 0; i < arr.length-1; i++) {
            if (arr[i] != b) {
                result[j] = arr[i];
                j++;
            }
        }

        return result;
    }
}
