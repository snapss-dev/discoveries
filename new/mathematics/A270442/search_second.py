"""A270442, second implementation (numpy only, sympy for roots and factoring; shares no code with sqsieve.py).
For LO <= k < HI: bit j of mask[k] is set when p^2 | k^2 - j for a prime p < P0.  Every k with at most one of the
bits 1..N unset is then tested exactly from the definition (sympy.factorint).  Prints all k in the range for which
none of k^2 - 0, ..., k^2 - N is squarefree and that this procedure can see (see the page for what it cannot).
Usage: a270442_check2.py N LO HI P0"""
import sys, time
import numpy as np
from sympy import factorint, primerange
from sympy.ntheory import sqrt_mod

N = int(sys.argv[1]); LO = int(float(sys.argv[2])); HI = int(float(sys.argv[3])); P0 = int(float(sys.argv[4]))
t0 = time.time()
cls = []   # (modulus, residue, bit)
for p in primerange(2, P0):
    q = p * p
    for j in range(1, N + 1):
        if j % p == 0:
            if j % q == 0:
                roots = [r for r in range(q) if (r * r - j) % q == 0]
            else:
                roots = []          # p || j: p^2 | k^2 - j would force p | k and then p^2 | j
        else:
            roots = sqrt_mod(j, q, all_roots=True) or []
        for r in roots:
            assert (r * r - j) % q == 0
            cls.append((q, int(r), j))
FULL = (1 << (N + 1)) - 2          # bits 1..N
pop = np.array([bin(i).count("1") for i in range(1 << (N + 1))], np.uint8)
def is_squarefree(v):
    if v == 0: return False
    return all(e == 1 for e in factorint(abs(v)).values())
L = 1 << 24
found = []; tested = 0
lo = LO
while lo < HI:
    n = min(L, HI - lo)
    mask = np.zeros(n, np.uint16)
    for q, r, j in cls:
        s = (r - lo) % q
        if s < n:
            mask[s::q] |= np.uint16(1 << j)
    miss = pop[(mask & FULL) ^ FULL]
    for i in np.nonzero(miss <= 1)[0]:
        k = lo + int(i)
        if k < 2: continue
        tested += 1
        if not any(is_squarefree(k * k - j) for j in range(0, N + 1)):
            found.append(k); print("k =", k, "satisfies the definition for n =", N, flush=True)
    lo += n
print(f"N={N} range [{LO},{HI}) P0={P0}: classes {len(cls)}, k tested exactly {tested}, solutions {found}, {time.time()-t0:.0f}s")
