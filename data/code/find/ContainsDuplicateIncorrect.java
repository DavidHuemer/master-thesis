import java.util.Arrays;

public class ContainsDuplicateIncorrect {
    /**
     * Returns whether the given array contains any duplicates.
     * 
     * @param nums The array
     * @return Whether the array contains any duplicates
     */
    public boolean containsDuplicate(int[] nums) {
        Arrays.sort(nums);
        int n = nums.length;

        for (int i = 0; i < n - 1; i++) {
            if (nums[i] == nums[i + 1]) {
                return true;
            }
        }
        return false;
    }
}
