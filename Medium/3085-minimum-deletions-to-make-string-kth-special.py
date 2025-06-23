"""
3085. Minimum Deletions to Make String K-Special

URL: https://leetcode.com/problems/minimum-deletions-to-make-string-k-special/

Tags: hash table, greedy, sorting, string, counting

Approach:
- Count the frequency of each character in the string.
- Sort the frequencies.
- For each frequency as a base (freq[i]), try to include as many higher frequencies
  as possible such that the difference is ≤ k.
- If a frequency is too big, truncate it down to (base + k) to minimize deletions.
- Track the max total kept, and subtract from original to find deletions.

Time: O(n^2), where n = number of unique characters (max 26)
Space: O(1), ignoring Counter and list (small fixed size)
"""

class Solution:
    def minimumDeletions(self, word: str, k: int) -> int:
        # Count character frequencies manually
        # (can be replaced with: freq = Counter(word))
        freq = {}
        for ch in word:
            freq[ch] = freq.get(ch, 0) + 1

        # Sort frequencies
        freq = sorted(freq.values())
        ans = len(word)

        for i in range(len(freq)):
            cnt = len(word)
            for j in range(i, len(freq)):
                # If within k-difference, subtract nothing extra
                # Else, subtract excess over (freq[i] + k)
                if freq[j] <= freq[i] + k:
                    cnt -= freq[j]
                else:
                    cnt -= freq[i] + k

            # Update minimum deletions found
            ans = min(ans, cnt)

        return ans
