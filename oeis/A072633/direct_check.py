"""A072633: direct verification that a(n) = F(n) = 1 + round(n/log 2) for all 1 <= n <= NMAX.

Why: Gallot, Moree & Zudilin (Math. Comp. 2011, Theorem 1) control the crossover only for M > 10^9.
This script covers every n whose M = F(n) + 1 is at most 10^9 (and a little more) by computation,
so the minimality proof does not need the unrefereed Theorem 3 of Best & te Riele (1976).

By Lemma A, a(n) >= F(n) always.  So a(n) = F(n) iff S(F+1, n) >= 1, where
    S(M, n) = sum_{j=1}^{M-1} (1 - j/M)^n.
All terms are positive, so any partial sum >= 1 proves S >= 1.

Stage 1 (numba, float64): partial sum of the first 64 terms.  The accumulated floating-point error
is below 1e-14 (each term exp(n*log1p(-j/M)) carries a relative error of a few ulp times j, and
the terms decay like 2^-j).  n is accepted if the computed partial sum is >= 1 + 1e-12, and only if
n/log 2 is at least 1e-6 away from a half-integer (so that round() in float64 is unambiguous).
Stage 2 (Arb balls): every n not accepted in stage 1 is decided rigorously.

Run:  python direct_check.py [NMAX] [threads]      default NMAX = 693200000
"""
import sys, time, math
import numpy as np
from numba import njit, prange, set_num_threads

L = math.log(2.0)

@njit(parallel=True, cache=False)
def stage1(n0, n1, out_flags):
    """Flags n in [n0, n1) that stage 1 cannot accept.  Returns the count of flagged n."""
    cnt = 0
    for i in prange(n1 - n0):
        n = n0 + i
        x = n / 0.6931471805599453
        r = np.floor(x + 0.5)
        frac = x + 0.5 - r                       # in [0, 1); distance of n/L from the half-integers
        if frac < 1e-6 or frac > 1.0 - 1e-6:
            out_flags[i] = 1; cnt += 1; continue
        M = r + 2.0                               # M = F + 1 = round(n/L) + 2
        s = 0.0
        ok = False
        for j in range(1, 65):
            if j >= M: break
            s += math.exp(n * math.log1p(-j / M))
            if s >= 1.0 + 1e-12:
                ok = True; break
        if not ok:
            out_flags[i] = 1; cnt += 1
    return cnt

def stage2(ns):
    from flint import arb, ctx
    ctx.prec = 160
    Lb = arb.const_log2()
    bad = []
    for n in ns:
        n = int(n)
        x = arb(n) / Lb + arb(1) / 2
        r = x.floor().unique_fmpz()
        assert r is not None, n
        M = int(r) + 2
        if M <= 600:
            ok = sum(pow(k, n) for k in range(1, M)) >= pow(M, n)
        else:
            Mb = arb(M); nb = arb(n); s = arb(0); ok = False
            for j in range(1, min(M, 400)):
                s += (nb * (1 - arb(j) / Mb).log()).exp()
                if s >= 1: ok = True; break
            if not ok and not (s < 1): raise RuntimeError("undecided n=%d" % n)
        if not ok: bad.append(n)
    return bad

if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 693200000
    threads = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    set_num_threads(threads)
    t0 = time.time(); CH = 20_000_000
    flagged_total = 0; bad = []
    for n0 in range(1, NMAX + 1, CH):
        n1 = min(n0 + CH, NMAX + 1)
        flags = np.zeros(n1 - n0, dtype=np.uint8)
        c = stage1(n0, n1, flags)
        idx = np.nonzero(flags)[0] + n0
        b = stage2(idx)
        flagged_total += c; bad += b
        print(f"n in [{n0}, {n1-1}]: stage-2 cases {c}, failures {len(b)}   [{time.time()-t0:.0f} s]", flush=True)
    print(f"DONE: a(n) = 1 + round(n/log 2) for all 1 <= n <= {NMAX}: {len(bad) == 0}; "
          f"stage-2 cases {flagged_total}; failures {bad[:10]}")
    Mtop = round(NMAX / L) + 2
    print(f"largest M = F + 1 covered: {Mtop}  (> 10^9: {Mtop > 10**9})")
