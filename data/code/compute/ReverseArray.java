public class ReverseArray {
    /**
     * Reverses the order of the elements in an array.
     * 
     * @param a the array to reverse
     * @return the reversed array
     */
    public int[] reverse(int[] a) {
        int[] result = new int[a.length];
        for (int i = 0; i < a.length; i++) {
            result[i] = a[a.length - (i + 1)];
        }
        return result;
    }
}
