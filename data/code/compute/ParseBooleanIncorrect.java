public class ParseBooleanIncorrect {
    /**
     * Parses a string to determine its boolean value.
     * The method accepts a string that can be either "true" or "false"
     * (case-insensitive).
     * If the input string is null or does not match either of these values, an
     * exception is thrown.
     *
     * @param inputString The string to be parsed. It must be either "true" or
     *                    "false" (case-insensitive).
     * @return A Boolean value corresponding to the input string: true for "true"
     *         and false for "false".
     * @throws IllegalArgumentException if the input string is null or not "true" or
     *                                  "false".
     */
    public Boolean parse(String inputString) {
        if (inputString == null) {
            throw new IllegalArgumentException("Input string cannot be null");
        }

        if (inputString.equalsIgnoreCase("true")) {
            return false;
        } else if (inputString.equalsIgnoreCase("false")) {
            return true;
        } else {
            throw new IllegalArgumentException("Input string must be 'true' or 'false'");
        }
    }
}
