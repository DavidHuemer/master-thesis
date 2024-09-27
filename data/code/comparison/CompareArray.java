public class CompareArray {
    /**
    * Compares two arrays for equality. Two arrays are considered equal if they have the same length and contain the same elements in the same order.
    * @param a The first array
    * @param b The second array
    * @return true if the arrays are equal, false otherwise
    */
    public boolean compare(int[] a, int[] b) {
        if (a.length != b.length) {
            return false;
        }

        for (int i = 0; i < a.length; i++) {
            if (a[i] != b[i]) {
                return false;
            }
        }
        return true;
    }
}