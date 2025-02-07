public class CopyOfRange {
    /**
     * Copies the specified range of the specified array into a new array.
     * The initial index of the range ({@code from}) must lie between zero
     * and {@code original.length}, inclusive. The value at
     * {@code original[from]} is placed into the initial element of the copy
     * (unless {@code from == original.length} or {@code from == to}).
     * Values from subsequent elements in the original array are placed into
     * subsequent elements in the copy. The final index of the range
     * ({@code to}), which must be greater than or equal to {@code from},
     * may be greater than {@code original.length}, in which case
     * {@code 0} is placed in all elements of the copy whose index is
     * greater than or equal to {@code original.length - from}. The length
     * of the returned array will be {@code to - from}.
     *
     * @param original the array from which a range is to be copied
     * @param from     the initial index of the range to be copied, inclusive
     * @param to       the final index of the range to be copied, exclusive.
     *                 (This index may lie outside the array.)
     * @return a new array containing the specified range from the original array,
     *         truncated or padded with zeros to obtain the required length
     * @throws ArrayIndexOutOfBoundsException if {@code from < 0}
     *                                        or {@code from > original.length}
     * @throws IllegalArgumentException       if {@code from > to}
     * @since 1.6
     */
    public static int[] copyOfRange(int[] original, int from, int to) {
        if (from == 0 && to == original.length) {
            return original.clone();
        }
        int newLength = to - from;
        if (newLength < 0) {
            throw new IllegalArgumentException(from + " > " + to);
        }
        int[] copy = new int[newLength];
        System.arraycopy(original, from, copy, 0,
                Math.min(original.length - from, newLength));
        return copy;
    }
}