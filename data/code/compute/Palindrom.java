public class Palindrom {
    /**
     * Returns whether a string is a palindrom.
     * 
     * A palindrom is a string that reads the same forwards and backwards.
     * A empty string is considered a palindrom.
     * 
     * @param s the string to check
     * @return true if the string is a palindrom, false otherwise
     */
    public boolean isPalindrom(String s) {
        String reversed = "";
        for (int i = s.length() - 1; i >= 0; i--) {
            reversed += s.charAt(i);
        }
        return s.equals(reversed);
    }
}
