"""A121860: a(n) = sum_{d|n} n!/(d! (n/d)!).  Checks a(n) == 2 (mod k) for all n >= (k+2)^2.
Run:  python check.py [N] [K]      default N = 2000, K = 40
"""
import sys
from math import factorial
from sympy import divisors
N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
K = int(sys.argv[2]) if len(sys.argv) > 2 else 40
fact = [factorial(i) for i in range(N + 1)]
a = [None] + [sum(fact[n] // (fact[d] * fact[n // d]) for d in divisors(n)) for n in range(1, N + 1)]
print("a(1..8) =", a[1:9], "(entry: 1, 2, 2, 8, 2, 122, 2, 1682)")
# the divisibility used in the proof: each middle term is divisible by (n - d - n/d)!
ok = all((fact[n] // (fact[d] * fact[n // d])) % fact[n - d - n // d] == 0
         for n in range(4, min(N, 600) + 1) for d in divisors(n) if 1 < d < n)
print("every middle term divisible by (n - d - n/d)! for n <= 600:", ok)
print(f"a(n) == 2 (mod k) for all 3 <= k <= {K} and (k+2)^2 <= n <= {N}:",
      all(a[n] % k == 2 % k for k in range(3, K + 1) for n in range((k + 2)**2, N + 1)))
last = {k: max([n for n in range(1, N + 1) if a[n] % k != 2 % k] or [0]) for k in (3, 11, 37)}
print("last n with a(n) != 2 (mod k), for k = 3, 11, 37:", last, "(the bound (k+2)^2 is far from sharp)")
