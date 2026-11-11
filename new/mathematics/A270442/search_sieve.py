"""Smallest k > 1 such that none of k^2 + s*j, j = 0..n, is squarefree (s = -1: A270442, s = +1: A271817).
Segmented sieve over k with all primes p < P0: every residue class r mod p^2 with p^2 | r^2 + s*j sets bit j.
Reports, for each n <= NMAX, the first k whose bits 0..n are all set ("full hit"), and checks exactly
(python-flint factorisation) every k for which at most MAXMISS of the bits 1..NMAX are missing.
Usage: sqsieve.py SIGN KMAX NMAX P0 MAXMISS [KSTART]"""
import sys, time
import numpy as np
import numba
from numba import njit, prange
import flint

SIGN = int(sys.argv[1]); KMAX = int(float(sys.argv[2])); NMAX = int(sys.argv[3]); P0 = int(float(sys.argv[4]))
MAXMISS = int(sys.argv[5]); KSTART = int(float(sys.argv[6])) if len(sys.argv) > 6 else 0
numba.set_num_threads(4)

def primes_upto(N):
    s = np.ones(N + 1, np.bool_); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def classes(P0, NMAX, SIGN):
    Q = []; R = []; J = []
    for p in primes_upto(P0 - 1):
        p = int(p); q = p * p
        if p < 50:
            # brute force modulo p^2
            for j in range(NMAX + 1):
                for r in range(q):
                    if (r * r + SIGN * j) % q == 0:
                        Q.append(q); R.append(r); J.append(j)
            continue
        # p > NMAX: p does not divide j for 1 <= j <= NMAX; j = 0 handled by "k^2 never squarefree"
        sq = (np.arange(p, dtype=np.int64) ** 2) % p
        for j in range(1, NMAX + 1):
            target = (-SIGN * j) % p
            for r in np.nonzero(sq == target)[0]:
                r = int(r)
                f = (r * r + SIGN * j) // p
                t = (-f * pow(2 * r, -1, p)) % p
                x = r + p * t
                assert (x * x + SIGN * j) % q == 0
                Q.append(q); R.append(x); J.append(j)
    return np.array(Q, np.int64), np.array(R, np.int64), np.array(J, np.int64)

@njit(parallel=True, cache=True)
def seg(k0, nseg, S, Q, R, J, NMAX, out_full, out_near_k, out_near_m, maxnear, MAXMISS):
    for s in prange(nseg):
        lo = k0 + s * S
        mask = np.ones(S, np.int32)
        for i in range(len(Q)):
            q = Q[i]
            t = (R[i] - lo) % q
            b = np.int32(1 << J[i])
            while t < S:
                mask[t] |= b
                t += q
        full = (1 << (NMAX + 1)) - 1
        c = 0
        for t in range(S):
            m = mask[t] & full
            # longest prefix of set bits
            n = 0
            while n <= NMAX and (m >> n) & 1:
                n += 1
            n -= 1  # bits 0..n set
            for i in range(n + 1):
                if out_full[s, i] < 0 and lo + t > 1:
                    out_full[s, i] = lo + t
            miss = full ^ m
            pc = 0
            mm = miss
            while mm:
                mm &= mm - 1; pc += 1
            if pc >= 1 and pc <= MAXMISS and c < maxnear:
                out_near_k[s, c] = lo + t; out_near_m[s, c] = miss; c += 1

def nonsquarefree(x):
    if x == 0: return True
    x = abs(x)
    f = flint.fmpz(x).factor()
    # python-flint can list a repeated prime as two entries (seen for x > 2^64): merge before testing
    prod = 1; d = {}
    for p, e in f:
        p = int(p); assert flint.fmpz(p).is_prime()
        d[p] = d.get(p, 0) + int(e); prod *= p ** int(e)
    assert prod == x
    return any(e > 1 for e in d.values())

if __name__ == "__main__":
    t0 = time.time()
    Q, R, J = classes(P0, NMAX, SIGN)
    print("sign", SIGN, "NMAX", NMAX, "P0", P0, "residue classes", len(Q), f"{time.time()-t0:.0f}s", flush=True)
    S = 1 << 22; nseg = 16; maxnear = 1 << 16
    best = {}; near_checked = 0; near_hits = []
    k0 = (KSTART // S) * S; it = 0
    while k0 < KMAX:
        of = np.full((nseg, NMAX + 1), -1, np.int64)
        nk = np.full((nseg, maxnear), -1, np.int64); nm = np.zeros((nseg, maxnear), np.int64)
        seg(k0, nseg, S, Q, R, J, NMAX, of, nk, nm, maxnear, MAXMISS)
        for s in range(nseg):
            if nk[s, maxnear - 1] >= 0: print("WARNING near buffer overflow", flush=True)
            for c in range(maxnear):
                k = int(nk[s, c])
                if k < 0: break
                if k <= 1: continue
                near_checked += 1
                mm = int(nm[s, c])
                if all(nonsquarefree(k * k + SIGN * j) for j in range(NMAX + 1) if (mm >> j) & 1):
                    print("NEAR-HIT (large prime square) k", k, "missing mask", mm, flush=True)
                    near_hits.append(k)
                    for n in range(NMAX + 1):
                        if of[s, n] < 0 or k < of[s, n]: of[s, n] = k
        for n in range(NMAX + 1):
            if n in best: continue
            for s in range(nseg):
                if of[s, n] >= 0:
                    best[n] = int(of[s, n]); print(f"n={n} k={best[n]}  {time.time()-t0:.0f}s", flush=True); break
        k0 += nseg * S; it += 1
        if NMAX in best: break
        if it % 20 == 0:
            print(f"progress k<{k0:.4e} near_checked={near_checked} {time.time()-t0:.0f}s", flush=True)
    print("done: searched k <", k0, "from", (KSTART // S) * S, "; first hits", best, "; near_checked", near_checked, "; near_hits", near_hits)
