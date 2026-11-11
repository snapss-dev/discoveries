"""Graded Keller maps of C^3 of type (1,-r,-s), r, s >= 1, with all components of degree <= 6:
the component of weight 1 is c*x (p is constant), so the map is injective.

Usage:  python check.py          (a few minutes; needs sympy and python-flint)

Notation: F = (a*p(u,v), M(u,v)/a^r, N(u,v)/a^s), u = a^r y, v = a^s z; here a is the variable of weight 1.
Two routes, which share the supports (function monos), the list of normalised branches and the
normal forms, and differ in how the equations are derived and in the Groebner engine:
  A. equations from the reduced condition  p{M,N} + r M{p,N} - s N{p,M} = kappa;  python-flint (FLINT's
     Buchberger routine) with splitting on factors;
  B. equations from the 3x3 Jacobian determinant in (a,y,z);  sympy's own Buchberger routine, for every
     branch (with a split on top coefficients for types (1,-1,-1) and (1,-1,-2)).
Control: with component degrees <= (4,6,7) the same machinery finds exactly the Alpoge map.
"""
import sys, time, itertools
from fractions import Fraction
import sympy as sp
import flint

ONLY = [a for a in sys.argv[1:] if a.startswith('--only=')]
D = 6

# ---------------------------------------------------------------- 0. the known counterexample
x, y, z = sp.symbols('x y z')
F = [(1 + x*y)**3*z + y**2*(1 + x*y)*(4 + 3*x*y),
     y + 3*x*(1 + x*y)**2*z + 3*x*y**2*(4 + 3*x*y),
     2*x - 3*x**2*y - x**3*z]
det = sp.expand(sp.Matrix(F).jacobian([x, y, z]).det())
pts = [(0, 0, sp.Rational(-1, 4)), (1, sp.Rational(-3, 2), sp.Rational(13, 2)), (-1, sp.Rational(3, 2), sp.Rational(13, 2))]
vals = [tuple(f.subs(dict(zip((x, y, z), p))) for f in F) for p in pts]
degs = [sp.Poly(f, x, y, z).total_degree() for f in F]
t = sp.Symbol('t')
graded = [sp.expand(f.subs({x: t*x, y: y/t, z: z/t**2}, simultaneous=True) - t**w*f) == 0 for f, w in zip(F, (-2, -1, 1))]
print('0. Alpoge map: det =', det, '| degrees', degs, '| three points with image', set(vals),
      '| homogeneous of weights (-2,-1,1) for wt(x,y,z)=(1,-1,-2):', all(graded))
assert det == -2 and len(set(vals)) == 1 and degs == [7, 6, 4] and all(graded)


# ---------------------------------------------------------------- supports
def monos(r, s, D):
    """exponents (j,k) of u^j v^k allowed in p, M, N when the components a*p, M/a^r, N/a^s of F have
    degrees <= D (one bound), or <= D[0], D[1], D[2] (one bound per component)"""
    D1, D2, D3 = (D, D, D) if isinstance(D, int) else D
    mp, mM, mN = [], [], []
    for j in range(max(D1, D2, D3) + 2):
        for k in range(max(D1, D2, D3) + 2):
            w = (r + 1)*j + (s + 1)*k           # degree of u^j v^k in (a,y,z)
            if 1 + w <= D1: mp.append((j, k))
            if w - r <= D2 and r*j + s*k >= r: mM.append((j, k))
            if w - s <= D3 and r*j + s*k >= s: mN.append((j, k))
    return mp, mM, mN


# ---------------------------------------------------------------- 1. the reduction identity, checked symbolically
def reduction_identity(r, s):
    a, yy, zz, u, v = sp.symbols('a y z u v')
    mp, mM, mN = monos(r, s, D)
    cp = sp.symbols('P0:%d' % len(mp)); cM = sp.symbols('M0:%d' % len(mM)); cN = sp.symbols('N0:%d' % len(mN))
    p = sum(c*u**j*v**k for c, (j, k) in zip(cp, mp))
    M = sum(c*u**j*v**k for c, (j, k) in zip(cM, mM))
    N = sum(c*u**j*v**k for c, (j, k) in zip(cN, mN))
    br = lambda f, g: sp.diff(f, u)*sp.diff(g, v) - sp.diff(f, v)*sp.diff(g, u)
    E = sp.expand(p*br(M, N) + r*M*br(p, N) - s*N*br(p, M))
    sub = {u: a**r*yy, v: a**s*zz}
    G = [sp.expand(a*p.subs(sub)), sp.expand(M.subs(sub)/a**r), sp.expand(N.subs(sub)/a**s)]
    assert all(sp.Poly(g, a, yy, zz).total_degree() <= D for g in G)
    d3 = sp.expand(sp.Matrix(G).jacobian([a, yy, zz]).det())
    return sp.expand(d3 - E.subs(sub)) == 0


if not ONLY:
    ids = {rs: reduction_identity(*rs) for rs in [(1, 1), (1, 2), (1, 3), (2, 3), (3, 3)]}
    print('1. det JF = p{M,N} + r M{p,N} - s N{p,M} (with unknown coefficients):', ids)
    assert all(ids.values())


# ---------------------------------------------------------------- 2. route A: python-flint
SPARE = ['t0', 't1', 't2', 't3', 't4']      # Rabinowitsch variables (t*x = 1 encodes x != 0)


def system(r, s, D, last=None):
    mp, mM, mN = monos(r, s, D)
    names = [f'p{j}_{k}' for j, k in mp] + [f'm{j}_{k}' for j, k in mM] + [f'n{j}_{k}' for j, k in mN]
    allnames = names + SPARE
    if last:                                   # make `last` the smallest variable of the term order
        allnames = [n for n in allnames if n != last] + [last]
    ctx = flint.fmpz_mpoly_ctx.get(allnames, 'degrevlex')
    g = dict(zip(allnames, ctx.gens()))
    eq = {}
    for (pj, pk) in mp:
        for (mj, mk) in mM:
            for (nj, nk) in mN:
                c = (mj*nk - mk*nj) + r*(pj*nk - pk*nj) - s*(pj*mk - pk*mj)
                if c:
                    key = (pj + mj + nj - 1, pk + mk + nk - 1)
                    eq[key] = eq.get(key, 0) + c*g[f'p{pj}_{pk}']*g[f'm{mj}_{mk}']*g[f'n{nj}_{nk}']
    kappa = eq.pop((0, 0), 0)
    return (mp, mM, mN), ctx, g, [e for e in eq.values() if e != 0], kappa


stats = {'leaves': 0, 'splits': 0}


def has_unit(polys):
    return any(q.total_degree() == 0 and q != 0 for q in polys)


def empty(polys, ctx, limits=(300, 3000, 20000), found=None, plain=False):
    """True iff the system has no solution over an algebraic closure of Q.
    Soundness: every polynomial flint derives lies in the ideal I of `polys`; a nonzero constant among
    them proves emptiness; if g = c*f1^e1...fk^ek is in I then V(I) is the union of the V(I+(fi)).
    A basis returned after the limits are hit is used only as a set of elements of I, never as a
    generating set."""
    polys = [q for q in polys if q != 0]
    if has_unit(polys):
        stats['leaves'] += 1; return True
    if plain:                                         # one unrestricted Buchberger run
        stats['leaves'] += 1
        return has_unit(flint.fmpz_mpoly_vec(polys, ctx).buchberger_naive())
    G, ok = flint.fmpz_mpoly_vec(polys, ctx).buchberger_naive(limits=(len(polys) + limits[0], limits[1], limits[2]))
    Gl = [q for q in G if q != 0]
    if has_unit(Gl):
        stats['leaves'] += 1; return True
    best = None
    if not ok and limits[0] <= 3000:
        have = set(str(q) for q in polys)
        for q in sorted(Gl + polys, key=lambda w: len(w)):
            if len(q) > 120: break
            c, fac = q.factor()
            if len(fac) >= 2 or (len(fac) == 1 and fac[0][1] > 1):
                fs = [f for f, e in fac]
                if any(str(f) in have or str(-f) in have for f in fs): continue
                score = (len(fs), sum(len(f) for f in fs))
                if best is None or score < best[0]:
                    best = (score, fs)
                    if score[1] <= 3: break
        if best is None:
            return empty(polys, ctx, (limits[0]*3, limits[1]*3, limits[2]*3), found)
    if best is None:                                  # finished, or no split left: unrestricted run decides
        G2 = [q for q in flint.fmpz_mpoly_vec(polys, ctx).buchberger_naive().autoreduction() if q != 0]
        stats['leaves'] += 1
        if has_unit(G2): return True
        if found is not None: found.append(G2)
        return False
    stats['splits'] += 1
    res = True
    for f in best[1]:
        res = empty(polys + [f], ctx, limits, found) and res
    return res


def branches(r, s, D):
    """normalised branches that together cover 'p is not constant' (torus scalings; GL2 when r = s)"""
    (mp, mM, mN), ctx, g, eqs, kappa = system(r, s, D)
    nonconst = [jk for jk in mp if jk != (0, 0)]
    if r < s:
        # kappa = p00*m10*n01 != 0; scale p, M, N so that p00 = m10 = n01 = 1. Order the nonconstant
        # monomials of p by decreasing degree; branch i: the first i-1 coefficients vanish and the i-th
        # is nonzero, scaled to 1 by u -> c*u or v -> c*v. The branches cover "p is not constant".
        assert str(kappa) == 'p0_0*m1_0*n0_1'
        base = eqs + [g['p0_0'] - 1, g['m1_0'] - 1, g['n0_1'] - 1]
        order = sorted(nonconst, key=lambda jk: -((r + 1)*jk[0] + (s + 1)*jk[1]))
        out = []
        for i, (j, k) in enumerate(order):
            zero = [g[f'p{a}_{b}'] for a, b in order[:i]]
            out.append((f'p{j}_{k}=1' + ''.join(f',p{a}_{b}=0' for a, b in order[:i]), base + zero + [g[f'p{j}_{k}'] - 1]))
    else:
        # r = s: GL2 on (M,N) makes their linear parts (u,v); the remaining simultaneous GL2 puts the
        # quadratic part of p in one of the forms u*v, u^2, 0, and in the last case the linear part is u
        base = eqs + [g['p0_0'] - 1, g['m1_0'] - 1, g['m0_1'], g['n1_0'], g['n0_1'] - 1]
        if (2, 0) in mp:
            out = [('quadratic part of p is u*v', base + [g['p2_0'], g['p1_1'] - 1, g['p0_2']]),
                   ('quadratic part of p is u^2', base + [g['p2_0'] - 1, g['p1_1'], g['p0_2']]),
                   ('p = 1 + u', base + [g['p2_0'], g['p1_1'], g['p0_2'], g['p1_0'] - 1, g['p0_1']])]
        else:
            out = [('p = 1 + u', base + [g['p1_0'] - 1, g['p0_1']])]
    if (r, s) == (1, 2) and D == 6:
        # the branch p = 1 + p10*u + v: the scaling of u is still free, so p10 = 0 or p10 = 1; in the
        # chart p = 1 + u + v, split further on five top coefficients (x = 0, or x != 0 via t*x = 1)
        name0, polys0 = out[2]
        assert name0 == 'p0_1=1,p1_1=0,p2_0=0'
        sub = [(name0 + ',p1_0=0', polys0 + [g['p1_0']])]
        top = ['n4_0', 'n1_2', 'm2_1', 'm3_0', 'n2_1']
        for pattern in itertools.product([0, 1], repeat=5):
            extra = [g['p1_0'] - 1]
            for i, (nm, bit) in enumerate(zip(top, pattern)):
                extra.append(g[nm] if bit == 0 else g[f't{i}']*g[nm] - 1)
            sub.append((name0 + ',p1_0=1,' + ''.join(str(b) for b in pattern), polys0 + extra))
        out = out[:2] + sub + out[3:]
    return (mp, mM, mN), ctx, out


PLAIN = {(2, 3)}     # types where one unrestricted Buchberger run is quicker than splitting
print('2. route A (python-flint), all types (1,-r,-s) with 1 <= r <= s, degree <=', D)
todo, summary = [], {'p constant by degree': 0, 'one-variable lemma': 0, 'Groebner': 0}
for r in range(1, 9):
    for s in range(r, r + 40):
        mp, mM, mN = monos(r, s, D)
        if len(mp) == 1:
            summary['p constant by degree'] += 1
        elif all(k == 0 for j, k in mp) and all(k == 0 for j, k in mM):
            summary['one-variable lemma'] += 1          # p, M in C[u]: (p^r M)' = c p^(r-1) has no solution
        else:
            summary['Groebner'] += 1; todo.append((r, s))
# outside the scanned range nothing new happens: u enters p only if r <= 4; v enters M only if s <= r + 5
assert all(s <= r + 5 and r <= 4 for r, s in todo)
print('   types scanned (r <= 8, s < r + 40):', summary, '| Groebner types:', todo)
allok = True
sub32 = []
for (r, s) in todo:
    (mp, mM, mN), ctx, brs = branches(r, s, D)
    for name, polys in brs:
        tag = f'--only={r},{s},{name}'
        if ONLY and tag not in ONLY: continue
        t0 = time.time(); stats['leaves'] = stats['splits'] = 0; found = []
        e = empty(polys, ctx, found=found, plain=(r, s) in PLAIN)
        allok = allok and e
        if name.count(',') >= 4 and name[-5:].isdigit() and e:
            sub32.append(time.time() - t0)
            if len(sub32) == 32: print(f'   (1,-1,-2) branch [p = 1 + u + v, 32 sub-branches on the top coefficients {"n4_0, n1_2, m2_1, m3_0, n2_1"}]: all EMPTY  ({sum(sub32):.1f}s)', flush=True)
            continue
        print(f'   (1,-{r},-{s}) branch [{name}]: {"EMPTY" if e else "NONEMPTY " + str([[str(q) for q in w] for w in found[:1]])}  '
              f'({len(ctx.gens()) - len(SPARE)} unknowns, {stats["splits"]} splits, {stats["leaves"]} leaves, {time.time()-t0:.1f}s)', flush=True)
print('   route A: every branch run is empty:', allok)
assert allok
if ONLY:
    sys.exit(0)

# ---------------------------------------------------------------- control: component degrees <= (4,6,7)
# Type (1,-1,-2) with deg(a*p) <= 4, deg(M/a) <= 6, deg(N/a^2) <= 7, the degree vector of the Alpoge map.
# Then p = 1 + p10*u + p01*v, and after scaling u, v the non-constant cases are 1+u+v, 1+u, 1+v.
# Each is split on five top coefficients (c = 0, or c != 0 via t*c = 1), as at degree 6.
print('   control, type (1,-1,-2) with component degrees <= (4,6,7):')
CAPS = (4, 6, 7)
(mp, mM, mN), ctx, g, eqs, kappa = system(1, 2, CAPS, last='n3_1')
assert mp == [(0, 0), (0, 1), (1, 0)]
top = ['n3_1', 'm2_1', 'm3_0', 'n4_0', 'n1_2']
base = eqs + [g['p0_0'] - 1, g['m1_0'] - 1, g['n0_1'] - 1]
hits = {}
for name, (c10, c01) in (('p = 1 + u + v', (1, 1)), ('p = 1 + u', (1, 0)), ('p = 1 + v', (0, 1))):
    hits[name] = []
    for pattern in itertools.product([0, 1], repeat=5):
        extra = [g['p1_0'] - c10, g['p0_1'] - c01]
        for i, (nm, bit) in enumerate(zip(top, pattern)):
            extra += [g[nm], g[f't{i}']] if bit == 0 else [g[f't{i}']*g[nm] - 1]
        found = []
        if not empty(base + extra, ctx, found=found):
            hits[name].append((pattern, found))
    print(f'      {name}: non-empty sub-branches: {[h[0] for h in hits[name]]}')
assert hits['p = 1 + u'] == [] and hits['p = 1 + v'] == []
assert len(hits['p = 1 + u + v']) == 1 and hits['p = 1 + u + v'][0][0] == (1, 1, 1, 1, 0) and len(hits['p = 1 + u + v'][0][1]) == 1
W = hits['p = 1 + u + v'][0][1][0]                 # reduced Groebner basis of the one non-empty piece
leads = [sum(q.monoms()[0]) for q in W]
square = [q for q in W if sum(q.monoms()[0]) == 2]
c = g['n3_1']
print('      its reduced Groebner basis:', [str(q) for q in W])
# one generator per variable, all with a leading term of degree 1 except (27c+8)^2: a single double point
assert len(W) == len(ctx.gens()) and sorted(leads) == [1]*(len(W) - 1) + [2]
assert square[0] == (27*c + 8)**2 or square[0] == -(27*c + 8)**2
# the Alpoge map in the same normal form: p -> p/2, u -> -2u/3, v -> -2v, then M and N rescaled
u, v = sp.symbols('u v')
Mp = v*(1 + u)**2 + u**2*(4 + 3*u)
lam, mu = sp.Rational(-2, 3), -2
alp = {'p': sp.Poly(sp.expand(((2 - 3*u - v)/2).subs({u: lam*u, v: mu*v}, simultaneous=True)), u, v),
       'm': sp.Poly(sp.expand((u + 3*Mp).subs({u: lam*u, v: mu*v}, simultaneous=True)/lam), u, v),
       'n': sp.Poly(sp.expand(((1 + u)*Mp).subs({u: lam*u, v: mu*v}, simultaneous=True)/mu), u, v)}
for nm, lst in (('p', mp), ('m', mM), ('n', mN)):
    assert all((j, k) in lst for (j, k), cf in alp[nm].terms())          # it lies in the (4,6,7) supports
names = list(g.keys())
vals = {}
for nm in names:
    if nm in SPARE: continue
    j, k = map(int, nm[1:].split('_'))
    cf = alp[nm[0]].coeff_monomial(u**j*v**k)
    vals[nm] = Fraction(int(cf.p), int(cf.q))
for i, nm in enumerate(top):
    vals[f't{i}'] = 1/vals[nm] if vals[nm] != 0 else Fraction(0)


def ev(q):
    tot = Fraction(0)
    for mon, cf in q.to_dict().items():
        term = Fraction(int(cf))
        for n, e in zip(names, mon):
            if int(e): term *= vals[n]**int(e)
        tot += term
    return tot


assert all(ev(q) == 0 for q in eqs) and vals['n3_1'] == Fraction(-8, 27)
assert all(ev(q) == 0 for q in W if q not in square) and ev(square[0]) == 0
print('      the Alpoge map, normalised, satisfies the equations and every basis element; its n3_1 =', vals['n3_1'],
      '| so the solution set is this one point, with multiplicity 2: (27*n3_1 + 8)^2 = 0')
print('      the same branch p = 1 + u + v with all degrees <= 6: EMPTY (the 32 sub-branches above):', len(sub32) == 32)
assert len(sub32) == 32


# ---------------------------------------------------------------- overlap with Kistner-Shaska, Theorem 8.5
# Their box: deg N <= 4, deg M <= 3, deg p <= 1 in (u,v). The degree-6 supports with deg p <= 1 lie inside it,
# and no member of the orbit (u,v) -> (a*u + b*v, c*v), a*c != 0, of the Alpoge triple has degree <= 6.
mp6, mM6, mN6 = monos(1, 2, 6)
assert all(j + k <= 3 for j, k in mM6) and all(j + k <= 4 for j, k in mN6)
aa, bb, cc, tt = sp.symbols('a b c t')
orbit = {'m': sp.Poly(sp.expand((u + 3*Mp).subs({u: aa*u + bb*v, v: cc*v}, simultaneous=True)), u, v),
         'n': sp.Poly(sp.expand(((1 + u)*Mp).subs({u: aa*u + bb*v, v: cc*v}, simultaneous=True)), u, v)}
high = [cf for (j, k), cf in orbit['m'].terms() if 2*j + 3*k - 1 > 6] + [cf for (j, k), cf in orbit['n'].terms() if 2*j + 3*k - 2 > 6]
gb = sp.groebner(high + [tt*aa*cc - 1], tt, aa, bb, cc, order='grevlex', domain=sp.QQ)
print('   overlap: degree-6 supports with deg p <= 1 lie in the Kistner-Shaska box (4,3,1): True;',
      'no member of the orbit of the Alpoge triple has degree <= 6:', list(gb.exprs) == [1])
assert list(gb.exprs) == [1]


# ---------------------------------------------------------------- 3. route B: sympy, from the 3x3 determinant
def route_b(r, s):
    """sympy only: equations from the 3x3 determinant in (a,y,z); same supports and normalised branches as route A"""
    a, yy, zz = sp.symbols('a y z')
    mp, mM, mN = monos(r, s, D)
    cp = [sp.Symbol(f'p{j}_{k}') for j, k in mp]; cM = [sp.Symbol(f'm{j}_{k}') for j, k in mM]; cN = [sp.Symbol(f'n{j}_{k}') for j, k in mN]
    F1 = sum(c*a**(1 + r*j + s*k)*yy**j*zz**k for c, (j, k) in zip(cp, mp))
    F2 = sum(c*a**(r*j + s*k - r)*yy**j*zz**k for c, (j, k) in zip(cM, mM))
    F3 = sum(c*a**(r*j + s*k - s)*yy**j*zz**k for c, (j, k) in zip(cN, mN))
    P = sp.Poly(sp.expand(sp.Matrix([F1, F2, F3]).jacobian([a, yy, zz]).det()), a, yy, zz)
    eqs = [c for mon, c in P.terms() if mon != (0, 0, 0)]
    S = {str(c): c for c in cp + cM + cN}
    subs = []
    if r < s:
        order = sorted([jk for jk in mp if jk != (0, 0)], key=lambda jk: -((r + 1)*jk[0] + (s + 1)*jk[1]))
        for i, (j, k) in enumerate(order):
            sub = {S['p0_0']: 1, S['m1_0']: 1, S['n0_1']: 1, S[f'p{j}_{k}']: 1}
            sub.update({S[f'p{a_}_{b_}']: 0 for a_, b_ in order[:i]})
            subs.append(sub)
    else:
        base = {S['p0_0']: 1, S['m1_0']: 1, S['m0_1']: 0, S['n1_0']: 0, S['n0_1']: 1}
        if (2, 0) in mp:
            subs.append({**base, S['p2_0']: 0, S['p1_1']: 1, S['p0_2']: 0})
            subs.append({**base, S['p2_0']: 1, S['p1_1']: 0, S['p0_2']: 0})
            subs.append({**base, S['p2_0']: 0, S['p1_1']: 0, S['p0_2']: 0, S['p1_0']: 1, S['p0_1']: 0})
        else:
            subs.append({**base, S['p1_0']: 1, S['p0_1']: 0})
    if (r, s) == (1, 2):          # the branch p = 1 + p10*u + v: p10 = 0, or p10 = 1 after scaling u
        subs = subs[:2] + [{**subs[2], S['p1_0']: 0}, {**subs[2], S['p1_0']: 1}] + subs[3:]
    top = TOP_B.get((r, s), {})
    ts = sp.symbols('t0:5')
    out = []
    for i, sub in enumerate(subs):
        names = top.get(i, top.get('all', []))
        ok = True
        # split on the listed top coefficients: x = 0, or x != 0 encoded by t*x = 1
        for pattern in itertools.product([0, 1], repeat=len(names)):
            sub2 = dict(sub); extra = []; tg = []
            for q, (nm, bit) in enumerate(zip(names, pattern)):
                if bit == 0: sub2[S[nm]] = 0
                else: extra.append(ts[q]*S[nm] - 1); tg.append(ts[q])
            E = [e for e in (sp.expand(q.subs(sub2)) for q in eqs) if e != 0] + extra
            gens = tg + [q for q in cp + cM + cN if q not in sub2]
            ok = ok and list(sp.groebner(E, *gens, order='grevlex', domain=sp.QQ).exprs) == [1]
        out.append(ok)
    return out


# pre-splits that make sympy's Groebner routine fast enough (branch index -> coefficients to split on)
TOP_B = {(1, 2): {'all': ['n4_0', 'n1_2', 'm2_1', 'm3_0', 'n2_1']},
         (1, 1): {1: ['m3_0', 'm0_3', 'n3_0', 'n0_3', 'm2_1'], 2: ['m3_0', 'm0_3', 'n3_0', 'n0_3', 'm2_1']}}
print('3. route B (sympy, 3x3 determinant), branch by branch:')
okb = True
for (r, s) in todo:
    t0 = time.time(); res = route_b(r, s); okb = okb and all(res)
    print(f'   (1,-{r},-{s}): branches empty: {res}  ({time.time()-t0:.1f}s)', flush=True)
assert okb
print('ALL CHECKS PASSED')
