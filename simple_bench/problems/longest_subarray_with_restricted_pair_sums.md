# 4067. Longest Subarray With Restricted Pair Sums (Medium)

You are given an integer array `nums`.

A **subarray** `nums[l..r]` is valid if there are no three **distinct** indices `i`, `j`, and `k` such that `l <= i, j, k <= r` and:

* `nums[i] + nums[j] == nums[k]`

Return the **maximum** length of a valid subarray of `nums`.

**Example 1:**

**Input:** nums = [2,3,5,3,2,1]

**Output:** 3

**Explanation:**

Consider the subarray `[3, 5, 3]`. The pairs of elements at distinct indices have the following sums:

* `3 + 5 = 8`
* `3 + 3 = 6`, using the two different occurrences of 3
* `5 + 3 = 8`

None of these sums is an element at the remaining index, so the subarray is valid.

Every subarray of length 4 contains 2, 3, and 5 at distinct indices, where `2 + 3 = 5`. Therefore, no longer valid subarray exists, and the answer is 3.

**Example 2:**

**Input:** nums = [3,4,5,6]

**Output:** 4

**Explanation:**

The sums obtained from every pair of elements at distinct indices are 7, 8, 9, 9, 10, and 11. None of these values appears at the remaining index, so the entire array is valid.

**Constraints:**

* `1 <= nums.length <= 1000`
* `1 <= nums[i] <= 500`

**Time limit:** 2s

```python
class Solution:
    def maxSubarray(self, nums: list[int]) -> int:
```
