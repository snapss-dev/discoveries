"""A165075: fixed points of the base-7 Kaprekar map (digits sorted descending minus digits sorted ascending).

Remark tested (M. F. Hasler, Jul 17 2026): "All terms appear to be multiples of 48, and more precisely congruent
to -48 (mod 14*48), except for the initial 0."

Part 1 (own enumeration, numba): every fixed point with at most LMAX base-7 digits, found by running through all
        digit multisets of each length; compared with the published b-file (b165075.txt, by Joseph Myers).
Part 2 (exact integers, plain Python): each b-file term is re-tested with the definition K(n) = n, and the
        residues mod 48 and mod 672 are tabulated by parity of the number of base-7 digits.
Part 3: the divisibility statement proved on the page (odd length => multiple of 48) is tested for the
        Kaprekar image of random numbers, not only fixed points.  (That every fixed point is a multiple of 12 is
        asserted in part 2.)
"""
import os, random, time
from math import gcd
import numpy as np
from numba import njit

LMAX = 40
HERE = os.path.dirname(os.path.abspath(__file__))


@njit(cache=False)
def fixed_points_of_length(L, out, maxout):
    # all digit multisets (c0..c6), sum L; number = desc - asc; fixed iff the digits of the difference are the multiset
    cnt = np.zeros(7, dtype=np.int64)
    desc = np.zeros(L, dtype=np.int64)
    diff = np.zeros(L, dtype=np.int64)
    c2 = np.zeros(7, dtype=np.int64)
    nout = 0
    # iterate compositions of L into 7 parts with an odometer
    cnt[0] = L
    while True:
        # desc[0] is the most significant digit
        p = 0
        for d in range(6, -1, -1):
            for _ in range(cnt[d]):
                desc[p] = d
                p += 1
        # subtract asc (= desc reversed) from desc, least significant position first
        borrow = 0
        for i in range(L - 1, -1, -1):
            x = desc[i] - desc[L - 1 - i] - borrow
            if x < 0:
                x += 7
                borrow = 1
            else:
                borrow = 0
            diff[i] = x
        ok = diff[0] != 0 or L == 1
        if ok:
            for d in range(7):
                c2[d] = 0
            for i in range(L):
                c2[diff[i]] += 1
            for d in range(7):
                if c2[d] != cnt[d]:
                    ok = False
                    break
        if ok and nout < maxout:
            for i in range(L):
                out[nout, i] = diff[i]
            nout += 1
        # next composition
        i = 0
        while i < 6 and cnt[i] == 0:
            i += 1
        if i == 6:
            break
        v = cnt[i]
        cnt[i] = 0
        cnt[0] = v - 1
        cnt[i + 1] += 1
    return nout


def digits7(n):
    d = []
    while n:
        d.append(n % 7)
        n //= 7
    return d[::-1] or [0]


def kaprekar7(n):
    d = sorted(digits7(n))
    asc = 0
    for x in d:
        asc = asc * 7 + x
    desc = 0
    for x in reversed(d):
        desc = desc * 7 + x
    return desc - asc


t0 = time.time()
bfile = [int(l.split()[1]) for l in open(os.path.join(HERE, "b165075.txt")) if l.strip() and not l.startswith("#")]
print("b-file: %d terms, the largest with %d base-7 digits" % (len(bfile), len(digits7(bfile[-1]))))

# ---- Part 1
mine = []
for L in range(1, LMAX + 1):
    out = np.zeros((2000, L), dtype=np.int64)
    k = fixed_points_of_length(L, out, 2000)
    assert k < 2000
    for r in range(k):
        v = 0
        for x in out[r]:
            v = v * 7 + int(x)
        mine.append(v)
mine = sorted(set(mine))
ref = [t for t in bfile if len(digits7(t)) <= LMAX]
print("part 1: own enumeration finds %d fixed points with at most %d base-7 digits; the b-file has %d; identical: %s"
      % (len(mine), LMAX, len(ref), mine == ref))
assert mine == ref
print("        a(17) =", mine[16], "= base 7", "".join(map(str, digits7(mine[16]))),
      "; mod 48 =", mine[16] % 48, "; mod 672 =", mine[16] % 672)
assert mine[16] == 77852854787906052 and mine[16] % 48 == 36
first48 = next(i for i, t in enumerate(mine) if t % 48)
first672 = next(i for i, t in enumerate(mine) if i > 0 and t % 672 != 624)
first48only = next(i for i, t in enumerate(mine) if i > 0 and t % 48 == 0 and t % 672 != 624)
print("        first term that is not a multiple of 48: a(%d) = %d" % (first48 + 1, mine[first48]))
print("        first nonzero term not == -48 (mod 672): a(%d) = %d" % (first672 + 1, mine[first672]))
print("        first multiple of 48 that is not == -48 (mod 672): a(%d) = %d (mod 672 = %d)"
      % (first48only + 1, mine[first48only], mine[first48only] % 672))

# ---- Part 2
assert all(kaprekar7(t) == t for t in bfile), "every b-file term is a fixed point"
stats = {0: [0, 0, 0, 0], 1: [0, 0, 0, 0]}
g = {0: 0, 1: 0}
for t in bfile[1:]:
    par = len(digits7(t)) % 2
    s = stats[par]
    s[0] += 1
    s[1] += (t % 48 != 0)
    s[2] += (t % 672 != 624)
    g[par] = gcd(g[par], t)
print("part 2: all %d b-file terms satisfy K(n) = n (exact integers)" % len(bfile))
for par, name in ((1, "odd "), (0, "even")):
    s = stats[par]
    print("        %s number of base-7 digits: %4d terms, %4d not multiples of 48, %4d not == -48 (mod 672), gcd of all = %d"
          % (name, s[0], s[1], s[2], g[par]))
assert stats[1][1] == 0 and stats[1][2] == 0 and stats[0][1] > 0
assert all(t % 12 == 0 for t in bfile) and g[0] == 12 and g[1] == 48
print("        every term is a multiple of 12")
print("        in all: %d terms not multiples of 48, %d nonzero terms not == -48 (mod 672)"
      % (stats[0][1] + stats[1][1], stats[0][2] + stats[1][2]))

# ---- Part 3
random.seed(1)
for _ in range(200000):
    L = random.randrange(1, 60)
    n = random.randrange(7 ** (L - 1), 7 ** L)
    k = kaprekar7(n)
    assert k % 6 == 0
    if L % 2 == 1:
        assert k % 48 == 0
print("part 3: K(n) is a multiple of 6 for 200000 random n, and a multiple of 48 whenever n has an odd number of digits")
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
