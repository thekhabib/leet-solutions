"""
2894. Divisible and Non-divisible Sums Difference

URL: https://leetcode.com/problems/divisible-and-non-divisible-sums-difference/

Tags: math

Approach:
- Calculate the sum from 1 to n using arithmetic sum formula.
- Calculate the sum of numbers divisible by m using the formula for an arithmetic progression.
- Return the difference between the total sum and twice the divisible sum.

Time: O(1), constant time arithmetic operations only.
Space: O(1), uses only constant space.
"""

class Solution:
    def differenceOfSums(self, n: int, m: int) -> int:
        cnt = n // m
        return n * (n + 1) // 2 - m * cnt * (cnt + 1) // 2
