public class LeapYear {
    /**
     * Returns whether a year is a leap year.
     * 
     * @param year the year to check
     * @return true if the year is a leap year, false otherwise
     */
    public boolean isLeapYear(int year) {
        if (year % 4 == 0) {
            if (year % 100 == 0) {
                return year % 400 == 0;
            }
            return true;
        }
        return false;
    }
}
