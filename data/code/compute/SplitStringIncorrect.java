public class SplitStringIncorrect {
    /**
     * Splits a string into two parts at the specified index.
     * 
     * @param s     the string to split
     * @param index the index at which to split the string
     * @return an array containing the two parts of the split string
     */
    public String[] split(String s, int index) {
        String[] result = new String[2];
        result[0] = s.substring(0, index-1);
        result[1] = s.substring(index);
        return result;
    }
}
