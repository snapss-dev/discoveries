"""Large-prime pass for "none of k^2 + s*j (j = 1..n) squarefree", s = SIGN.
Lists every k <= K for which some prime p >= P0 has p^2 | k^2 + s*j for some 1 <= j <= n, then tests each such k exactly.
 (A) P0 <= p <= P1: for each j the two roots of x^2 = -s*j mod p^2 (Tonelli-Shanks, Hensel); a root x <= K gives k = x
     and, when p^2 <= K, also x + i*p^2.
 (B) p > P1: write k^2 + s*j = m*p^2, so 1 <= m <= (K^2+n)/P1^2 and (k, p) solves x^2 - m*y^2 = -s*j =: N.
     m square: no solution with y > P1 (|x - c*y| * (x + c*y) = |N| <= n).  m > n^2: |N| < sqrt(m), so x/y (reduced) is a
     convergent of sqrt(m) (Legendre); all convergents with numerator <= K are listed.  m <= n^2: all solutions from
     the fundamental solutions (Nagell's bounds) times powers of the fundamental unit.
     Here y need not be prime: the list is a superset.
Usage: sqlarge.py SIGN K P0 P1 NMAX [validate]"""
import sys, time, math
import numpy as np
import numba
from numba import njit, prange
import flint

SIGN = int(sys.argv[1]); K = int(float(sys.argv[2])); P0 = int(float(sys.argv[3])); P1 = int(float(sys.argv[4])); NMAX = int(sys.argv[5])
VALIDATE = len(sys.argv) > 6 and sys.argv[6] == "validate"
RUNS = int(sys.argv[6][4:]) if len(sys.argv) > 6 and sys.argv[6].startswith("runs") else 0
numba.set_num_threads(4)

@njit(cache=True)
def pw(a, e, m):
    r = 1; a %= m
    while e > 0:
        if e & 1: r = r * a % m
        a = a * a % m; e >>= 1
    return r

@njit(cache=True)
def sqrt_p(a, p):
    # a a nonzero quadratic residue mod the odd prime p < 2^31
    if p % 4 == 3: return pw(a, (p + 1) // 4, p)
    q = p - 1; s = 0
    while q % 2 == 0: q //= 2; s += 1
    z = 2
    while pw(z, (p - 1) // 2, p) != p - 1: z += 1
    c = pw(z, q, p); t = pw(a, q, p); r = pw(a, (q + 1) // 2, p); M = s
    while t != 1:
        i = 0; tt = t
        while tt != 1: tt = tt * tt % p; i += 1
        b = c
        for _ in range(M - i - 1): b = b * b % p
        M = i; c = b * b % p; t = t * c % p; r = r * b % p
    return r

@njit(parallel=True, cache=True)
def roots_block(primes, K, NMAX, SIGN, outk, outj, cnt, cap):
    for i in prange(len(primes)):
        p = primes[i]; q = p * p; c = 0
        for j in range(1, NMAX + 1):
            a = (-SIGN * j) % p
            if a == 0: continue
            if pw(a, (p - 1) // 2, p) != 1: continue
            r0 = sqrt_p(a, p)
            for sg in range(2):
                r = r0 if sg == 0 else p - r0
                f = (r * r + SIGN * j) // p
                t = ((-f) % p) * pw(2 * r % p, p - 2, p) % p
                x = r + p * t
                while x <= K:
                    if c < cap: outk[i, c] = x; outj[i, c] = j
                    c += 1
                    x += q
        cnt[i] = c

def primes_seg(lo, hi):
    lim = int(hi ** 0.5) + 1
    s = np.ones(lim + 1, np.bool_); s[:2] = False
    for i in range(2, int(lim ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    isp = np.ones(hi - lo, np.bool_)
    for p in np.nonzero(s)[0]:
        p = int(p); st = max(p * p, ((lo + p - 1) // p) * p)
        isp[st - lo::p] = False
    return (np.nonzero(isp)[0] + lo).astype(np.int64)

def part_A():
    hits = {}
    lo = max(P0, 3); npr = 0; B = 1 << 21
    cap = 2 * NMAX * (K // (P0 * P0) + 2)
    while lo <= P1:
        hi = min(lo + B, P1 + 1)
        pr = primes_seg(lo, hi); npr += len(pr)
        capb = 2 * NMAX * (K // (lo * lo) + 2)
        outk = np.zeros((len(pr), capb), np.int64); outj = np.zeros((len(pr), capb), np.int64); cnt = np.zeros(len(pr), np.int64)
        roots_block(pr, K, NMAX, SIGN, outk, outj, cnt, capb)
        assert cnt.max(initial=0) <= capb
        for i in np.nonzero(cnt)[0]:
            for c in range(cnt[i]):
                hits.setdefault(int(outk[i, c]), set()).add(int(outj[i, c]))
        lo = hi
    return hits, npr

def isqrt_exact(v):
    r = math.isqrt(v)
    return r if r * r == v else -1

def pell_unit(m):
    a0 = math.isqrt(m); mm = 0; d = 1; a = a0
    h2, h1 = 1, a0; k2, k1 = 0, 1
    while h1 * h1 - m * k1 * k1 != 1:
        mm = d * a - mm; d = (m - mm * mm) // d; a = (a0 + mm) // d
        h2, h1 = h1, a * h1 + h2; k2, k1 = k1, a * k1 + k2
    return h1, k1

def part_B():
    hits = {}
    mmax = (K * K + NMAX) // (P1 * P1) + 1
    nconv = 0
    for m in range(1, mmax + 1):
        a0 = math.isqrt(m)
        if a0 * a0 == m: continue
        if m > NMAX * NMAX:
            mm = 0; d = 1; a = a0
            h2, h1 = 1, a0; k2, k1 = 0, 1
            while h1 <= K:
                N = h1 * h1 - m * k1 * k1
                nconv += 1
                g = 1
                while abs(N) * g * g <= NMAX:
                    j = -SIGN * N * g * g      # k^2 + s*j = m p^2  <=>  x^2 - m y^2 = -s*j
                    if 1 <= j <= NMAX and g * h1 <= K and g * k1 > P1:
                        hits.setdefault(g * h1, set()).add(j)
                    g += 1
                    if N == 0: break
                mm = d * a - mm; d = (m - mm * mm) // d; a = (a0 + mm) // d
                h2, h1 = h1, a * h1 + h2; k2, k1 = k1, a * k1 + k2
        else:
            t, u = pell_unit(m)
            for j in range(1, NMAX + 1):
                N = -SIGN * j
                if N > 0:
                    vb = int(u * math.sqrt(N) / math.sqrt(2 * (t + 1))) + 2
                else:
                    vb = int(u * math.sqrt(-N) / math.sqrt(2 * (t - 1))) + 2
                v = np.arange(0, vb + 1, dtype=object) if vb < 10 else None
                # candidates v with N + m v^2 a perfect square
                vs = np.arange(0, vb + 1, dtype=np.float64)
                cand = np.nonzero(np.abs(np.sqrt(np.maximum(N + m * vs * vs, 0)) - np.rint(np.sqrt(np.maximum(N + m * vs * vs, 0)))) < 1e-3)[0]
                for v0 in cand:
                    v0 = int(v0); w = N + m * v0 * v0
                    if w < 0: continue
                    u0 = isqrt_exact(w)
                    if u0 < 0: continue
                    for su in (1, -1):
                        for tu in (u, -u):
                            x, y = su * u0, v0
                            while abs(x) <= K * (t + abs(u) * m + 1):
                                if 2 <= abs(x) <= K and abs(y) > P1:
                                    assert x * x - m * y * y == N
                                    hits.setdefault(abs(x), set()).add(j)
                                x, y = x * t + m * y * tu, x * tu + y * t
                                if abs(x) > K and abs(y) > 0 and abs(x) > abs(su * u0):
                                    if abs(x) > K: break
    return hits, mmax, nconv

def nonsquarefree(x):
    if x == 0: return True
    x = abs(x)
    for p in (4, 9, 25, 49, 121, 169, 289, 361):
        if x % p == 0: return True
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
    hA, npr = part_A()
    print(f"(A) primes {P0}..{P1}: {npr} primes, {len(hA)} values k, {sum(len(v) for v in hA.values())} pairs (k,j), {time.time()-t0:.0f}s", flush=True)
    hB, mmax, nconv = part_B()
    print(f"(B) m <= {mmax}: {len(hB)} values k, {sum(len(v) for v in hB.values())} pairs (k,j), {nconv} convergents, {time.time()-t0:.0f}s", flush=True)
    if VALIDATE:
        # brute force: all (k, j) with p^2 | k^2 + s*j for a prime p >= P0
        brute = set(); bruteB = set()
        pr = [p for p in range(2, int((K * K + NMAX) ** 0.5) + 2) if all(p % d for d in range(2, int(p ** 0.5) + 1))]
        for k in range(2, K + 1):
            for j in range(1, NMAX + 1):
                v = k * k + SIGN * j
                if v <= 0: continue
                for p in pr:
                    if p * p > v: break
                    if p >= P0 and v % (p * p) == 0:
                        brute.add((k, j))
                        if p > P1: bruteB.add((k, j))
        got = set((k, j) for k, s in hA.items() for j in s) | set((k, j) for k, s in hB.items() for j in s)
        gotA = set((k, j) for k, s in hA.items() for j in s if k * k + SIGN * j > 0)
        bruteA = set()
        for (k, j) in brute:
            v = k * k + SIGN * j
            if any(P0 <= p <= P1 and v % (p * p) == 0 for p in pr if p % 2 == 1 or P0 > 2): bruteA.add((k, j))
        print("validate: brute pairs", len(brute), "missing from lists", len(brute - got), "; A exact match", gotA == bruteA,
              "; B superset of brute(p>P1)", bruteB <= set((k, j) for k, s in hB.items() for j in s), len(bruteB))
        sys.exit()
    allk = sorted(set(hA) | set(hB))
    if RUNS:
        # A218049-type question (SIGN = +1, NMAX = 1): runs of RUNS consecutive k with k^2+1 non-squarefree
        # that contain a k whose square factor is p^2 with p >= P0
        found = []; longest = 0
        for k in allk:
            if not nonsquarefree(k * k + 1):
                print('BAD', k, k * k + 1, flint.fmpz(k * k + 1).factor(), sorted(hA.get(k, [])), sorted(hB.get(k, [])), flush=True); continue
            a = k
            while a > 1 and nonsquarefree((a - 1) ** 2 + 1): a -= 1
            b = k
            while nonsquarefree((b + 1) ** 2 + 1): b += 1
            longest = max(longest, b - a + 1)
            if b - a + 1 >= RUNS: found.append((a, b))
        print(f"touched k: {len(allk)}; longest run through a touched k: {longest}; runs of length >= {RUNS}: {sorted(set(found))}; {time.time()-t0:.0f}s")
        sys.exit()
    sols = []
    for k in allk:
        if all(nonsquarefree(k * k + SIGN * j) for j in range(1, NMAX + 1)):
            sols.append(k); print("k with all of j=1..%d non-squarefree and a square of a prime >= P0:" % NMAX, k, flush=True)
    print(f"touched k: {len(allk)}; solutions among them (k <= {K}): {sols}; {time.time()-t0:.0f}s")
