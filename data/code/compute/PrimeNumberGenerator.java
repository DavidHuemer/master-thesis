public class PrimeNumberGenerator {
    /**
     * Generates an array of prime numbers up to the given number.
     * 
     * It uses the isPrime method to check if a number is prime.
     * 
     * @param n the number up to which to generate primes
     * @return an array of prime numbers
     * 
     * @throws IllegalArgumentException if n is greater than 20 or less than 0
     */
    public int[] generatePrimes(int n) {
        if (n > 20 || n < 0) {
            throw new IllegalArgumentException("n must be less than or equal to 20");
        }

        int[] primes = new int[n];
        int count = 0;
        for (int i = 2; i < n; i++) {
            if (isPrime(i)) {
                primes[count++] = i;
            }
        }

        int[] result = new int[count];
        for (int i = 0; i < count; i++) {
            result[i] = primes[i];
        }

        return result;
    }

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
