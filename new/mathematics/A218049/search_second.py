"""A218049, second implementation (numpy only, sympy for roots and factoring; shares no code with a218049_sieve.py).
For LO <= k < HI: mark k when p^2 | k^2 + 1 for a prime p < P0.  Every window of N consecutive k with at most one
unmarked k is tested exactly (sympy.factorint).  Usage: a218049_check2.py N LO HI P0"""
import sys, time
import numpy as np
from sympy import factorint, primerange
from sympy.ntheory import sqrt_mod

N = int(sys.argv[1]); LO = int(float(sys.argv[2])); HI = int(float(sys.argv[3])); P0 = int(float(sys.argv[4]))
t0 = time.time()
cls = []
for p in primerange(2, P0):
    q = p * p
    for r in (sqrt_mod(-1, q, all_roots=True) or []):
        assert (r * r + 1) % q == 0
        cls.append((q, int(r)))
def nonsquarefree(v):
    return any(e > 1 for e in factorint(v).values())
L = 1 << 24
found = []; tested = 0
lo = LO
while lo < HI:
    n = min(L, HI - lo) + N          # overlap so that windows starting in [lo, lo+L) are complete
    m = np.zeros(n, np.int8)
    for q, r in cls:
        s = (r - lo) % q
        if s < n:
            m[s::q] = 1
    c = np.concatenate(([0], np.cumsum(m, dtype=np.int64)))
    w = c[N:] - c[:-N]               # marked k in the window starting at lo + i
    for i in np.nonzero(w[:n - N] >= N - 1)[0]:
        k = lo + int(i)
        if k < 1 or k >= HI: continue
        tested += 1
        if all(nonsquarefree((k + d) ** 2 + 1) for d in range(N)):
            found.append(k); print("window start k =", k, "all", N, "values non-squarefree", flush=True)
    lo += n - N
print(f"N={N} range [{LO},{HI}) P0={P0}: classes {len(cls)}, windows tested exactly {tested}, runs found {found[:5]}, {time.time()-t0:.0f}s")
