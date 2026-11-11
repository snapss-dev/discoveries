# Recomputes the numerical tables of the NIST Digital Library of Mathematical Functions listed in
# README/PAGE (release 1.2.x as fetched on 2026-11-11) and reports every printed entry that is not the
# correctly rounded value.  Two independent methods per entry:
#   Gauss rules: Arb (python-flint) on exact rational moments / certified Legendre roots, and mpmath.
#   Zeros and special values: mpmath root finding, and Arb.
#   Integer tables: two different formulas or a library and a direct recurrence.
# Usage: python check.py     (reads dlmf_tables.json next to this file)
import os, sys, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
TABLES = os.path.join(HERE, 'dlmf_tables.json')
# Recompute DLMF 3.5 Gauss tables two ways.
import json, re, sys
from fractions import Fraction
import flint, mpmath
from flint import fmpq, fmpq_mat, fmpz_poly, fmpq_poly, arb, acb
flint.ctx.prec=600
mpmath.mp.dps=120
T=json.load(open(TABLES,encoding='utf8'))
def num(cell, exp=''):
    s=cell.replace('\;','').replace('\u2009','').replace(' ','').replace('\u2005','').replace('\xa0','')
    s=re.sub(r'[^0-9.+\-]','',s)
    e=0
    m=re.search(r'10\^\{(-?\d+)\}',exp or '')
    if m: e=int(m.group(1))
    return s,e
def parse_pairs(rows):
    out=[]
    for r in rows[1:]:
        r=[c for c in r]
        if len(r)==2: out.append((num(r[0]),num(r[1])))
        elif len(r)==4: out.append((num(r[0],r[1]),num(r[2],r[3])))
    return out
def ortho_poly(n, mom):
    # monic p_n orthogonal for exact rational moments mom[0..2n-1]
    A=fmpq_mat(n,n,[mom(i+j) for i in range(n) for j in range(n)])
    b=fmpq_mat(n,1,[-mom(i+n) for i in range(n)])
    c=A.solve(b)
    return [c[i,0] for i in range(n)]+[fmpq(1)]
def rule_exact(n, mom):
    co=ortho_poly(n,mom)
    P=fmpq_poly(co)
    den=P.denom(); Z=fmpz_poly([int(x) for x in (P*den).numer().coeffs()]) if hasattr(P,'numer') else None
    roots=[r for r,m in Z.complex_roots()]
    xs=sorted([r.real for r in roots], key=lambda a: float(a.mid()))
    ca=[arb(c.p)/arb(c.q) for c in co]
    res=[]
    for x in xs:
        # synthetic division p/(x-xj): q_{n-1}=1, q_{k-1}=c_k + x q_k
        q=[None]*n; q[n-1]=arb(1)
        for k in range(n-1,0,-1): q[k-1]=ca[k]+x*q[k]
        dp=sum(k*ca[k]*x**(k-1) for k in range(1,n+1))
        w=sum(q[k]*(arb(mom(k).p)/arb(mom(k).q)) for k in range(n))/dp
        res.append((x,w))
    return res
def fmt_ok(printed, e, val):
    # printed: decimal string (mantissa), e exponent; val arb. Return 'ok-round','ok-trunc','BAD'
    s=printed; neg=s.startswith('-'); s=s.lstrip('+-')
    nd=len(s.split('.')[1]) if '.' in s else 0
    scaled=abs(val)/arb(10)**e*arb(10)**nd   # should be near integer int(s without '.')
    pi=int(s.replace('.',''))
    lo=scaled-pi
    # round: |lo|<=0.5 ; trunc: 0<=lo<1
    r=''
    if lo.abs_upper()<0.5: r='ok-round'
    elif (lo>0)==True and (lo<1)==True: r='ok-trunc'
    else: r='BAD'
    if (val<0)==True and not neg and pi!=0: r='BAD-sign'
    return r
results=[]
def compare(tab, comp1, comp2, label):
    pr=parse_pairs(T[tab]['rows'])
    bad=0; n=0
    # match printed rows to computed by nearest node
    for (xs,xe),(ws,we) in pr:
        xv=float(xs)*10**xe
        j=min(range(len(comp1)), key=lambda i: abs(float(comp1[i][0].mid())-xv))
        x1,w1=comp1[j]
        j2=min(range(len(comp2)), key=lambda i: abs(float(comp2[i][0])-xv))
        x2,w2=comp2[j2]
        agree = abs(mpmath.mpf(x1.mid().str(100,radius=False))-x2)<mpmath.mpf(10)**(-60)*max(1,abs(x2)) and abs(mpmath.mpf(w1.mid().str(100,radius=False))-w2)<mpmath.mpf(10)**(-60)*abs(w2)
        for s,e,v in ((xs,xe,x1),(ws,we,w1)):
            st=fmt_ok(s,e,v); n+=1
            if st!='ok-round' or not agree:
                bad+=1; print('  NOT CORRECTLY ROUNDED',tab,'printed',s,'x 10^%d'%e,'| value',(v/arb(10)**e).str(len(s)+6,radius=False),'|',st,'| methods agree' if agree else '| METHODS DISAGREE')
            results.append((tab,s,e,st))
    print(tab,label,'values',n,'bad',bad,'conventions',sorted(set(r[3] for r in results if r[0]==tab)))
# --- Legendre
def leg_mp(n):
    def pn(x):
        p0,p1=mpmath.mpf(1),x
        for k in range(2,n+1): p0,p1=p1,((2*k-1)*x*p1-(k-1)*p0)/k
        return p1,n*(x*p1-p0)/(x*x-1)
    out=[]
    for k in range(1,n+1):
        x=mpmath.cos(mpmath.pi*(k-mpmath.mpf(1)/4)/(n+mpmath.mpf(1)/2))
        for it in range(12):
            p,d=pn(x); x=x-p/d
        p,d=pn(x)
        out.append((x,2/((1-x*x)*d*d)))
    return out
for tab,n in (('Table 3.5.1',5),('Table 3.5.2',10),('Table 3.5.3',20),('Table 3.5.4',40),('Table 3.5.5',80)):
    c1=[arb.legendre_p_root(n,k,weight=True) for k in range(n)]
    if n<=20:
        c0=rule_exact(n, lambda k: fmpq(2,k+1) if k%2==0 else fmpq(0))
        for (a,b),(c,d) in zip(sorted(c1,key=lambda t: float(t[0].mid())),c0): assert a.overlaps(c) and b.overlaps(d)
    compare(tab,c1,leg_mp(n),'Gauss-Legendre n=%d'%n)
# --- Laguerre
def fact(k): return fmpq(int(mpmath.factorial(k)))
def lag_mp(n):
    rts=mpmath.polyroots(mpmath.taylor(lambda t: mpmath.laguerre(n,0,t),0,n)[::-1],maxsteps=500,extraprec=2000)
    return [(mpmath.re(x), mpmath.re(x)/((n+1)**2*mpmath.laguerre(n+1,0,mpmath.re(x))**2)) for x in rts]
for tab,n in (('Table 3.5.6',5),('Table 3.5.7',10),('Table 3.5.8',15),('Table 3.5.9',20)):
    compare(tab,rule_exact(n,fact),lag_mp(n),'Gauss-Laguerre n=%d'%n)
# --- Hermite: moments mu_{2j}=sqrt(pi)*(2j)!/(4^j j!)
def hmom(k):
    if k%2: return fmpq(0)
    j=k//2
    return fmpq(int(mpmath.factorial(2*j)), 4**j*int(mpmath.factorial(j)))
def her_mp(n):
    co=mpmath.taylor(lambda t: mpmath.hermite(n,t),0,n)[::-1]
    rts=mpmath.polyroots(co,maxsteps=500,extraprec=2000)
    return [(mpmath.re(x), 2**(n-1)*mpmath.factorial(n)*mpmath.sqrt(mpmath.pi)/(n**2*mpmath.hermite(n-1,mpmath.re(x))**2)) for x in rts]
for tab,n in (('Table 3.5.10',5),('Table 3.5.11',10),('Table 3.5.12',15),('Table 3.5.13',20)):
    c=[(x,w*arb.pi().sqrt()) for x,w in rule_exact(n,hmom)]
    compare(tab,c,her_mp(n),'Gauss-Hermite n=%d'%n)
# --- log weight ln(1/x) on (0,1): mu_k=1/(k+1)^2
def log_mp(n):
    # Golub-Welsch from Cholesky of the Hankel matrix at high precision
    old=mpmath.mp.dps; mpmath.mp.dps=250
    H=mpmath.matrix(n+1,n+1)
    for i in range(n+1):
        for j in range(n+1): H[i,j]=mpmath.mpf(1)/(i+j+1)**2
    L=mpmath.cholesky(H); R=L.T
    al=[];be=[]
    for j in range(n):
        a=R[j,j+1]/R[j,j]-(R[j-1,j]/R[j-1,j-1] if j>0 else 0); al.append(a)
        if j<n-1: be.append(R[j+1,j+1]/R[j,j])
    J=mpmath.matrix(n,n)
    for j in range(n):
        J[j,j]=al[j]
        if j<n-1: J[j,j+1]=be[j]; J[j+1,j]=be[j]
    E,Q=mpmath.eigsy(J)
    out=[(E[i],Q[0,i]**2*H[0,0]) for i in range(n)]
    mpmath.mp.dps=old
    return [(+a,+b) for a,b in out]
for tab,n in (('Table 3.5.14',5),('Table 3.5.15',10),('Table 3.5.16',15),('Table 3.5.17',20)):
    compare(tab,rule_exact(n,lambda k: fmpq(1,(k+1)**2)),log_mp(n),'Gauss log-weight n=%d'%n)


# ---------------------------------------------------------------- other tables
import itertools, math
from fractions import Fraction
import flint, mpmath, sympy
from flint import arb, acb
flint.ctx.prec = 300
mp = mpmath.mp; mp.dps = 60

res = []   # (table, what, printed, status)
def cl(c):
    c = c.replace('\\;', '').replace('\\,', '').replace('%\n', '')
    return re.sub(r'[\s  \xa0  ]', '', c)
def chk(tab, what, printed, e, v1, v2):
    s = cl(printed); neg = s.startswith('-'); t = s.lstrip('+-')
    nd = len(t.split('.')[1]) if '.' in t else 0
    pi = int(t.replace('.', ''))
    v1 = mpmath.mpf(v1); v2 = mpmath.mpf(v2)
    agree = abs(v1 - v2) <= mpmath.mpf(10) ** (-nd - 8 + e)
    d = abs(v1) / mpmath.mpf(10) ** e * mpmath.mpf(10) ** nd - pi
    if abs(d) <= 0.5: st = 'ok-round'
    elif 0 < d < 1: st = 'ok-trunc'
    else: st = 'BAD'
    if pi != 0 and (v1 < 0) != neg: st = 'BAD-sign'
    if not agree: st += '/METHODS-DISAGREE'
    res.append((tab, what, s + ('e%d' % e if e else ''), st))
    if st != 'ok-round': print('  NOTE', tab, what, 'printed', s, 'e', e, 'value', mpmath.nstr(v1, nd + 8), st)
def chki(tab, what, printed, v1, v2):
    s = cl(printed).replace('−', '-')
    try: p = int(s)
    except Exception:
        res.append((tab, what, s, 'UNPARSED')); print('  UNPARSED', tab, what, ascii(s)); return
    st = 'ok' if (p == v1 == v2) else ('BAD' if v1 == v2 else 'METHODS-DISAGREE')
    res.append((tab, what, s, st))
    if st != 'ok': print('  NOTE', tab, what, 'printed', p, 'computed', v1, v2)
def arbf(x): return mpmath.mpf(x.mid().str(70, radius=False))
# ---- 5.4.1 zeros of psi
tab = 'Table 5.4.1'
for r in T[tab]['rows'][1:]:
    n = int(r[0]); x0 = mpmath.mpf(cl(r[1]))
    x1 = mpmath.findroot(mpmath.digamma, x0)
    lo = arb(str(x1)) - arb(10) ** -40; hi = arb(str(x1)) + arb(10) ** -40
    a = lo.digamma(); b = hi.digamma()
    assert (a < 0 and b > 0) or (a > 0 and b < 0), (n, a, b)   # certified sign change
    x2 = (lo + hi) / 2
    chk(tab, 'x_%d' % n, r[1], 0, x1, arbf(x2))
    chk(tab, 'Gamma(x_%d)' % n, r[2], 0, mpmath.gamma(x1), arbf(x2.gamma()))
# ---- 7.13 complex zeros
def newton_acb(f, df, z0):
    z = acb(z0.real, z0.imag)
    for i in range(60):
        z = acb(z.real.mid(), z.imag.mid()); z = z - f(z) / df(z)
    return acb(z.real.mid(), z.imag.mid())
sp = acb(arb.pi()).sqrt()
funcs = {'Table 7.13.1': (mpmath.erf, lambda z: z.erf(), lambda z: 2 / sp * (-z * z).exp()),
         'Table 7.13.2': (mpmath.erfc, lambda z: z.erfc(), lambda z: -2 / sp * (-z * z).exp()),
         'Table 7.13.3': (mpmath.fresnelc, lambda z: z.fresnel_c(), lambda z: (acb(arb.pi()) * z * z / 2).cos()),
         'Table 7.13.4': (mpmath.fresnels, lambda z: z.fresnel_s(), lambda z: (acb(arb.pi()) * z * z / 2).sin())}
for tab, (fm, fa, dfa) in funcs.items():
    for r in T[tab]['rows'][1:]:
        n = int(r[0]); xs, ys = cl(r[1]), cl(r[2])
        z0 = complex(float(xs), float(ys))
        z1 = mpmath.findroot(fm, mpmath.mpc(z0))
        z2 = newton_acb(fa, dfa, z0)
        chk(tab, 'x_%d' % n, xs, 0, z1.real, arbf(z2.real))
        chk(tab, 'y_%d' % n, ys, 0, z1.imag, arbf(z2.imag))
# ---- 9.9.1 / 9.9.2 real Airy zeros
for r in T['Table 9.9.1']['rows'][1:]:
    k = int(r[0])
    a1 = mpmath.airyaizero(k); a2 = arb.airy_ai_zero(k)
    chk('Table 9.9.1', 'a_%d' % k, r[1], 0, a1, arbf(a2))
    chk('Table 9.9.1', "Ai'(a_%d)" % k, r[2], 0, mpmath.airyai(a1, derivative=1), arbf(a2.airy_ai(derivative=1)))
    b1 = mpmath.airyaizero(k, 1); b2 = arb.airy_ai_zero(k, derivative=1)
    chk('Table 9.9.1', "a'_%d" % k, r[3], 0, b1, arbf(b2))
    chk('Table 9.9.1', "Ai(a'_%d)" % k, r[4], 0, mpmath.airyai(b1), arbf(b2.airy_ai()))
for r in T['Table 9.9.2']['rows'][1:]:
    k = int(r[0])
    a1 = mpmath.airybizero(k); a2 = arb.airy_bi_zero(k)
    chk('Table 9.9.2', 'b_%d' % k, r[1], 0, a1, arbf(a2))
    chk('Table 9.9.2', "Bi'(b_%d)" % k, r[2], 0, mpmath.airybi(a1, derivative=1), arbf(a2.airy_bi(derivative=1)))
    b1 = mpmath.airybizero(k, 1); b2 = arb.airy_bi_zero(k, derivative=1)
    chk('Table 9.9.2', "b'_%d" % k, r[3], 0, b1, arbf(b2))
    chk('Table 9.9.2', "Bi(b'_%d)" % k, r[4], 0, mpmath.airybi(b1), arbf(b2.airy_bi()))
# ---- 9.9.3 / 9.9.4 complex zeros of Bi, Bi'
rot = mpmath.exp(-1j * mpmath.pi / 3)
for tab, der in (('Table 9.9.3', 0), ('Table 9.9.4', 1)):
    for r in T[tab]['rows'][2:]:
        k = int(r[0])
        z1 = mpmath.airybizero(k, der, complex=True)
        z0 = mpmath.mpf(cl(r[1])) * mpmath.exp(1j * (mpmath.mpf(cl(r[2])) + mpmath.pi / 3))
        def f(z): return z.airy()[2 + der]
        def df(z): return z.airy()[3] if der == 0 else z * z.airy()[2]
        z2 = newton_acb(f, df, complex(z0))
        z2m = mpmath.mpc(arbf(z2.real), arbf(z2.imag))
        z1c = z1 if abs(z1 - z2m) < 1e-20 else mpmath.conj(z1)
        w1 = z1c * rot; w2 = z2m * rot
        chk(tab, 'modulus %d' % k, r[1], 0, abs(w1), abs(w2)); chk(tab, 'phase %d' % k, r[2], 0, mpmath.arg(w1), mpmath.arg(w2))
        v1 = mpmath.airybi(z1c, derivative=1 - der); a = z2.airy(); v2a = a[3 - der]; v2 = mpmath.mpc(arbf(v2a.real), arbf(v2a.imag))
        chk(tab, 'value modulus %d' % k, r[3], 0, abs(v1), abs(v2)); chk(tab, 'value phase %d' % k, r[4], 0, mpmath.arg(v1), mpmath.arg(v2))
# ---- 24.2.3 Bernoulli, 24.2.4 Euler
def bern_own(N):
    B = [Fraction(0)] * (N + 1); B[0] = Fraction(1)
    for m in range(1, N + 1):
        B[m] = -sum(Fraction(math.comb(m + 1, k)) * B[k] for k in range(m)) / (m + 1)
    return B
B = bern_own(60)
for r in T['Table 24.2.3']['rows'][1:]:
    n = int(r[0]); b2 = sympy.bernoulli(n) if n != 1 else sympy.Rational(-1, 2)
    chki('Table 24.2.3', 'N_%d' % n, r[1], B[n].numerator, int(b2.p)); chki('Table 24.2.3', 'D_%d' % n, r[2], B[n].denominator, int(b2.q))
    e = 0; m = re.search(r'10\^\{(-?\d+)\}', r[4] if len(r) > 4 else '')
    if m: e = int(m.group(1))
    chk('Table 24.2.3', 'B_%d decimal' % n, r[3], e, mpmath.mpf(B[n].numerator) / B[n].denominator, mpmath.bernoulli(n) if n != 1 else mpmath.mpf(-0.5))
def euler_own(N):
    E = {0: 1}
    for n in range(1, N // 2 + 1): E[2 * n] = -sum(math.comb(2 * n, 2 * k) * E[2 * k] for k in range(n))
    return E
E = euler_own(60)
for r in T['Table 24.2.4']['rows'][1:]:
    n = int(r[0]); chki('Table 24.2.4', 'E_%d' % n, r[1], E[n], int(sympy.euler(n)))
def frac(c):
    c = cl(c).replace('\\tfrac', '').replace('\\frac', '')
    m = re.fullmatch(r'(-?)\{(\d+)\}\{(\d+)\}', c)
    if m: return Fraction(int(m.group(1) + m.group(2)), int(m.group(3)))
    return Fraction(int(c))
x = sympy.symbols('x')
for tab, fn in (('Table 24.2.5', 'B'), ('Table 24.2.6', 'E')):
    for r in T[tab]['rows'][2:]:
        n = int(r[0])
        p = sympy.Poly(sympy.bernoulli(n, x) if fn == 'B' else sympy.euler(n, x), x)
        if fn == 'B':
            own = [Fraction(math.comb(n, k)) * (B[n - k] if (n - k) != 1 else Fraction(-1, 2)) for k in range(n + 1)]
        else:
            poly = sympy.Poly(sympy.expand(sum(sympy.binomial(n, k) * sympy.Rational(E.get(k, 0), 2 ** k) * (x - sympy.Rational(1, 2)) ** (n - k) for k in range(n + 1))), x)
            own = [Fraction(int(poly.coeff_monomial(x ** k).p), int(poly.coeff_monomial(x ** k).q)) for k in range(n + 1)]
        for k in range(n + 1):
            c = r[1 + k]
            if c == '': continue
            pr = frac(c); s2 = p.coeff_monomial(x ** k); s2 = Fraction(int(s2.p), int(s2.q))
            st = 'ok' if pr == own[k] == s2 else 'BAD'
            res.append((tab, '%s_%d,%d' % (fn, n, k), str(pr), st))
            if st != 'ok': print('  NOTE', tab, n, k, pr, own[k], s2)
# ---- combinatorial integer tables
from sympy import binomial, catalan, bell, totient, divisor_count, divisor_sigma, prime
from sympy.functions.combinatorial.numbers import stirling
def multi(tab, colsper, f1, f2):
    for r in T[tab]['rows'][1:]:
        for i in range(0, len(r), colsper):
            if r[i] == '' or r[i + 1] == '': continue
            n = int(cl(r[i])); chki(tab, 'n=%d' % n, r[i + 1], f1(n), f2(n))
def part_own(N):
    p = [1] + [0] * N
    for k in range(1, N + 1):
        for n in range(k, N + 1): p[n] += p[n - k]
    return p
P = part_own(60)
multi('Table 26.2.1', 2, lambda n: P[n], lambda n: int(sympy.functions.combinatorial.numbers.partition(n)))
multi('Table 26.5.1', 2, lambda n: int(catalan(n)), lambda n: math.comb(2 * n, n) // (n + 1))
def bell_own(N):
    row = [1]; out = [1]
    for n in range(1, N + 1):
        new = [row[-1]]
        for v in row: new.append(new[-1] + v)
        row = new; out.append(row[0])
    return out
BL = bell_own(30)
multi('Table 26.7.1', 2, lambda n: BL[n], lambda n: int(bell(n)))
MZ = [1, 1]
for n in range(2, 31): MZ.append(((2 * n + 1) * MZ[n - 1] + (3 * n - 3) * MZ[n - 2]) // (n + 2))
multi('Table 26.6.2', 2, lambda n: MZ[n], lambda n: sum(math.comb(n, 2 * k) * int(catalan(k)) for k in range(n // 2 + 1)))
def dela(m, n): return sum(math.comb(m, k) * math.comb(n, k) * 2 ** k for k in range(min(m, n) + 1))
DL = {}
def dela2(m, n):
    if m == 0 or n == 0: return 1
    if (m, n) not in DL: DL[(m, n)] = dela2(m - 1, n) + dela2(m, n - 1) + dela2(m - 1, n - 1)
    return DL[(m, n)]
SC = [1, 2]
for n in range(2, 30): SC.append((3 * (2 * n - 1) * SC[n - 1] - (n - 2) * SC[n - 2]) // (n + 1))
multi('Table 26.6.4', 2, lambda n: SC[n], lambda n: dela(n, n) - (dela(n + 1, n - 1) if n > 0 else 0))
def pp_own(N):
    a = [1] + [0] * N
    for k in range(1, N + 1):
        for rep in range(k):
            for n in range(k, N + 1): a[n] += a[n - k]
    return a
PP = pp_own(50)
PP2 = [1]
for n in range(1, 51): PP2.append(sum(int(divisor_sigma(k, 2)) * PP2[n - k] for k in range(1, n + 1)) // n)
multi('Table 26.12.1', 2, lambda n: PP[n], lambda n: PP2[n])
def tri(tab, f1, f2, hdr=2):
    ks = [int(c) for c in T[tab]['rows'][1]]
    for r in T[tab]['rows'][hdr:]:
        n = int(r[0])
        for j, c in enumerate(r[1:]):
            if c == '': continue
            chki(tab, '(%d,%d)' % (n, ks[j]), c, f1(n, ks[j]), f2(n, ks[j]))
tri('Table 26.3.1', lambda m, n: math.comb(m, n), lambda m, n: int(binomial(m, n)))
tri('Table 26.3.2', lambda m, n: math.comb(m + n, m), lambda m, n: int(binomial(m + n, n)))
tri('Table 26.6.1', dela, dela2)
def nara(n, k):
    if n == 0: return 1 if k == 0 else 0
    return math.comb(n, k) * math.comb(n, k - 1) // n if k >= 1 else 0
from functools import lru_cache
@lru_cache(None)
def dyck(steps, h, last, peaks):
    # number of ways to finish a Dyck path with `steps` steps left at height h, needing `peaks` more peaks
    if peaks < 0: return 0
    if steps == 0: return 1 if (h == 0 and peaks == 0) else 0
    t = 0
    if h + 1 <= steps - 1: t += dyck(steps - 1, h + 1, 1, peaks)
    if h > 0: t += dyck(steps - 1, h - 1, 0, peaks - (1 if last == 1 else 0))
    return t
tri('Table 26.6.3', nara, lambda n, k: dyck(2 * n, 0, 0, k))
S1 = {}; S2 = {}
def s1(n, k):
    if n == 0: return 1 if k == 0 else 0
    if k == 0 or k > n: return 0
    if (n, k) not in S1: S1[(n, k)] = s1(n - 1, k - 1) - (n - 1) * s1(n - 1, k)
    return S1[(n, k)]
def s2(n, k):
    if n == 0: return 1 if k == 0 else 0
    if k == 0 or k > n: return 0
    if (n, k) not in S2: S2[(n, k)] = s2(n - 1, k - 1) + k * s2(n - 1, k)
    return S2[(n, k)]
tri('Table 26.8.1', s1, lambda n, k: int(stirling(n, k, kind=1, signed=True)))
tri('Table 26.8.2', s2, lambda n, k: int(stirling(n, k, kind=2)))
def pk(n, k):
    a = [1] + [0] * n
    for j in range(1, k + 1):
        for m in range(j, n + 1): a[m] += a[m - j]
    return a[n]
def pk2(n, k):
    from sympy.utilities.iterables import partitions
    if n == 0: return 1
    return sum(1 for p in partitions(n, m=k)) if k > 0 else 0
tri('Table 26.9.1', pk, pk2)
def eul(n, k):
    if n == 0: return 1 if k == 0 else 0
    return sum((-1) ** j * math.comb(n + 1, j) * (k + 1 - j) ** n for j in range(k + 2))
def eul2(n, k):
    if n == 0: return 1 if k == 0 else 0
    if n <= 8:
        return sum(1 for p in itertools.permutations(range(n)) if sum(1 for i in range(n - 1) if p[i] > p[i + 1]) == k)
    A = [[0] * (n + 1) for _ in range(n + 1)]; A[0][0] = 1
    for m in range(1, n + 1):
        for j in range(m):
            A[m][j] = (j + 1) * A[m - 1][j] + (m - j) * (A[m - 1][j - 1] if j > 0 else 0)
    return A[n][k]
tri('Table 26.14.1', eul, eul2)
own = [p for p in range(2, 600) if all(p % q for q in range(2, int(p ** 0.5) + 1))]
for r in T['Table 27.2.1']['rows'][1:]:
    n = int(r[0])
    for j, c in enumerate(r[1:]): chki('Table 27.2.1', 'p_%d' % (n + 10 * j), c, own[n + 10 * j - 1], int(prime(n + 10 * j)))
for r in T['Table 27.2.2']['rows'][1:]:
    for i in range(0, len(r), 4):
        if r[i] == '': continue
        n = int(r[i]); ds = [d for d in range(1, n + 1) if n % d == 0]
        chki('Table 27.2.2', 'phi(%d)' % n, r[i + 1], sum(1 for k in range(1, n + 1) if math.gcd(k, n) == 1), int(totient(n)))
        chki('Table 27.2.2', 'd(%d)' % n, r[i + 2], len(ds), int(divisor_count(n)))
        chki('Table 27.2.2', 'sigma(%d)' % n, r[i + 3], sum(ds), int(divisor_sigma(n)))
def gf(parts_ok, N):
    a = [1] + [0] * N
    for k in range(1, N + 1):
        if parts_ok(k):
            for n in range(k, N + 1): a[n] += a[n - k]
    return a
def brute(cond, N):
    from sympy.utilities.iterables import partitions
    out = [1]
    for n in range(1, N + 1):
        c = 0
        for p in partitions(n):
            if all(v == 1 for v in p.values()) and cond(sorted(p)): c += 1
        out.append(c)
    return out
N = 20
cols = [(gf(lambda k: k % 2 == 1, N), brute(lambda ks: True, N)),
        (gf(lambda k: k % 5 in (1, 4), N), brute(lambda ks: all(b - a >= 2 for a, b in zip(ks, ks[1:])), N)),
        (gf(lambda k: k % 5 in (2, 3), N), brute(lambda ks: all(b - a >= 2 for a, b in zip(ks, ks[1:])) and (not ks or ks[0] >= 2), N)),
        (gf(lambda k: k % 6 in (1, 5), N), brute(lambda ks: all(b - a >= 3 and (b - a >= 6 or a % 3 or b % 3) for a, b in zip(ks, ks[1:])), N))]
for r in T['Table 26.10.1']['rows'][3:]:
    n = int(r[0])
    for j in range(4): chki('Table 26.10.1', 'col%d n=%d' % (j + 1, n), r[1 + j], cols[j][0][n], cols[j][1][n])
from collections import Counter, defaultdict
by = defaultdict(Counter)
for t, w, p, s in res: by[t][s] += 1
tot = 0
for t in by: print(t, dict(by[t])); tot += sum(by[t].values())
print('total values', tot)


gauss_total = len(results); gauss_bad = [r for r in results if r[3] != 'ok-round']
other_bad = [r for r in res if r[3] not in ('ok', 'ok-round')]
print()
print('SUMMARY: tables', len(set(r[0] for r in results)) + len(by), 'values', gauss_total + tot,
      '| not correctly rounded:', len(gauss_bad) + len(other_bad))
for r in gauss_bad: print('  ', r)
for r in other_bad: print('  ', r)
