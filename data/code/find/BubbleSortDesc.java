public class BubbleSortDesc {

    private void swap(int x, int y, int[] array) {
        int temp;
        temp = array[x];
        array[x] = array[y];
        array[y] = temp;
    }

    /**
     * Returns a sorted array using the bubbleSort algorithm. The resulting array is
     * sorted in descending order.
     * The initial array is not modified.
     * 
     * @param arr The array to sort
     * @return The sorted array
     */
    public int[] bubbleSort(int[] arr) {
        int n = arr.length;

        for (int i = 0; i < n - 1; i++) {

            for (int j = 0; j < n - i - 1; j++) {
                if (arr[j + 1] > arr[j]) {
                    swap(j, j + 1, arr);
                }
            }
        }
        return arr;
    }
}