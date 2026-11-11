"""A270442: smallest k > 1 such that none of k^2 - 0, k^2 - 1, ..., k^2 - n is squarefree.
Factors k^2 - j for the new term a(11) = 25812395459 and reproduces a(0..5) from the definition.
Run:  python check.py   (seconds; needs sympy).  It does not repeat the minimality searches."""
from sympy import factorint, primerange

k = 25812395459
for j in range(0, 13):
    f = factorint(k * k - j)
    sq = [p for p, e in f.items() if e > 1]
    print(f"k^2 - {j:2d} = " + " * ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in sorted(f.items()))
          + ("   squarefree" if not sq else ""))
print("none of k^2 - j, j = 0..11, squarefree:",
      all(max(factorint(k * k - j).values()) > 1 for j in range(12)),
      "; k^2 - 12 squarefree:", max(factorint(k * k - 12).values()) == 1)

PR = list(primerange(2, 8200))
def squarefree(m):
    m = abs(m)
    if m == 0: return False
    for p in PR:
        if p * p > m: return True
        if m % (p * p) == 0: return False
    return True
terms = {}; kk = 2
while len(terms) < 6:
    run = 0
    while not squarefree(kk * kk - run): run += 1
    for n in range(run):
        terms.setdefault(n, kk)
    kk += 1
print("a(0..5) from the definition:", [terms[n] for n in range(6)], "(entry: 2, 3, 10, 941, 3052, 8173)")
