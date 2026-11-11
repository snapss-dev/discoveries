"""A036283(n) = denominator of (2^(2n-1) - 1) B_{2n} / n, against 6 * A202318(n), and the two values of
the A036283 b-file that disagree.
Run:  python check.py [N]        (N = 10000 takes a few minutes)
"""
import sys
from math import gcd

from flint import fmpq
from sympy import bernoulli, divisors, isprime

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000


def vp(n, p):
    v = 0
    while n % p == 0:
        n //= p
        v += 1
    return v


def a036283(n):
    b = fmpq.bernoulli(2 * n)
    num, den = (2 ** (2 * n - 1) - 1) * int(b.p), int(b.q) * n
    return den // gcd(num, den)


def a202318(n):
    """From the definition in the entry: exponents of 2 and 3 as in n; a prime p >= 5 appears, with
    exponent 1 + v_p(2n / (p - 1)), exactly when p - 1 divides 2n."""
    r = 2 ** vp(n, 2) * 3 ** vp(n, 3)
    for d in divisors(2 * n):
        p = d + 1
        if p >= 5 and isprime(p):
            r *= p ** (1 + vp(2 * n // (p - 1), p))
    return r


print("first terms:", [a036283(n) for n in range(1, 13)])
bad = [n for n in range(1, N + 1) if a036283(n) != 6 * a202318(n)]
print(f"A036283(n) = 6 * A202318(n) for every n <= {N}: {not bad}")

for n, in_bfile, extra in ((6951, 346793879715066, 331), (8308, 2162760, 67)):
    val = a036283(n)
    b = bernoulli(2 * n)                        # second implementation (mpmath)
    num, den = (2 ** (2 * n - 1) - 1) * int(b.p), int(b.q) * n
    val2 = den // gcd(num, den)
    print(f"n = {n}: computed {val} (FLINT), {val2} (sympy); 6 * A202318 = {6 * a202318(n)}; "
          f"b-file has {in_bfile} = {in_bfile // val} * computed")
    print(f"   {extra} divides n: {n % extra == 0}; {extra} - 1 divides 2n: {2 * n % (extra - 1) == 0}; "
          f"{extra} divides the numerator of B_2n: {int(fmpq.bernoulli(2 * n).p) % extra == 0}")
