public class CreditCard {
    public double balance;

    public CreditCard(double balance) {
        this.balance = balance;
    }

    public CreditCard() {
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
        balance += amount;
    }
}
