"""
2131. Longest Palindrome by Concatenating Two Letter Words

URL: https://leetcode.com/problems/longest-palindrome-by-concatenating-two-letter-words/

#tags: hashmap, palindrome, string, greedy

Approach:
- Count the frequency of each two-letter word using a hash map.
- For each word, try to pair it with its reverse (e.g., 'ab' with 'ba').
- Special handling for palindromic words like 'aa', 'bb', etc. — keep one in the center if there's an odd count.

Time: O(n), we iterate over the list once and then over the unique words (which is at most 676, i.e., 26*26).
Space: O(n), for storing word frequencies in a hash map.
"""

from typing import List
from collections import Counter

class Solution:
    def longestPalindrome(self, words: List[str]) -> int:

        freq = Counter(words)
        pairs = 0
        central = 0

        for word, cnt in freq.items():
            reserved_word = word[::-1]

            if word == reserved_word:
                pairs += cnt // 2
                if cnt % 2:
                    central = 1
            else:
                if reserved_word in freq and reserved_word < word:
                    pairs += min(cnt, freq[reserved_word])

        return pairs * 4 + central * 2
