public class BiggestIncorrect {
    /**
    Returns the biggest element in the given array.
    If the array is empty, returns -1.
    */
    public int biggest(int[] a) {
        if (a.length == 0) return -1;

        int biggest = a[0];

        for (int i = 1; i < a.length; i++) {
            if (a[i] > biggest) {
                biggest = i;
            }
        }

        return biggest;
    }
}