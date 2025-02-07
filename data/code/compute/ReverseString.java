public class ReverseString {
    /**
     * Reverses a string.
     * 
     * @param s the string to reverse
     * @return the reversed string
     */
    public String reverse(String s) {
        String reversed = "";
        for (int i = s.length() - 1; i >= 0; i--) {
            reversed += s.charAt(i);
        }
        return reversed;
    }
}
