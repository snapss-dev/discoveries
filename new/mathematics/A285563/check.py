"""A285563: the diagonal of the two-dimensional "Rule 51" cellular automaton (von Neumann neighbourhood)
against the empirical generating function in the entry.
Run:  python check.py [stages]
"""
import sys
from fractions import Fraction

N = int(sys.argv[1]) if len(sys.argv) > 1 else 60


def stages(n_max):
    """Outer-totalistic code 51: a cell is ON next step iff exactly 0 or 2 of its four neighbours are ON
    (bit 2s + c of 51, with s the neighbour count and c the cell). The empty background therefore flips
    every step, so the grid is padded with the current background value."""
    size = 2 * n_max + 5
    c0 = size // 2
    grid = [[0] * size for _ in range(size)]
    grid[c0][c0] = 1
    bg = 0
    yield grid, c0
    for _ in range(n_max):
        new = [[0] * size for _ in range(size)]
        for i in range(size):
            for j in range(size):
                s = ((grid[i - 1][j] if i > 0 else bg) + (grid[i + 1][j] if i < size - 1 else bg)
                     + (grid[i][j - 1] if j > 0 else bg) + (grid[i][j + 1] if j < size - 1 else bg))
                new[i][j] = 1 if s in (0, 2) else 0
        bg = 1 - bg
        grid = new
        yield grid, c0


def diagonal_values(n_max):
    out = []
    for n, (grid, c0) in enumerate(stages(n_max)):
        bits = "".join(str(grid[c0 + d][c0 + d]) for d in range(n + 1))    # from the origin to the corner
        out.append(int(bits, 2))
    return out


def gf_coefficients(n_max):
    num = [1, 1, -1, 2, -6, 0, 0, 0, -64, 128, 64, -128]
    # (1 - x)(1 + x)(1 - 2x)(1 - 2x^2)(1 + 2x^2) = (1 - x^2)(1 - 2x)(1 - 4x^4)
    den = [1, -2, -1, 2, -4, 8, 4, -8]
    out = []
    for i in range(n_max + 1):
        v = Fraction(num[i] if i < len(num) else 0)
        v -= sum(den[j] * out[i - j] for j in range(1, min(i, len(den) - 1) + 1))
        out.append(v)
    return [int(v) for v in out]


ca, gf = diagonal_values(N), gf_coefficients(N)
print("first terms from the automaton:", ca[:12])
bfile = {34: 34359607296, 35: 68719476735, 36: 120257773568, 37: 274877906943, 38: 549654626304}
print("automaton agrees with the entry's b-file at n = 34..38:", all(ca[n] == v for n, v in bfile.items()))
bad = [n for n in range(N + 1) if ca[n] != gf[n]]
print(f"generating function agrees for n = 0..{bad[0] - 1}; first failure at n = {bad[0]}")
print(f"  a({bad[0]}) = {ca[bad[0]]} (bits {ca[bad[0]]:b}), generating function gives {gf[bad[0]]}")
print(f"failures for n <= {N}: {len(bad)}, all at even n: {all(n % 2 == 0 for n in bad)}")
print("odd n: a(n) = 2^(n+1) - 1 throughout:", all(ca[n] == 2 ** (n + 1) - 1 for n in range(1, N + 1, 2)))
