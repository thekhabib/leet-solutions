"""
2081. Sum of k-Mirror Numbers

URL: https://leetcode.com/problems/sum-of-k-mirror-numbers/

Tags: math,enumeration, base-conversion, backtracking

Approach:
- Generate palindromes in base 10, starting from 1-digit numbers and increasing their length.
- For each palindrome, check if it is also a palindrome in base `k` using math-based conversion.
- Accumulate such numbers until we collect `n` of them and return their total sum.

Time: O(T * log N), where T = number of palindromes tested, N = current number value
Space: O(1), excluding output and generator stack
"""

class Solution:
    def kMirror(self, k: int, n: int) -> int:

        # Check if a number is a palindrome in base-k
        def is_k_palindrome(x: int) -> bool:
            original = x
            reversed_k = 0
            while x > 0:
                reversed_k = reversed_k * k + x % k
                x //= k
            return original == reversed_k

        # Generate all base-10 palindromes in increasing length
        def generate_palindromes():
            yield from range(1, 10)  # 1-digit palindromes

            length = 2
            while True:
                half = length // 2
                start = 10 ** (half - 1)
                end = 10 ** half

                for i in range(start, end):
                    s = str(i)
                    if length % 2:
                        # Odd-length palindromes: s + m + reverse(s)
                        for m in range(10):
                            yield int(s + str(m) + s[::-1])
                    else:
                        # Even-length palindromes: s + reverse(s)
                        yield int(s + s[::-1])

                length += 1

        total = count = 0
        for num in generate_palindromes():
            if is_k_palindrome(num):
                total += num
                count += 1
                if count == n:
                    break

        return total