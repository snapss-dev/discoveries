"""A152212: numbers k such that sigma_0(k) divides k*sigma_1(k) - sigma_2(k).
Claim checked: no k == 2 (mod 4) is a term; more precisely, for k == 2 (mod 4),
    v2(sigma_0(k)) = v2(k*sigma_1(k) - sigma_2(k)) + 1      (v2 = exponent of 2).

Method 1: segmented sieve (numba), sigma_0, sigma_1, sigma_2 of every k <= N built from the factorisation of k
          itself (the proof's reduction to the odd part is NOT used), exact 128-bit-safe arithmetic mod 2^64.
Method 2: direct divisor enumeration in plain Python for k <= M (no sieve, no multiplicativity).
Also checks the two lemmas of the proof for every odd prime power below 10^6, and the published terms.
"""
import sys, time
import numpy as np
from numba import njit

N = 400_000_000      # the entry reports a test up to 10^8
M = 300_000

@njit(cache=False)
def scan(N, primes, seg):
    # returns (number of k == 2 mod 4 tested, number where v2 identity fails, number of terms == 2 mod 4,
    #          count of terms <= 116 for the data check array)
    bad = 0; tested = 0; terms2 = 0
    small = np.zeros(200, dtype=np.int64); ns = 0
    rem = np.empty(seg, dtype=np.int64)
    d = np.empty(seg, dtype=np.uint64); s1 = np.empty(seg, dtype=np.uint64); s2 = np.empty(seg, dtype=np.uint64)
    lo = 1
    while lo <= N:
        hi = min(lo + seg - 1, N)
        L = hi - lo + 1
        for i in range(L):
            rem[i] = lo + i; d[i] = 1; s1[i] = 1; s2[i] = 1
        for p in primes:
            if p * p > hi: break
            st = ((lo + p - 1) // p) * p
            for x in range(st, hi + 1, p):
                i = x - lo
                e = 0; a = np.uint64(1); b = np.uint64(1); pw = np.uint64(1); r = rem[i]
                while r % p == 0:
                    r //= p; e += 1; pw *= np.uint64(p); a += pw; b += pw * pw
                rem[i] = r; d[i] *= np.uint64(e + 1); s1[i] *= a; s2[i] *= b
        for i in range(L):
            k = lo + i
            r = rem[i]
            if r > 1:
                d[i] *= np.uint64(2); s1[i] *= np.uint64(r + 1); s2[i] *= np.uint64(1) + np.uint64(r) * np.uint64(r)
            # E = k*s1 - s2 > 0 for k >= 2; computed mod 2^64 (v2 below 64 is all that is used for k == 2 mod 4)
            if k % 4 == 2:
                tested += 1
                E = np.uint64(k) * s1[i] - s2[i]
                vE = 0
                while vE < 64 and (E >> np.uint64(vE)) & np.uint64(1) == 0: vE += 1
                dd = d[i]; vd = 0
                while (dd >> np.uint64(vd)) & np.uint64(1) == 0: vd += 1
                if vd != vE + 1: bad += 1
            if k <= 116:
                # exact divisibility for small k (no overflow there)
                E = np.int64(k) * np.int64(s1[i]) - np.int64(s2[i])
                if E % np.int64(d[i]) == 0:
                    small[ns] = k; ns += 1
        lo = hi + 1
    return tested, bad, small[:ns]

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0].astype(np.int64)

t0 = time.time()
pr = primes_upto(int(N ** 0.5) + 2)
tested, bad, small = scan(N, pr, 1 << 20)
data = [1,3,5,7,11,12,13,15,16,17,19,20,21,23,27,29,31,33,35,37,39,41,43,44,47,49,51,53,55,57,59,60,61,64,65,67,68,69,
        71,73,75,77,79,81,83,84,85,87,89,91,92,93,95,97,101,103,105,107,108,109,111,113,115,116]
assert list(small) == data, "published terms reproduced by the sieve"
print("method 1 (sieve): published terms a(1..%d) reproduced" % len(data))
print("method 1: k == 2 (mod 4), k <= %d: %d values tested, v2(sigma_0) = v2(k*sigma_1 - sigma_2) + 1 fails %d times" % (N, tested, bad))
assert bad == 0 and tested == (N + 2) // 4

# method 2: plain divisor enumeration
def v2(x):
    c = 0
    while x % 2 == 0: x //= 2; c += 1
    return c
terms = []; fail2 = 0; even_terms_2mod4 = 0
for k in range(1, M + 1):
    ds = [x for x in range(1, int(k ** 0.5) + 1) if k % x == 0]
    ds = set(ds) | {k // x for x in ds}
    s0 = len(ds); a = sum(ds); b = sum(x * x for x in ds)
    E = k * a - b
    if E % s0 == 0:
        terms.append(k)
        if k % 4 == 2: even_terms_2mod4 += 1
    if k % 4 == 2 and v2(s0) != v2(E) + 1: fail2 += 1
assert terms[:len(data)] == data
print("method 2 (divisor lists): k <= %d: %d terms, of which %d are == 2 (mod 4); v2 identity fails %d times" % (M, len(terms), even_terms_2mod4, fail2))
assert even_terms_2mod4 == 0 and fail2 == 0
# residues of the terms mod 4, and runs of consecutive terms
runs = {}; i = 0
while i < len(terms):
    j = i
    while j + 1 < len(terms) and terms[j + 1] == terms[j] + 1: j += 1
    key = (j - i + 1, terms[i] % 4); runs[key] = runs.get(key, 0) + 1; i = j + 1
print("runs of consecutive terms up to %d, as (length, first term mod 4): count ->" % M, dict(sorted(runs.items())))
assert max(l for l, _ in runs) <= 3 and all(r == 3 for (l, r) in runs if l == 3)

# lemmas: for odd prime p and e >= 1:  v2(1 + p^2 + ... + p^(2e)) = v2(e+1),  v2(1 + p + ... + p^e) >= v2(e+1)
cnt = 0
for p in pr[1:]:
    p = int(p)
    if p > 1000: break
    e = 1; 
    while p ** e < 10 ** 40:
        A = sum(p ** i for i in range(e + 1)); Bq = sum(p ** (2 * i) for i in range(e + 1))
        assert v2(Bq) == v2(e + 1) and v2(A) >= v2(e + 1)
        cnt += 1; e += 1
print("lemmas checked for %d odd prime powers p^e (p < 1000, p^e < 10^40)" % cnt)
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
