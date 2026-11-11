"""A006579(n) = Sum_{k=1..n-1} gcd(n, k) at Varun Vejalla's number n = 3 * 37 * 43 * 42307 * 116341.
Run:  python check.py
"""
from math import gcd
from sympy import divisors, factorint, isprime, totient


def a(n):
    return sum((d - 1) * totient(n // d) for d in divisors(n))


def a_multiplicative(n):
    """Second route: Pillai's function is multiplicative, P(p^e) = p^(e-1) ((p - 1) e + p); a(n) = P(n) - n."""
    r = 1
    for p, e in factorint(n).items():
        r *= p ** (e - 1) * ((p - 1) * e + p)
    return r - n


print("definition agrees with both formulas for n <= 400:",
      all(sum(gcd(n, k) for k in range(1, n)) == a(n) == a_multiplicative(n) for n in range(1, 401)))
n = 3 * 37 * 43 * 42307 * 116341
print("n =", n, "composite:", not isprime(n))
print("a(n) =", a(n), "=", a_multiplicative(n))
print("(a(n) + 1) / n =", (a(n) + 1) // n, "remainder", (a(n) + 1) % n)
print("composite n <= 200000 with a(n) = -1 (mod n):",
      [m for m in range(4, 200001) if not isprime(m) and (a_multiplicative(m) + 1) % m == 0])
