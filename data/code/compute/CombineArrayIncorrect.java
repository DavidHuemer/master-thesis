public class CombineArrayIncorrect {
    /**
     * Combines two arrays into a single array.
     * 
     * @param a the first array
     * @param b the second array
     * @return the combined array
     */
    public int[] combine(int[] a, int[] b) {
        int[] result = new int[a.length + b.length];
        for (int i = 0; i < a.length; i++) {
            result[i] = a[i];
        }
        for (int i = 0; i < b.length; i++) {
            result[a.length] = b[i];
        }
        return result;
    }
}
