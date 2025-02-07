public class Dart {
    /**
     * Calculates the new score in a dart game after a throw. Remember, dart scores start at 501 and go down to 0.
     *
     * @param number       The number hit (1-20).
     * @param region       The region hit (1 for single, 2 for double, 3 for
     *                     triple).
     * @param currentScore The player's current score before the throw.
     * @return The new score after the throw, or the current score if the throw
     *         would result in a negative score.
     * @throws IllegalArgumentException if the number or region is invalid.
     */
    public static int calculateScore(int number, int region, int currentScore) {
        if (number < 1 || number > 20) {
            throw new IllegalArgumentException("Invalid number hit. Must be between 1 and 20.");
        }

        if (region < 1 || region > 3) {
            throw new IllegalArgumentException("Invalid region. Must be 1, 2, or 3.");
        }

        int throwScore = number * region;

        // Ensure the new score is not negative (Überfressen rule)
        return (currentScore - throwScore >= 0) ? currentScore - throwScore : currentScore;
    }
}
