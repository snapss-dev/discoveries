"""A125314, n = 11: second, independent search (no roots modulo primes, no sieve).
S_11(k) = k^2 (k+1)^2 g(k) / 24,  g(k) = 2k^8+8k^7+4k^6-16k^5-5k^4+26k^3-3k^2-20k+10.
For every k in [LO, HI): compute z = P mod g(k) with a product/remainder tree (P = product of all primes <= PB, PB >= HI),
then g(k) | z^256 iff every prime factor of g(k) is <= PB (g(k) < 2^256).  If not, g(k) has a prime factor q > PB >= k,
q divides S_11(k) and not k!, so k fails.  The remaining k ("candidates") are examined one by one:
 - reject if gcd(g(k), product of the primes in (k, PB]) > 1 (a prime factor > k) or if k+1 is prime;
 - otherwise test the definition literally: (k! mod S)^11 mod S == 0 with S = Sum i^11.
Usage: a125314_batch.py LO HI PB"""
import sys, time, math
import numpy as np
from flint import fmpz

LO = int(float(sys.argv[1])); HI = int(float(sys.argv[2])); PB = int(float(sys.argv[3]))
assert PB >= HI - 1
t0 = time.time()

def g(k):
    return 2*k**8 + 8*k**7 + 4*k**6 - 16*k**5 - 5*k**4 + 26*k**3 - 3*k**2 - 20*k + 10

def primes_upto(N):
    s = np.ones(N + 1, np.bool_); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def prod_tree(v):
    tree = [v]
    while len(tree[-1]) > 1:
        l = tree[-1]
        tree.append([l[i] * l[i + 1] if i + 1 < len(l) else l[i] for i in range(0, len(l), 2)])
    return tree

PR = [int(p) for p in primes_upto(PB)]
P = prod_tree([fmpz(p) for p in PR])[-1][0]
print("primes <=", PB, ":", len(PR), "; bits of P:", int(P).bit_length(), f"{time.time()-t0:.0f}s", flush=True)

def literal(k):
    S = sum(i ** 11 for i in range(1, k + 1))
    f = 1
    for i in range(2, k + 1):
        f = f * i % S
    return pow(f, 11, S) == 0

B = 1 << 15
cands = []
k0 = max(LO, 2)
while k0 < HI:
    ks = list(range(k0, min(k0 + B, HI)))
    vals = [fmpz(g(k)) for k in ks]
    tree = prod_tree(vals)
    rems = [P % tree[-1][0]]
    for lvl in reversed(tree[:-1]):
        rems = [rems[i // 2] % lvl[i] for i in range(len(lvl))]
    for k, v, r in zip(ks, vals, rems):
        y = r
        for _ in range(8):
            y = y * y % v
        if y == 0:
            cands.append(k)
    k0 += B
print("range", LO, HI, "candidates (g(k) has no prime factor >", PB, "):", len(cands), f"{time.time()-t0:.0f}s", flush=True)
import bisect
sols = []
for k in cands:
    v = g(k)
    i = bisect.bisect_right(PR, k)
    if i < len(PR) and PR[i] == k + 1:
        print(k, "rejected: k+1 prime"); continue
    m = 1
    for p in PR[i:]:
        m = m * p % v
    d = math.gcd(m, v)
    if d > 1:
        print(k, "rejected: g(k) has a prime factor > k, gcd with the product of primes in (k, PB] =", d); continue
    ok = literal(k)
    print(k, "literal test of the definition:", ok, flush=True)
    if ok: sols.append(k)
print("solutions in [%d, %d):" % (LO, HI), sols, f"{time.time()-t0:.0f}s")
