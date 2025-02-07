public class SubstringIncorrect {
    /**
     * Returns a substring of a string.
     * 
     * The substring starts at the specified start index and extends to the
     * character at index end - 1.
     * 
     * @param s     the string to extract the substring from
     * @param start the starting index of the substring
     * @param end   the ending index of the substring
     * @return the substring
     * 
     * @throws IndexOutOfBoundsException if start is negative or end is greater than
     *                                   the length of the string
     * @throws IllegalArgumentException  if start is greater than end
     */
    public String substring(String s, int start, int end) {
        if (start < 0 || end > s.length()) {
            throw new IndexOutOfBoundsException();
        }

        if (start > end) {
            throw new IllegalArgumentException("start must be less than or equal to end");
        }

        String sub = "";
        for (int i = start; i < end - 1; i++) {
            sub += s.charAt(i);
        }
        return sub;
    }
}
