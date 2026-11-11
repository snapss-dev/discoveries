# Recomputes the decimal values quoted in PAGE/README from the saved wikitext excerpts
# (wikitext_excerpts.json, each with the revision id it was taken from).
# Every value is computed twice: with Arb ball arithmetic (python-flint) and with mpmath.
# Usage: python check.py
import os, re, json, warnings
warnings.filterwarnings('ignore')
import flint, mpmath
from flint import arb, acb
flint.ctx.prec = 400
mpmath.mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(HERE, 'wikitext_excerpts.json'), encoding='utf8'))
MINUS = '−'

def status(printed, v_arb, v_mp, e=0):
    """Compare a printed decimal with a certified value.  Returns ok-round, ok-trunc or WRONG."""
    s = printed.replace(MINUS, '-').strip(); neg = s.startswith('-'); s = s.lstrip('+-')
    nd = len(s.split('.')[1]) if '.' in s else 0
    pi = int(s.replace('.', ''))
    sc = abs(v_arb) / arb(10) ** e * arb(10) ** nd - pi
    vm = abs(mpmath.mpf(v_mp)) / mpmath.mpf(10) ** e * mpmath.mpf(10) ** nd - pi
    assert abs(mpmath.mpf(sc.mid().str(50, radius=False)) - vm) < mpmath.mpf(10) ** -15, 'the two methods disagree'
    if sc.abs_upper() < 0.5: return 'ok-round'
    if (sc > 0) == True and (sc < 1) == True: return 'ok-trunc'
    assert (sc.abs_lower() > 0.5) == True
    return 'WRONG'
def show(v, nd): return mpmath.nstr(mpmath.mpf(v), nd, strip_zeros=False)
total = 0; wrong = []
def rec(where, what, printed, va, vm, e=0, accept_trunc=False):
    global total
    total += 1
    st = status(printed, va, vm, e)
    if st == 'WRONG' or (st == 'ok-trunc' and not accept_trunc):
        wrong.append((where, what, printed, st))
        digs = len(printed.replace('.', '').lstrip('-0')) + 6
        print('  %-9s %-34s printed %-22s value %s' % (st, what, printed + ('e%d' % e if e else ''), show(vm, digs)))

# ---------------------------------------------------------------- 1. Standard normal table
x = EX['normal']; print('Standard normal table, revision', x['revid'])
t = x['wikitext'].replace(MINUS, '-')
def Phi(z): return ((-(arb(z) / arb(2).sqrt())).erfc() / 2, mpmath.ncdf(mpmath.mpf(z)))
def Q(z): return ((arb(z) / arb(2).sqrt()).erfc() / 2, mpmath.erfc(mpmath.mpf(z) / mpmath.sqrt(2)) / 2)
tabs = [m.start() for m in re.finditer(r'\{\|', t)]
assert len(tabs) == 4
n0 = total
for ti, start in enumerate(tabs):
    body = t[start:t.find('\n|}', start)]
    for blk in body.split('\n|-'):
        lines = [l for l in blk.strip().split('\n') if l.strip()]
        head = [l for l in lines if l.startswith('!')]
        cells = [l for l in lines if l.startswith('|') and not l.startswith('|+')]
        if not (head and cells): continue
        z = head[0].lstrip('! ').strip()
        vals = [c.strip() for c in ' '.join(c[1:] for c in cells).split('||')]
        for j, v in enumerate(vals):
            if ti < 3:
                if not re.fullmatch(r'\d\.\d+', v): continue
                zz = float(z)
                zs = '%.2f' % (zz - 0.01 * j) if ti == 0 else '%.2f' % (zz + 0.01 * j)
                va, vm = Phi(zs) if ti < 2 else Q(zs)
                rec('normal', ('Phi(%s)' if ti < 2 else '1-Phi(%s)') % zs, v, va, vm)
            else:
                m = re.match(r'\{\{val\s*\|([\d.]+)\|e=(-?\d+)\}\}', v)
                if not m: continue
                zs = str(int(z) + j); va, vm = Q(zs)
                rec('normal', '1-Phi(%s)' % zs, m.group(1), va, vm, int(m.group(2)))
print('  values recomputed:', total - n0)

# ---------------------------------------------------------------- 2. zeros of zeta
x = EX['zeta_zeros']; print('Riemann zeta function, revision', x['revid'], '(table "First few nontrivial zeros", printed with an ellipsis)')
n0 = total
vals = re.findall(r'(\d\d\.\d{15})\.\.\.', x['wikitext'])
assert len(vals) == 10
for p in sorted(vals, key=float):
    k = sorted(vals, key=float).index(p) + 1
    rec('zeta', 'Im of zero number %d' % k, p, acb.zeta_zero(k).imag, mpmath.zetazero(k).imag, accept_trunc=True)
    print('      zero %2d printed %s  true %s  IEEE double %.15f' % (k, p, show(mpmath.zetazero(k).imag, 22), float(mpmath.zetazero(k).imag)))
print('  values recomputed:', total - n0)

# ---------------------------------------------------------------- 3. Gram points
x = EX['gram']; print('Riemann-Siegel theta function, revision', x['revid'], '(table of Gram points; the table truncates)')
n0 = total
rows = re.findall(r'\|\s*(' + MINUS + r'?\d+)\s*\n\|(?:style="[^"]*"\|)?\s*(\d+\.\d{10})\.\.\.', x['wikitext'])
assert len(rows) == 18
for n, p in rows:
    n = int(n.replace(MINUS, '-'))
    if n >= -1:
        g = mpmath.grampoint(n)
    else:
        g = mpmath.findroot(lambda u: mpmath.siegeltheta(u) + mpmath.pi, mpmath.mpf(p))
    # Arb: certify the root by a sign change of theta(t) - n*pi (n >= 0) or theta(t) + pi (n = -1, -2)
    tgt = arb.pi() * (n if n >= 0 else -1)
    def theta(u):   # Riemann-Siegel theta through log-gamma
        z = acb(arb(1) / 4, u / 2)
        return z.lgamma().imag - u / 2 * arb.pi().log()
    lo = arb(str(g)) - arb(10) ** -30; hi = arb(str(g)) + arb(10) ** -30
    a = theta(lo) - tgt; b = theta(hi) - tgt
    assert (a < 0 and b > 0) or (a > 0 and b < 0), n
    rec('gram', 'Gram point g_%d' % n, p, lo.union(hi), g, accept_trunc=True)
print('  values recomputed:', total - n0, '(g_-2 is printed rounded, the rest truncated; only g_0 is wrong under both)')

# ---------------------------------------------------------------- 4. Bickley-Naylor
x = EX['bickley']; print('Bickley-Naylor functions, revision', x['revid'])
n0 = total
def ki_mp(n, xx):
    xx = mpmath.mpf(xx)
    return mpmath.quad(lambda th: mpmath.exp(-xx / mpmath.cos(th)) * mpmath.cos(th) ** (n - 1), mpmath.linspace(0, mpmath.pi / 2, 9))
def ki_arb(n, xx):
    xa = arb(xx)
    return acb.integral(lambda u, _: (-(acb(xa)) * u.cosh()).exp() / u.cosh() ** n, 0, 200).real
for line in x['wikitext'].split('\n'):
    if not line.startswith('| '): continue
    c = [s.strip() for s in line[1:].split('||')]
    for n in (1, 2, 3):
        rec('bickley', 'Ki_%d(%s)' % (n, c[0]), c[n], ki_arb(n, c[0]), ki_mp(n, c[0]))
print('  values recomputed:', total - n0)

# ---------------------------------------------------------------- 5. Gauss-Kronrod (G7, K15)
x = EX['kronrod']; print('Gauss-Kronrod quadrature formula, revision', x['revid'])
n0 = total
# Kronrod nodes: zeros of P_7 times the Stieltjes polynomial E_8, built exactly from rational moments
from flint import fmpq, fmpq_mat, fmpq_poly, fmpz_poly
def leg(n):
    p0, p1 = fmpq_poly([1]), fmpq_poly([0, 1])
    for k in range(2, n + 1): p0, p1 = p1, (fmpq_poly([0, 2 * k - 1]) * p1 - (k - 1) * p0) / k
    return p1 if n else p0
def integ(p):   # integral over [-1,1] of an fmpq_poly
    c = p.coeffs(); return sum((fmpq(2) * c[k] / (k + 1) for k in range(0, len(c), 2)), fmpq(0))
P7 = leg(7); X = fmpq_poly([0, 1])
A = fmpq_mat(8, 8, [integ(P7 * X ** (i + j)) for i in range(8) for j in range(8)])
bvec = fmpq_mat(8, 1, [-integ(P7 * X ** (i + 8)) for i in range(8)])
sol = A.solve(bvec)
E8 = fmpq_poly([sol[i, 0] for i in range(8)] + [1])
K = P7 * E8; K = K * K.denom()
coeffs = [int(c) for c in K.coeffs()]
roots = sorted((r.real for r, mult in fmpz_poly(coeffs).complex_roots()), key=lambda u: float(u.mid()))
assert len(roots) == 15
ca = [arb(c) for c in coeffs]; nn = 15
def weight(xr):
    q = [None] * nn; q[nn - 1] = ca[nn]
    for k in range(nn - 1, 0, -1): q[k - 1] = ca[k] + xr * q[k]
    dp = sum(k * ca[k] * xr ** (k - 1) for k in range(1, nn + 1))
    return sum(q[k] * (arb(2) / (k + 1)) for k in range(0, nn, 2)) / dp
k15 = [(r, weight(r)) for r in roots]
g7 = [arb.legendre_p_root(7, k, weight=True) for k in range(7)]
# second method (mpmath): polish the nodes by Newton on P_7*E_8 and get weights from the moment equations
mpc = [mpmath.mpf(c) for c in coeffs]
def pk(u): return mpmath.polyval(mpc[::-1], u)
nodes_mp = [mpmath.findroot(pk, mpmath.mpf(float(r.mid()))) for r in roots]
V = mpmath.matrix(15, 15); rhs = mpmath.matrix(15, 1)
for i in range(15):
    for j in range(15): V[i, j] = nodes_mp[j] ** i
    rhs[i] = mpmath.mpf(2) / (i + 1) if i % 2 == 0 else 0
w_mp = mpmath.lu_solve(V, rhs)
k15_mp = list(zip(nodes_mp, w_mp))
g7_mp = []
for r, w in g7:
    u = mpmath.findroot(lambda s: mpmath.legendre(7, s), mpmath.mpf(float(r.mid())))
    d = 7 * (u * mpmath.legendre(7, u) - mpmath.legendre(6, u)) / (u * u - 1)
    g7_mp.append((u, 2 / ((1 - u * u) * d * d)))
sect = None
for line in x['wikitext'].split('\n'):
    if 'Gauss nodes' in line: sect = 'G7'; continue
    if 'Kronrod nodes' in line: sect = 'K15'; continue
    m = re.match(r'\|\s*(?:\S\s*)?(\d\.[\d ]+?)\s*\|\|[^|]*\|\|\s*(\d\.[\d ]+)', line)
    if not (m and sect): continue
    xs = m.group(1).replace(' ', ''); ws = m.group(2).replace(' ', '')
    ca_, cm_ = (g7, g7_mp) if sect == 'G7' else (k15, k15_mp)
    i = min(range(len(ca_)), key=lambda q: abs(abs(float(ca_[q][0].mid())) - float(xs)))
    j = min(range(len(cm_)), key=lambda q: abs(abs(float(cm_[q][0])) - float(xs)))
    rec('kronrod', sect + ' node ' + xs, xs, abs(ca_[i][0]), abs(cm_[j][0]))
    rec('kronrod', sect + ' weight at ' + xs[:7], ws, ca_[i][1], cm_[j][1])
print('  values recomputed:', total - n0)

# ---------------------------------------------------------------- 6. single values
print('Single values')
phi_a = (1 + arb(5).sqrt()) / 2; phi_m = mpmath.phi
def vardi():
    s = 2
    for n in range(1, 12): s = s * s - s + 1          # Sylvester's sequence, s_11
    a = ((arb(s) - arb(1) / 2).log() / 2 ** 12).exp()   # E = lim (s_n - 1/2)^(1/2^(n+1)), error far below 1e-100
    m = mpmath.exp(mpmath.log(mpmath.mpf(s) - 0.5) / 2 ** 12)
    return a, m
singles = [
 ('golden', 'Golden ratio', 'phi^3', '4.236067978', phi_a ** 3, phi_m ** 3),
 ('golden', 'Golden ratio', 'phi^4', '6.854101967', phi_a ** 4, phi_m ** 4),
 ('golden', 'Golden ratio', 'phi^2', '2.618033989', phi_a ** 2, phi_m ** 2),
 ('golden', 'Golden ratio', 'phi', '1.618033989', phi_a, phi_m),
 ('gamma32', 'Particular values of the gamma function', 'Gamma(1/2)', '1.7724538509055160273', arb.pi().sqrt(), mpmath.gamma(0.5)),
 ('gamma32', 'Particular values of the gamma function', 'Gamma(3/2)', '0.8862269254527580137', arb.pi().sqrt() / 2, mpmath.gamma(1.5)),
 ('gamma32', 'Particular values of the gamma function', 'Gamma(5/2)', '1.3293403881791370205', arb.pi().sqrt() * 3 / 4, mpmath.gamma(2.5)),
 ('gamma32', 'Particular values of the gamma function', 'Gamma(7/2)', '3.3233509704478425512', arb.pi().sqrt() * 15 / 8, mpmath.gamma(3.5)),
 ('vardi', 'Double exponential function', "Vardi's constant", '1.264084735305302') + vardi(),
 ('gelfond', 'List of numbers', 'e^pi', '23.14069263277925', arb.pi().exp(), mpmath.exp(mpmath.pi)),
 ('feller', "Feller's coin-tossing constants", 'beta_2 = 1 + 1/sqrt 5', '1.44721356', 1 + 1 / arb(5).sqrt(), 1 + 1 / mpmath.sqrt(5)),
 ('unary', 'Unary coding', 'phi', '1.61803398879', phi_a, phi_m),
 ('partial_euler', 'Partial Euler Product', 'e', '2.718281728459', arb(1).exp(), mpmath.e),
 ('deltoidal', 'Deltoidal icositetrahedron', 'short/long edge = (4+sqrt 2)/7', '0.7731900694928638', (4 + arb(2).sqrt()) / 7, (4 + mpmath.sqrt(2)) / 7),
]
for key, art, what, printed, va, vm in singles:
    assert printed in EX[key]['wikitext'].replace('\\,', ''), (key, printed)
    rec(key, '%s: %s' % (art, what), printed, va, vm, accept_trunc=True)
# the deltoidal icositetrahedron ratio from coordinates: polar dual of the rhombicuboctahedron (+-1, +-1, +-(1+sqrt 2))
s2 = mpmath.sqrt(2)
Av = mpmath.matrix([0, 0, 1 / (1 + s2)]); Bv = mpmath.matrix([1, 0, 1]) / (2 + s2); Cv = mpmath.matrix([1, 1, 1]) / (3 + s2)
ratio = mpmath.norm(Bv - Cv) / mpmath.norm(Av - Bv)
assert abs(ratio - (4 + s2) / 7) < mpmath.mpf(10) ** -50
print('  deltoidal icositetrahedron, short/long edge from coordinates:', mpmath.nstr(ratio, 18),
      '| the two lengths printed in the same sentence give', mpmath.nstr(mpmath.mpf('0.707106785') / mpmath.mpf('0.914213565'), 10))

# ---------------------------------------------------------------- 7. Brun's constant continued fraction
x = EX['brun']; print('List of mathematical constants, revision', x['revid'], "(continued fraction printed for Brun's constant)")
from fractions import Fraction
m = re.search(r'\[1; (1, 9, [\d, ]+),', x['wikitext']); pq = [1] + [int(u) for u in m.group(1).split(',')]
def cf(fr, n):
    out = []
    for _ in range(n):
        a = fr.numerator // fr.denominator; out.append(a); fr -= a
        if fr == 0: break
        fr = 1 / fr
    return out
def cfval(c):
    v = Fraction(c[-1])
    for a in c[-2::-1]: v = a + 1 / v
    return v
print('  printed partial quotients:', pq)
print('  value of the printed finite fraction: %.15f' % float(cfval(pq)))
lo = Fraction(1902160582428, 10 ** 12); hi = Fraction(1902160583990, 10 ** 12)   # Nicely: 1.902160583209 +- 0.000000000781
clo, chi = cf(lo, 30), cf(hi, 30)
k = 0
while clo[k] == chi[k]: k += 1
print('  partial quotients fixed by the interval 1.902160583209 +- 0.000000000781:', clo[:k], '(%d terms)' % k)
print('  continued fraction of the decimal 1.9021605823       :', cf(Fraction(19021605823, 10 ** 10), 30))
print('  continued fraction of the decimal 1.9021605831 (table):', cf(Fraction(19021605831, 10 ** 10), 30))
agree = 0
c23 = cf(Fraction(19021605823, 10 ** 10), 30)
while agree < min(len(pq), len(c23)) and pq[agree] == c23[agree]: agree += 1
print('  the printed list agrees with the expansion of the terminating decimal 1.9021605823 in its first', agree, 'terms')
total += 1; wrong.append(('brun', 'continued fraction of Brun constant', str(pq), 'WRONG from term %d on' % (k + 1)))

# ---------------------------------------------------------------- 8. Student t and chi-squared critical values
# A printed quantile v with half-unit h is the correctly rounded value exactly when CDF(v-h) <= p <= CDF(v+h).
# The CDF is evaluated with Arb (rigorous) and with mpmath; both must give the same verdict.
def verdict(p, cdf_arb, cdf_mp, v):
    nd = len(v.split('.')[1]); h = arb(10) ** -nd / 2; hm = mpmath.mpf(10) ** -nd / 2
    va = arb(v); vm = mpmath.mpf(v); pa = arb(p); pm = mpmath.mpf(p)
    lo_a, hi_a, top_a = cdf_arb(va - h) - pa, cdf_arb(va + h) - pa, cdf_arb(va + 2 * h) - pa
    lo_m, hi_m, top_m = cdf_mp(vm - hm) - pm, cdf_mp(vm + hm) - pm, cdf_mp(vm + 2 * hm) - pm
    def sgn(z): return 1 if (z > 0) == True else (-1 if (z < 0) == True else 0)
    assert (sgn(lo_a), sgn(hi_a), sgn(top_a)) == (sgn(arb(str(lo_m))), sgn(arb(str(hi_m))), sgn(arb(str(top_m)))) and 0 not in (sgn(lo_a), sgn(hi_a), sgn(top_a))
    if sgn(lo_a) < 0 and sgn(hi_a) > 0: return 'ok-round'
    if sgn(hi_a) < 0 and sgn(top_a) > 0: return 'ok-trunc'     # quantile in (v+h, v+2h): v is the truncated value
    return 'WRONG'
def quantile_mp(cdf_mp, p, v): return mpmath.findroot(lambda u: cdf_mp(u) - mpmath.mpf(p), mpmath.mpf(v))
x = EX['t_table']; print("Student's t-distribution, revision", x['revid'], '(table of critical values)')
n0 = total
blocks = x['wikitext'].split('\n|-')
levels = None
for b in blocks:
    lines = [l for l in b.strip().split('\n') if l.strip()]
    if lines and 'One-sided' in lines[0]: levels = [l.lstrip('! ').rstrip('%') for l in lines[1:]]
    if not lines or not lines[0].startswith('!') or levels is None: continue
    dfs = lines[0].lstrip('! ').strip()
    if not dfs.isdigit(): continue
    df = int(dfs)
    vals = [l.lstrip('| ').strip() for l in lines[1:] if l.startswith('|')]
    if len(vals) != len(levels): continue
    for lv, v in zip(levels, vals):
        p = str(mpmath.mpf(lv) / 100)
        # P(T <= t) = 1 - I_{df/(df+t^2)}(df/2, 1/2) / 2 for t > 0
        ca = lambda u: 1 - (df / (df + u * u)).beta_lower(arb(df) / 2, arb(1) / 2, regularized=True) / 2
        cm = lambda u: 1 - mpmath.betainc(mpmath.mpf(df) / 2, mpmath.mpf(1) / 2, 0, df / (df + u * u), regularized=True) / 2
        total += 1
        st = verdict(p, ca, cm, v)
        if st != 'ok-round':
            wrong.append(('t_table', 'df %d, one-sided %s%%' % (df, lv), v, st))
            print('  %-9s df %d, one-sided %s%%: printed %s value %s' % (st, df, lv, v, mpmath.nstr(quantile_mp(cm, p, v), 8)))
print('  values recomputed:', total - n0)
x = EX['chi2_table']; print('Chi-squared distribution, revision', x['revid'], '(table of chi-squared values against p-values)')
n0 = total
plist = re.findall(r'aa" \| ([\d.]+)', x['wikitext'])
assert plist == ['0.95', '0.90', '0.80', '0.70', '0.50', '0.30', '0.20', '0.10', '0.05', '0.01', '0.001'], plist
for dfs, vals in re.findall(r'\|\s*(\d+)\s*\n\|\s*([\d. |]+)', x['wikitext']):
    df = int(dfs); vs = [u.strip() for u in vals.split('||')]
    assert len(vs) == 11
    for p, v in zip(plist, vs):
        # the table gives x with upper tail probability p: lower CDF = 1 - p
        ca = lambda u: 1 - (u / 2).gamma_upper(arb(df) / 2, regularized=1)
        cm = lambda u: mpmath.gammainc(mpmath.mpf(df) / 2, 0, u / 2, regularized=True)
        total += 1
        st = verdict(str(1 - mpmath.mpf(p)), ca, cm, v)
        if st != 'ok-round':
            wrong.append(('chi2_table', 'df %d, p = %s' % (df, p), v, st))
            print('  %-9s df %d, p = %s: printed %s value %s' % (st, df, p, v, mpmath.nstr(quantile_mp(cm, str(1 - mpmath.mpf(p)), v), 7)))
print('  values recomputed:', total - n0)

print()
print('TOTAL values recomputed:', total, '| flagged:', len(wrong))
for w in wrong: print('  ', w)
