"""A276531: a(n)a(n-6) = a(n-1)a(n-5) + a(n-2)a(n-3)a(n-4), a(0..5)=1.
Run:  python check.py 40
Certificate that the recurrence is the exchange relation of a mutation-period-1 quiver (Fordy-Marsh 2011):
build skew-symmetric 6x6 B with first row (0, m1..m5), m = (1,-1,-1,-1,1), complete it by the Fordy-Marsh
rule, then CHECK  mu_1(B) = rho(B)  (rho = cyclic relabelling i -> i-1). Also checks integrality of a(n), n<=N."""
import sys
from fractions import Fraction
import numpy as np

def mutate(B, k):
    n = B.shape[0]; C = B.copy()
    for i in range(n):
        for j in range(n):
            if i == k or j == k:
                C[i, j] = -B[i, j]
            else:
                C[i, j] = B[i, j] + (abs(B[i, k]) * B[k, j] + B[i, k] * abs(B[k, j])) // 2
    return C

N = 6
m = [1, -1, -1, -1, 1]
B = np.zeros((N, N), dtype=np.int64)
B[0, 1:] = m; B[1:, 0] = [-x for x in m]
pos = lambda t: max(t, 0)
# Fordy-Marsh: b_{i+1,j+1} = b_{i,j} + b_{1,i+1}[-b_{1,j+1}]_+ - b_{1,j+1}[-b_{1,i+1}]_+  (1-indexed)
for i in range(1, N):
    for j in range(1, N):
        if i < j:
            B[i, j] = B[i - 1, j - 1] + B[0, i] * pos(-B[0, j]) - B[0, j] * pos(-B[0, i])
            B[j, i] = -B[i, j]
print('B =\n', B)
print('skew-symmetric:', (B == -B.T).all())
M = mutate(B, 0)
perm = [(i + 1) % N for i in range(N)]   # node 1 becomes node N after mutation
R = M[np.ix_(perm, perm)]
print('mu_1(B) relabelled == B :', (R == B).all())
# exchange relation at node 1: x1*x1' = prod_{b1j>0} xj^b1j + prod_{b1j<0} xj^-b1j  -> with x_{j} = a(n-6+j-1)
print('first row:', B[0].tolist(), '=> x1 x7 = x2*x6 + x3*x4*x5, i.e. a(n)a(n-6)=a(n-5)a(n-1)+a(n-4)a(n-3)a(n-2)')
Nn = int(sys.argv[1]) if len(sys.argv) > 1 else 300
a = [Fraction(1)] * 6
for n in range(6, Nn + 1):
    a.append((a[n - 1] * a[n - 5] + a[n - 2] * a[n - 3] * a[n - 4]) / a[n - 6])
print('all a(n), n<=%d, integers:' % Nn, all(x.denominator == 1 for x in a), ' a(6..12)=', [int(x) for x in a[6:13]])
