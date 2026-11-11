"""Numeric checks for the short proofs on this page (A069097, A234307, A055210) and for A023887.
Run:  python check.py
"""
from math import gcd, isqrt
import mpmath as mp
from sympy import totient, divisors, factorint, divisor_sigma

mp.mp.dps = 40
worst = max(abs(sum((-1)**(k + 1) * gcd(k, n) / mp.cos(k * mp.pi / n)**2 for k in range(1, n + 1)) - n)
            for n in range(1, 302, 2))
print("A069097: sum_{k<=n} (-1)^(k+1) gcd(k,n)/cos(k pi/n)^2 = n for odd n <= 301; max error", mp.nstr(worst, 3))

a234 = lambda n: sum(gcd(2 * n - i, i) for i in range(1, n + 1))
print("A234307: a(n) = (1/4) sum_{k<=4n} (-1)^k gcd(k, 8n) for n <= 800:",
      all(4 * a234(n) == sum((-1)**k * gcd(k, 8 * n) for k in range(1, 4 * n + 1)) for n in range(1, 801)))

def core(n):
    c = 1
    for p, e in factorint(n).items():
        if e % 2: c *= p
    return c
a055 = lambda n: sum(int(totient(d)) for d in divisors(n) if isqrt(d)**2 == d)
print("A055210: a(n) = sigma_2(s)/sigma_1(s), s = n/core(n), for n <= 20000:",
      all(a055(n) * int(divisor_sigma(n // core(n), 1)) == int(divisor_sigma(n // core(n), 2)) for n in range(1, 20001)))

def rad(n):
    r = 1
    for p in factorint(n): r *= p
    return r
print("A023887: sigma_m(n) = sigma(n^m rad(n)^(m-1)) / sigma(rad(n)^(m-1)) for n <= 500, m <= 6:",
      all(int(divisor_sigma(n, m)) * int(divisor_sigma(rad(n)**(m - 1), 1)) == int(divisor_sigma(n**m * rad(n)**(m - 1), 1))
          for n in range(1, 501) for m in range(1, 7)))
