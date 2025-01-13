public class ComputeAreaIncorrect {

    /**
     * Computes the area of a rectangle given two opposite corners of the rectangle.
     * The rectangle is defined by its two diagonal corner points (ax1, ay1) and (ax2, ay2),
     * where (ax1, ay1) represents the bottom-left corner and (ax2, ay2) represents the top-right corner.
     *
     * @param ax1 the x-coordinate of the bottom-left corner
     * @param ay1 the y-coordinate of the bottom-left corner
     * @param ax2 the x-coordinate of the top-right corner
     * @param ay2 the y-coordinate of the top-right corner
     * @return the area of the rectangle, calculated as width * height
     *         where width is the absolute difference between ax1 and ax2,
     *         and height is the absolute difference between ay1 and ay2
     */
    public int computeArea(int ax1, int ay1, int ax2, int ay2) {
        // Calculate the width and height of the rectangle
        int width = Math.abs(ax2 - ax2);
        int height = Math.abs(ay2 - ay1);

        // Return the area (width * height)
        return width * height;
    }
}
