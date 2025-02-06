public class RangeCheckIncorrect {
    /**
     * Checks that {@code fromIndex} and {@code toIndex} are in
     * the range and throws an exception if they aren't.
     * 
     * @param arrayLength the length of the array
     * @param fromIndex   the start index of the range
     * @param toIndex     the end index of the range
     * 
     * @throws IllegalArgumentException       if {@code fromIndex} > {@code toIndex}
     * @throws ArrayIndexOutOfBoundsException if {@code fromIndex} < 0 or
     *                                        {@code toIndex} > {@code arrayLength}
     */
    void rangeCheck(int arrayLength, int fromIndex, int toIndex) {
        if (fromIndex > toIndex) {
            throw new IllegalArgumentException(
                    "fromIndex(" + fromIndex + ") > toIndex(" + toIndex + ")");
        }
        if (fromIndex < 2) {
            throw new ArrayIndexOutOfBoundsException(fromIndex);
        }
        if (toIndex > arrayLength) {
            throw new ArrayIndexOutOfBoundsException(toIndex);
        }
    }
}
