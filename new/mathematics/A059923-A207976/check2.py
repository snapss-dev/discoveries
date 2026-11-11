"""Independent second check for A059923 and A207976 (shares no code with check.py):
FLINT integer roots for the sequences, 400-digit mpmath for the constants.
The constants are taken as a(399)^(1/399); their error (below 10^-70) is far too small to matter for n < 150.
"""
from mpmath import mp, mpf, floor, log, exp
from flint import fmpz
mp.dps = 400
N = 399

a = [None, 1]                                   # A059923
for n in range(1, N):
    a.append(int(fmpz(a[n] ** (n + 1)).root(n)) + 1)
x = exp(log(mpf(a[N])) / N)
bad = [n for n in range(1, 150) if int(floor(x ** n)) != a[n]]
print("A059923: x =", mp.nstr(x, 30))
print("  x^24 =", mp.nstr(x ** 24, 12), " a(24) =", a[24])
print("  n < 150 with floor(x^n) != a(n):", bad)

c = [None, 2]                                   # A207976
for n in range(2, N + 1):
    T = fmpz(c[n - 1] ** n)
    r = int(T.root(n - 1))
    if r ** (n - 1) == T: r -= 1
    c.append(r)
q = exp(log(mpf(c[N])) / N)
bad2 = [n for n in range(1, 150) if 1 + int(floor(q ** n)) != c[n]]
print("A207976: q =", mp.nstr(q, 30))
print("  q^27 =", mp.nstr(q ** 27, 12), " a(27) =", c[27])
print("  n < 150 with 1 + floor(q^n) != a(n):", bad2)
