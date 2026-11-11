"""A332102: least m > 0 with 2*m^n <= sum_{k<m} k^n.  Conjecture in the entry: a(n) = round(n/log(3/2) + 3).

Certifies with Arb ball arithmetic (python-flint) that at the 1614-digit n in counterexample_n.txt
    S(F, n) < 2 <= S(F+1, n),   S(M, n) = sum_{k=1}^{M-1} (k/M)^n,   F = round(n/log(3/2) + 3),
so a(n) = F + 1.  (S(M, n) is increasing in M, since k/M <= (k+1)/(M+1) term by term.)
Run:  python check.py      (about half a minute)
"""
import os, time
from flint import arb, ctx

def S_ball(M, n, J):
    """Ball enclosing S(M, n): terms j = 1..J as balls, plus the tail in [0, e^{-(J+1)u}/(1 - e^{-u})],
    u = n/M, which follows from 1 - x <= e^{-x}."""
    Mb = arb(M); nb = arb(n); s = arb(0)
    for j in range(1, J + 1):
        s += (nb * (1 - arb(j) / Mb).log()).exp()
    u = nb / Mb
    tail_hi = (-(J + 1) * u).exp() / (1 - (-u).exp())
    return s + tail_hi.union(arb(0))

here = os.path.dirname(os.path.abspath(__file__))
n = int(open(os.path.join(here, "counterexample_n.txt")).read().split()[0])
ctx.prec = 17500
L = (arb(3) / 2).log()
F = int((arb(n) / L + 3 + arb(1) / 2).floor().unique_fmpz())       # round(n/log(3/2) + 3), certified
t = time.time()
s0 = S_ball(F, n, 19500) - 2
s1 = S_ball(F + 1, n, 19500) - 2
print("digits of n:", len(str(n)))
print("S(F, n)   - 2 =", s0.mid().str(10, radius=False), "  certified negative:", bool(s0 < 0))
print("S(F+1, n) - 2 =", s1.mid().str(10, radius=False), "  certified positive:", bool(s1 > 0))
assert s0 < 0 and s1 > 0
print("hence a(n) = F + 1 = round(n/log(3/2) + 3) + 1      [%.0f s]" % (time.time() - t))

# the definition and the formula agree for small n
def a_def(nn):
    m = 1
    while 2 * m ** nn > sum(k ** nn for k in range(1, m)): m += 1
    return m
import mpmath as mp
mp.mp.dps = 30
print("a(0..7) from the definition:", [a_def(i) for i in range(8)], "(entry: 3, 5, 8, 10, 13, 15, 18, 20)")
print("formula = definition for n <= 300:", all(a_def(i) == int(mp.nint(i / mp.log(1.5) + 3)) for i in range(301)))
