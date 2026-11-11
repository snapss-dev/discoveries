"""A044140: k such that "02" occurs in the base-7 representation of k but not of k-1.
Tests the conjectured recurrence a(n) = a(n-1) + a(n-8) - a(n-9) for n > 9.
Run:  python check.py
"""
def base7(k):
    s = ""
    while k: s = str(k % 7) + s; k //= 7
    return s or "0"

a = [None] + [k for k in range(1, 20000) if "02" in base7(k) and "02" not in base7(k - 1)]
print("a(1..8) =", a[1:9], "(entry: 51, 100, 149, 198, 247, 296, 345, 357)")
bad = [n for n in range(10, len(a)) if a[n] != a[n-1] + a[n-8] - a[n-9]]
n = bad[0]
print(f"recurrence holds for 10 <= n <= {n - 1}; first failure at n = {n}: "
      f"a({n}) = {a[n]} = {base7(a[n])} in base 7, predicted {a[n-1] + a[n-8] - a[n-9]}")
print("number of failures among the first", len(a) - 1, "terms:", len(bad))
