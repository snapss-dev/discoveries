"""Two Mills-type formulas, checked with exact integer arithmetic only.

A059923: a(1) = 1, a(n+1) = smallest integer with a(n+1)^n > a(n)^(n+1).
         b(n) = a(n)^(1/n) increases to x = 1.538851315...   Formula in the entry: a(n) = floor(x^n).
A207976: a(1) = 2, a(n) = largest integer with a(n)^(1/n) < a(n-1)^(1/(n-1)).
         b(n) decreases to q = 1.652212713...                 Formula in the entry: a(n) = 1 + floor(q^n).
A080869 (control): a(n) + 1 follows the A059923 rule from first term 2; formula a(n) = floor(t^n) - 1.

Bounds used (N = NTOP, all comparisons between integers):
  A059923:  a(N)^(1/N) < x <= (a(N)+2)^(1/N)
      formula fails at n   if  a(N)^n >= (a(n)+1)^N          (then x^n > a(n)+1)
      formula holds at n   if  (a(N)+2)^n < (a(n)+1)^N       (then a(n) < x^n < a(n)+1)
  A207976:  (a(N)-2)^(1/N) <= q < a(N)^(1/N)
      formula fails at n   if  a(N)^n <= (a(n)-1)^N          (then q^n < a(n)-1)
      formula holds at n   if  (a(N)-2)^n >= (a(n)-1)^N      (then a(n)-1 <= q^n < a(n))
The outer bounds hold because (a(n)+2)^(1/n) is non-increasing, resp. (a(n)-2)^(1/n) non-decreasing,
from n = 3 on; the script verifies this monotonicity directly for 3 <= n < NTOP.
Usage: python check.py [NMAX] [NTOP]   (defaults 300, 420)
"""
import sys
from math import isqrt

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
NTOP = int(sys.argv[2]) if len(sys.argv) > 2 else 420

def iroot(a, n):
    """floor of the n-th root of a >= 0, exact."""
    if n == 1 or a < 2: return a
    r = 1 << ((a.bit_length() + n - 1) // n)
    while True:
        s = ((n - 1) * r + a // r ** (n - 1)) // n
        if s >= r: return r
        r = s

def runs_summary(v):
    out = []; i = 0
    while i < len(v):
        j = i
        while j + 1 < len(v) and v[j + 1] == v[j] + 1: j += 1
        out.append(str(v[i]) if i == j else "%d-%d" % (v[i], v[j])); i = j + 1
    return ", ".join(out)

# ---------------- A059923
a = [None, 1]
for n in range(1, NTOP):
    a.append(iroot(a[n] ** (n + 1), n) + 1)
LISTED = [1,2,3,5,8,13,20,31,48,74,114,176,271,417,642,988,1521,2341,3603,5545]
assert a[1:21] == LISTED
for n in range(1, NTOP):                       # definition, checked directly
    assert a[n + 1] ** n > a[n] ** (n + 1) and (a[n + 1] - 1) ** n <= a[n] ** (n + 1)
for n in range(3, NTOP):                       # monotonicity behind the bounds on x
    assert a[n + 1] ** n > a[n] ** (n + 1)                          # b increasing
    assert (a[n + 1] + 2) ** n <= (a[n] + 2) ** (n + 1)             # (a+2)^(1/n) non-increasing
N = NTOP; lo, hi = a[N], a[N] + 2
fail, hold, und = [], [], []
for n in range(1, NMAX + 1):
    t = (a[n] + 1) ** N
    if lo ** n >= t: fail.append(n)
    elif hi ** n < t: hold.append(n)
    else: und.append(n)
print("A059923, a(n) = floor(x^n), 1 <= n <= %d" % NMAX)
print("  formula fails at %d values of n, holds at %d, undecided %d" % (len(fail), len(hold), len(und)))
print("  first failure: n = %d, a(n) = %d, floor(x^n) = a(n) + 1" % (fail[0], a[fail[0]]))
print("  failures:", runs_summary(fail))
for n in fail:                                  # at a failure, floor(x^n) is exactly a(n)+1
    assert hi ** n < (a[n] + 2) ** N
res1 = (fail[0], len(fail), len(und))

# ---------------- A207976
c = [None, 2]
for n in range(2, NTOP + 1):
    T = c[n - 1] ** n                           # largest c(n) with c(n)^(n-1) < c(n-1)^n
    r = iroot(T, n - 1)
    if r ** (n - 1) == T: r -= 1
    c.append(r)
LISTED2 = [2,3,5,8,13,21,34,56,92,152,251,414,684,1130,1867,3084,5095,8418]
assert c[1:19] == LISTED2
for n in range(2, NTOP + 1):
    assert c[n] ** (n - 1) < c[n - 1] ** n and (c[n] + 1) ** (n - 1) >= c[n - 1] ** n
for n in range(3, NTOP):
    assert (c[n + 1] - 2) ** n >= (c[n] - 2) ** (n + 1)             # (c-2)^(1/n) non-decreasing
lo, hi = c[N] - 2, c[N]
fail2, hold2, und2 = [], [], []
for n in range(1, NMAX + 1):
    t = (c[n] - 1) ** N
    if hi ** n <= t: fail2.append(n)
    elif lo ** n >= t: hold2.append(n)
    else: und2.append(n)
print("A207976, a(n) = 1 + floor(q^n), 1 <= n <= %d" % NMAX)
print("  formula fails at %d values of n, holds at %d, undecided %d" % (len(fail2), len(hold2), len(und2)))
print("  first failure: n = %d, a(n) = %d, 1 + floor(q^n) = a(n) - 1" % (fail2[0], c[fail2[0]]))
print("  failures:", runs_summary(fail2))
for n in fail2:
    assert lo ** n >= (c[n] - 2) ** N

# ---------------- control: A080869(n) + 1 obeys the A059923 recurrence with first term 2 (t = 2.3055... > 2)
d = [None, 2]
for n in range(1, NTOP):
    d.append(iroot(d[n] ** (n + 1), n) + 1)
assert [v - 1 for v in d[1:16]] == [1,4,11,27,64,149,345,797,1839,4242,9782,22554,52001,119892,276417]
for n in range(3, NTOP):
    assert (d[n + 1] + 2) ** n <= (d[n] + 2) ** (n + 1)
lo, hi = d[N], d[N] + 2
fail3 = [n for n in range(1, NMAX + 1) if lo ** n >= (d[n] + 1) ** N]
hold3 = [n for n in range(1, NMAX + 1) if hi ** n < (d[n] + 1) ** N]
print("A080869 (control), a(n) = floor(t^n) - 1, 1 <= n <= %d: fails at %d values of n, holds at %d"
      % (NMAX, len(fail3), len(hold3)))

# decimal values of the constants from the same integer bounds (first 30 digits agree)
from decimal import Decimal, getcontext
getcontext().prec = 60
print("  x = %s..." % str(Decimal(a[N]).ln().__truediv__(N).exp())[:32])
print("  q = %s..." % str(Decimal(c[N]).ln().__truediv__(N).exp())[:32])
print("RESULT:", "OK" if res1[0] == 24 and res1[2] == 0 and fail2[0] == 27 and not und2
      and not fail3 and len(hold3) == NMAX else "CHECK")
