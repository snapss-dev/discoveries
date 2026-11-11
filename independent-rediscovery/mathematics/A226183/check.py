"""A226183(n) = least k with H(k) > 2 H(n);  A289183(n) = greatest m with H(m) < 2 H(n) = A226183(n) - 1.
(A tie H(k) = 2 H(n) with n >= 2 never occurs in the range examined; the script would stop on one.)

Formulas compared with the definition:
  W(n) = round(e^g n(n+1) + g)                         A226183, White 2021           (g = Euler's constant)
  f(n) = floor(n^2 exp(g + 1/n) - 1/2 - e^g/6)         A289183, Schoenfield and Kotesovec 2017
  G(n) = floor(e^g (n^2 + n + 1/3) - 1/2)              for A289183;  A226183(n) = G(n) + 1
Part 1  exact rationals, n <= 60.
Part 2  Arb balls (digamma), 1 <= n <= NMAX: every value certified, failures of W, f, G listed.
Part 3  the n listed in A289183 as exceptions of f, and their neighbours.
Part 4  mpmath (independent), n <= 3000.
Usage: python check.py [NMAX]   (default 10000000)
"""
import sys, time
from fractions import Fraction
from flint import arb, ctx
import mpmath
from mpmath import mp, mpf

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 10000000

print("Part 1: exact rationals, n <= 60")
k = 0; Hk = Fraction(0); Hn = Fraction(0); exact = {}
for n in range(1, 61):
    Hn += Fraction(1, n)
    while Hk <= 2 * Hn:
        k += 1; Hk += Fraction(1, k)
    exact[n] = k                      # least k with H(k) > 2 H(n)
    assert Hk - Fraction(1, k) != 2 * Hn or n == 1
print("  A226183(1..12) =", [exact[n] for n in range(1, 13)])
mp.dps = 40
eg_mp = mpmath.exp(mpmath.euler)
W_mp = lambda n: int(mpmath.floor(eg_mp * n * (n + 1) + mpmath.euler + mpf(1) / 2))
print("  n <= 60 where round(e^g n(n+1) + g) differs from A226183(n):",
      [(n, exact[n], W_mp(n)) for n in exact if exact[n] != W_mp(n)])

ctx.prec = 200
EG = arb.const_euler().exp()
GAM = arb.const_euler()
def fl(x):
    r = x.floor()
    return int(r.unique_fmpz())       # raises if the ball contains an integer boundary
def A289183(n, guess):
    """greatest m with H(m) < 2 H(n), certified; H(m) = digamma(m+1) + gamma."""
    t = 2 * arb(n + 1).digamma() + GAM          # H(m) < 2H(n)  <=>  digamma(m+1) < t
    m = guess
    while True:
        lo = arb(m + 1).digamma() - t           # must be < 0
        hi = arb(m + 2).digamma() - t           # must be > 0
        if lo < 0 and hi > 0: return m
        if lo > 0: m -= 1
        elif hi < 0: m += 1
        else: raise RuntimeError("undecided n=%d" % n)

print("Part 2: Arb (200 bits), 1 <= n <= %d" % NMAX)
t0 = time.time()
badW, badf, badG = [], [], []
third = arb(1) / 3; half = arb(1) / 2
for n in range(1, NMAX + 1):
    G = fl(EG * (n * n + n + third) - half)
    m = A289183(n, G)
    if n <= 60: assert m + 1 == exact[n]
    if G != m: badG.append(n)
    if n >= 2:
        f = fl(arb(n) ** 2 * (GAM + 1 / arb(n)).exp() - half - EG / 6)
        if f != m: badf.append(n)
    W = fl(EG * n * (n + 1) + GAM + half)
    if W != m + 1:
        assert W == m
        badW.append(n)
print("  W fails at %d of %d values of n (fraction %.5f; predicted density e^g/3 - g = %.5f)"
      % (len(badW), NMAX, len(badW) / NMAX, float(EG / 3 - GAM)))
print("  first failures of W:", badW[:15])
print("  failures of f (n >= 2):", badf)
print("  failures of G:", badG)
print("  (%.0f s)" % (time.time() - t0))

print("Part 3: the exceptions of f listed in A289183")
for n in (66, 39087, 517345, 2013005, 10240491, 80968833):
    for nn in (n - 1, n, n + 1):
        G = fl(EG * (nn * nn + nn + third) - half)
        m = A289183(nn, G)
        f = fl(arb(nn) ** 2 * (GAM + 1 / arb(nn)).exp() - half - EG / 6)
        if nn == n:
            print("  n = %d: A289183(n) = %d, f(n) = %d, G(n) = %d" % (n, m, f, G))
            assert G == m and f == m + 1
        else:
            assert G == m

print("Part 4: mpmath (independent), n <= 3000")
mp.dps = 50
bad = []; wf = []
for n in range(1, 3001):
    t = 2 * mpmath.harmonic(n)
    m = int(mpmath.floor(eg_mp * (n * n + n + mpf(1) / 3) - mpf(1) / 2))
    while mpmath.harmonic(m) >= t: m -= 1
    while mpmath.harmonic(m + 1) < t: m += 1
    if m != int(mpmath.floor(eg_mp * (n * n + n + mpf(1) / 3) - mpf(1) / 2)): bad.append(n)
    if W_mp(n) != m + 1: wf.append(n)
print("  failures of G:", bad, "  failures of W:", wf[:12], "... (%d)" % len(wf))
ok = (not badG) and badW[:3] == [10, 123, 193] and wf == [n for n in badW if n <= 3000] and \
     badf == [n for n in (66, 39087, 517345, 2013005, 10240491, 80968833) if n <= NMAX]
print("RESULT:", "OK" if ok else "CHECK")
