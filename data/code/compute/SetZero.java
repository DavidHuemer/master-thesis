public class SetZero {

	/**
	 * Returns a new array where the elements of the array a from index iBegin to
	 * index iEnd are set to zero. The original array is not modified.
	 * 
	 * @param a      The array to modify
	 * @param iBegin The index of the first element to set to zero
	 * @param iEnd   The index of the last element to set to zero
	 * @return The modified array
	 */
	public int[] setZero(int[] a, int iBegin, int iEnd) {
		int[] b = new int[a.length];
		int k = iBegin;

		for (int i = 0; i < a.length; i++) {
			b[i] = a[i];
		}

		while (k <= iEnd) {
			b[k] = 0;
			k = k + 1;
		}

		return b;
	}
}