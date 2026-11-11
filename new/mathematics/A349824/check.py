"""A349824: a(n) = Omega(n) * sopfr(n)  (number of prime factors times their sum, both with repetition).
Claim checked: n divides a(n) exactly when n is prime or n is one of 1, 4, 16, 27, 30.

Method 1: segmented sieve (numba) for every n <= N.
Method 2: trial-division factorisation in plain Python for n <= M (shares no code with method 1).
The proof needs only n <= 7776; both methods go far beyond.  Also checks the inequalities used in the proof.
"""
import time
import numpy as np
from numba import njit

N = 1_000_000_000
M = 200_000

@njit(cache=False)
def scan(N, primes, seg):
    out = np.zeros(100, dtype=np.int64); no = 0
    nprime = 0; nprime_div = 0
    rem = np.empty(seg, dtype=np.int64); om = np.empty(seg, dtype=np.int64); sp = np.empty(seg, dtype=np.int64)
    lo = 1
    while lo <= N:
        hi = min(lo + seg - 1, N); L = hi - lo + 1
        for i in range(L):
            rem[i] = lo + i; om[i] = 0; sp[i] = 0
        for p in primes:
            if p * p > hi: break
            st = ((lo + p - 1) // p) * p
            for x in range(st, hi + 1, p):
                i = x - lo; r = rem[i]
                while r % p == 0:
                    r //= p; om[i] += 1; sp[i] += p
                rem[i] = r
        for i in range(L):
            n = lo + i
            if rem[i] > 1:
                om[i] += 1; sp[i] += rem[i]
            a = om[i] * sp[i]
            if om[i] == 1:
                nprime += 1
                if a % n == 0: nprime_div += 1
            elif a % n == 0:
                if no < 100: out[no] = n
                no += 1
        lo = hi + 1
    return out[:min(no, 100)], no, nprime, nprime_div

def primes_upto(n):
    s = np.ones(n + 1, dtype=bool); s[:2] = False
    for i in range(2, int(n ** 0.5) + 1):
        if s[i]: s[i * i::i] = False
    return np.nonzero(s)[0].astype(np.int64)

t0 = time.time()
pr = primes_upto(int(N ** 0.5) + 2)
exc, no, nprime, nprime_div = scan(N, pr, 1 << 20)
exc = [int(v) for v in exc]
print("method 1 (sieve), n <= %d: non-prime n with n | a(n): %s" % (N, exc))
print("   primes seen: %d (pi(10^9) = 50847534), all with n | a(n): %s" % (nprime, nprime == nprime_div))
assert exc == [1, 4, 16, 27, 30] and no == 5 and nprime == nprime_div
if N == 10 ** 9: assert nprime == 50847534

def fac(n):
    f = []; p = 2
    while p * p <= n:
        while n % p == 0: f.append(p); n //= p
        p += 1
    if n > 1: f.append(n)
    return f
data = [0,0,2,3,8,5,10,7,18,12,14,11,21,13,18,16,32,17,24,19,27,20,26,23,36,20,30,27,33,29,30,31,50,28,38,24,40,37,42,
        32,44,41,36,43,45,33,50,47,55,28,36,40,51,53,44,32,52,44,62,59,48,61,66,39,72,36,48,67,63,52,42,71,60,73]
exc2 = []; maxratio = 0
for n in range(1, M + 1):
    f = fac(n); a = len(f) * sum(f)
    if n < len(data): assert a == data[n]
    if len(f) != 1 and a % n == 0: exc2.append(n)
    if len(f) == 1: assert a == n
    if len(f) >= 2:
        P = f[-1]; m = n // P; k = len(f)
        assert sum(f) <= k * P and m >= 2 ** (k - 1) and sum(f[:-1]) <= m      # inequalities used in the proof
        if a % n == 0:
            assert m <= k * k and k <= 6 and (k * sum(f[:-1])) % P == 0 and n <= 7776
print("method 2 (trial division), n <= %d: published terms reproduced; non-prime n with n | a(n): %s" % (M, exc2))
assert exc2 == [1, 4, 16, 27, 30]
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
