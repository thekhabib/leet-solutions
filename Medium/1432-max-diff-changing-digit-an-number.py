"""
1432. Max Difference You Can Get From Changing an Integer

URL: https://leetcode.com/problems/max-difference-you-can-get-from-changing-an-integer/

Tags: math, greedy

Approach:
- Convert the number to a string for easy digit manipulation.
- To maximize the number, find the first digit that is not 9 and replace all its occurrences with 9.
- To minimize the number:
  - If the first digit is not 1, replace all its occurrences with 1.
  - Otherwise, find the first digit (after the first) that is not 0 and not equal to the first digit, and replace all its occurrences with 0.
- Compute the difference between the maximum and minimum variants.

Time: O(d), where d is the number of digits in the number.
Space: O(d), for storing the string representation of the number.
"""


class Solution:
    def maxDiff(self, num: int) -> int:
        s = str(num)

        # maximize
        max_value = num
        for d in s:
            if d != '9':
                max_value = int(s.replace(d, '9'))
                break

        # minimize
        min_value = num
        if s[0] != '1':
            min_value = int(s.replace(s[0], '1'))
        else:
            for d in s:
                if d != '0' and d != s[0]:
                    min_value = int(s.replace(d, '0'))
                    break

        return max_value - min_value