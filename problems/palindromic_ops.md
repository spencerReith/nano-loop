# 4053. Minimum Operations to Make Every Element Palindromic (Medium)

You are given an integer array `nums`.

In one **operation**, you may choose an index `i` and either increment or decrement `nums[i]` by 2.

Return the **minimum** number of operations required to make every element in `nums` a **positive** palindrome. Different elements may be changed into different palindromic integers.

**Example 1:**
- Input: `nums = [10,12,14,16]`
- Output: `9`
- Explanation: 10→8 (1 op), 12→8 (2 ops), 14→8 (3 ops), 16→22 (3 ops). Total = 9.

**Example 2:**
- Input: `nums = [9,10,11,10]`
- Output: `2`
- Explanation: Decrement `nums[1]` and `nums[3]` by 2 once each → `[9, 8, 11, 8]`.

**Example 3:**
- Input: `nums = [125]`
- Output: `2`
- Explanation: 125→121 takes 2 ops. 123 and 127 are not palindromes.

**Constraints:**
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
