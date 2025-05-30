public class TemperaturesIncorrect {
    /**
     * Convert a temperature in Celsius to Kelvin and Fahrenheit.
     * 
     * @param celsius the temperature in Celsius
     * @return an array containing the temperature in Celsius, Kelvin, and
     *         Fahrenheit
     */
    public double[] convertTemperature(double celsius) {
        return new double[] { celsius, celsius + 32.00, celsius * 1.80 + 32.00 };
    }
}
