"""
2150. Find All Lonely Numbers in the Array

url: https://leetcode.com/problems/find-all-lonely-numbers-in-the-array/

#tags: arrays, hash table, counting

Approach:
1. Count number frequencies
2. Check for each number:
   - Appears exactly once
   - No adjacent numbers (x-1, x+1) exist

Time: O(n)
Space: O(n)
"""

class Solution:
    def findLonely(self, nums: List[int]) -> List[int]:
        res = []
        freq = {}

        for num in nums:
            freq[num] = freq.get(num, 0) + 1
        
        for num in nums:
            if freq[num] == 1 and freq.get(num - 1, 0) + freq.get(num + 1, 0) == 0:
                res.append(num)
        
        return res