# 4022. K-th Digit in Infinite String (Medium)

You are given an integer `k`.

An **infinite** string is formed by **concatenating** the **decimal** representations of the **positive** integers, without separators.

For every nonnegative integer `b`, block `b` contains the **positive** integers from `10 * b` through `10 * b + 9`. The integers in each block are appended as follows:

- If `b` is even, append the integers in **increasing** order.
- If `b` is odd, append the integers in **decreasing** order.

Therefore, the string starts with the integers 1 through 9, followed by 19 through 10, then 20 through 29, then 39 through 30, and so on.

Return the `k^th` digit (1-indexed) of this string.

**Example 1:**

**Input:** k = 4

**Output:** 4

**Explanation:**

The string begins as `"123456789.."`. The 4^th digit is `'4'`.

**Example 2:**

**Input:** k = 15

**Output:** 7

**Explanation:**

The string begins as `"123456789191817.."`. The 15^th digit is `'7'`.

**Example 3:**

**Input:** k = 11

**Output:** 9

**Explanation:**

The string begins as `"12345678919.."`. The 11^th digit is `'9'`.

**Constraints:**

- `1 <= k <= 10^15`

**Time limit:** 2s

```python
class Solution:
    def kthDigit(self, k: int) -> int:
```
