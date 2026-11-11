"""A000846 and A051924 at n = p^2 for the Wolstenholme prime p = 16843: the congruences modulo p^4 that
the argument needs, with exact binomial coefficients, plus small-n checks of both remarks.
Run:  python check.py
"""
from math import comb
from sympy import isprime

for p in (16843, 16831, 10007):
    M = p ** 4
    c2, c3 = comb(2 * p, p) % M, comb(3 * p, p) % M
    print(f"p = {p}: C(2p,p) mod p^4 = {c2}, C(3p,p) mod p^4 = {c3}  ->  "
          f"{'Wolstenholme: both remarks fail at n = p^2' if (c2, c3) == (2, 3) else 'ordinary prime'}")

A846 = lambda n: comb(3 * n, n) - comb(2 * n, n)
A924 = lambda n: comb(2 * n, n) - comb(2 * n - 2, n - 1)
print("A000846, composite n <= 600 with a(n) == 1 (mod n^2):",
      [n for n in range(2, 601) if A846(n) % (n * n) == 1 and not isprime(n)])
print("A051924, n <= 600 that are not odd primes with a(n) mod n^2 == n + 2:",
      [n for n in range(3, 601) if A924(n) % (n * n) == n + 2 and not isprime(n)])
n = 16843 ** 2
print("n = 16843^2 =", n, "| (3n-2)/(2n-1) mod n^2 == n + 2:", (3 * n - 2) * pow(2 * n - 1, -1, n * n) % (n * n) == n + 2)
