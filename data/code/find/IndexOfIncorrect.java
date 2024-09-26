public class IndexOfIncorrect {
    /**
    * Searches for the first occurrence of a specified element in an array and returns its index.
    * @param arr the array to search in
    * @param target the value to search for
    * @return the index of the first occurrence of the target value in the array, or -1 if the target is not found
    * @throws NullPointerException if the array is null
    */
    public int find(int[] arr, int target) {
        int index = -1;

        for (int i = 0; i < arr.length; i++) {
            if (arr[i] == target) {
                index = i;
            }
        }
        return index;
    }
}