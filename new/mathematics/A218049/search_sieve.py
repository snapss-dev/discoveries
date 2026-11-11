"""A218049: smallest k such that k^2+1, (k+1)^2+1, ..., (k+n-1)^2+1 are all divisible by a square > 1.
Sieve: mark k when p^2 | k^2+1 for a prime p < P0 (p = 1 mod 4; two residue classes mod p^2).
Reports for each n <= NMAX the first run of n marked k, and tests exactly (factorisation) every window of NMAX
consecutive k with exactly one unmarked position.  Usage: a218049_sieve.py KMAX NMAX P0 [KSTART]"""
import sys, time
import numpy as np
import numba
from numba import njit, prange
import flint

KMAX = int(float(sys.argv[1])); NMAX = int(sys.argv[2]); P0 = int(float(sys.argv[3]))
KSTART = int(float(sys.argv[4])) if len(sys.argv) > 4 else 0
numba.set_num_threads(4)

def primes_upto(N):
    s = np.ones(N + 1, np.bool_); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

Q = []; R = []
for p in primes_upto(P0 - 1):
    p = int(p)
    if p % 4 != 1: continue
    # a square root of -1 mod p: g^((p-1)/4) for a non-residue g
    g = 2
    while pow(g, (p - 1) // 2, p) != p - 1: g += 1
    r = pow(g, (p - 1) // 4, p)
    assert (r * r + 1) % p == 0
    for r0 in (r, p - r):
        f = (r0 * r0 + 1) // p
        t = (-f * pow(2 * r0, -1, p)) % p
        x = r0 + p * t
        assert (x * x + 1) % (p * p) == 0
        Q.append(p * p); R.append(x)
Q = np.array(Q, np.int64); R = np.array(R, np.int64)
OV = 64

@njit(parallel=True, cache=True)
def seg(k0, nseg, S, OV, Q, R, NMAX, first, nearw, maxnear):
    for s in prange(nseg):
        lo = k0 + s * S - OV          # the segment covers [lo, lo + S + OV)
        L = S + OV
        m = np.zeros(L, np.uint8)
        for i in range(len(Q)):
            q = Q[i]
            t = (R[i] - lo) % q
            while t < L:
                m[t] = 1
                t += q
        run = 0; c = 0
        unm = 0   # unmarked positions in the window of the last NMAX positions
        for t in range(L):
            if lo + t < 1:
                run = 0; continue
            if m[t]:
                run += 1
                if run <= NMAX and first[s, run] < 0 and t - run + 1 >= 0:
                    first[s, run] = lo + t - run + 1
            else:
                run = 0
            unm += 1 - m[t]
            if t >= NMAX:
                unm -= 1 - m[t - NMAX]
            if t >= NMAX - 1 and unm == 1 and t >= OV and lo + t - NMAX + 1 >= 1 and c < maxnear:
                nearw[s, c] = lo + t - NMAX + 1; c += 1

def nonsquarefree(x):
    f = flint.fmpz(x).factor()
    # python-flint can list a repeated prime as two entries (seen for x > 2^64): merge before testing
    prod = 1; d = {}
    for p, e in f:
        p = int(p); assert flint.fmpz(p).is_prime()
        d[p] = d.get(p, 0) + int(e); prod *= p ** int(e)
    assert prod == x
    return any(e > 1 for e in d.values())

t0 = time.time()
print("NMAX", NMAX, "P0", P0, "classes", len(Q), flush=True)
S = 1 << 23; nseg = 16; maxnear = 1 << 14
best = {}; near_checked = 0; near_hits = []
k0 = (KSTART // S) * S; it = 0
while k0 < KMAX:
    first = np.full((nseg, NMAX + 1), -1, np.int64)
    nearw = np.full((nseg, maxnear), -1, np.int64)
    seg(k0, nseg, S, OV, Q, R, NMAX, first, nearw, maxnear)
    for s in range(nseg):
        assert nearw[s, maxnear - 1] < 0
        for c in range(maxnear):
            w = int(nearw[s, c])
            if w < 0: break
            near_checked += 1
            if all(nonsquarefree(k * k + 1) for k in range(w, w + NMAX)):
                print("NEAR-HIT window start", w, flush=True); near_hits.append(w)
                if first[s, NMAX] < 0 or w < first[s, NMAX]: first[s, NMAX] = w
    for n in range(1, NMAX + 1):
        if n in best: continue
        v = [int(first[s, n]) for s in range(nseg) if first[s, n] >= 0]
        if v:
            best[n] = min(v); print(f"n={n} k={best[n]}  {time.time()-t0:.0f}s", flush=True)
    k0 += nseg * S; it += 1
    if NMAX in best: break
    if it % 100 == 0: print(f"progress k<{k0:.4e} near_checked={near_checked} {time.time()-t0:.0f}s", flush=True)
print("done: searched k <", k0, "; first runs", best, "; near windows checked", near_checked, "; near hits", near_hits)
