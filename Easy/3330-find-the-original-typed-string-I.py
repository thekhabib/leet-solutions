"""
3330. Find the Original Typed String I

URL: https://leetcode.com/problems/find-the-original-typed-string-i/

Tags: string, greedy

Approach:
- Iterate through the input string and group identical consecutive characters.
- For each group of length >= 2, we can remove 1 to (k-1) characters to simulate Alice releasing the key earlier.
- Since only one group can be affected, we sum (length - 1) for all groups and add 1 (for the original string with no changes).

Time: O(n), where n is the length of the string.
Space: O(1)
"""


class Solution:
    def possibleStringCount(self, word: str) -> int:
        ans = 1  # include the original string (no typo)
        current = word[0]
        cnt = 1

        for i in word[1:]:
            if current != i:
                ans += cnt - 1  # add possible shortenings for the previous group
                current = i
                cnt = 1
            else:
                cnt += 1  # same character group continues

        return ans + cnt - 1  # remember the last group