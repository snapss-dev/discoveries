"""A072633 counterexample: second, independent certificate with mpmath interval arithmetic.
Shares no code with verify_arb.py.  Run:  python verify_mpmath.py counterexample_n.txt"""
import sys
from mpmath import iv, mp

n = int(open(sys.argv[1]).read().split()[0])
iv.dps = 1500; mp.dps = 1500

x = iv.mpf(n) / iv.log(2)                       # interval enclosing n/log 2
k = int(mp.nint(mp.mpf(n) / mp.log(2)))
d = (iv.mpf(k) + iv.mpf(1) / 2) - x             # must be strictly inside (0, 1) for round() = k
assert d.a > 0 and d.b < 1
print("digits of n:", len(str(n)))
print("(k + 1/2) - n/log 2 in [%s, %s]  => round(n/log 2) = k, F = k + 1" % (mp.nstr(mp.mpf(d.a), 8), mp.nstr(mp.mpf(d.b), 8)))
F = k + 1

def enclosure(m, J):
    """Interval for sum_{j<=J} (1 - j/M)^n and an upper bound for the tail, M = m + 1."""
    M = iv.mpf(m) + 1; nn = iv.mpf(n); s = iv.mpf(0)
    for j in range(1, J + 1):
        s += iv.exp(nn * iv.log(1 - iv.mpf(j) / M))
    u = nn / M                                   # (1 - j/M)^n <= exp(-j u)
    tail = iv.exp(-(J + 1) * u) / (1 - iv.exp(-u))
    return s, tail

s, tail = enclosure(F, 2600)
upper = (s + tail).b
print("R(F)   <= 1 + (%s)     [tail bound %s]" % (mp.nstr(mp.mpf(upper) - 1, 12), mp.nstr(mp.mpf(tail.b), 4)))
s2, _ = enclosure(F + 1, 1400)
lower = s2.a
print("R(F+1) >= 1 + (%s)" % mp.nstr(mp.mpf(lower) - 1, 12))
assert mp.mpf(upper) < 1 <= mp.mpf(lower)
print("CERTIFIED: R(F) < 1 <= R(F+1), so a(n) = F + 1 = 2 + round(n/log 2)")
