public class RemoveElements {
    /**
     * Removes all occurrences of an element from an array.
     * 
     * @param arr the array to remove elements from
     * @param b   the element to remove
     * @return the array with the element removed (may be shorter than the original array)
     */
    public int[] removeElement(int[] arr, int b) {
        int count = 0;
        for (int i = 0; i < arr.length; i++) {
            if (arr[i] != b) {
                count++;
            }
        }

        int[] result = new int[count];

        for (int i = 0, j = 0; i < arr.length; i++) {
            if (arr[i] != b) {
                result[j] = arr[i];
                j++;
            }
        }

        return result;
    }
}
