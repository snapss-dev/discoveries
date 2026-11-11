"""A227728: a(n) = greatest k with H(k) - H(a(n-1)) < H(a(n-1)) - H(a(n-2)), H the harmonic numbers,
starting from H(k) - H(2) < 1/1 + 1/2. Terms are recomputed at a precision that grows with their size,
tested against the conjectured recurrence, and compared with a b-file if one is given.
Run:  python check.py [N] [b227728.txt]
"""
import sys

from mpmath import mp, mpf, harmonic, floor, log10

N = int(sys.argv[1]) if len(sys.argv) > 1 else 700
SIG = (5, -4, 2, -2, 2, -2, 2, -2, 2, -2)


def next_term(prev, prev2):
    """Greatest k with H(k) < T, where T = 2 H(prev) - H(prev2). Returns k and the decision margin
    min(T - H(k), H(k+1) - T) as a multiple of the step 1/(k+1)."""
    digits = len(str(prev)) + 2
    mp.dps = 3 * digits + 60
    T = 2 * harmonic(mpf(prev)) - harmonic(mpf(prev2))
    x = mpf(prev) * prev / max(prev2, 1)            # the ratio of consecutive terms is nearly constant
    for _ in range(60):
        step = (T - harmonic(x)) * (x + mpf(1) / 2)   # Newton: H'(x) is about 1 / (x + 1/2)
        x += step
        if abs(step) < mpf(10) ** (-digits - 20):
            break
    k = int(floor(x))
    while harmonic(mpf(k)) >= T:
        k -= 1
    while harmonic(mpf(k + 1)) < T:
        k += 1
    margin = min(T - harmonic(mpf(k)), harmonic(mpf(k + 1)) - T) * (k + 1)
    return k, margin


a = [None, None]                                     # a[n + 1] holds a(n); a(-1) and a(0) are set below
prev2, prev = 0, 2                                   # H(2) - H(0) = 1/1 + 1/2
terms, worst = [], mpf(1)
for n in range(1, N + 1):
    k, margin = next_term(prev, prev2)
    terms.append(k)
    worst = min(worst, margin)
    prev2, prev = prev, k
print("first terms:", terms[:8])
print(f"computed a(1..{N}); a({N}) has {len(str(terms[-1]))} digits")
mp.dps = 30
print("smallest decision margin, in units of the gap between consecutive H values: 10^%.1f" % float(log10(worst)))
print("    (the working precision is far below this, so every 'greatest k' is decided)")

fails = [n for n in range(11, N + 1)
         if terms[n - 1] != sum(c * terms[n - 2 - i] for i, c in enumerate(SIG))]
print(f"conjectured recurrence holds for n = 11..{N}: {not fails}" + (f"; fails at {fails[:5]}" if fails else ""))

if len(sys.argv) > 2:
    b = {}
    for line in open(sys.argv[2]):
        parts = line.split()
        if len(parts) == 2 and parts[0].isdigit():
            b[int(parts[0])] = int(parts[1])
    diff = [n for n in range(1, N + 1) if n in b and b[n] != terms[n - 1]]
    print(f"b-file entries compared: {sum(1 for n in range(1, N + 1) if n in b)}; disagreements: {len(diff)}"
          + (f"; first at n = {diff[0]}" if diff else ""))
    if diff:
        n = diff[0]
        s, t = str(b[n]), str(terms[n - 1])
        same = next(i for i in range(min(len(s), len(t))) if s[i] != t[i])
        print(f"  n = {n}: both have {len(t)} digits and share the first {same}")
        bf = [m for m in range(11, max(b) + 1)
              if all(m - 1 - i in b for i in range(-1, 10)) and b[m] != sum(c * b[m - 1 - i] for i, c in enumerate(SIG))]
        print(f"  the b-file itself breaks the recurrence from n = {bf[0] if bf else None}")
