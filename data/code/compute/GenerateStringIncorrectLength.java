public class GenerateStringIncorrectLength {
    /**
     * Generates a String with the given length.
     * 
     * The generated string consists of repeating characters from 'a' to 'z'.
     * 
     * @param length The length of the generated string
     * 
     * @return The generated string
     */
    public String generateString(int length) {
        String str = "";
        for (int i = 0; i <= length; i++) {
            str += (char) ('a' + i % 26);
        }
        return str;
    }
}
