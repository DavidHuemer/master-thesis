public class Withdraw{

    /**
     * Withdraws money from an account.
     * 
     * @param balance the current balance
     * @param amount the amount to withdraw
     * @return the new balance after the withdrawal
     * 
     * @throws IllegalArgumentException if the amount is negative
     * @throws IllegalArgumentException if the amount is greater than the balance
     * @throws IllegalArgumentException if the balance is negative
     * @throws IllegalArgumentException if the new balance is negative
     */
    public double withdraw(double balance, double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("Amount cannot be negative");
        }
        if (amount > balance) {
            throw new IllegalArgumentException("Amount cannot be greater than balance");
        }
        if (balance < 0) {
            throw new IllegalArgumentException("Balance cannot be negative");
        }
        double newBalance = balance - amount;
        if (newBalance < 0) {
            throw new IllegalArgumentException("New balance cannot be negative");
        }
        return newBalance;
    }
}