"""A338857: a(n) = k + 1 where k is minimal with sum_{j=n..k} 1/(2j+1) >= 1.
The formula printed in the entry, ceiling(n e^2 + (e^2 + e^-2)/(24n)), against the same formula with a
minus sign, ceiling(n e^2 + (e^2 - e^-2)/(24n)).
Uses sum_{j=n..k} 1/(2j+1) = (psi(k + 3/2) - psi(n + 1/2)) / 2 with mpmath at 150 digits.
Run:  python check.py
"""
from fractions import Fraction
import mpmath as mp
mp.mp.dps = 150
E2 = mp.e ** 2

def a(n):
    f = lambda k: (mp.digamma(mp.mpf(k) + mp.mpf(3) / 2) - mp.digamma(mp.mpf(n) + mp.mpf(1) / 2)) / 2
    k = int(mp.floor(n * E2)) - 3
    while f(k) < 1: k += 1
    assert f(k - 1) < 1 <= f(k)
    return k + 1
def a_exact(n):
    s = Fraction(0); k = n
    while True:
        s += Fraction(1, 2 * k + 1)
        if s >= 1: return k + 1
        k += 1
printed = lambda n: int(mp.ceil(n * E2 + (E2 + 1 / E2) / (24 * n)))
minus = lambda n: int(mp.ceil(n * E2 + (E2 - 1 / E2) / (24 * n)))

print("a(1..8) =", [a_exact(n) for n in range(1, 9)], "(entry: 8, 15, 23, 30, 38, 45, 52, 60)")
print("digamma method = exact rational sum for n <= 400:", all(a(n) == a_exact(n) for n in range(1, 401)))
print("both formulas agree with a(n) for 1 <= n <= 3000:", all(a(n) == printed(n) == minus(n) for n in range(1, 3001)))
N = 541727237873320516868722558441138350267
print("n =", N)
print("  a(n)                    =", a(N))
print("  printed formula (+e^-2) =", printed(N))
print("  with minus sign (-e^-2) =", minus(N))
