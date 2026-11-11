"""A246754: least k such that k^k has at least 10^n decimal digits.

k^k has at least 10^n digits  <=>  k^k >= 10^(10^n - 1)  <=>  k*log10(k) >= 10^n - 1.
The entry's formula ceiling(exp(LambertW(10^n*log(10)))) is the least k with k^k >= 10^(10^n),
i.e. with at least 10^n + 1 digits.

Part 1  exact integers (FLINT): 13993959^13993959 has exactly 10^8 digits.
Part 2  Arb ball arithmetic: true a(n) and the formula for 1 <= n <= NMAX, each certified.
Part 3  mpmath (independent code, different precision): same table.
Usage: python check.py [NMAX]   (default 1000)
"""
import sys, time
from flint import fmpz, arb, ctx
import mpmath
from mpmath import mp, mpf

NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
LISTED = [1,10,57,387,2890,22934,189482,1611056,13993960,123579654,1105747503,
          10000000000,91239358932,838673386122,7758099162327,72158973089377,
          674359248152535,6328590417713813,59611349660814244,563355446524384647,
          5339735395113038337,50747473680621582632]   # A246754 data, n = 0..21, as listed in the OEIS

print("Part 1: exact integer arithmetic")
t0 = time.time()
T = fmpz(10) ** (10**8 - 1)
for k in (13993958, 13993959):
    v = fmpz(k) ** k
    print("  k = %d:  k^k >= 10^(10^8-1): %s   k^k >= 10^(10^8): %s" % (k, v >= T, v >= 10 * T))
    del v
print("  => 13993958^13993958 has fewer than 10^8 digits, 13993959^13993959 has exactly 10^8 digits.")
print("  => a(8) = 13993959; the OEIS lists a(8) = %d.   (%.0f s)" % (LISTED[8], time.time() - t0))

def least_k_arb(target_num, n):
    """least integer k with k*log10(k) >= target (an integer), certified with Arb balls."""
    ctx.prec = int(3.33 * n) + 200
    L10 = arb(10).log()
    x = (arb(target_num) * L10)
    w = x.lambertw()
    r = w.exp()                       # real solution of k*log(k) = target*log(10)
    k = int(r.mid().ceil().unique_fmpz())
    # certify by direct evaluation, adjusting if the midpoint guess is off by one
    def ge(k):      # is k*log10(k) >= target ?   returns True/False/None
        d = arb(k) * arb(k).log() - arb(target_num) * L10
        if d > 0: return True
        if d < 0: return False
        return None
    for kk in (k - 1, k, k + 1):
        a, b = ge(kk), ge(kk - 1)
        if a is True and b is False:
            return kk, False
    # undecided: exact tie possible only if k^k = 10^target exactly
    for kk in (k - 1, k, k + 1):
        if ge(kk) is None and ge(kk - 1) is False:
            # tie test: kk must be a power of 10, kk = 10^j with j*10^j = target
            s = str(kk)
            if s[0] == "1" and set(s[1:]) <= {"0"} and (len(s) - 1) * kk == target_num:
                return kk, True
    raise RuntimeError("undecided at n=%d" % n)

print("Part 2: Arb, n = 1..%d" % NMAX)
t0 = time.time()
true_a, form_a, diff_n, ties = {}, {}, [], []
for n in range(1, NMAX + 1):
    t, _ = least_k_arb(10**n - 1, n)
    f, tie = least_k_arb(10**n, n)
    true_a[n], form_a[n] = t, f
    if tie: ties.append(n)
    if t != f: diff_n.append(n)
print("  n where the formula differs from the definition:", diff_n)
print("  n where exp(LambertW(10^n log 10)) is exactly an integer (k = 10^j, j*10^j = 10^n):", ties)
def short(v):
    s = str(v)
    return s if len(s) <= 60 else "%s...%s (%d digits)" % (s[:12], s[-12:], len(s))
for n in diff_n:
    assert form_a[n] == true_a[n] + 1
    print("    n = %d: a(n) = %s, formula gives a(n) + 1" % (n, short(true_a[n])))
bad_listed = [n for n in range(1, 22) if LISTED[n] != true_a[n]]
print("  listed terms a(1..21) that differ from the definition: n =", bad_listed,
      [(LISTED[n], true_a[n]) for n in bad_listed])
print("  listed terms a(1..21) that differ from the formula:    n =",
      [n for n in range(1, 22) if LISTED[n] != form_a[n]])
print("  (%.0f s)" % (time.time() - t0))

print("Part 3: mpmath, independent")
t0 = time.time()
mm = []
for n in range(1, NMAX + 1):
    mp.dps = n + 60
    tgt = mpf(10) ** n
    def least(target):
        r = mpmath.exp(mpmath.lambertw(target * mpmath.log(10)))
        k = int(mpmath.nint(r))
        for kk in (k - 1, k, k + 1, k + 2):
            if kk * mpmath.log10(kk) >= target - mpf(10) ** (-(n + 40)) and \
               (kk - 1) * mpmath.log10(kk - 1) < target - mpf(10) ** (-(n + 40)):
                return kk
    t, f = least(tgt - 1), least(tgt)
    if t != true_a[n] or f != form_a[n]:
        mm.append(n)
print("  disagreements with Part 2:", mm, "  (%.0f s)" % (time.time() - t0))
print("RESULT:", "OK" if not mm and bad_listed == [8] and diff_n[:1] == [8] else "CHECK")
