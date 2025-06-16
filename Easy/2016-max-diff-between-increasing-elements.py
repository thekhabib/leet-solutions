"""
2016. Maximum Difference Between Increasing Elements

URL: https://leetcode.com/problems/maximum-difference-between-increasing-elements/

Tags: array, greedy

Approach:
- Initialize `min_value` with the first element of the array.
- Traverse the array from the second element:
  - If current element > min_value, calculate the difference and update max_diff.
  - Else, update `min_value` to current element.
- If no such i, j found, return -1.

Time: O(n), where n is the number of elements in the array.
Space: O(1), constant extra space is used.
"""

from typing import List


class Solution:
    def maximumDifference(self, nums: List[int]) -> int:
        min_value = nums[0]
        max_diff = -1

        for i in range(1, len(nums)):
            if nums[i] > min_value:
                max_diff = max(max_diff, nums[i] - min_value)
            else:
                min_value = nums[i]

        return max_diff
