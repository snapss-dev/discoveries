"""A218049: smallest k such that k^2+1, (k+1)^2+1, ..., (k+n-1)^2+1 are each divisible by a square > 1.
Factors the values at the two new terms and reproduces a(1..4) from the definition.
Run:  python check.py   (under a minute; needs sympy and numpy).  It does not repeat the minimality searches."""
import numpy as np
from sympy import factorint, primerange

for k0, n in ((5990500988, 6), (20106639730, 7)):
    print(f"n = {n}, k = {k0}:")
    for k in range(k0 - 1, k0 + n + 1):
        f = factorint(k * k + 1)
        sq = [p for p, e in f.items() if e > 1]
        print(f"   {k}^2+1 = " + " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
              + ("   squarefree" if not sq else ""))
    print("   run of non-squarefree values has length exactly", n, ":",
          all(any(e > 1 for e in factorint(k * k + 1).values()) for k in range(k0, k0 + n))
          and all(max(factorint(k * k + 1).values()) == 1 for k in (k0 - 1, k0 + n)))

# listed terms a(1..4) from the definition: p^2 | k^2+1 forces p <= k, so trial squares of all primes up to K suffice
K = 460000
k = np.arange(K + 1, dtype=np.int64); v = k * k + 1
ns = np.zeros(K + 1, bool)
for p in primerange(2, K + 1):
    if p % 4 == 1:
        ns |= (v % (p * p) == 0)
ns[0] = False
terms = []
for n in range(1, 5):
    w = np.convolve(ns.astype(np.int64), np.ones(n, dtype=np.int64), "valid")   # w[i] = number of marked in i..i+n-1
    terms.append(int(np.nonzero(w == n)[0][0]))
print("a(1..4) from the definition:", terms, "(entry: 7, 117, 5742, 455356)")
