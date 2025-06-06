public class DistinctArrayIncorrect {
    /**
     * Returns whether the elements of the array are all distinct
     * 
     * @param arr: The array that is checked whether all elements are distinct
     * 
     * @return Whether the elements of the array are all distinct
     */
    public boolean isDistinct(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            for (int j = i + 1; j < arr.length; j++) {
                if (arr[i] == arr[j]) {
                    return true;
                }
            }
        }
        return false;
    }
}
