public class RemoveElementsIncorrect {
    /**
    * Returns a new array with all occurrences of the specified element removed.
    *
    * This method iterates through the given array and constructs a new array
    * that contains all elements except those equal to the specified value {@code b}.
    *
    *
    * @param arr the input array of integers
    * @param b the integer value to be removed from the array
    * @return a new array containing all elements of {@code arr} except those equal to {@code b}
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
