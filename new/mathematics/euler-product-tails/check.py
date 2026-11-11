# Recomputes five Euler-product constants and compares them with the OEIS DATA lines
# (as served by oeis.org on 2026-11-11):
#   A175639  decimal expansion of Taniguchi's constant  Prod_p (1 - 3/p^3 + 2/p^4 + 1/p^5 - 1/p^6)
#   A078076  continued fraction of Prod_p (1 - 1/(p^2-2))
#   A078077  continued fraction of Prod_p (1 + 1/(p^2+p-1))
#   A078086  continued fraction of Prod_p (1 - 1/(p^2*(p^2-1)))
#   A078088  continued fraction of (5*Pi^2/48) * Prod_{p>=3} (1 - (p+2)/p^3)
#
# Each product is written as Prod_{p >= p0} N(1/p)/D(1/p) with integer polynomials N, D, N(0) = D(0) = 1.
# Method 1 (Arb balls, python-flint): primes below 100 are multiplied directly; for the rest,
#     log Prod_{p>100} = sum_{n>=2} l_n * T(n),   log(N/D)(x) = sum l_n x^n  (exact rationals),
#     T(n) = sum_{p>100} p^-n = P(n) - sum_{p<100} p^-n,   P(n) = sum_{k>=1} mu(k)/k * log zeta(k n).
#   Truncations are enclosed: see the comments at each one.  The result is a ball that contains the product.
# Method 2 (mpmath): the same decomposition coded separately, with mpmath's own prime zeta function.
# (A third, unrelated implementation is PARI/GP's prodeulerrat; its output is quoted on the page.)
# Run:  python check.py
from fractions import Fraction
import mpmath as mp
from flint import arb, ctx, fmpq

DATA = {
 'A175639': "6,7,8,2,3,4,4,9,1,9,1,7,3,9,1,9,7,8,0,3,5,5,3,8,2,7,9,4,8,2,8,9,4,8,1,4,0,9,6,3,3,2,2,3,9,1,8,9,4,4,0,1,0,3,0,3,6,4,6,0,4,1,5,9,6,4,9,8,3,3,7,0,7,4,0,1,2,3,2,3,3,2,1,3,7,6,2,1,2,2,9,3,3,4,8,4,6,1,6,8,8,8,3,2,8",
 'A078076': "0,2,1,1,3,54,1,1,5,2,3,2,2,2,2,2,1,3,32,2,1,2,17,1,1,1,1,14,4,1,19,4,2,3,40,1,1,2,1,19,2,3,5324,2,1,3,2,1,5,3,1,1,17,1,1,2,8,1,2,2,3,2,2,1,2,15,1,7,1,5,2,1,4,16,272,1,8,3,1,2,3,3,39,2,2,1,4,1,1,1,2,3",
 'A078077': "1,2,2,1,1,1,1,4,2,1,1,3,703,2,1,1,1,3,5,1,1,4,10,2,10,2,1,2,1,4,4,11,5,1,2,1,1,30,37,2,75,1,1,8,5,1,1,7,44,280,5,1,1,1,1,2,1,1,3,1,1,3,1,9,94,1,127,2,2,7,3,3,3,6,2,1,705,24,2,7,2,2,1,3,7,1,1,3,40,6,1",
 'A078086': "0,1,9,5,10,1,6,1,1,1,11,1,5,1,10,1,17,5,5,6,1,13,6,3,1,1,4,1,1,2,1,3,3,1,5,7,1,17,5,2,1,10,2,2,1,14,62,3,3,4,1,1,4,8,1041,86,1,6,1,2,6,12,1,45,2,45,2,3,2,1,1,2,2,1,4,1,1,21,5,6,4,1,1,4,1,2,2,3,2,6,1",
 'A078088': "0,1,2,1,9,1,1,1,1,1,1,3,3,3,1,1,5,1,11,1,2,1,10,1,68,2,1,15,11,1,5,3,2,1,2,82,2,7,2,1,3,6,1,1,2,5,43,9,3,6,2,1,1,2,8,1,1,3,1,1,4,1,1,1,5,6,2,1,9,13,1,2,14,2,7,1,1,1,3,1,5,169,1,2,1,2,7,43,2,3,1,1,7,1,96",
}
# name: (N, D, first prime, multiply by 5*Pi^2/48 ?)   polynomials in x = 1/p, lowest degree first
CASES = {
 'A175639': ([1, 0, 0, -3, 2, 1, -1], [1], 2, False),
 'A078076': ([1, 0, -3], [1, 0, -2], 2, False),          # 1 - 1/(p^2-2) = (p^2-3)/(p^2-2)
 'A078077': ([1, 1], [1, 1, -1], 2, False),              # 1 + 1/(p^2+p-1) = (p^2+p)/(p^2+p-1)
 'A078086': ([1, 0, -1, 0, -1], [1, 0, -1], 2, False),   # 1 - 1/(p^2(p^2-1)) = (p^4-p^2-1)/(p^4-p^2)
 'A078088': ([1, 0, -1, -2], [1], 3, True),              # 1 - (p+2)/p^3
}
B = 100          # primes below B are handled directly
NMAX = 140       # the log series is cut here
DPS = 420

def log_series(poly, nmax):
    c = [Fraction(v) for v in poly] + [Fraction(0)] * (nmax + 1)
    l = [Fraction(0)] * (nmax + 1)
    for n in range(1, nmax + 1):
        s = n * c[n]
        for k in range(1, n): s -= k * l[k] * c[n - k]
        l[n] = s / n
    return l

def primes_upto(n):
    return [p for p in range(2, n + 1) if all(p % q for q in range(2, int(p ** 0.5) + 1))]

def mobius(n):
    r = 1; p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r

def check_roots(N, D):
    # every zero of N and D has modulus > 1/2, hence |l_n| <= (deg N + deg D) * 2^n / n
    mp.mp.dps = 30
    for poly in (N, D):
        if len(poly) > 1:
            for z in mp.polyroots(list(reversed(poly)), maxsteps=200, extraprec=200):
                assert abs(z) > 0.55, "root too close to 0"

def euler_arb(N, D, p0):
    ctx.dps = DPS
    check_roots(N, D)
    ln = log_series(N, NMAX); ld = log_series(D, NMAX)
    l = [a - b for a, b in zip(ln, ld)]
    ps = primes_upto(B)
    def ev(poly, x):
        s = arb(0)
        for c in reversed(poly): s = s * x + c
        return s
    prod = arb(1)
    for p in ps:
        if p >= p0:
            x = arb(1) / p; prod *= ev(N, x) / ev(D, x)
    unit = arb(0, 1)                                  # the ball [-1, 1]
    logt = arb(0)
    for n in range(2, NMAX + 1):
        if l[n] == 0: continue
        P = arb(0); k = 1
        while k * n * 0.30102 < DPS + 20:
            m = mobius(k)
            if m: P += arb(m) / k * arb(k * n).zeta().log()
            k += 1
        # dropped terms k' >= k: |log zeta(s)| <= 2 * 2^-s for s >= 2, so their sum is below 4 * 2^-(k n)
        P += unit * (arb(4) / arb(2) ** (k * n))
        T = P
        for p in ps: T -= (arb(1) / p) ** n
        logt += arb(fmpq(l[n].numerator, l[n].denominator)) * T
    # dropped n > NMAX: |l_n| <= deg * 2^n and T(n) <= 2 * 101^-n, a geometric series with ratio 2/101
    deg = len(N) + len(D) - 2
    q = Fraction(2, 101)
    bound = 2 * deg * q ** (NMAX + 1) / (1 - q)
    logt += unit * arb(fmpq(bound.numerator, bound.denominator))
    return prod * logt.exp()

def euler_mp(N, D, p0):
    mp.mp.dps = 320
    ln = log_series(N, NMAX); ld = log_series(D, NMAX)
    ps = primes_upto(B)
    prod = mp.mpf(1)
    for p in ps:
        if p >= p0:
            x = mp.mpf(1) / p
            prod *= mp.polyval(list(reversed(N)), x) / mp.polyval(list(reversed(D)), x)
    s = mp.mpf(0)
    for n in range(2, NMAX + 1):
        c = ln[n] - ld[n]
        if c == 0: continue
        T = mp.primezeta(n) - mp.fsum(mp.mpf(p) ** (-n) for p in ps)
        s += mp.mpf(c.numerator) / c.denominator * T
    return prod * mp.exp(s)

def cf(fr, nmax):
    out = []; a, b = fr.numerator, fr.denominator
    while b and len(out) < nmax:
        t = a // b; out.append(t); a, b = b, a - t * b
    return out

def first_diff(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]: k += 1
    return k

ok = True
for name, (N, D, p0, withpi) in CASES.items():
    v = euler_arb(N, D, p0)
    w = euler_mp(N, D, p0)
    if withpi:
        v = v * 5 * arb.pi() ** 2 / 48
        w = w * 5 * mp.pi ** 2 / 48
    # exact rational enclosure [lo, hi] of the Arb ball
    r = Fraction(1, 10 ** 200)
    assert v.rad() < arb(fmpq(1, 10 ** 201)), "ball too wide"
    mid = Fraction(v.str(215, radius=False))
    lo, hi = mid - r, mid + r
    wm = Fraction(mp.nstr(w, 215, strip_zeros=False))
    assert lo < wm < hi, "mpmath value outside the Arb enclosure"
    data = DATA[name].split(",")
    print("=== %s ===" % name)
    print("  value (Arb, radius < 1e-200; mpmath agrees): %s..." % v.str(130, radius=False)[:122])
    if name == 'A175639':
        n = 125
        dlo = str((lo.numerator * 10 ** n) // lo.denominator); dhi = str((hi.numerator * 10 ** n) // hi.denominator)
        assert dlo == dhi
        d = "".join(data); k = first_diff(d, dlo)
        print("  DATA: %d digits a(0..%d); the first %d are correct" % (len(d), len(d) - 1, k))
        print("  printed a(%d..%d): %s" % (k, len(d) - 1, d[k:]))
        print("  correct a(%d..%d): %s   (next digits: %s)" % (k, len(d) - 1, dlo[k:len(d)], dlo[len(d):len(d) + 15]))
        ok &= (k == 99)
    else:
        clo = cf(lo, 130); chi = cf(hi, 130); c = clo[:first_diff(clo, chi)]     # certified partial quotients
        assert len(c) >= 110
        dv = [int(x) for x in data]; k = first_diff(dv, c)
        print("  DATA: %d terms a(0..%d); the first %d are correct" % (len(dv), len(dv) - 1, k))
        print("  printed a(%d..%d): %s" % (k, len(dv) - 1, dv[k:]))
        print("  correct a(%d..%d): %s   (next terms: %s)" % (k, len(dv) - 1, c[k:len(dv)], c[len(dv):len(dv) + 6]))
        ok &= (k == {'A078076': 91, 'A078077': 83, 'A078086': 85, 'A078088': 94}[name])
        # where the printed tail comes from: the continued fraction of the constant cut to 98 decimals
        t98 = Fraction((mid.numerator * 10 ** 98) // mid.denominator, 10 ** 98)
        same = cf(t98, len(dv)) == dv
        print("  printed terms = continued fraction of the value truncated to 98 decimal places: %s" % same)
        ok &= (same == (name != 'A078088'))
print()
print("ALL CHECKS PASSED" if ok else "MISMATCH WITH THE PAGE")
