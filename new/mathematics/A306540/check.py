"""A306540: least k >= 1 such that n^k starts with 99 or 100.  Checks that a(n) <= 231 and that 231 is attained.

Method 1 (exact): big-integer powers, tested with integer comparisons only.
Method 2 (independent): fractional parts of k*log10(n) in floating point, with every case that comes
within 1e-9 of a window edge re-decided by method 1.
Also prints the constants used in the proof, with certified interval arithmetic (python-flint), if available.
"""
import math, sys, time
import numpy as np

def starts_99_or_100(v):
    # v >= 1 integer; leading digits of v are 99... or 100... (trailing zeros after the decimal point allowed,
    # as in the entry: 1 = 1.00, 10 = 10.0).  Same test as the entry's Maple: r < 101/100 or r >= 99/10.
    L = len(str(v)) - 1
    p = 10 ** L
    return 100 * v < 101 * p or 10 * v >= 99 * p

def a_exact(n, kmax=100000):
    v = 1
    for k in range(1, kmax + 1):
        v *= n
        if starts_99_or_100(v):
            return k
    raise RuntimeError("no k found for n=%d" % n)

t0 = time.time()
# ---- constants of the proof
try:
    from flint import arb, ctx
    ctx.prec = 200
    lo = 1 - (arb(99) / 10).log() / arb(10).log()     # 1 - log10(9.9)
    hi = (arb(101) / 100).log() / arb(10).log()        # log10(1.01)
    print("1 - log10(9.9) =", lo.str(20), "  log10(1.01) =", hi.str(20))
    print("1/232 =", (arb(1) / 232).str(20), "  1/231 =", (arb(1) / 231).str(20))
    assert (arb(1) / 232 < hi) and (arb(1) / 232 < lo), "Dirichlet bound with Q = 231 fits inside the window"
    assert (arb(1) / 231 > hi), "Q = 230 would not be enough by this argument"
    print("certified: 1/232 < log10(1.01) < 1/231 and 1/232 < 1 - log10(9.9)")
except ImportError:
    print("python-flint not installed; skipping certified constants")
# rational certificate, integers only: 1.01^232 > 10  and  9.9^232 < 10^231 ... i.e. 1/232 < log10(1.01), 1/232 < 1-log10(9.9)
assert 101 ** 232 > 10 * 100 ** 232
assert 99 ** 232 < 10 ** 463          # 9.9^232 < 10^231
assert 101 ** 231 < 10 * 100 ** 231
print("integer certificate: 1.01^232 > 10 > 1.01^231, and 9.9^232 < 10^231")

# ---- method 1: exact, n <= N1
N1 = 30000
ex = [0] * (N1 + 1)
for n in range(1, N1 + 1):
    ex[n] = a_exact(n)
data = [1,93,153,98,93,9,71,31,153,1,145,101,79,130,159,49,13,47,61,93,90,73,47,192,98,147,51,123,93,153,116,97,27,
        143,68,151,44,188,22,98,31,69,30,115,124,86,61,160,71,93,106,81,29,71,104,139,127,93,48,9,177,53,5,129,155,133,23,197,211]
assert ex[1:len(data) + 1] == data, "published terms reproduced"
print("method 1 (exact integers): published terms a(1..%d) reproduced; max a(n) for n <= %d is %d" % (len(data), N1, max(ex[1:])))
print("  n <= %d with a(n) = 231:" % N1, [n for n in range(1, N1 + 1) if ex[n] == 231])
assert max(ex[1:]) == 231 and ex[101] == 231

# ---- method 2: floating point with exact fallback, n <= N2
N2 = 20_000_000
LO = math.log10(9.9); HI = math.log10(1.01); EPS = 1e-9
worst = 0; hist231 = 0; nfallback = 0; mism = 0
B = 2_000_000
for start in range(1, N2 + 1, B):
    n = np.arange(start, min(start + B, N2 + 1), dtype=np.int64)
    al = np.log10(n.astype(np.float64))
    res = np.zeros(len(n), dtype=np.int32)
    doubt = np.zeros(len(n), dtype=bool)
    todo = np.ones(len(n), dtype=bool)
    for k in range(1, 232):
        f = k * al; f -= np.floor(f)
        near = (np.abs(f - LO) < EPS) | (np.abs(f - HI) < EPS) | (f < EPS) | (f > 1 - EPS)
        doubt |= (near & todo)
        hit = ((f >= LO) | (f < HI)) & todo
        res[hit] = k; todo &= ~hit
    for i in np.nonzero(doubt | todo)[0]:
        res[i] = a_exact(int(n[i])); nfallback += 1
    worst = max(worst, int(res.max())); hist231 += int((res == 231).sum())
    if start <= N1:
        m = min(N1, int(n[-1]))
        mism += sum(1 for j in range(start, m + 1) if ex[j] != int(res[j - start]))
print("method 2 (float + exact fallback on %d doubtful n): max a(n) for n <= %d is %d; a(n) = 231 for %d values of n" % (nfallback, N2, worst, hist231))
print("methods 1 and 2 disagree on %d of the first %d n" % (mism, N1))
assert worst == 231 and mism == 0
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
