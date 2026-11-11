"""A115066: a(n) = T_n(n), Chebyshev polynomial of the first kind at x = n.  Checks the three congruences.
Run:  python check.py [N]      default N = 500
"""
import sys
N = int(sys.argv[1]) if len(sys.argv) > 1 else 500
def T(n, x):
    if n == 0: return 1
    a, b = 1, x
    for _ in range(n - 1): a, b = b, 2 * x * b - a
    return b
print("a(0..5) =", [T(n, n) for n in range(6)], "(entry: 1, 1, 7, 99, 1921, 47525)")
ok1 = all(T(n, n) % (n * n) == 0 for n in range(1, N + 1, 2))
ok2 = all((2 * T(n, n) + 2) % n**4 == 0 for n in range(2, N + 1, 4))
ok3 = all((2 * T(n, n) - 2) % n**4 == 0 for n in range(4, N + 1, 4))
ok4 = all((T(n, n) - (-1)**((n - 1) // 2) * n * n) % n**3 == 0 for n in range(1, N + 1, 2))
print(f"odd n <= {N}: n^2 | a(n): {ok1};  sharper a(n) == (-1)^((n-1)/2) n^2 (mod n^3): {ok4}")
print(f"n == 2 (mod 4): 2a(n) == -2 (mod n^4): {ok2};   n == 0 (mod 4): 2a(n) == 2 (mod n^4): {ok3}")
