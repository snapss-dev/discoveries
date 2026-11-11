# Checks the digits of two OEIS constants against exact integer arithmetic.
#   A261114  Sum_{n>=0} 1/(n!)^n                       (DATA and the 440-term b-file)
#   A333507  1 - 365!/((365-23)! * 365^23)             (DATA)
# The DATA lines below and b261114.txt are as served by oeis.org on 2026-11-11.
# Run:  python check.py
import os
from fractions import Fraction
from math import factorial

HERE = os.path.dirname(os.path.abspath(__file__))

A261114_DATA = "2,2,5,4,6,3,2,6,4,3,7,5,1,6,0,7,5,1,7,4,6,6,0,9,1,7,6,1,9,4,2,3,6,2,4,8,7,3,6,0,2,8,6,2,4,2,7,9,1,0,8,1,6,9,7,0,1,4,3,0,0,8,6,5,2,0,9,2,7,1,9,4,4,7,4,0,9,3,0,9,8,8,9,0,5,9,5"
A333507_DATA = "5,0,7,2,9,7,2,3,4,3,2,3,9,8,5,4,0,7,2,2,5,4,1,7,2,2,8,3,3,7,0,3,2,5,0,0,2,3,5,9,7,1,8,4,5,2,9,2,9,8,7,8,0,9,9,0,1,9,7,4,0,0,2,0,0,1,8,8,4,1,8,3,9,1,8,1,2,7,7,1,5,9,9,2,2,3,3,1,6,8,0,5,3,7,0,5,3,2,0,1,1,8,6,4,8,3,2,8,4,7,7,6,5,4,2,4,6,8,6,0"

def first_diff(a, b):
    k = 0
    while k < min(len(a), len(b)) and a[k] == b[k]: k += 1
    return k

print("=== A261114: Sum_{n>=0} 1/(n!)^n ===")
# Exact partial sum to n = N and a rigorous tail bound: for n >= 2 each term is at most half the
# one before, so the tail after N is below 2/((N+1)!)^(N+1).
N = 30
S = sum(Fraction(1, factorial(n) ** n) for n in range(N + 1))
tail = Fraction(2, factorial(N + 1) ** (N + 1))
D = 445                                   # decimal places wanted
lo = (S.numerator * 10 ** D) // S.denominator
hi = ((S + tail).numerator * 10 ** D) // (S + tail).denominator
assert lo == hi, "tail bound too weak"
true = str(lo)                            # '2' followed by 445 decimals, all certified
print("method 1 (exact rationals, tail < 2/(31!)^31):")
print("  ", true[0] + "." + true[1:101] + "...")

# method 2: Arb ball arithmetic (python-flint), independent of the rational code above
from flint import arb, ctx
ctx.dps = 520
s = arb(0)
for n in range(0, 40):
    s += 1 / (arb(n + 1).gamma() ** n)             # n! = Gamma(n+1), as a ball
s += arb(0, 1) * (2 / (arb(41).gamma() ** 40))     # enclosure of the tail: [-r, r] with r = 2/(40!)^40
arb_digits = s.str(460, radius=False).replace(".", "")
assert arb_digits[:440] == true[:440], "Arb disagrees with exact rationals"
print("method 2 (Arb balls, 40 terms + tail enclosure): agrees with method 1 to 440 digits")

# method 3: mpmath
import mpmath as mp
mp.mp.dps = 520
m = mp.fsum(1 / mp.factorial(n) ** n for n in range(0, 40))
mp_digits = mp.nstr(m, 470, strip_zeros=False).replace(".", "")
assert mp_digits[:440] == true[:440], "mpmath disagrees"
print("method 3 (mpmath, 520 digits): agrees with method 1 to 440 digits")

data = A261114_DATA.replace(",", "")
k = first_diff(data, true)
print("DATA: %d terms, the first %d are correct; a(%d) is printed %s, correct %s" % (len(data), k, k + 1, data[k], true[k]))
print("   printed a(%d..%d): %s" % (k + 1, len(data), data[k:]))
print("   correct a(%d..%d): %s" % (k + 1, len(data), true[k:len(data)]))
b = [l.split() for l in open(os.path.join(HERE, "b261114.txt")) if l.strip() and not l.startswith("#")]
assert [int(x[0]) for x in b] == list(range(1, len(b) + 1))
bd = "".join(x[1] for x in b)
kb = first_diff(bd, true)
wrong_after = sum(1 for i in range(len(bd)) if bd[i] != true[i])
print("b-file: %d terms, the first %d are correct; %d of the remaining %d terms differ from the correct digit"
      % (len(bd), kb, wrong_after, len(bd) - kb))
print("   b-file begins with the DATA terms:", bd.startswith(data))
diff = Fraction(int(bd), 10 ** (len(bd) - 1)) - S
print("   (number printed in the b-file) - (true value) = %.4e" % float(diff))
print("   correct a(1..440):")
for i in range(0, 440, 88): print("     " + true[i:i + 88])
assert k == 42 and kb == 42

print()
print("=== A333507: 1 - 365!/((365-23)! * 365^23) ===")
p = 1 - Fraction(factorial(365), factorial(365 - 23) * 365 ** 23)
print("exact value = %d / %d" % (p.numerator, p.denominator))
print("   numerator has %d digits, denominator %d" % (len(str(p.numerator)), len(str(p.denominator))))
D = 130
true2 = str((p.numerator * 10 ** D) // p.denominator).rjust(D, "0")
# independent route: long division of the complementary product, without Fraction or factorial
num = 1
for j in range(23): num *= 365 - j
den = 365 ** 23
rem = den - num                              # p = (den - num)/den
digs = []
for _ in range(D):
    rem *= 10; digs.append(str(rem // den)); rem %= den
assert "".join(digs) == true2, "long division disagrees"
ctx.dps = 200
pa = 1 - arb(366).gamma() / (arb(343).gamma() * arb(365) ** 23)
assert pa.str(150, radius=False).split(".")[1][:D - 2] == true2[:D - 2], "Arb disagrees"
print("three routes agree (Fraction; long division of 1 - prod (365-j)/365; Arb balls)")
data2 = A333507_DATA.replace(",", "")
k2 = first_diff(data2, true2)
print("DATA: %d terms a(0..%d), the first %d are correct; a(%d) is printed %s, correct %s"
      % (len(data2), len(data2) - 1, k2, k2, data2[k2], true2[k2]))
print("   printed a(%d..%d): %s" % (k2 - 4, len(data2) - 1, data2[k2 - 4:]))
print("   correct a(%d..%d): %s" % (k2 - 4, len(data2) - 1, true2[k2 - 4:len(data2)]))
shifted = data2[k2 + 1:] == true2[k2:len(data2) - 1]
print("   deleting the printed a(%d) makes all later terms correct (one inserted digit): %s" % (k2, shifted))
print("   terms a(%d..%d) that differ from the correct digit: %d of %d"
      % (k2, len(data2) - 1, sum(1 for i in range(k2, len(data2)) if data2[i] != true2[i]), len(data2) - k2))
assert k2 == 84 and shifted
print()
print("ALL CHECKS PASSED")
