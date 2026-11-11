"""Numerical checks, from the definitions, for the short proofs on this page.  Each block prints one line.
Plain Python + sympy; a few minutes in total.
"""
import sys
import time
from fractions import Fraction
from math import gcd, isqrt
import sympy
from sympy import bernoulli, primerange, isprime, factorint, totient, divisors

t00 = time.time()


def sieve_spf(n):
    spf = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


def digsum(n):
    return sum(map(int, str(n)))


# ---------------------------------------------------------------- A120566, A091713: all terms odd
def compose(f, g, N):
    # f(g(x)) mod x^(N+1); g has zero constant term; lists of ints indexed by exponent
    res = [0] * (N + 1)
    for c in reversed(f[:N + 1]):
        # res = res * g + c
        new = [0] * (N + 1)
        for i, a in enumerate(res):
            if a:
                for j in range(1, N + 1 - i):
                    b = g[j]
                    if b:
                        new[i + j] += a * b
        new[0] += c
        res = new
    return res


N1 = 40
A = [0, 1]                       # A091713: A = x + x*A(A(A))
for n in range(2, N1 + 1):
    A.append(0)
    AAA = compose(A, compose(A, A, n), n)
    A[n] = AAA[n - 1]
d091713 = [1, 1, 3, 15, 99, 781, 7001, 69253, 742071, 8506775, 103411463, 1324477033]
assert A[1:13] == d091713 and all(x % 2 == 1 for x in A[1:])
B = [0, 1]                       # A120566: A = A(A) - x*A(A(A)), a(1) = 1
for n in range(2, N1 + 1):
    B.append(0)
    BB = compose(B, B, n)
    BBB = compose(B, BB, n)
    B[n] = BBB[n - 1] - BB[n]    # a(n) = T_n - R_n, where [x^n]A(A) = 2a(n) + R_n and T_n = [x^(n-1)]A(A(A))
    # confirm that the functional equation holds through x^n with this value
    BB = compose(B, B, n)
    BBB = compose(B, BB, n)
    assert B[n] == BB[n] - BBB[n - 1]
d120566 = [1, 1, 1, 3, 7, 33, 109, 643, 2623, 17929, 85349, 652395, 3517911, 29484193]
assert B[1:15] == d120566 and all(x % 2 == 1 for x in B[1:])
print("A091713, A120566: series computed from the functional equations to n = %d; published terms reproduced; "
      "all terms odd" % N1)

# ---------------------------------------------------------------- A068206: terms == 7 (mod 21)
NB = 1200
terms = []
for n in range(2, NB + 1):
    b2n = bernoulli(2 * n)
    b2m = bernoulli(2 * n - 2)
    num = abs(int(b2n.p)); den = int(b2m.q)
    v7 = 0
    x = num
    while x % 7 == 0:
        x //= 7; v7 += 1
    # lemma of the proof: if n == 1 (mod 3) then v7(numerator of B(2n)) = v7(n)
    if n % 3 == 1:
        m = n; w = 0
        while m % 7 == 0:
            m //= 7; w += 1
        assert v7 == w
    if gcd(num, den) == 7:
        terms.append(n)
d068206 = [7, 28, 49, 70, 112, 133, 154, 196, 217, 238, 259, 280, 301, 322, 343, 364, 406, 427]
assert terms[:len(d068206)] == d068206 and all(t % 21 == 7 for t in terms)
print("A068206: %d terms up to n = %d (published terms reproduced), all == 7 (mod 21)" % (len(terms), NB))

# ---------------------------------------------------------------- A090818: never == 2 (mod 4)
terms = []
for k in range(1, 801):
    if isprime(k):
        continue
    v = 3 * (3 ** k - 1) * bernoulli(2 * k)
    if v.q == 1:
        terms.append(k)
d090818 = [1, 4, 12, 16, 25, 28, 32, 35, 36, 48, 49, 52, 55, 64, 65, 76, 77, 80, 84, 85, 91, 92, 95]
assert terms[:len(d090818)] == d090818 and all(t % 4 != 2 for t in terms)
print("A090818: %d terms up to 800 (published terms reproduced), none == 2 (mod 4)" % len(terms))

# ---------------------------------------------------------------- A048868: all terms even
NN = 100000
spf = sieve_spf(NN)
isp = [False] * (NN + 1)
for i in range(2, NN + 1):
    isp[i] = spf[i] == i
pi = [0] * (NN + 1)
for i in range(1, NN + 1):
    pi[i] = pi[i - 1] + isp[i]
terms = []
for n in range(1, NN + 1):
    ps = set()
    m = n
    while m > 1:
        ps.add(spf[m]); m //= spf[m]
    phi = n
    for p in ps:
        phi = phi // p * (p - 1)
    primes_in = pi[n - 1] - sum(1 for p in ps if p < n) if n > 1 else 0   # primes below n not dividing n
    if 2 * primes_in > phi:
        terms.append(n)
assert terms[:23] == [8, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54]
assert all(t % 2 == 0 for t in terms)
print("A048868: %d terms up to %d (the b-file has 586 below 10^5), all even" % (len(terms), NN))

# ---------------------------------------------------------------- A058059: all terms even
x = sympy.symbols("x")
terms = []
for n in range(2, 61):
    P = sympy.Poly(x ** n + x + 2, x, modulus=3)
    if P.is_irreducible:
        terms.append(n)
    if n % 2 == 1:
        assert ((-1) ** n + (-1) + 2) % 3 == 0          # x = 2 is a root
assert terms == [2, 4, 6, 14, 30, 40, 54]
print("A058059: terms up to 60 reproduced:", terms, "; x = 2 is a root for every odd n")

# ---------------------------------------------------------------- A130061: composite except 1 and 3
terms = [k for k in range(1, 2000001, 2) if (pow(3, (k - 1) // 2, k) - pow(2, (k - 1) // 2, k) - 1) % k == 0]
assert terms[:17] == [1, 3, 35, 147, 195, 219, 291, 399, 579, 583, 723, 939, 1011, 1023, 1227, 1299, 1371]
spf2 = sieve_spf(2000001)
assert all(spf2[t] != t for t in terms if t > 3)
print("A130061: %d terms up to 2*10^6, none prime except 3" % len(terms))

# ---------------------------------------------------------------- A131418: multiples of 9
cnt = 0
for n in range(0, 3000001):
    s = digsum(n)
    if s == digsum(n + s):
        cnt += 1
        assert n % 9 == 0
print("A131418: %d terms up to 3*10^6, all multiples of 9" % cnt)

# ---------------------------------------------------------------- A134460: no term == 2 (mod 4) after the first
c = [n for n in range(1, 400001) if isprime((n * n + n + 2) // 2)]
assert c[:12] == [1, 3, 4, 7, 8, 11, 12, 16, 19, 20, 23, 27]
dif = [c[i + 1] - c[i] for i in range(len(c) - 1)]
assert dif[:10] == [2, 1, 3, 1, 3, 1, 4, 3, 1, 3] and all(d % 4 != 2 for d in dif[1:])
assert all(n % 4 in (0, 3) for n in c[1:])
print("A134460: %d differences (A067186 up to 4*10^5), none == 2 (mod 4) after the first" % len(dif))

# ---------------------------------------------------------------- A008474: every m >= 5 reaches the cycle 5, 6, 7, 8
NM = 5000000
spf3 = sieve_spf(NM + 1)
f = [0] * (NM + 2)
for m in range(2, NM + 2):
    p = spf3[m]; r = m; k = 0
    while r % p == 0:
        r //= p; k += 1
    f[m] = p + k + f[r]
assert f[1:29] == [0, 3, 4, 4, 6, 7, 8, 5, 5, 9, 12, 8, 14, 11, 10, 6, 18, 8, 20, 10, 12, 15, 24, 9, 7, 17, 6, 12]
ok = [False] * (NM + 2)
for m in (5, 6, 7, 8):
    ok[m] = True
worst = 0
for m in range(9, NM + 1):
    a = f[m]
    if a >= m:                    # only for primes: f(p) = p + 1
        assert spf3[m] == m and a == m + 1
        a = f[a]
    assert 5 <= a < m             # the descent used in the proof
    ok[m] = ok[a]
assert all(ok[5:NM + 1])
print("A008474: every m with 5 <= m <= %d reaches the cycle (5, 6, 7, 8); f(m) < m for composite m > 8 and "
      "f(f(p)) < p for primes p > 5" % NM)

# ---------------------------------------------------------------- A332937: a(p+1) = 1 for primes p > 3
def wyth(n):
    # first two terms of row n of the Wythoff array: floor(floor(n*phi)*phi), floor(floor(n*phi)*phi^2), exact
    def fl_phi(m):                            # floor(m*phi) = (m + isqrt(5 m^2)) // 2
        return (m + isqrt(5 * m * m)) // 2
    a = fl_phi(n)
    w1 = fl_phi(a)
    w2 = w1 + a                               # phi^2 = phi + 1 and a*phi is irrational
    return w1, w2
d332937 = [1, 1, 2, 3, 4, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 5, 1, 1, 6, 1, 1, 7, 1, 1, 8, 1, 1, 9, 2, 1, 10, 1, 1]
assert [gcd(*wyth(n)) for n in range(1, len(d332937) + 1)] == d332937
assert all(gcd(*wyth(n)) == gcd(n - 1, (n + isqrt(5 * n * n)) // 2) for n in range(1, 200000))
np_ = 0
for p in primerange(5, 20000000):
    assert gcd(*wyth(p + 1)) == 1
    np_ += 1
assert gcd(*wyth(4)) == 3 and gcd(*wyth(3)) == 2
print("A332937: a(p+1) = 1 for all %d primes 3 < p < 2*10^7; a(n) = gcd(n-1, floor(n*phi)) for n < 2*10^5" % np_)

# ---------------------------------------------------------------- A328881: odd terms are never multiples of 5
a = [1, 0, 1]
for n in range(0, 6000):
    a.append(2 ** n - a[n])
assert a[:19] == [1, 0, 1, 0, 2, 3, 8, 14, 29, 56, 114, 227, 456, 910, 1821, 3640, 7282, 14563, 29128]
res = [x % 10 for x in a]
assert all(res[n] == res[n + 12] for n in range(4, 5900))
assert all(x % 10 != 5 for x in a)
print("A328881: a(n) mod 10 has period 12 for n >= 4:", res[4:16], "; no term ends in 5 (n <= 6000)")

# ---------------------------------------------------------------- A348158: all terms odd
for n in range(1, 200001):
    s = sum(set(int(totient(d)) for d in divisors(n))) if n <= 20000 else None
    if s is not None:
        assert s % 2 == 1
print("A348158: all terms odd for n <= 20000")

# ---------------------------------------------------------------- A342681: odd number of digits
terms = []
for p in primerange(2, 10 ** 7):
    q = p + int(str(p)[::-1])
    s = str(q)
    if s == s[::-1] and isprime(q):
        terms.append(p)
    if len(str(p)) % 2 == 0:
        assert q % 11 == 0 and q > 11
assert terms[:8] == [241, 443, 613, 641, 811, 20011, 20047, 20051]
assert all(len(str(t)) % 2 == 1 for t in terms)
print("A342681: %d terms below 10^7, all with an odd number of digits; p + reverse(p) is a multiple of 11 "
      "for every prime with an even number of digits" % len(terms))

# ---------------------------------------------------------------- A300984: terms are 2^i * p^j
def squarefree(n):
    return all(e == 1 for e in factorint(n).values())
terms = []
NQ = 300000
spf4 = sieve_spf(NQ)
for n in range(2, NQ + 1):
    fac = {}
    m = n
    while m > 1:
        fac[spf4[m]] = fac.get(spf4[m], 0) + 1; m //= spf4[m]
    ssf = 1; sig = 1
    for p, e in fac.items():
        ssf *= (1 + p); sig *= (p ** (e + 1) - 1) // (p - 1)
    odd = [p for p in fac if p > 2]
    if len(odd) >= 2:
        assert ssf % 4 == 0
        continue
    nsf = sig - ssf
    if nsf > 0 and squarefree(ssf) and squarefree(nsf):
        terms.append(n)
assert terms[:12] == [676, 1352, 2704, 5408, 5476, 8788, 10816, 10952, 14884, 21316, 21632, 21904]
print("A300984: %d terms up to %d (published terms reproduced); with two odd primes the sum of squarefree "
      "divisors is a multiple of 4" % (len(terms), NQ))

# ---------------------------------------------------------------- A254074: no multiple of 5
assert all((k * k) % 100 == 25 for k in range(5, 10 ** 6, 10))
for t in [759576, 97759786, 97957576, 887579686, 987759576, 987859786, 7599859786]:
    assert set(str(t)) <= set("56789") and "5" in str(t) and "9" in str(t)
    assert set(str(t * t)) <= set("56789") and "5" in str(t * t) and "9" in str(t * t)
print("A254074: k ending in 5 has k^2 ending in 25 (k < 10^6); the seven published terms satisfy the definition")

# ---------------------------------------------------------------- A326328: a(n) == 6 (mod 9) for n >= 1
NE = 150
# cosh(x)^(-3) = sum a(n) x^(2n)/(2n)!  : exact rational power series in y = x^2
ch = [Fraction(1, sympy.factorial(2 * k)) for k in range(NE + 1)]
def smul(u, v):
    r = [Fraction(0)] * (NE + 1)
    for i, a_ in enumerate(u):
        if a_:
            for j in range(NE + 1 - i):
                r[i + j] += a_ * v[j]
    return r
def sinv(u):
    r = [Fraction(0)] * (NE + 1)
    r[0] = 1 / u[0]
    for n in range(1, NE + 1):
        r[n] = -sum(u[k] * r[n - k] for k in range(1, n + 1)) / u[0]
    return r
sech = sinv(ch)
s3 = smul(sech, smul(sech, sech))
an = [s3[n] * sympy.factorial(2 * n) for n in range(NE + 1)]
assert all(v.denominator == 1 for v in an)
an = [int(v) for v in an]
assert an[:9] == [1, -3, 33, -723, 25953, -1376643, 101031873, -9795436563, 1212135593793]
assert all(v % 9 == 6 for v in an[1:])
E = [int(sech[n] * sympy.factorial(2 * n)) for n in range(NE + 1)]          # Euler numbers E_(2n)
assert all(2 * an[n] == E[n] - E[n + 1] for n in range(NE))
assert all(E[n] % 9 == (8, 5, 2)[(n - 1) % 3] for n in range(1, NE + 1))
print("A326328: a(n) == 6 (mod 9), hence 3-adic valuation exactly 1, for 1 <= n <= %d; E_(2n) mod 9 cycles 8, 5, 2" % NE)

# ---------------------------------------------------------------- A044279: digit sum == 0 or 1 (mod 9)
def has31(k):
    prev = -1
    while k:
        d = k % 9
        if d == 3 and prev == 1:
            return True
        prev = d; k //= 9
    return False
cnt = 0
pv = False
first = []
for k in range(1, 9 ** 7):
    cur = has31(k)
    if cur and not pv:
        cnt += 1
        if len(first) < 8:
            first.append(k)
        assert k % 9 in (0, 1) and digsum(k) % 9 in (0, 1)
    pv = cur
assert first == [28, 109, 190, 252, 271, 352, 433, 514]
print("A044279: %d terms below 9^7, each == 0 or 1 (mod 9), so the decimal digit sum is too" % cnt)

# ---------------------------------------------------------------- A037915: number of distinct floor(i^2/n)
bad = [n for n in range(1, 20001) if len(set(i * i // n for i in range(0, n + 1))) != (3 * n + 4) // 4]
bad1 = [n for n in range(1, 20001) if len(set(i * i // n for i in range(1, n + 1))) != (3 * n + 4) // 4]
assert bad == [1] and bad1 == []
print("A037915: #{floor(i^2/n), 0 <= i <= n} = floor(3n/4) + 1 for 2 <= n <= 20000; fails only at n = 1 "
      "(2 values, a(1) = 1); with 1 <= i <= n it holds for every n")

# ---------------------------------------------------------------- A002791: the two "conjectured" formulas
NS = 3000
def a002791(n):
    return sum(d * d if d <= 4 else 4 * d for d in divisors(n))
assert [a002791(n) for n in range(1, 12)] == [1, 5, 10, 21, 21, 38, 29, 53, 46, 65, 45]
def coeffs(num, N):
    # num / (1-x)^2
    out = []
    for n in range(N + 1):
        out.append(sum(c * (n - e + 1) for e, c in num.items() if e <= n))
    return out
good = coeffs({1: 1, 2: 2, 3: 2, 4: 2, 5: -3}, NS)       # ... - 3x^5
typo = coeffs({1: 1, 2: 2, 3: 2, 4: 2 - 3}, NS)           # as printed: ... + 2x^4 - 3x^4
fmod = {0: 10, 1: 3, 2: 7, 3: 6, 4: 7, 5: 3}
okg = okt = okf = True
for n in range(1, NS + 1):
    v = a002791(n)
    okg &= v == sum(good[d] for d in divisors(n))
    okt &= v == sum(typo[d] for d in divisors(n))
    okf &= v == 4 * int(sympy.divisor_sigma(n)) - fmod[n % 6]
assert okg and okf and not okt
print("A002791: both formulas hold for n <= %d once the g.f. numerator ends in -3x^5; as printed (-3x^4) it fails" % NS)

print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t00))
