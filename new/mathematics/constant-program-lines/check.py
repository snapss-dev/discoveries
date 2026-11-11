# Five OEIS constant entries whose DATA is right but whose program line computes something else.
# For each: the constant in the NAME and the expression in the program line are evaluated (exactly
# where possible, otherwise with mpmath and with Arb balls) and compared with the DATA line.
# DATA lines and program lines as in the OEIS on 2026-11-11.   Run:  python check.py
from fractions import Fraction
import mpmath as mp
from flint import arb, ctx

def digits_of_fraction(fr, n):
    """first n significant digits of a positive rational"""
    s = str((fr.numerator * 10 ** (n + 400)) // fr.denominator)
    return s.lstrip('0')[:n]

def digits_mp(v, n):
    return mp.nstr(abs(v), n + 20, strip_zeros=False, min_fixed=-10**9, max_fixed=10**9).replace('.', '').lstrip('0')[:n]

def agree(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]: k += 1
    return k

def mobius(n):
    r = 1; p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0: return 0
            r = -r
        p += 1
    return -r if n > 1 else r

def fac2(n):
    r = 1
    while n > 1: r *= n; n -= 2
    return r

D = {
 'A036665': "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,2,0,2,0,2,0,2,0,2,0,2,0,2,0,3,0,4,0,4,0,4,0,4,0,4,0,4,0,4,0,5,0,6,0,6,0,6,0,6,0,6,0,6,0,6,0,7,0,8,0,8,0,8,0,8,0,8,0,8,0,8,0,9,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,2,1",
 'A134877': "1,2,8,7,0,3,7,0,9,6,6,4,1,6,8,1,8,1,4,7,1,1,3,2,0,2,9,7,5,5,8,2,0,4,2,5,9,0,4,2,1,6,9,5,5,3,4,0,2,2,2,0,8,1,0,2,6,7,9,8,7,6,5,9,2,6,9,0,9,9,7,3,0,0,3,5,1,8,6,6,5,4,1,9,3,0,7,3,6,8,0,1,0,8,8,0,8,3,9,3,7,7,8,7,5",
 'A194657': "1,1,7,5,7,5,8,3,4,0,7,2,3,3,2,4,8,2,0,6,2,4,2,9,0,6,7,9,4,9,1,4,7,5,8,4,3,3,4,1,6,4,3,8,9,9,8,1,6,2,9,0,8,8,8,6,9,5,3,0,2,4,7,6,4,9,1,9,1,2,8,4,2,7,1,5,5,9,4,7,1,1,8,2,6,8,8,8,9,0,0,3,1,4,1,1,5,9,4,4,7,1,9,9,4",
 'A221363': "1,0,1,3,6,4,3,2,6,4,7,7,0,5,0,7,8,1,2,5",
 'A238273': "7,1,2,6,6,3,1,8,2,2,6,4,2,8,3,4,5,7,1,2,1,6,0,4,1,6,8,3,2,1,8,6,1,2,5,0,6,0,5,3,0,7,0,2,1,7,4,7,1,6,1,3,6,9,0,7,0,3,5,0,5,0,6,3,2,9,5,5,5,6,6,1,2,1,0,4,4,7,0,6,1,4,3,6,4,1,1,4,6,2,7,0,5,9,4,3,6,2,7,6,2,1,6,0,8",
}
def data(a): return D[a].replace(",", "").lstrip("0")
ok = True
def report(a, label, digs):
    d = data(a); k = agree(d, digs)
    print("  %-52s agrees with DATA on %3d of %3d digits" % (label, k, len(d)))
    return k == len(d)

print("A036665  Decimal expansion of 1/9801980198019801")
ok &= report('A036665', "name: 1/9801980198019801 (exact)", digits_of_fraction(Fraction(1, 9801980198019801), 120))
ok &= not report('A036665', "PARI line: 1/9801980198019800. (exact)", digits_of_fraction(Fraction(1, 9801980198019800), 120))

print("A134877  Decimal expansion of Sum_{k>=1} 1/(k!!)^(k!!)")
# terms fall faster than geometrically; 12 terms leave a tail below 10^-1000
S = sum(Fraction(1, fac2(k) ** fac2(k)) for k in range(1, 13))
ok &= report('A134877', "name: Sum 1/(k!!)^(k!!) (exact, 12 terms)", digits_of_fraction(S, 120))
S2 = sum(Fraction(1, n ** n) for n in range(1, 101))
ok &= not report('A134877', "Mathematica line: Sum_{n=1..100} 1/n^n (exact)", digits_of_fraction(S2, 120))

print("A194657  (4 Pi^6 log 2 - 90 Pi^4 zeta(3) + 1350 Pi^2 zeta(5) - 5715 zeta(7))/1536")
mp.mp.dps = 160
pi, z = mp.pi, mp.zeta
v1 = (4 * pi**6 * mp.log(2) - 90 * pi**4 * z(3) + 1350 * pi**2 * z(5) - 5715 * z(7)) / 1536
v2 = (4 * pi**6 * mp.log(2) - 90 * pi**4 * z(3) + 1350 * pi**2 * z(5) - 5715 * pi**2 * z(7)) / 1536
ctx.dps = 160
P = arb.pi()
w1 = (4 * P**6 * arb(2).log() - 90 * P**4 * arb(3).zeta() + 1350 * P**2 * arb(5).zeta() - 5715 * arb(7).zeta()) / 1536
assert abs(arb(mp.nstr(v1, 150)) - w1) < arb("1e-140"), "mpmath and Arb disagree"
ok &= report('A194657', "name (mpmath; Arb agrees)", digits_mp(v1, 120))
ok &= not report('A194657', "Mathematica line: ... - 5715 Pi^2 Zeta[7] (= %s...)" % mp.nstr(v2, 8), digits_mp(v2, 120))

print("A221363  Decimal expansion of the Pythagorean comma, 3^12/2^19 = 531441/524288")
ok &= report('A221363', "531441/524288 (exact)", digits_of_fraction(Fraction(531441, 524288), 40).ljust(20, "0"))
ok &= not report('A221363', "Mathematica line: 31441/524288 (exact)", digits_of_fraction(Fraction(31441, 524288), 40))

print("A238273  Decimal expansion of Sum_{n>=1} mu(n)/n^n")
full = sum(Fraction(mobius(n), n ** n) for n in range(1, 120))        # tail below 10^-240
part = sum(Fraction(mobius(n), n ** n) for n in range(1, 48))         # what PARI's suminf returns, see pari_check.log
ok &= report('A238273', "name: full sum (exact, 119 terms)", digits_of_fraction(full, 130))
ok &= not report('A238273', "sum stopped before n = 48 (exact)", digits_of_fraction(part, 130))
print("  mu(48) = mu(49) = mu(50) = %d, %d, %d; first omitted nonzero term 1/51^51 = %.2e"
      % (mobius(48), mobius(49), mobius(50), float(Fraction(1, 51 ** 51))))
print()
print("ALL CHECKS PASSED" if ok else "SOMETHING DIFFERS FROM THE PAGE")
