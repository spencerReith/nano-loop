# 4055. Count Shadow Pairs II (Hard)

You are given an integer array `nums` of length `n`.

A pair of indices `(i, j)` is called a **shadow pair** if all of the following conditions are satisfied:
- `0 <= i < j < n`
- `nums[i] < nums[j]`
- There **does not exist** an index `k` such that `i < k < j` and `nums[i] < nums[k] < nums[j]`.

Return the total number of **shadow pairs**.

**Example 1:**
- Input: `nums = [3,1,4,2,5]`
- Output: `5`
- Explanation: The shadow pairs are (0,2), (1,2), (1,3), (2,4), (3,4).

**Example 2:**
- Input: `nums = [6,7,8,9]`
- Output: `3`
- Explanation: The shadow pairs are (0,1), (1,2), (2,3).

**Constraints:**
- `3 <= n == nums.length <= 5 * 10^4`
- `1 <= nums[i] <= 10^9`
