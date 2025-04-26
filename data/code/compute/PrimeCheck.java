public class PrimeCheck {
    /**
     * Checks if a number is prime.
     * 
     * @param n the number to check
     * @return true if the number is prime, false otherwise
     */
    public boolean isPrime(int n) {
        if (n <= 1) {
            return false;
        }
        for (int i = 2; i < n; i++) {
            if (n % i == 0) {
                return false;
            }
        }
        return true;
    }
}
