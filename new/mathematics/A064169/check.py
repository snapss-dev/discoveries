"""A064169: a(n) = numerator(H_n) - denominator(H_n).  Lists every n <= N where
a(n) != numerator(3*(H_n - 1) / (n*(n^2 + 6n + 11))).
Run:  python check.py [N]      default N = 20000
"""
import sys
from fractions import Fraction
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
H = Fraction(0); exc = []
for n in range(1, N + 1):
    H += Fraction(1, n)
    if n >= 2:
        a = H.numerator - H.denominator
        if (3 * (H - 1) / (n * (n * n + 6 * n + 11))).numerator != a: exc.append(n)
print(f"exceptions for 2 <= n <= {N}:", exc)
print("listed in the entry: 5, 82, 115, 383")
