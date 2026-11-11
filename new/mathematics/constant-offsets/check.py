# Twelve OEIS decimal-expansion entries whose OFFSET does not match the size of the constant.
# OEIS convention: with listed digits d1, d2, d3, ... and offset o, the constant is 0.d1 d2 d3 ... * 10^o,
# so o = floor(log10(x)) + 1 (the number of digits before the decimal point when x >= 1).
# Each constant is evaluated from its NAME with mpmath, and again with Arb balls where Arb has the
# functions; the first digits must agree with the DATA line, and the offset that fits is printed.
# OFFSET and first DATA digits as served by oeis.org on 2026-11-11.   Run:  python check.py
import mpmath as mp
from flint import arb, ctx

mp.mp.dps = 60
ctx.dps = 60
phi = (1 + mp.sqrt(5)) / 2

def a114610():
    return mp.fsum(mp.log(2) / (mp.mpf(2) ** (-mp.mpf(k) / 2) + mp.mpf(2) ** (mp.mpf(k) / 2)) ** 2 for k in range(-600, 601))
def a248181():
    return mp.fsum(1 / mp.binomial(h, h // 2) for h in range(0, 500))
def a246644():
    r = [z for z in mp.polyroots([1, -1, 1, -mp.mpf(1) / 3], maxsteps=200, extraprec=200) if abs(mp.im(z)) < mp.mpf(10) ** -40]
    assert len(r) == 1
    return mp.re(r[0])
def a293380():
    f = lambda r: mp.fsum((mp.mpf(1) / 2 - r ** n) ** n / n for n in range(1, 400))
    return mp.findroot(f, mp.mpf('0.547'))

# entry: (listed offset, first listed digits, mpmath value, Arb value or None, name)
ENTRIES = [
 ('A110993', 1, "100603175", lambda: mp.zeta(mp.zeta(10)), lambda: arb(10).zeta().zeta(), "Zeta(Zeta(10))"),
 ('A111513', 0, "175814468", lambda: abs(mp.log10(mp.sin(mp.pi / 180))), lambda: abs((arb.pi() / 180).sin().log() / arb(10).log()), "abs(log_10(sine of 1 degree))"),
 ('A113272', 0, "557281571", lambda: mp.gamma(mp.mpf(1) / 4) ** 4 / mp.pi ** 3, lambda: (arb(1) / 4).gamma() ** 4 / arb.pi() ** 3, "Gamma(1/4)^4/Pi^3"),
 ('A113477', 0, "242865064", lambda: mp.gamma(mp.mpf(1) / 3) ** 3 / (mp.mpf(2) ** (mp.mpf(4) / 3) * mp.pi), lambda: (arb(1) / 3).gamma() ** 3 / (arb(2) ** (arb(4) / 3) * arb.pi()), "Gamma(1/3)^3/(2^(4/3)*Pi)"),
 ('A114610', 0, "100000000", a114610, None, "Sum_{k=-inf..inf} log(2)/(2^(-k/2) + 2^(k/2))^2"),
 ('A248181', 0, "320919957", a248181, None, "Sum_{h>=0} 1/binomial(h, floor(h/2))"),
 ('A319129', 0, "229663026", lambda: (1 + mp.sqrt(3) + mp.sqrt(2 * mp.sqrt(3))) / 2, lambda: (1 + arb(3).sqrt() + (2 * arb(3).sqrt()).sqrt()) / 2, "(1 + sqrt(3) + sqrt(2*sqrt(3)))/2"),
 ('A242600', 1, "542191216", lambda: -mp.polylog(2, 1 - phi), None, "-dilog(phi) = -polylog(2, 1-phi)"),
 ('A246644', 1, "442493334", a246644, None, "real root of s^3 - s^2 + s - 1/3 = 0"),
 ('A293380', 1, "547180243", a293380, None, "r with 0 = Sum_{n>=1} (1/2 - r^n)^n/n"),
 ('A156547', 1, "729727656", lambda: mp.acos(mp.sqrt(5) / 3), lambda: (arb(5).sqrt() / 3).acos(), "central angle of a dodecahedron, arccos(sqrt(5)/3)"),
 ('A160205', 11, "264418510", lambda: (989043 + 524338 * mp.sqrt(2)) / 809 ** 2, lambda: (989043 + 524338 * arb(2).sqrt()) / 809 ** 2, "(989043+524338*sqrt(2))/809^2"),
]
ok = True
print("%-8s %-50s %-18s %-7s %-7s" % ("entry", "constant", "value", "listed", "fits"))
for a, off, first, f, g, name in ENTRIES:
    v = f()
    s = mp.nstr(v, 30, strip_zeros=False, min_fixed=-10**9, max_fixed=10**9)
    digs = s.replace('.', '').lstrip('0')
    assert digs.startswith(first), (a, digs, first)           # the listed digits are those of this constant
    if g is not None:
        w = g()
        assert abs(arb(mp.nstr(v, 50)) - w) < arb("1e-40"), a  # Arb agrees with mpmath
    right = int(mp.floor(mp.log10(v))) + 1
    print("%-8s %-50s %-18s %-7d %-7d" % (a, name, mp.nstr(v, 12), off, right))
    ok &= (right != off)
print()
print("ALL TWELVE OFFSETS DIFFER FROM THE SIZE OF THE CONSTANT" if ok else "SOMETHING DIFFERS FROM THE PAGE")
