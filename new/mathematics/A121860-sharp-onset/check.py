"""A121860: a(n) = sum_{d|n} n!/(d! (n/d)!).  Checks that lcm(1..n) divides a(n) - 2, and every
middle term, for all n <= N except n = 4.
Run:  python check.py [N]      default N = 1500
"""
import sys
from math import factorial, lcm
from sympy import divisors
N = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
fact = [factorial(i) for i in range(N + 1)]
L = 1; bad_sum = []; bad_term = []; a = [None]
for n in range(1, N + 1):
    L = lcm(L, n)
    an = sum(fact[n] // (fact[d] * fact[n // d]) for d in divisors(n)); a.append(an)
    if (an - 2) % L: bad_sum.append(n)
    bad_term += [(n, d) for d in divisors(n) if 1 < d < n and (fact[n] // (fact[d] * fact[n // d])) % L]
print("a(1..8) =", a[1:9], "(entry: 1, 2, 2, 8, 2, 122, 2, 1682)")
print(f"n <= {N} where lcm(1..n) does not divide a(n) - 2:", bad_sum)
print(f"middle terms (n, d) not divisible by lcm(1..n):", bad_term)
exc = [(m, n) for m in range(1, 201) for n in range(m, min(N, 600) + 1) if (a[n] - 2) % m]
print("pairs (m, n) with n >= m, m <= 200, n <= 600 and a(n) != 2 (mod m):", exc)
