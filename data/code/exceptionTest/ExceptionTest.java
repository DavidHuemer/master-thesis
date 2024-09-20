public class ExceptionTest {
    /**
    Returns the same integer as given. If the integer is greater than 10, throws an IllegalArgumentException.
    */
    public int test(int a) {
        if (a > 10){
            throw new IllegalArgumentException("a is too big");
        }

        return a;
    }
}