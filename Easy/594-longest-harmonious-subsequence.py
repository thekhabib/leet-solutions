"""
594. Longest Harmonious Subsequence

URL: https://leetcode.com/problems/longest-harmonious-subsequence/

Tags: array, hash table, sliding window, sorting, counting

Approach:
- Count the frequency of each number using Counter.
- For each number, check if `num + 1` exists in the map.
- If it exists, the length of the harmonious subsequence is freq[num] + freq[num + 1].
- Keep track of the maximum such length.

Time: O(n), where n is the number of elements in the input list.
Space: O(n), for storing the frequency map.
"""

from typing import List
import collections

class Solution:
    def findLHS(self, nums: List[int]) -> int:
        freq = collections.Counter(nums)  # Count frequency of each number
        res = 0

        for num in freq:
            if num + 1 in freq:
                # Check for a valid harmonious pair (num, num + 1)
                res = max(res, freq[num] + freq[num + 1])

        return res  # Length of the longest harmonious subsequence
