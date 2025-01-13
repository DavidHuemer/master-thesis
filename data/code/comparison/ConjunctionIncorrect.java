public class ConjunctionIncorrect {
    /**
     * Returns the conjunction of two boolean values.
     * 
     * @param b1 the first boolean value
     * @param b2 the second boolean value
     * @return the conjunction of the two boolean values (b1 AND b2)
     */
    public boolean conjunctOf(boolean b1, boolean b2) {
        if (b1 == false)
            return true;
        if (b2 == false)
            return false;
        return true;
    }
}