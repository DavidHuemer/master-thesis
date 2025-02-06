public class Temperatures {
    /**
     * Convert a temperature in Celsius to Kelvin and Fahrenheit.
     * 
     * @param celsius the temperature in Celsius
     * @return an array containing the temperature in Celsius, Kelvin, and
     *         Fahrenheit
     * @throws IllegalArgumentException if the temperature is less than -273.15
     */
    public double[] convertTemperature(double celsius) {
        if (celsius < -273.15) {
            throw new IllegalArgumentException("Temperature must be greater than or equal to -273.15 degrees Celsius.");
        }

        return new double[] { celsius, celsius + 273.15, celsius * 1.80 + 32.00 };
    }
}
