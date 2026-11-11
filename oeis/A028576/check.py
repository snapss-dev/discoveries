"""A028576: a(n) = (1/(4n)) * sum_{d|n} mu(n/d) * binomial(2d, d)^2.
Checks n | a(n) and n^2 | 3 a(n), and the p-adic lemma behind the proof.
Run:  python check.py [N]      default N = 3000
"""
import sys
from math import comb
from sympy import mobius, divisors, primerange

N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
c2 = [comb(2*d, d)**2 for d in range(N + 1)]

def vp(x, p):
    if x == 0: return 10**9
    v = 0
    while x % p == 0: x //= p; v += 1
    return v

ok = True; need3 = []
for n in range(1, N + 1):
    S = sum(int(mobius(n // d)) * c2[d] for d in divisors(n))
    assert S % (4 * n) == 0
    a = S // (4 * n)
    if a % n or (3 * a) % (n * n): ok = False; print("FAILS at", n)
    if a % (n * n) and len(need3) < 8: need3.append(n)
print(f"n | a(n) and n^2 | 3a(n) for 1 <= n <= {N}: {ok}")
print("the factor 3 is needed: n^2 does not divide a(n) for n =", need3, "...")

# Lemma: for N = p*x with k = v_p(N):  v_p(C(2N,N)^2 - C(2x,x)^2) >= 3k (p >= 5), 3k-1 (p = 3), 3k+2 (p = 2)
worst = {}
for p in primerange(2, 60):
    for x in range(1, N // p + 1):
        M = p * x; k = vp(M, p)
        bound = 3*k + 2 if p == 2 else (3*k - 1 if p == 3 else 3*k)
        excess = vp(c2[M] - c2[x], p) - bound
        assert excess >= 0, (p, x)
        cls = 2 if p == 2 else (3 if p == 3 else 5)
        worst[cls] = min(worst.get(cls, 99), excess)
print(f"lemma holds for all primes p < 60 with p*x <= {N}; smallest slack: p=2: {worst[2]}, p=3: {worst[3]}, p>=5: {worst[5]}")
