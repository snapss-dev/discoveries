"""A123855: a(n) = Sum_{j=1..n} Sum_{i=1..n} prime(i)^j. Check that 2^k divides a(2^k - 1).
Run:  python check.py [kmax]
"""
import sys
from sympy import prime, primerange

K = int(sys.argv[1]) if len(sys.argv) > 1 else 13


def a(n):
    """Exact value: for each of the first n primes q, q + q^2 + ... + q^n = q (q^n - 1) / (q - 1)."""
    return sum(q * (q ** n - 1) // (q - 1) for q in primerange(2, prime(n) + 1))


print("first terms:", [a(n) for n in range(1, 7)])
for k in range(1, K + 1):
    n = 2 ** k - 1
    v = a(n)
    two = (v & -v).bit_length() - 1
    print(f"k = {k:2d}  n = {n:5d}  2-adic valuation of a(n) = {two:2d}  2^k divides a(n): {v % 2 ** k == 0}")
