"""A125314: smallest k > 1 such that S_n(k) = Sum_{i=1..k} i^n divides (k!)^n.
S_n(k) = (product of integer polynomials f_i(k)^m_i) / den.  A necessary condition is that every prime factor
of every f_i(k) (apart from primes of den) is <= k.  Sieve: for every prime p < K and every root r of f_i mod p,
lifted to all prime powers p^e that can divide f_i(k) for some k <= K, add m_i*log(p) on the class k = r mod p^e.
k is a candidate when the accumulated sum equals sum_i m_i*log|f_i(k)| (so prod f_i(k) is completely factored
over primes < segment end).  Candidates are then tested exactly.
Usage: a125314_sieve.py n K [rootfile-prefix,... for the factor of degree > 2]"""
import sys, time, math
import numpy as np
import numba
from numba import njit, prange
import sympy as sp
import flint

n = int(sys.argv[1]); K = int(float(sys.argv[2])); rootfiles = sys.argv[3].split(",") if len(sys.argv) > 3 else []
numba.set_num_threads(4)
t0 = time.time()

ks, isym = sp.symbols("k i")
Spoly = sp.factor(sp.summation(isym ** n, (isym, 1, ks)))
num, den = sp.fraction(sp.together(Spoly))
den = int(den)
cont, facs = sp.factor_list(num)
assert cont == 1, cont
F = []  # (coeff list low->high, multiplicity)
for f, m in facs:
    F.append(([int(c) for c in sp.Poly(f, ks).all_coeffs()[::-1]], int(m)))
print("n", n, "den", den, "factors", F, flush=True)

def primes_upto(N):
    s = np.ones(N + 1, np.bool_); s[:2] = False
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

def ev(c, x, mod):
    v = 0
    for a in reversed(c): v = (v * x + a) % mod
    return v

def lifted_classes(c, p, r, K, out):
    """all classes (q = p^e, residue) with p^e | f(k) for k = residue mod q, k = r mod p, reachable for k <= K"""
    dc = [i * a for i, a in enumerate(c)][1:]
    level = [r]; q = p
    out.append((q, r))
    while level:
        nxt = []
        q2 = q * p
        for x in level:
            if q > K and not (1 <= x <= K): continue
            if ev(dc, x, p) != 0:
                fx = ev(c, x, q2) // q
                t = (-fx * pow(ev(dc, x, p), -1, p)) % p
                y = x + t * q
                if q2 <= K or 1 <= y <= K: nxt.append(y); out.append((q2, y))
            else:
                if p > 20000: raise RuntimeError("non-simple root for large p %d" % p)
                for t in range(p):
                    y = x + t * q
                    if ev(c, y, q2) == 0 and (q2 <= K or 1 <= y <= K):
                        nxt.append(y); out.append((q2, y))
        level = nxt; q = q2

PR = primes_upto(K)
Qs = []; Rs = []; Ps = []; Ws = []
for c, m in F:
    deg = len(c) - 1
    if deg > 2 and rootfiles:
        pp = np.concatenate([np.load(f + "_p.npy") for f in rootfiles]); rr = np.concatenate([np.load(f + "_r.npy") for f in rootfiles])
        assert pp.max() >= PR[-1] and len(np.unique(pp)) <= len(PR)
        it = zip(pp.tolist(), rr.tolist())
    else:
        def gen(c=c):
            for p in PR:
                p = int(p)
                if all(a % p == 0 for a in c): raise RuntimeError("content")
                for r, mult in flint.nmod_poly(c, p).roots():
                    yield p, int(r)
        it = gen()
    cnt = 0
    for p, r in it:
        if p > K: continue
        out = []
        lifted_classes(c, p, r, K, out)
        for q, x in out:
            Qs.append(q); Rs.append(x); Ps.append(p); Ws.append(m * math.log(p))
        cnt += 1
    print("factor deg", deg, "roots", cnt, "classes so far", len(Qs), f"{time.time()-t0:.0f}s", flush=True)
Qs = np.array(Qs, np.int64); Rs = np.array(Rs, np.int64); Ps = np.array(Ps, np.int64); Ws = np.array(Ws, np.float64)
o = np.argsort(Ps, kind="stable"); Qs = Qs[o]; Rs = Rs[o]; Ps = Ps[o]; Ws = Ws[o]

@njit(parallel=True, cache=True)
def sieve(lo0, nseg, S, Q, R, W, P, coef, mult, off, outk, maxc):
    for s in prange(nseg):
        lo = lo0 + s * S
        A = np.zeros(S, np.float64)
        hi = lo + S
        for i in range(len(Q)):
            if P[i] >= hi: break
            q = Q[i]
            t = (R[i] - lo) % q
            w = W[i]
            while t < S:
                A[t] += w
                t += q
        c = 0
        for t in range(S):
            k = lo + t
            if k < 2: continue
            x = float(k); tot = 0.0
            for f in range(len(mult)):
                v = 0.0
                for j in range(off[f + 1] - 1, off[f] - 1, -1):
                    v = v * x + coef[j]
                tot += mult[f] * math.log(abs(v))
            if A[t] > tot - 0.5 and c < maxc:
                outk[s, c] = k; c += 1

coef = np.array([a for c, m in F for a in c], np.float64)
off = np.cumsum([0] + [len(c) for c, m in F]).astype(np.int64)
mult = np.array([m for c, m in F], np.float64)

def vfact(k, p):
    v = 0
    while k: k //= p; v += k
    return v

def exact(k):
    """exact test of the definition through the factorisation of S_n(k)"""
    N = 1
    fac = {}
    for c, m in F:
        v = abs(ev(c, k, 10 ** 400))  # plain integer value (modulus larger than any value)
        v = sum(a * k ** i for i, a in enumerate(c))
        N *= v ** m
        for p, e in flint.fmpz(abs(v)).factor():
            fac[int(p)] = fac.get(int(p), 0) + int(e) * m
    assert N % den == 0
    for p, e in flint.fmpz(den).factor():
        fac[int(p)] -= int(e)
    return all(p <= k and e <= n * vfact(k, p) for p, e in fac.items() if e > 0), fac

S = 1 << 21; nseg = 8; maxc = 4096
lo0 = 0; found = None; ncand = 0
print("classes", len(Qs), "sieving", f"{time.time()-t0:.0f}s", flush=True)
while lo0 <= K and found is None:
    outk = np.full((nseg, maxc), -1, np.int64)
    sieve(lo0, nseg, S, Qs, Rs, Ws, Ps, coef, mult, off, outk, maxc)
    for s in range(nseg):
        assert outk[s, maxc - 1] < 0
        for c in range(maxc):
            k = int(outk[s, c])
            if k < 0: break
            if k > K: break
            ncand += 1
            ok, fac = exact(k)
            if k <= 3000:
                lit = pow(math.factorial(k), n, sum(i ** n for i in range(1, k + 1))) == 0
                assert lit == ok, (k, lit, ok)
            if ok and found is None:
                found = k
                print("FOUND k =", k, "S_n(k) =", " * ".join(f"{p}^{e}" for p, e in sorted(fac.items()) if e), flush=True)
    lo0 += nseg * S
print("n", n, "result", found, "searched k <=", min(K, lo0 - 1), "candidates tested exactly", ncand, f"{time.time()-t0:.0f}s")
