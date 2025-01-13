public class DisjunctionIncorrect {
    /**
     * Returns the disjunction of two boolean values.
     * 
     * @param b1 The first boolean value
     * @param b2 The second boolean value
     * @return The disjunction of the two values
     */
    public boolean disjunctOf(boolean b1, boolean b2) {
        if (b1 == true)
            return false;
        if (b2 == true)
            return true;
        return false;
    }
}
