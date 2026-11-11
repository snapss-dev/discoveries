"""A202194 / A202202: count R x C binary arrays with no consecutive 001 or 101 in any row or column,
straight from the definition, and compare with 2*R*C*binomial(R+C-2, R-1).
Run:  python check.py [MAX]      default MAX = 7 (all 3 <= R, C <= MAX)
"""
import sys
from math import comb
from collections import defaultdict
MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
BAD = {(0, 0, 1), (1, 0, 1)}

def count(R, C):
    rows = [r for r in range(1 << C)
            if all(((r >> (C-1-i)) & 1, (r >> (C-2-i)) & 1, (r >> (C-3-i)) & 1) not in BAD for i in range(C - 2))]
    def col_ok(x, y, z):
        return all(((x >> c) & 1, (y >> c) & 1, (z >> c) & 1) not in BAD for c in range(C))
    state = defaultdict(int)
    for x in rows:
        for y in rows: state[(x, y)] += 1
    for _ in range(R - 2):
        new = defaultdict(int)
        for (x, y), v in state.items():
            for z in rows:
                if col_ok(x, y, z): new[(y, z)] += v
        state = new
    return sum(state.values())

ok = True
for R in range(3, MAX + 1):
    for C in range(3, MAX + 1):
        got, want = count(R, C), 2 * R * C * comb(R + C - 2, R - 1)
        if got != want: ok = False; print("MISMATCH", R, C, got, want)
print("diagonal (A202194 lists 108, 640, 3500, 18144, ...):", [count(n, n) for n in range(3, min(MAX, 6) + 1)])
print(f"T(R, C) = 2RC*binomial(R+C-2, R-1) for all 3 <= R, C <= {MAX}: {ok}")
