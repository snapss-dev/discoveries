"""A092674: check a(n) = phi(n) - mu(n) + [n even]*mu(n/2) against the defining recursion.

Definition (OEIS): s(1) = x (an indeterminate) and, for n >= 2,
    s(n) = binomial(n+1, 2) - sum_{i=1}^{n-1} s(i) * floor(n/i);
a(n) is the constant term of s(n).  Each s(n) is linear in x, so it is stored as (constant, x-coefficient).
Run:  python check.py [N]      default N = 5000
"""
import sys
from sympy import totient, mobius

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
const = [0, 0]; coef = [0, 1]                    # index 1: s(1) = 0 + 1*x
for n in range(2, N + 1):
    c = n * (n + 1) // 2; k = 0
    for i in range(1, n):
        q = n // i
        c -= const[i] * q; k -= coef[i] * q
    const.append(c); coef.append(k)

bad = []
for n in range(1, N + 1):
    f = int(totient(n)) - int(mobius(n)) + (int(mobius(n // 2)) if n % 2 == 0 else 0)
    if f != const[n]: bad.append(n)
    assert const[n] >= 0
print("first terms:", const[1:21])
print(f"formula matches the recursion for 1 <= n <= {N}: {not bad}")
print("zeros at n =", [n for n in range(1, N + 1) if const[n] == 0])
