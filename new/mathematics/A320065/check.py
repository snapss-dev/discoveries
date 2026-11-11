"""A320065: a(n) = smallest i with binomial(2i,i) > n.
Formula in the entry (Jean and Kotesovec, 2025), for n > 1:
  a(n) = ceiling( x0 * (1 + 2 log2 / (3 log2 + (2 + log2) w + 2 w^2)) ),
  w = LambertW(-1, -4 log2 / (Pi n^2)),  x0 = -w / (4 log2).
Part 1  mpmath: compare with the definition for 2 <= n < NSCAN; list every failure.
Part 2  Arb balls (independent LambertW code): g(C-1) - i and g(C) - i at C = binomial(2i,i), 2 <= i <= IMAX.
Part 3  number of failing n in each block [binomial(2i-2,i-1), binomial(2i,i)), by bisection (Arb).
Usage: python check.py [NSCAN] [IMAX]   (defaults 200000, 400)
"""
import sys
from math import comb
import mpmath
from mpmath import mp, mpf
from flint import arb, ctx

NSCAN = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
IMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 400

def g_mp(n):
    L2 = mpmath.log(2)
    w = mpmath.lambertw(-4 * L2 / (mpmath.pi * mpf(n) ** 2), -1).real
    return (-w / (4 * L2)) * (1 + 2 * L2 / (3 * L2 + (2 + L2) * w + 2 * w * w))

def g_arb(n):
    L2 = arb(2).log()
    w = (-4 * L2 / (arb.pi() * arb(n) ** 2)).lambertw(-1)
    return (-w / (4 * L2)) * (1 + 2 * L2 / (3 * L2 + (2 + L2) * w + 2 * w * w))

print("Part 1: definition against formula, 2 <= n < %d (mpmath, 30 digits)" % NSCAN)
mp.dps = 30
fails = []; i = 1
for n in range(2, NSCAN):
    while comb(2 * i, i) <= n: i += 1
    v = g_mp(n)
    f = int(mpmath.ceil(v))
    assert abs(v - mpmath.nint(v)) > mpf(10) ** -15, n      # no rounding ambiguity
    if f != i: fails.append((n, i, f))
print("  number of failures:", len(fails))
print("  first failures (n, a(n), formula):", fails[:6])
blocks = {}
for n, a, f in fails: blocks.setdefault(a, []).append(n)
for a in sorted(blocks):
    print("  a(n) = %d: formula wrong for n = %d..%d (%d values); binomial(%d,%d) = %d"
          % (a, blocks[a][0], blocks[a][-1], len(blocks[a]), 2 * a, a, comb(2 * a, a)))

print("Part 2: Arb, at C = binomial(2i,i): signs of g(C-1) - i and g(C) - i, 2 <= i <= %d" % IMAX)
first_bad = None; all_bad_from = None; ok_at_C = True
for i in range(2, IMAX + 1):
    C = comb(2 * i, i)
    ctx.prec = 2 * C.bit_length() + 200
    dm, d0 = g_arb(C - 1) - i, g_arb(C) - i
    assert (dm > 0 or dm < 0) and (d0 > 0 or d0 < 0), i
    wrong_below = bool(dm > 0)          # formula gives more than i at n = C-1, where a(n) = i
    if not (d0 > 0) or not (d0 < 1): ok_at_C = False     # at n = C the formula must give i+1
    if wrong_below and first_bad is None: first_bad = i
    if not wrong_below: all_bad_from = None
    elif all_bad_from is None: all_bad_from = i
    if i in (2, 5, 6, 7, 8, 10, 20, 50, 100, 200, 400) or i == IMAX:
        print("  i = %3d: g(C-1) - i = %s   g(C) - i = %s   i^2*(g(C)-i) = %s"
              % (i, dm.str(8, radius=False), d0.str(8, radius=False), (d0 * i * i).str(6, radius=False)))
print("  formula correct at n = C for all these i:", ok_at_C)
print("  first i with a wrong value at n = binomial(2i,i) - 1: i =", first_bad,
      " n =", comb(2 * first_bad, first_bad) - 1)
print("  wrong at n = binomial(2i,i) - 1 for every i from", all_bad_from, "to", IMAX)

print("Part 3: failing n per block (smallest n with g(n) > i, Arb bisection)")
for i in range(7, 21):
    lo, hi = comb(2 * i - 2, i - 1), comb(2 * i, i) - 1      # g(lo) <= i < g(hi)
    ctx.prec = 2 * hi.bit_length() + 200
    assert g_arb(lo) - i < 0 and g_arb(hi) - i > 0
    while hi - lo > 1:
        m = (lo + hi) // 2
        d = g_arb(m) - i
        assert d > 0 or d < 0
        if d > 0: hi = m
        else: lo = m
    C = comb(2 * i, i)
    print("  i = %2d: formula gives %d instead of %d for n = %d..%d  (%d values, %.3g of the block)"
          % (i, i + 1, i, hi, C - 1, C - hi, (C - hi) / (C - comb(2 * i - 2, i - 1))))
print("RESULT:", "OK" if fails and fails[0][0] == 3431 and first_bad == 7 and all_bad_from == 7 else "CHECK")
