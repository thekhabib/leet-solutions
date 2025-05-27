"""
2942. Find Words Containing Character

URL: https://leetcode.com/problems/find-words-containing-character/

Tags: string, array

Approach:
- Iterate through each word in the list.
- Check if the character `x` is present in the word.
- If yes, include the index in the result list.

Time: O(n*m), where n = number of words, m = average length of a word
Space: O(1), excluding output list
"""

from typing import List

class Solution:
    def findWordsContaining(self, words: List[str], x: str) -> List[int]:
        return [i for i, word in enumerate(words) if x in word]
