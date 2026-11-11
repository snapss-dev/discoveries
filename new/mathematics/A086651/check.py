"""A086651: simulate the definition and compare with the closed form.

Reading of the definition that reproduces every listed term: a(1) = a(2) = 1 and, with
d(j) = |a(j+1) - a(j)|, a(n) is the smallest positive integer such that |d(n-1) - d(n-2)| = F(n-1),
where F is the Fibonacci sequence (F(1) = F(2) = 1).
Run:  python check.py [N]      default N = 3000
"""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 3000
F = [0, 1]
while len(F) < N + 10: F.append(F[-1] + F[-2])

a = [None, 1, 1]
for n in range(3, N + 1):
    d_prev = abs(a[n-1] - a[n-2]); best = None
    for d_new in {d_prev + F[n-1], d_prev - F[n-1]}:
        if d_new < 0: continue
        for cand in (a[n-1] + d_new, a[n-1] - d_new):
            if cand >= 1 and (best is None or cand < best): best = cand
    a.append(best)

DATA = [1,1,2,5,5,10,23,23,2,57,57,146,379,379,2,989,989,2586,6767,6767,2]
def closed(n):
    m = 3 + 6 * ((n - 3) // 6); r = n - m
    return [2, 2 + F[m+1], 2 + F[m+1], 2 + F[m+3], 2 + F[m+5], 2 + F[m+5]][r]

print("reproduces the 21 listed terms:", a[1:22] == DATA)
print(f"a(6k+3) = 2 for all 6k+3 <= {N}:", all(a[n] == 2 for n in range(3, N + 1, 6)))
print(f"closed form matches for 3 <= n <= {N}:", all(a[n] == closed(n) for n in range(3, N + 1)))
print(f"a(n) = 18a(n-6) - a(n-12) - 32 for 15 <= n <= {N}:", all(a[n] == 18*a[n-6] - a[n-12] - 32 for n in range(15, N + 1)))
print(f"the recurrence listed in the entry, for 16 <= n <= {N}:", all(a[n] == a[n-1] + 18*a[n-6] - 18*a[n-7] - a[n-12] + a[n-13] for n in range(16, N + 1)))
