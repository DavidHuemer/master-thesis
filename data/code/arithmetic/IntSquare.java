public class IntSquare {

    /**
     * Calculates the square of an integer.
     * 
     * @param x the integer to square
     * @return the square of the integer
     */
    public int squareOf(int x) {
        if (x < 0)
            x = -x;
        int res = 0;
        for (int i = 0; i < x; i++) {
            for (int j = 0; j < x; j++) {
                res = res + 1;
            }
        }
        return res;
    }

}