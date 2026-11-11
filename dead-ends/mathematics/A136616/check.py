"""A136616: a(n) = largest m with H(m) - H(n) <= 1.
Formula in the entry ("after a suggestion by David Cantrell"):
    F(n) = floor(e*n + (e-1)/2 + (e - 1/e)/(24*(n + 1/2))).
Search for an n with F(n) != a(n).

Part 1  every n from 1 to NDIRECT, certified with Arb balls.
Part 2  every candidate from the continued fraction of (e-1)/2 = [0; 1, 6, 10, 14, 18, ...] with
        2n+1 < 10^DIGITS: for each convergent R/S above (e-1)/2 and the two multipliers t next to
        sqrt(((e-1/e)/12) / (S*(R - S*(e-1)/2))) with t*S odd, n = (t*S - 1)/2 is tested directly.
Part 3  mpmath (independent) on n <= 20000 and on the Part 2 candidates below 10^60.
Usage: python check.py [NDIRECT] [DIGITS]   (defaults 1000000, 3000)
"""
import sys, time
sys.set_int_max_str_digits(0)
from flint import arb, fmpz, ctx
import mpmath
from mpmath import mp, mpf

NDIRECT = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
DIGITS = int(sys.argv[2]) if len(sys.argv) > 2 else 3000

def test(n, prec):
    """returns (F(n), a(n) - F(n)) with every comparison certified; raises if undecided."""
    ctx.prec = prec
    E = arb(1).exp()
    y = E * n + (E - 1) / 2 + (E - 1 / E) / (24 * (arb(n) + arb(1) / 2))
    j = int(y.floor().unique_fmpz())
    base = arb(n + 1).digamma() + 1                 # H(m) - H(n) <= 1  <=>  digamma(m+1) <= base
    lo = arb(j + 1).digamma() - base                # want <= 0   (m = j admissible)
    hi = arb(j + 2).digamma() - base                # want > 0    (m = j+1 not admissible)
    if lo < 0 and hi > 0: return j, 0
    if lo > 0:
        lo2 = arb(j).digamma() - base
        if lo2 < 0: return j, -1
    if hi < 0:
        hi2 = arb(j + 3).digamma() - base
        if hi2 > 0: return j, +1
    raise RuntimeError("undecided at n = %d" % n)

print("Part 1: direct, 1 <= n <= %d (Arb, 160 bits)" % NDIRECT)
t0 = time.time()
bad = []
for n in range(1, NDIRECT + 1):
    if test(n, 160)[1] != 0: bad.append(n)
print("  n with F(n) != a(n):", bad, "  (%.0f s)" % (time.time() - t0))

print("Part 2: continued-fraction candidates with 2n+1 < 10^%d" % DIGITS)
t0 = time.time()
LIMIT = 10 ** DIGITS
# convergents of beta = (e-1)/2 = [0; 1, 6, 10, 14, ...]
R0, S0, R1, S1 = 0, 1, 1, 1          # index 0: 0/1, index 1: 1/1
k = 1
cands = []; closest = None; fails2 = []
while S1 < LIMIT:
    if k % 2 == 1:                    # odd index: R1/S1 > beta
        prec = 2 * S1.bit_length() + 300
        ctx.prec = prec
        E = arb(1).exp()
        beta = (E - 1) / 2
        w = S1 * (R1 - S1 * beta)                    # S*(R - S*beta) > 0
        half_kappa = (E - 1 / E) / 12
        tt = (half_kappa / w).sqrt()
        tf = int(tt.floor().unique_fmpz())
        for t in (tf, tf + 1):
            if t < 1 or (t * S1) % 2 == 0: continue
            q = t * S1
            if q >= LIMIT: continue
            n = (q - 1) // 2
            if n < 1: continue
            D = t * t * w - half_kappa               # failure needs -0.133/q^2 < D <= 0 (see page)
            F, d = test(n, 4 * q.bit_length() + 400)
            cands.append((k, t, n))
            if d != 0: fails2.append((k, t, n, d))
            absD = abs(float(D.mid()))
            if n > NDIRECT and (closest is None or absD < closest[0]):
                closest = (absD, k, t, len(str(q)), 2 * len(str(q)))
    a = 4 * (k + 1) - 2               # next partial quotient a_{k+1} = 4(k+1) - 2 for k+1 >= 2
    R0, S0, R1, S1 = R1, S1, a * R1 + R0, a * S1 + S0
    k += 1
print("  convergents used up to index %d; candidates tested: %d" % (k - 1, len(cands)))
print("  candidates with F(n) != a(n):", fails2)
print("  smallest candidates n:", [c[2] for c in cands[:8]])
print("  smallest |D| among candidates beyond Part 1: %.3g (index %d, t = %d, q = 2n+1 has %d digits;"
      " a failure there would need |D| < about 10^-%d)" % closest)
print("  (%.0f s)" % (time.time() - t0))

print("Part 3: mpmath, independent")
mp.dps = 50
def test_mp(n):
    e = mpmath.e
    y = e * n + (e - 1) / 2 + (e - 1 / e) / (24 * (mpf(n) + mpf(1) / 2))
    j = int(mpmath.floor(y))
    base = mpmath.digamma(n + 1) + 1
    m = j
    while mpmath.digamma(m + 1) > base: m -= 1
    while mpmath.digamma(m + 2) <= base: m += 1
    return m - j
b3 = [n for n in range(1, 20001) if test_mp(n) != 0]
mp.dps = 400
b4 = [c for c in cands if c[2] < 10 ** 60 and test_mp(c[2]) != 0]
print("  n <= 20000 with F(n) != a(n):", b3, "  candidates below 10^60 failing:", b4)
print("RESULT:", "no failure found" if not bad and not fails2 and not b3 and not b4 else "FAILURE FOUND")
