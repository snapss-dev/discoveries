"""A338627: smallest k such that n consecutive integers starting at k have the same value of A002828
(least number of squares that sum to the integer).  Claim: the seven listed terms are the whole sequence.
Computes A002828 up to N by brute force (no use of the three-square theorem), then checks the listed terms,
the two facts used in the proof, and the longest run.  Run: python check.py  (about ten seconds; numpy)"""
import numpy as np
N = 3_000_000
sq = np.arange(1, int(N ** 0.5) + 1, dtype=np.int64) ** 2
one = np.zeros(N + 1, bool); one[sq] = True
two = np.zeros(N + 1, bool)
for s in sq:                                   # sums of two positive squares
    t = sq[sq <= N - s] + s
    two[t] = True
three = np.zeros(N + 1, bool)
for s in sq:                                   # a square plus a sum of two positive squares
    m = N - s
    if m >= 2: three[s + 2:N + 1] |= two[2:m + 1]
A = np.full(N + 1, 4, np.int8)
A[three] = 3; A[two] = 2; A[one] = 1; A[0] = 0   # every positive integer is a sum of four squares (Lagrange)
# runs of equal values among 1..N
v = A[1:]
change = np.nonzero(np.diff(v) != 0)[0] + 1
starts = np.concatenate(([0], change)); ends = np.concatenate((change, [len(v)]))
length = ends - starts
first = {}
for s, L in zip(starts, length):
    for n in range(1, int(L) + 1):
        first.setdefault(n, int(s) + 1)          # a run of length L contains runs of every length n <= L, first at s
print("first k starting n equal values, n = 1..:", [first[n] for n in sorted(first)], "(entry: 1, 11, 42, 75, 138, 713, 1672)")
print("longest run up to", N, ":", int(length.max()))
for val in (1, 2, 3, 4):
    print("  longest run with value", val, ":", int(length[v[starts] == val].max()))
k = np.arange(1, N + 1)
print("every k = 7 mod 8 has value 4:", bool((v[k % 8 == 7] == 4).all()))
f = k.copy()
while True:
    m = f % 4 == 0
    if not m.any(): break
    f[m] //= 4
print("value 4 exactly for k = 4^a (8b+7):", bool(((v == 4) == (f % 8 == 7)).all()))
