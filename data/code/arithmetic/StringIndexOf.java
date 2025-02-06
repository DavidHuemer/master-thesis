public class StringIndexOf {
    /**
     * Returns the index of the first occurrence of character in a string.
     * 
     * If the character is not found in the string, the method returns -1.
     * 
     * @param s   the string to search
     * @param sub the character to search for
     * @return the index of the first occurrence of the substring in the string
     */
    public int indexOf(String s, char sub) {
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == sub) {
                return i;
            }
        }
        return -1;
    }
}
