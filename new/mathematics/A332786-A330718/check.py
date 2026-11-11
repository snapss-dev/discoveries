"""A332786: a(n) = numerator(-1/n + Sum_{k=1..n} 2^(k-1)/k).

Claim checked here: for p = 16843 and n = p^2 = 283686649, the p-adic valuation of a(n) is exactly 2.
So the composite number n divides a(n) (n is a second "weak pseudoprime" after 49), and n^2 does not.
The same is checked for the companion entry A330718, b(n) = numerator(Sum_{k=1..n} (2^k-2)/k).
Half of that rational, Sum (2^(k-1)-1)/k, differs from the rational above by the harmonic number
H(n-1): A is replaced by A - Sum 1/k and B by B - Sum 1/j. The factor 2 does not change the valuation
at an odd prime.

Method. Let S(n) = -1/n + Sum 2^(k-1)/k and T = p^2 S(p^2). Then T is a p-adic integer and
    T = p^2 A + p B + C - 1,
    A = Sum over k <= p^2 with p not dividing k of 2^(k-1)/k     (needed modulo p^3),
    B = Sum over j < p of 2^(pj-1)/j                              (needed modulo p^4),
    C = 2^(p^2-1)                                                 (needed modulo p^5),
and v_p(a(p^2)) = v_p(T) - 2 as soon as v_p(T) >= 2 (the denominator of S(p^2) carries p^2 at most,
and the numerator in lowest terms keeps every power of p beyond that).

A has 2.8 * 10^8 terms. It is summed with vectorised 64-bit integers; products of two residues below
p^3 < 2^43 are formed in 15-bit limbs so that nothing exceeds 2^59. Inverses of k come from a table of
inverses modulo p, lifted twice by Newton's step. The file check.gp does the same sum in PARI/GP with
arbitrary-precision modular arithmetic and a single plain loop; the two share no code.

Run time: about one to three minutes.
"""
import random
import sys
import time
from fractions import Fraction

import numpy as np

U = np.uint64
MASK15 = U(32767)
S15 = U(15)
S30 = U(30)


def mulmod(a, b, m):
    """a * b mod m for uint64 arrays (or scalars) with a, b < m < 2^43."""
    b2 = b >> S30
    b1 = (b >> S15) & MASK15
    b0 = b & MASK15
    r = (a * b2) % m
    r = ((r << S15) + a * b1) % m
    r = ((r << S15) + a * b0) % m
    return r


def sum_A(p, chunk=1 << 20):
    """Sums over k = 1..p^2, p not dividing k, of 2^(k-1)/k and of 1/k, modulo p^3 (Python ints)."""
    n = p * p
    m2 = U(p * p)
    m3i = p ** 3
    m3 = U(m3i)
    assert m3i < 2 ** 43
    invp = np.zeros(p, dtype=np.uint64)
    for r in range(1, p):
        invp[r] = pow(r, -1, p)
    size = min(chunk, n)
    tbl = np.empty(size, dtype=np.uint64)          # 2^i mod p^3
    v = 1
    for i in range(size):
        tbl[i] = v
        v = (v * 2) % m3i
    total = 0
    harm = 0
    two = U(2)
    for k0 in range(1, n + 1, size):
        k = np.arange(k0, min(k0 + size, n + 1), dtype=np.uint64)
        keep = (k % U(p)) != 0
        x0 = invp[(k % U(p)).astype(np.int64)]
        x0[~keep] = 1
        t = ((k % m2) * x0) % m2
        x1 = (x0 * ((two + m2 - t) % m2)) % m2      # inverse of k modulo p^2
        t = (k * x1) % m3
        x2 = mulmod((two + m3 - t) % m3, x1, m3)    # inverse of k modulo p^3 (x1 < 2^30)
        start = U(pow(2, k0 - 1, m3i))
        pw = mulmod(tbl[:len(k)], start, m3)        # 2^(k-1) modulo p^3
        term = mulmod(pw, x2, m3)
        total += int(term[keep].sum(dtype=np.uint64))
        harm += int(x2[keep].sum(dtype=np.uint64))
    return total % m3i, harm % m3i


def valuation_T(p):
    """(v_p(T), unit residue) for A332786 and for A330718; valuations capped at 5."""
    n = p * p
    A, AH = sum_A(p)
    B = sum(pow(2, p * j - 1, p ** 4) * pow(j, -1, p ** 4) for j in range(1, p)) % p ** 4
    BH = sum(pow(j, -1, p ** 4) for j in range(1, p)) % p ** 4
    C = pow(2, n - 1, p ** 5)
    out = []
    for T in ((p * p * A + p * B + C - 1) % p ** 5, (p * p * (A - AH) + p * (B - BH) + C - 1) % p ** 5):
        v = 0
        while v < 5 and T % p == 0:
            T //= p
            v += 1
        out.append((v, T % p))
    return out


def exact_b(n):
    return sum(Fraction(2 ** k - 2, k) for k in range(1, n + 1)).numerator


def exact_a(n):
    s = Fraction(-1, n) + sum(Fraction(2 ** (k - 1), k) for k in range(1, n + 1))
    return s.numerator


def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


ok = True
print("1. mulmod against Python integers (10000 random pairs below 16843^3)")
m = 16843 ** 3
rng = random.Random(1)
a = np.array([rng.randrange(m) for _ in range(10000)], dtype=np.uint64)
b = np.array([rng.randrange(m) for _ in range(10000)], dtype=np.uint64)
good = all(int(x) * int(y) % m == int(z) for x, y, z in zip(a, b, mulmod(a, b, U(m))))
print("   ", "PASS" if good else "FAIL")
ok &= good

print("2. first terms of A332786 and A330718 against the entries' data")
data = [0, 3, 3, 61, 25, 137, 343, 32663, 2357, 74689, 66671, 5299069, 2416531, 115545821]
datab = [0, 1, 3, 13, 25, 137, 245, 871, 517, 4629, 8349, 45517, 83317, 1074679, 1992127]
good = [exact_a(n) for n in range(1, len(data) + 1)] == data and [exact_b(n) for n in range(1, len(datab) + 1)] == datab
print("   ", "PASS" if good else "FAIL")
ok &= good

print("3. the modular method against exact rational arithmetic, n = p^2")
print("         A332786: v_p(a(p))  v_p(a(p^2))  modular   |  A330718: v_p(b(p))  v_p(b(p^2))  modular")
for p in (5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43):
    (v, _), (w, _) = valuation_T(p)
    e1, e2 = vp(exact_a(p), p), vp(exact_a(p * p), p)
    f1, f2 = vp(exact_b(p), p), vp(exact_b(p * p), p)
    good = (v - 2 == e2) and (w - 2 == f2)
    ok &= good
    print("   p=%2d            %d           %d           %d       |            %d           %d           %d     %s%s" % (
        p, e1, e2, v - 2, f1, f2, w - 2, "PASS" if good else "FAIL", "   <- 49 divides a(49)" if p == 7 else ""))

print("4. p = 16843 (the smaller Wolstenholme prime), n = p^2 = %d" % (16843 ** 2))
t0 = time.time()
(v, unit), (w, unit2) = valuation_T(16843)
print("    A332786: v_p(T) = %d, T / p^%d = %d (mod p), so v_p(a(n)) = %d      [%.0f s]" % (v, v, unit, v - 2, time.time() - t0))
good = (v == 4)
ok &= good
print("   ", "PASS: n divides a(n), n^2 does not" if good else "FAIL")
print("    A330718: v_p(T') = %d, T' / p^%d = %d (mod p), so v_p(b(n)) = %d" % (w, w, unit2, w - 2))
good = (w == 4)
ok &= good
print("   ", "PASS: n divides b(n), n^2 does not" if good else "FAIL (see the value above)")

LIMIT = 20000
print("5. exhaustive search for composite m <= %d with m | a(m) or m | b(m), exact rational arithmetic" % LIMIT)
t0 = time.time()
run = Fraction(0)
runb = Fraction(0)
hits, hitsb = [], []
prime = set(q for q in range(2, LIMIT + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1)))
for m_ in range(1, LIMIT + 1):
    run += Fraction(2 ** (m_ - 1), m_)
    runb += Fraction(2 ** m_ - 2, m_)
    if m_ > 3 and m_ not in prime:
        if (run - Fraction(1, m_)).numerator % m_ == 0:
            hits.append(m_)
        if runb.numerator % m_ == 0:
            hitsb.append(m_)
print("    A332786, composite m <= %d dividing a(m):" % LIMIT, hits, "     [%.0f s]" % (time.time() - t0))
print("    A330718, composite m <= %d dividing b(m):" % LIMIT, hitsb)
good = hits == [49] and hitsb == []
ok &= good
print("   ", "PASS: 49 is the only one for A332786, none for A330718, in this range" if good else "FAIL")

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
