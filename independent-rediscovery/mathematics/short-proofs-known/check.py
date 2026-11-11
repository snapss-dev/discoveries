"""Numerical checks for the page "Short proofs that were already known".  Plain Python + sympy, under a minute."""
import time
from math import isqrt, factorial
from sympy import isprime, primerange

t0 = time.time()


def sieve_spf(n):
    spf = list(range(n + 1))
    for i in range(2, isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i
    return spf


# ---- A008474: every m >= 5 reaches the cycle 5 -> 6 -> 7 -> 8 -> 5
NM = 3000000
spf = sieve_spf(NM + 1)
f = [0] * (NM + 2)
for m in range(2, NM + 2):
    p = spf[m]; r = m; k = 0
    while r % p == 0:
        r //= p; k += 1
    f[m] = p + k + f[r]
assert f[1:17] == [0, 3, 4, 4, 6, 7, 8, 5, 5, 9, 12, 8, 14, 11, 10, 6]
ok = [False] * (NM + 2)
for m in (5, 6, 7, 8):
    ok[m] = True
for m in range(9, NM + 1):
    a = f[m]
    if a >= m:
        assert spf[m] == m and a == m + 1          # only primes go up, by exactly 1
        a = f[a]
    assert 5 <= a < m
    ok[m] = ok[a]
assert all(ok[5:NM + 1])
print("A008474: every m with 5 <= m <= %d reaches the cycle (5, 6, 7, 8)" % NM)

# ---- A254074: a multiple of 5 cannot be a term
assert all((k * k) % 100 == 25 for k in range(5, 10 ** 6, 10))
print("A254074: k ending in 5 has k^2 ending in 25 (k < 10^6)")

# ---- A000680: (2n+1) | (2n)!/2^n + 2^n  iff  2n+1 is prime
NF = 3000
fct = 1
bad = 0
for n in range(1, NF + 1):
    fct *= (2 * n - 1) * (2 * n)
    a = fct >> n
    assert a << n == fct
    if ((a + 2 ** n) % (2 * n + 1) == 0) != isprime(2 * n + 1):
        bad += 1
assert bad == 0
print("A000680: the criterion holds for 1 <= n <= %d" % NF)

# ---- A088883 / A088884: concat(p, reverse(p)) +- 2
cp = cm = 0
for p in primerange(2, 3000000):
    s = str(p)
    N = int(s + s[::-1])
    plus = isprime(N + 2)
    minus = isprime(N - 2)
    assert not (plus and minus)
    if plus:
        cp += 1
        assert p % 6 == 1
    if minus:
        cm += 1
        assert p == 3 or p % 6 == 5
print("A088883 / A088884: primes below 3*10^6: %d with N+2 prime (all 6k+1), %d with N-2 prime (all 6k-1 or 3), "
      "never both" % (cp, cm))

# ---- A014865: k | s(k), s(1) = 1, s(j) = 15 s(j-1) + j
s = 0
for j in range(1, 1501):                       # closed form against the recurrence
    s = 15 * s + j
    assert 196 * s == 15 ** (j + 1) - 14 * j - 15
terms = [k for k in range(1, 2000001) if (pow(15, k + 1, 196 * k) - 14 * k - 15) % (196 * k) == 0]
assert terms[:20] == [1, 3, 5, 7, 15, 21, 35, 49, 55, 105, 147, 165, 245, 343, 385, 605, 723, 735, 903, 915]
assert all(k % 2 == 1 for k in terms)
assert all(not isprime(k) for k in terms if k > 7)
assert all(k % 3 == 0 or k % 5 == 0 or k % 7 == 0 for k in terms if k > 1)
print("A014865: %d terms up to 2*10^6: all odd, composite beyond 7, each > 1 divisible by 3, 5 or 7" % len(terms))
# ---- A065907: no value occurs more than three times
from collections import Counter
vals = []
PM = 3000000
for p in primerange(3, PM):
    if p % 8 == 7:
        # x^4 = 2 has exactly two solutions +-x; x = 2^((p+1)/8)... find a square root of a square root
        r = pow(2, (p + 1) // 4, p)          # r^2 = 2
        if pow(r, (p - 1) // 2, p) != 1:
            r = p - r                         # choose the square root that is itself a square
        y = pow(r, (p + 1) // 4, p)
        assert pow(y, 4, p) == 2
        vals.append(min(y, p - y))
assert vals[:12] == [2, 8, 15, 17, 15, 3, 48, 4, 16, 34, 33, 47]
cnt = Counter(vals)
mx = max(cnt.values())
thr = sorted(v for v, c in cnt.items() if c == 3)
assert mx == 3 and 221 in thr and 1159 in thr
print("A065907: %d primes == 7 (mod 8) below %d; largest multiplicity of a value: %d; %d values occur three times"
      % (len(vals), PM, mx, len(thr)))

# ---- A091713: A = x + x*A(A(A)), all coefficients odd
def compose(f, g, N):
    res = [0] * (N + 1)
    for c in reversed(f[:N + 1]):
        new = [0] * (N + 1)
        for i, a in enumerate(res):
            if a:
                for j in range(1, N + 1 - i):
                    if g[j]:
                        new[i + j] += a * g[j]
        new[0] += c
        res = new
    return res
A = [0, 1]
for n in range(2, 41):
    A.append(0)
    A[n] = compose(A, compose(A, A, n), n)[n - 1]
assert A[1:13] == [1, 1, 3, 15, 99, 781, 7001, 69253, 742071, 8506775, 103411463, 1324477033]
assert all(v % 2 == 1 for v in A[1:])
print("A091713: series computed from the functional equation to n = 40; published terms reproduced; all odd")

print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
