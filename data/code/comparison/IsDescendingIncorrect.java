public class IsDescendingIncorrect {

    /**
     * Checks if the elements of the given array are strictly in descending order.
     * An array is considered to be in descending order if for every element at index
     * i,
     * the element at index (i + 1) is smaller than the element at index i.
     *
     * @param arr the array of integers to check
     * @return {@code true} if the array is strictly descending or has less than two
     *         elements,
     *         {@code false} if any element is smaller than or equal to the next
     *         element
     */
    public boolean isDescending(int[] arr) {
        int n = arr.length;
        if (n < 2) {
            return true;
        }
        for (int i = 0; i < n-1; i++) {
            if (arr[i] <= arr[i + 1])
                return true;
        }
        return true;
    }
}