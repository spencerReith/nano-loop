# 4066. Maximum Equal Adjacent Pairs After at Most One Replacement (Medium)

You are given a **1-indexed** integer array `nums`.

You can choose two **distinct** values `x` and `y` and perform the following operation **at most** once:

- Replace every occurrence of `x` in `nums` with `y`.

Return the **maximum** possible number of pairs of adjacent elements that are equal after performing the operation.

**Example 1:**

**Input:** nums = [1,2,3,2]

**Output:** 2

**Explanation:**

- One optimal solution is to choose `x = 3` and `y = 2`.
- The resulting array is `[1, 2, 2, 2]`.
- There are 2 pairs of adjacent elements that are equal: `(nums[2], nums[3])` and `(nums[3], nums[4])`.
- Therefore, the answer is 2.

**Example 2:**

**Input:** nums = [1,2,1,2,1]

**Output:** 4

**Explanation:**

- One optimal solution is to choose `x = 1` and `y = 2`.
- The resulting array is `[2, 2, 2, 2, 2]`.
- There are 4 pairs of adjacent elements that are equal: `(nums[1], nums[2])`, `(nums[2], nums[3])`, `(nums[3], nums[4])`, and `(nums[4], nums[5])`.
- Therefore, the answer is 4.

**Example 3:**

**Input:** nums = [1,1,1]

**Output:** 2

**Explanation:**

- One optimal solution is to perform no operation.
- Thus, the resulting array is `[1, 1, 1]`.
- There are 2 pairs of adjacent elements that are equal: `(nums[1], nums[2])` and `(nums[2], nums[3])`.
- Therefore, the answer is 2.

**Constraints:**

- `2 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
