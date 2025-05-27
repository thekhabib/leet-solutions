"""
2150. Find All Lonely Numbers in the Array

URL: https://leetcode.com/problems/find-all-lonely-numbers-in-the-array/

Tags: arrays, hash table, counting

Approach:
- Use a hash table (Counter) to count the frequency of each number.
- Iterate through the list and check for each number:
  - It appears exactly once.
  - Neither its predecessor (num - 1) nor its successor (num + 1) is present.

Time: O(n), where n is the number of elements in the input list.
Space: O(n), for storing the frequency count of elements.
"""

from typing import List
from collections import Counter

class Solution:
    def findLonely(self, nums: List[int]) -> List[int]:
        freq = Counter(nums)
        res = []
        
        for num in nums:
            if freq[num] == 1 and freq.get(num - 1, 0) + freq.get(num + 1, 0) == 0:
                res.append(num)
        
        return res