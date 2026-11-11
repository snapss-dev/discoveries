"""A271817: smallest k > 1 such that none of k^2 + 0, ..., k^2 + n is squarefree.
Factors k^2 + j at k = 17546197568 (the term a(12) of the existing page) and reproduces a(0..5).
Run:  python check.py   (seconds; needs sympy).  The minimality searches are search_sieve.py and search_large.py."""
from sympy import factorint, primerange

k = 17546197568
for j in range(0, 14):
    f = factorint(k * k + j)
    sq = [p for p, e in f.items() if e > 1]
    print(f"k^2 + {j:2d} = " + " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
          + ("   squarefree" if not sq else ""))
PR = list(primerange(2, 14100))
def squarefree(m):
    for p in PR:
        if p * p > m: return True
        if m % (p * p) == 0: return False
    return True
terms = {}; kk = 2
while len(terms) < 6:
    run = 0
    while not squarefree(kk * kk + run): run += 1
    for n in range(run):
        terms.setdefault(n, kk)
    kk += 1
print("a(0..5) from the definition:", [terms[n] for n in range(6)], "(entry: 2, 7, 32, 41, 239, 13982)")
