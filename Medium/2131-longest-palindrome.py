"""
2131. Longest Palindrome by Concatenating Two Letter Words

#tag: hashmap, palindrome, string, greedy

Approach:
- Count frequency of all words
- Match reverse words
- Handle center palindromes

Time: O(n)
Space: O(n)
"""

class Solution:
    def longestPalindrome(self, words: List[str]) -> int:

        freq = {}
        for word in words:
            freq[word] = freq.get(word, 0) + 1
        
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
