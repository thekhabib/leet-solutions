"""
2566. Maximum Difference by Remapping a Digit

URL: https://leetcode.com/problems/maximum-difference-by-remapping-a-digit/

Tags: math, greedy, string manipulation

Approach:
- Convert the number to string for digit manipulation.
- To get the maximum value:
  - Find the first digit that is not '9' and replace all its occurrences with '9'.
- To get the minimum value:
  - Replace all occurrences of the first digit with '0'.
- Return the difference between the maximum and minimum values.

Time: O(d), where d is the number of digits in the number.
Space: O(d), due to string operations.
"""


class Solution:
    def minMaxDifference(self, num: int) -> int:
        s = str(num)

        max_value = num
        for d in s:
            if d != '9':
                max_value = int(s.replace(d, '9'))
                break

        min_value = int(s.replace(s[0], '0'))

        return max_value - min_value
