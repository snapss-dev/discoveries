"""A254069: smallest k such that none of 4k-4j+2 and 4k+4j-2 (j = 0..n) is squarefree.
Checks the eight values at k = 909764941 and reproduces a(0..2) from the definition.
Run:  python check.py
"""
from sympy import factorint, primerange

sq = lambda m: [p for p, e in factorint(m).items() if e > 1]
k = 909764941
vals = sorted({4 * k - 4 * j + 2 for j in range(5)} | {4 * k + 4 * j - 2 for j in range(5)})
print("k =", k, "| offsets from 4k and smallest square-factor prime:", [(v - 4 * k, sq(v)[0]) for v in vals])
print("the next values outward are squarefree:", sq(4 * k - 18) == [], sq(4 * k + 18) == [])

PR = list(primerange(2, 2000))
def squarefree(m):
    for p in PR:
        if p * p > m: return True
        if m % (p * p) == 0: return False
    return True
def ok(k, n):
    return all(not squarefree(4 * k - 4 * j + 2) and not squarefree(4 * k + 4 * j - 2) for j in range(n + 1))
print("a(0..2) from the definition:", [next(k for k in range(1, 10**6) if ok(k, n)) for n in range(3)], "(entry: 13, 13, 1263)")
