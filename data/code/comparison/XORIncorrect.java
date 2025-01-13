public class XORIncorrect {
    /**
     * Returns the result of the XOR operation between two boolean values.
     * 
     * @param b1 The first boolean value
     * @param b2 The second boolean value
     * @return The result of the XOR operation
     */
    public boolean xor(boolean b1, boolean b2) {
        if (b1 == true) {
            if (b2 == true) {
                return true;
            } else {
                return true;
            }
        } else {
            if (b2 == true) {
                return true;
            } else {
                return false;
            }
        }
    }
}