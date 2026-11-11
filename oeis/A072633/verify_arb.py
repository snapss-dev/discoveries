"""A072633: rigorous verification with Arb ball arithmetic (python-flint).

Notation.  L = log 2, theta = 2/L.  For integers M >= 2, n >= 1 let
    S(M, n) = sum_{k=1}^{M-1} (k/M)^n,
so that  1^n + ... + (M-1)^n >= M^n  iff  S(M, n) >= 1.  OEIS A072633 is a(n) = min{M : S(M, n) >= 1} - 1,
and the conjectured formula is F(n) = 1 + round(n/L).

Every comparison below is decided by Arb balls: an assertion passes only if it holds for every
real number in the ball.  Sections:
  1. Lemma A for 2 <= M <= 10^4:  n >= L(M - 3/2)  =>  S(M, n) < 1.
  2. Re-check of Best & te Riele's Theorem 3 for 2 <= M <= 10^4:  n <= L(M - 3/2 - 1/(256 M)) => S >= 1.
  3. Direct check that a(n) = F(n) for 1 <= n <= 6900.
  4. Continued fraction of 2/log 2; reproduction of Best & te Riele's Table 2 (calibration).
  5. All candidates for a(n) != F(n) among convergents (mu < 1/250, which contains the window
     mu < 1/256 of Best & te Riele and the window mu < 0.004 of Gallot-Moree-Zudilin); certificate for each.
Run:  python verify_arb.py [max_k]      (default max_k = 1300)
"""
import sys, time
from flint import arb, ctx, fmpz

def log2():
    return arb.const_log2()

def certain_int(x, what):
    """floor of a ball, required to be unique."""
    f = x.floor().unique_fmpz()
    if f is None:
        raise RuntimeError("precision too low to decide " + what)
    return int(f)

def S_ball(M, n, J=None):
    """Ball enclosing S(M, n).  Sums j = 1..J exactly as balls ((1 - j/M)^n), and encloses the tail
    sum_{j>J} (1 - j/M)^n in [0, e^{-(J+1)u}/(1 - e^{-u})] with u = n/M, using 1 - x <= e^{-x}."""
    Mb = arb(M); nb = arb(n)
    top = M - 1 if J is None else min(M - 1, J)
    s = arb(0)
    for j in range(1, top + 1):
        s += (nb * (1 - arb(j) / Mb).log()).exp()
    if top < M - 1:
        u = nb / Mb
        tail_hi = (-(top + 1) * u).exp() / (1 - (-u).exp())
        s += tail_hi.union(arb(0))          # tail lies in [0, tail_hi]
    return s

def holds(M, n):
    """True iff 1^n + ... + (M-1)^n >= M^n.  Exact integers for M <= 600 (this also settles the one
    case of equality, 1 + 2 = 3); certified balls above that."""
    if M <= 600:
        return sum(pow(k, n) for k in range(1, M)) >= pow(M, n)
    s = S_ball(M, n, J=600)
    if s >= 1: return True
    if s < 1: return False
    raise RuntimeError("undecided at M=%d n=%d" % (M, n))

def section1_2_3(MMAX=10000):
    ctx.prec = 160
    L = log2()
    t = time.time(); worstA = None; worstB = None
    for M in range(2, MMAX + 1):
        # Lemma A: smallest integer n >= L(M - 3/2)
        x = L * (arb(M) - arb(3) / 2)
        n0 = certain_int(x, "ceil") + 1                     # x is irrational, so ceil = floor + 1
        n0 = max(n0, 1)
        assert not holds(M, n0), ("Lemma A fails?", M, n0)
        s = S_ball(M, n0, J=None if M <= 600 else 600)
        gap = float((1 - s).lower()) * M * M
        if worstA is None or gap < worstA[0]: worstA = (gap, M, n0)
        # Theorem 3 (Best & te Riele): largest integer n <= L(M - 3/2 - 1/(256 M))
        y = L * (arb(M) - arb(3) / 2 - 1 / (arb(256) * M))
        n1 = certain_int(y, "floor")
        if n1 >= 1:
            assert holds(M, n1), ("Theorem 3 fails?", M, n1)
            s1 = S_ball(M, n1, J=None if M <= 600 else 600)
            g1 = float((s1 - 1).mid()) * M * M
            if worstB is None or g1 < worstB[0]: worstB = (g1, M, n1)
    print(f"1. Lemma A verified for 2 <= M <= {MMAX}: S(M, ceil(L(M-3/2))) < 1.  "
          f"Smallest (1-S)*M^2 = {worstA[0]:.6f} at M={worstA[1]}, n={worstA[2]}   [{time.time()-t:.0f} s]")
    print(f"2. Theorem 3 re-checked for 2 <= M <= {MMAX}: S(M, floor(L(M-3/2-1/(256M)))) >= 1.  "
          f"Smallest (S-1)*M^2 = {worstB[0]:.6f} at M={worstB[1]}, n={worstB[2]}")
    # 3. direct check of a(n) = F(n)
    t = time.time(); NMAX = 6900
    for n in range(1, NMAX + 1):
        x = arb(n) / L + arb(1) / 2
        F = certain_int(x, "round") + 1                     # 1 + round(n/L) = 1 + floor(n/L + 1/2)
        MF = F + 1
        assert holds(MF, n) and not holds(MF - 1, n), n
    print(f"3. a(n) = 1 + round(n/log 2) verified directly for 1 <= n <= {NMAX}   [{time.time()-t:.0f} s]")

BTR_TABLE2 = {35:0.02388,39:0.06676,41:0.01927,57:0.07266,77:0.06805,89:0.06600,91:0.01087,95:0.00685,
              157:0.08313,163:0.03168,195:0.06865,211:0.06792,255:0.06420,261:0.03473,267:0.03549,
              299:0.03870,313:0.07763,317:0.05315,321:0.08067,369:0.03335,399:0.07507,431:0.08035,
              439:0.02296,443:0.01758,447:0.04750,453:0.05180,467:0.01639,481:0.00913,485:0.01612,
              497:0.05776,507:0.05120,575:0.06678,583:0.04983}

def continued_fraction(kmax, bits):
    ctx.prec = bits
    x = 2 / log2()
    b = []
    for i in range(kmax + 2):
        a = certain_int(x, f"partial quotient {i}")
        b.append(a)
        x = 1 / (x - a)
    return b

def certify(M, n):
    """Decide S(M, n) >= 1 or < 1 rigorously; returns (+1 or -1, ball of S - 1)."""
    digits = len(str(n))
    for bits in (8 * digits + 600, 16 * digits + 2000):
        ctx.prec = bits
        J = int(7.0 * digits) + 400            # 2^-J far below the margin ~ 10^(-2*digits)
        s = S_ball(M, n, J=J) - 1
        if s < 0: return -1, s
        if s >= 0: return +1, s
    raise RuntimeError("undecided")

def section4_5(kmax):
    bits = int(kmax * 12) + 4000
    b = continued_fraction(kmax, bits)
    b2 = continued_fraction(kmax, bits + 3000)              # second precision: must agree
    assert b == b2
    print(f"4. 2/log 2 = [{', '.join(map(str, b[:20]))}, ...]  ({kmax+2} partial quotients certified at two precisions)")
    P = [b[0]]; Q = [1]; pm, qm = 1, 0
    for a in b[1:kmax + 1]:
        p = a * P[-1] + pm; q = a * Q[-1] + qm
        pm, qm = P[-1], Q[-1]; P.append(p); Q.append(q)
    ctx.prec = bits + 3000
    L = log2()
    def mu(M, n):                                           # n = (M - 3/2 - mu/M) L
        return arb(M) * (arb(M) - arb(3) / 2 - arb(n) / L)
    found = {}
    cands = []
    for k in range(1, kmax + 1, 2):                         # odd k: p_k/q_k > theta
        p, q = P[k], Q[k]
        if p % 2 == 0: continue
        m = mu((p + 3) // 2, q)
        assert m > 0, k
        if (m > arb(1) / 256) and (m < arb(1) / 12) and k <= 599:
            found[k] = float(m.mid())
        if m < arb(1) / 250:
            cands.append((k, 1, float(m.mid())))
        # odd multiples t >= 3 of the convergent: mu grows like t^2
        t = 3
        while True:
            mt = mu((t * p + 3) // 2, t * q)
            if not (mt < arb(1) / 250): break
            cands.append((k, t, float(mt.mid()))); t += 2
    ok = (sorted(found) == sorted(BTR_TABLE2)) and all(abs(found[k] - BTR_TABLE2[k]) < 6e-6 for k in found)
    print(f"   Best & te Riele Table 2 (33 values of k <= 599 with 1/256 < mu < 1/12) reproduced exactly: {ok}")
    assert ok
    print(f"5. Candidates (k odd, p_k odd, 0 < mu < 1/250 = 0.004, and odd multiples t) for k <= {kmax}:")
    c1 = 25 / 12 - 3 * 0.6931471805599453
    first = None
    for k, t, m in cands:
        n = t * Q[k]; M = (t * P[k] + 3) // 2               # M = F(n) + 1
        ctx.prec = bits + 3000
        x = arb(n) / log2() + arb(1) / 2
        F = certain_int(x, "round") + 1
        assert M == F + 1, (k, t)
        sgn0, s0 = certify(M, n)                            # is the formula's value enough?
        sgn1, s1 = certify(M + 1, n)
        assert sgn1 == +1
        fails = (sgn0 == -1)
        print(f"   k={k:5d} t={t} digits(n)={len(str(n)):4d} b_(k+1)={b[k+1]:6d} mu={m:.6f} (c1={c1:.6f})"
              f"  S(F+1,n)-1 = {s0.mid().str(8, radius=False)}  ->  a(n) = F(n){'+1  ** formula FAILS **' if fails else '      formula holds'}")
        if fails and first is None: first = (k, t, n, M, s0, s1)
    if first:
        k, t, n, M, s0, s1 = first
        print(f"\n   FIRST FAILURE: k = {k} (b_0 = 2 is k = 0), n = q_{k} has {len(str(n))} digits")
        print(f"   n = {n}")
        print(f"   F(n) = 1 + round(n/log 2) = {M-1}")
        print(f"   S(F+1, n) - 1 in {s0.str(12)}   (< 0: the formula's m is too small)")
        print(f"   S(F+2, n) - 1 in {s1.str(12)}   (>= 0)")
        print(f"   hence a(n) = F(n) + 1.")
    return first

if __name__ == "__main__":
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 1300
    t0 = time.time()
    section1_2_3()
    section4_5(kmax)
    print(f"\nall assertions passed   [{time.time()-t0:.0f} s total]")
