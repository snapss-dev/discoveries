"""A271817: smallest k > 1 such that none of k^2, k^2+1, ..., k^2+n is squarefree.
Checks the square factors at the two new values of k, and reproduces the listed terms for n <= 5.
Run:  python check.py
"""
from sympy import factorint, primerange

sq = lambda m: [p for p, e in factorint(m).items() if e > 1]
for k, n in ((2352655113, 11), (17546197568, 12)):
    f = [sq(k * k + j) for j in range(n + 2)]
    print(f"k = {k}: smallest square-factor prime of k^2+j, j = 0..{n}: {[x[0] for x in f[:-1]]}; "
          f"k^2+{n + 1} squarefree: {f[-1] == []}")

PR = list(primerange(2, 14100))
def squarefree(m):
    for p in PR:
        if p * p > m: return True
        if m % (p * p) == 0: return False
    return True
terms = {}; k = 2
while len(terms) < 6:
    run = 0
    while not squarefree(k * k + run): run += 1
    for n in range(run):
        terms.setdefault(n, k)
    k += 1
print("a(0..5) from the definition:", [terms[n] for n in range(6)], "(entry: 2, 7, 32, 41, 239, 13982)")
