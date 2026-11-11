"""Nothing was found on this page, so there is no result to verify. This file only restates the
arithmetic used in the page's argument about cyclic coverings (exact integers)."""
from math import comb, gcd


def phi(n):
    return sum(1 for i in range(1, n + 1) if gcd(i, n) == 1)


def orbits(v, t):
    """Number of orbits of t-subsets of Z_v under translation (Burnside)."""
    g = gcd(v, t)
    return sum(phi(d) * comb(v // d, t // d) for d in range(1, g + 1) if g % d == 0) // v


for v, k, t, record in ((83, 8, 3, 2082), (45, 16, 6, 4066)):
    m = (record - 1) // v
    print("C(%d,%d,%d): record %d, a cyclic covering must use at most %d base blocks; "
          "%d orbits of %d-subsets; each base block meets at most %d; record density %.3f"
          % (v, k, t, record, m, orbits(v, t), t, comb(k, t), record * comb(k, t) / comb(v, t)))
