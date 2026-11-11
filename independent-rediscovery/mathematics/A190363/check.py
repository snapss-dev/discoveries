"""A190363: a(n) = n + floor(n*sqrt(5)/2) + floor(5n/4).  Tests a(n) = a(n-4) + a(n-17) - a(n-21).
Run:  python check.py
"""
from math import isqrt
a = [None] + [n + isqrt(5 * n * n) // 2 + (5 * n) // 4 for n in range(1, 2001)]
print("a(1..8) =", a[1:9], "(entry: 3, 6, 9, 13, 16, 19, 22, 26)")
bad = [n for n in range(22, 2001) if a[n] != a[n-4] + a[n-17] - a[n-21]]
n = bad[0]
print(f"first failure at n = {n}: a({n}) = {a[n]}, predicted {a[n-4]} + {a[n-17]} - {a[n-21]} = {a[n-4] + a[n-17] - a[n-21]}")
print("failures up to n = 2000:", len(bad), "| first few:", bad[:6])
