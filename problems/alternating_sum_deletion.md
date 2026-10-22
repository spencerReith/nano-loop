# 4072. Maximum Alternating Subarray Sum With One Deletion (Medium)

You are given an integer array `nums`.

You may delete **at most one** element from `nums`, then choose a non-empty **subarray** of the resulting array.

Return the **maximum** possible **alternating sum** of the chosen subarray.

The **alternating sum** of an array is the sum of its elements at even indices minus the sum of its elements at odd indices. The chosen subarray is **reindexed starting from 0** before calculating its alternating sum.

**Example 1:**
- Input: `nums = [5,-5,1]`
- Output: `11`
- Explanation: No deletion, take the whole array: `5 - (-5) + 1 = 11`.

**Example 2:**
- Input: `nums = [10,-5,-100]`
- Output: `110`
- Explanation: Delete `-5` → `[10,-100]`, then `10 - (-100) = 110`.

**Example 3:**
- Input: `nums = [4,7]`
- Output: `7`
- Explanation: No deletion, take subarray `[7]`.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `-10^5 <= nums[i] <= 10^5`
