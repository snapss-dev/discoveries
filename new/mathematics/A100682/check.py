"""A100682: a(n) = floor(binomial(n+3, 4)^(1/4)), offset 0.

Conjecture in the entry (2012, written in the older indexing m = n + 3):
    floor(C(m,4)^(1/4)) = floor((m - 3/2) / 24^(1/4))  for m not in {0, 1, 6, 17, 2403, 5318}.
In the current offset the formula reads floor((n + 3/2) / 24^(1/4)) with exceptions n = 3, 14, 2400, 5315.

Everything here is exact integer arithmetic:
    a(n)       = largest k with 24 k^4 <= n(n+1)(n+2)(n+3),
    formula(n) = largest k with 384 k^4 <= (2n+3)^4.
Run:  python check.py [SCAN]     default SCAN = 3000000 (exhaustive exact scan of 0 <= n < SCAN)
      python check.py 2000000000 runs the full scan (a float pre-filter, then exact checks; needs numba)
"""
import sys, os
from math import isqrt

def iroot4(x):
    r = isqrt(isqrt(x))
    while (r + 1) ** 4 <= x: r += 1
    while r ** 4 > x: r -= 1
    return r
a = lambda n: iroot4(n * (n + 1) * (n + 2) * (n + 3) // 24)
formula = lambda n: iroot4((2 * n + 3) ** 4 // 384)

here = os.path.dirname(os.path.abspath(__file__))
exc = [int(x) for x in open(os.path.join(here, "exceptions.txt")).read().split()]
print(f"{len(exc)} listed exceptions, largest has {len(str(exc[-1]))} digits")
print("every listed n is an exception (a(n) = formula(n) - 1):", all(a(n) == formula(n) - 1 for n in exc))
print("a(n) <= formula(n) at the neighbours too:", all(a(n + d) == formula(n + d) for n in exc[4:] for d in (-1, 1)))
for n in exc[4:6]:
    print(f"  n = {n} (m = {n + 3}):  a(n) = {a(n)},  formula = {formula(n)}")

SCAN = int(sys.argv[1]) if len(sys.argv) > 1 else 3_000_000
if SCAN <= 20_000_000:
    found = [n for n in range(SCAN) if a(n) != formula(n)]
else:
    import numpy as np
    from numba import njit, prange
    @njit(parallel=True)
    def flag(n0, n1, out):
        c = 24.0 ** 0.25
        for i in prange(n1 - n0):
            u = n0 + i + 1.5
            t = u / c
            f = t - np.floor(t)
            # An exception needs t within about 0.2824/u above an integer.  Flag generously on both
            # sides of the integer, because t carries a float64 rounding error of up to about 1e-7.
            if f < 1.0 / u + 1e-5 or f > 1.0 - 1e-5: out[i] = 1
    found = []; CH = 50_000_000
    for n0 in range(0, SCAN, CH):
        n1 = min(SCAN, n0 + CH); out = np.zeros(n1 - n0, dtype=np.uint8)
        flag(n0, n1, out)
        found += [int(n) for n in (np.nonzero(out)[0] + n0) if a(int(n)) != formula(int(n))]
print(f"all exceptions with 0 <= n < {SCAN}: {found}")
print("agrees with the list:", found == [n for n in exc if n < SCAN])
