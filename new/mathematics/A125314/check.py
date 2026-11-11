"""A125314: smallest k > 1 such that Sum_{i=1..k} i^n divides Product_{i=1..k} i^n = (k!)^n.
Checks the new term a(11) = 10892793 literally from the definition and through the factorisation of the sum,
and reproduces the listed terms a(1..10).  Run:  python check.py   (about one minute; needs sympy)
It does not repeat the search for smaller k (see search_sieve.py and search_batch.py)."""
from sympy import factorint

def literal(n, k):
    """(k!)^n mod S == 0, with S = 1^n + ... + k^n, computed directly"""
    S = sum(i ** n for i in range(1, k + 1))
    f = 1
    for i in range(2, k + 1):
        f = f * i % S
    return pow(f, n, S) == 0, S

# 1. listed terms: brute force from the definition where the term is small, the test at the term otherwise
listed = [3, 7, 3, 31, 13, 1556, 733, 89037, 1441, 668073]
for n in range(1, 11):
    a = listed[n - 1]
    if a < 2000:
        S = 1; f = 1; k = 1
        while True:
            k += 1; S += k ** n; f *= k
            if pow(f, n, S) == 0: break
        print(f"n = {n}: first k > 1 by brute force = {k}   (entry: {a})")
    else:
        print(f"n = {n}: definition holds at the listed k = {a}: {literal(n, a)[0]}   (smaller k not rechecked here)")

# 2. the new term
k = 10892793
ok, S = literal(11, k)
print(f"n = 11, k = {k}: (k!)^11 mod S == 0 computed literally: {ok}")
g = 2*k**8 + 8*k**7 + 4*k**6 - 16*k**5 - 5*k**4 + 26*k**3 - 3*k**2 - 20*k + 10
print("closed form S = k^2 (k+1)^2 g(k) / 24 agrees with the literal sum:", k * k * (k + 1) ** 2 * g == 24 * S)
print("k    =", factorint(k)); print("k+1  =", factorint(k + 1)); print("g(k) =", factorint(g))
fac = factorint(S)
def v_fact(k, p):
    v = 0
    while k: k //= p; v += k
    return v
print("S =", " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(fac.items())))
print("largest prime factor of S:", max(fac), "<= k:", max(fac) <= k)
print("every exponent e of p in S satisfies e <= 11 * v_p(k!):", all(e <= 11 * v_fact(k, p) for p, e in fac.items()))
print('n = 11, k = 2..60 tested literally, k that work:', [kk for kk in range(2, 61) if literal(11, kk)[0]])
for kk in (k - 1, k + 1):
    print(f"for comparison, k = {kk}: definition holds: {literal(11, kk)[0]}")
