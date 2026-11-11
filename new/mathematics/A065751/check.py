"""A065751: numbers whose decimal digits form nested and/or concatenated pairs 0-9, 1-8, 2-7, 3-6, 4-5
(well-formed bracket words with five kinds of brackets, no leading 0).

The entry carries an "Empirical g.f." (Colin Barker, Mar 29 2013).  This script expands that g.f. exactly and
compares it with the sequence computed from the definition in two independent ways:
  1. a stack parser run over every integer below 10^8;
  2. direct generation of all bracket words of length 2, 4, ..., 10 from the grammar.
"""
from fractions import Fraction
import time

OPEN = "01234"
CLOSE = {"9": "0", "8": "1", "7": "2", "6": "3", "5": "4"}


def is_term(s):
    if s[0] == "0":
        return False
    st = []
    for ch in s:
        if ch in OPEN:
            st.append(ch)
        else:
            if not st or st[-1] != CLOSE[ch]:
                return False
            st.pop()
    return not st


def words(m, memo={}):
    # all well-formed words with m pairs (leading 0 allowed), as strings
    if m == 0:
        return [""]
    if m in memo:
        return memo[m]
    res = []
    for i in range(m):                       # first pair encloses i pairs, followed by m-1-i pairs
        for a in words(i):
            for b in words(m - 1 - i):
                for o in range(5):
                    res.append(str(o) + a + str(9 - o) + b)
    memo[m] = res
    return res


def catalan(m):
    from math import comb
    return comb(2 * m, m) // (m + 1)


t0 = time.time()
# ---- method 1: brute force over the integers (only even digit sums of lengths matter, but test everything)
LIMIT = 10 ** 8
m1 = []
for k in range(1, 10 ** 6):
    if is_term(str(k)):
        m1.append(k)
# for 10^6 <= k < 10^8 use the necessary conditions "8 digits, first digit 1-4, last digit 5-9" to skip quickly
for k in range(10 ** 7, 5 * 10 ** 7):
    if k % 10 >= 5:
        s = str(k)
        if is_term(s):
            m1.append(k)
# ---- method 2: generation from the grammar
m2 = []
for m in range(1, 6):
    m2 += [int(w) for w in words(m) if w[0] != "0"]
m2.sort()
m2_8 = [x for x in m2 if x < LIMIT]
print("method 1 (parser over all k < 10^8): %d terms; method 2 (grammar, up to 8 digits): %d terms; identical: %s"
      % (len(m1), len(m2_8), m1 == m2_8))
assert m1 == m2_8
for m in range(1, 6):
    c = sum(1 for x in m2 if len(str(x)) == 2 * m)
    assert c == 4 * 5 ** (m - 1) * catalan(m)
    print("   terms with %2d digits: %6d = 4 * 5^%d * Catalan(%d)" % (2 * m, c, m - 1, m))

data = [18,27,36,45,1098,1188,1278,1368,1458,1809,1818,1827,1836,1845,2097,2187,2277,2367,2457,2709,2718,2727,2736,
        2745,3096,3186,3276,3366,3456,3609,3618,3627,3636,3645,4095,4185,4275,4365,4455,4509,4518,4527,4536]
assert m2[:len(data)] == data
print("published terms a(0..%d) reproduced" % (len(data) - 1))

# ---- the empirical g.f., expanded with exact rationals
# -9*(100x^19 + x^15 + 50x^14 - 10x^13 - 10x^12 - 10x^11 - 9x^10 - 156x^9 - 11x^8 - 11x^7 - 11x^6 - 12x^5 - 117x^4
#      - x^3 - x^2 - x - 2) / ((x-1)^2 (x+1)^2 (x^4-x^3+x^2-x+1)^2 (x^4+x^3+x^2+x+1))
def pmul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            r[i + j] += x * y
    return r

num = [0] * 20
for e, c in {19: 100, 15: 1, 14: 50, 13: -10, 12: -10, 11: -10, 10: -9, 9: -156, 8: -11, 7: -11, 6: -11, 5: -12,
             4: -117, 3: -1, 2: -1, 1: -1, 0: -2}.items():
    num[e] = -9 * c
den = [1]
for f in ([-1, 1], [-1, 1], [1, 1], [1, 1], [1, -1, 1, -1, 1], [1, -1, 1, -1, 1], [1, 1, 1, 1, 1]):
    den = pmul(den, f)
N = 60
ser = []
for n in range(N):
    s = Fraction(num[n] if n < len(num) else 0)
    for j in range(1, min(n, len(den) - 1) + 1):
        s -= den[j] * ser[n - j]
    ser.append(s / den[0])
assert all(x.denominator == 1 for x in ser)
ser = [int(x) for x in ser]
first_bad = next(n for n in range(N) if ser[n] != m2[n])
print("the empirical g.f. reproduces a(0..%d) and first fails at n = %d: g.f. gives %d, the true a(%d) = %d"
      % (first_bad - 1, first_bad, ser[first_bad], first_bad, m2[first_bad]))
print("   g.f. coefficients n = 40..50:", ser[40:51])
print("   true terms        n = 40..50:", m2[40:51])
print("   is the g.f. value %d a term? %s" % (ser[first_bad], is_term(str(ser[first_bad]))))
assert first_bad == 44 and m2[44] == 100998 and ser[44] == 5094
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
