# 4033. Valid K-Unique Subarrays I (Hard)

You are given an integer array `nums` and an integer `k`.

You are also given a 2D integer array `queries`, where `queries[i] = [l_i, r_i]` represents the **subarray** `nums[l_i..r_i]`.

For each query, the **subarray** `nums[l_i..r_i]` is considered **valid** if:

* It contains **exactly** `k` **distinct** numbers, and
* The **frequency** of every number in the **subarray** is **even**.

Return a boolean array `ans`, where `ans[i]` is `true` if `nums[l_i..r_i]` is **valid**, and `false` otherwise.

**Example 1:**

**Input:** nums = [1,2,2,1], k = 2, queries = [[0,1],[0,3],[1,2]]

**Output:** [false,true,false]

**Explanation:**

| `i` | `[l_i, r_i]` | Subarray | Unique numbers | Frequency | Validity check |
| --- | --- | --- | --- | --- | --- |
| 0 | [0, 1] | [1, 2] | {1, 2} → 2 | {1: 1, 2: 1} | `false`: Element counts are not even. |
| 1 | [0, 3] | [1, 2, 2, 1] | {1, 2} → 2 | {1: 2, 2: 2} | `true`: Exactly `k = 2` distinct elements, all appear an even number of times. |
| 2 | [1, 2] | [2, 2] | {2} → 1 | {2: 2} | `false`: Number of distinct elements is less than `k = 2`. |

Thus, `ans = [false, true, false]`.

**Example 2:**

**Input:** nums = [3,3,3], k = 1, queries = [[1,2],[0,2]]

**Output:** [true,false]

**Explanation:**

| `i` | `[l_i, r_i]` | Subarray | Unique numbers | Frequency | Validity check |
| --- | --- | --- | --- | --- | --- |
| 0 | [1, 2] | [3, 3] | {3} → 1 | {3: 2} | `true`: Exactly `k = 1` distinct element, appears an even number of times. |
| 1 | [0, 2] | [3, 3, 3] | {3} → 1 | {3: 3} | `false`: 3 does not appear an even number of times. |

Thus, `ans = [true, false]`.

**Constraints:**

* `2 <= n == nums.length <= 10^5`
* `1 <= nums[i] <= 10^5`
* `1 <= k <= n`
* `1 <= queries.length <= 10^5`
* `queries[i] == [l_i, r_i]`
* `0 <= l_i < r_i <= n - 1`

**Time limit:** 2s

```python
class Solution:
    def validSubarrays(self, nums: list[int], k: int, queries: list[list[int]]) -> list[bool]:
```
