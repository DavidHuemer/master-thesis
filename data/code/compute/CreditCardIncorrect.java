public class CreditCardIncorrect {
    public double balance;

    public CreditCardIncorrect(double balance) {
        this.balance = balance;
    }

    public CreditCardIncorrect() {
        this(0.0);
    }

    /**
     * Charges the given amount to the credit card.
     * 
     * It updates the balance
     * 
     * @param amount The amount to charge
     */
    public void charge(double amount) {
        balance += amount + 1;
    }
}
