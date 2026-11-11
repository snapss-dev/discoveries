"""Lemma A, analytic part: exact coefficients of
   T(eps) = sum_{j>=1} 2^-j * ( L*g_j + L^2*g_j^2/2 ),   L = log 2,
   g_j = eps*j(3-j)/2 + eps^2*j^2(9-4j)/12 + eps^3*j^3/2,
and the range of eps = 1/M on which T(eps) + (cubic remainder for j = 1, 2) < 0."""
from fractions import Fraction as Fr
import sympy as sp

# F[k] = sum_{j>=1} j^k / 2^j (exact).  The Fubini numbers a_k = sum_{j>=0} j^k / 2^(j+1) satisfy
# a_0 = 1, a_k = sum_{i<k} C(k,i) a_i;  hence F[0] = 1 and F[k] = 2 a_k for k >= 1.
from math import comb
a=[Fr(1)]
for k in range(1,10):
    a.append(sum(comb(k,i)*a[i] for i in range(k)))
F=[Fr(1)]+[2*x for x in a[1:]]
# independent numeric check of F[k] by direct summation
for k in range(0,8):
    direct=sum(Fr(jj**k,2**jj) for jj in range(1,400))
    assert abs(direct-F[k]) < Fr(1,10**60), k
print("F_k = sum_{j>=1} j^k/2^j, k=0..7:", [int(x) for x in F[:8]])

e,j,L=sp.symbols('eps j L', positive=True)
g=e*j*(3-j)/2 + e**2*j**2*(9-4*j)/12 + e**3*j**3/2
def wsum(expr):                       # sum_j 2^-j * polynomial(j)
    p=sp.Poly(sp.expand(expr), j)
    return sum(c*sp.Rational(F[d].numerator,F[d].denominator) for (d,),c in p.terms())
S1=sp.expand(wsum(g)); S2=sp.expand(wsum(g**2))
print("sum 2^-j g_j   =", S1)
print("sum 2^-j g_j^2 =", S2)
T=sp.expand(L*S1 + L**2*S2/2)
print("T(eps) =", sp.collect(T, e))
Lv=sp.log(2)
coef={k:sp.N(T.coeff(e,k).subs(L,Lv),15) for k in range(2,7)}
print("numeric coefficients of eps^k:", coef)
print("check: -coef2/L = 25/6 - 6 log 2 =", sp.N(sp.Rational(25,6)-6*Lv,15))
# cubic remainder for the two terms with y_j > 0 (j = 1, 2):  e^y <= 1 + y + y^2/2 + (y^3/6) e^y
# y_1 = L g_1, y_2 = L g_2; for M >= 1000 both are <= 1.001 * L * eps, and e^y <= 1.001
rem_coef = (sp.Rational(1,2)+sp.Rational(1,4))*(1.001*Lv)**3/6*1.001
print("remainder <= %.6f * eps^3 for eps <= 1/1000" % float(rem_coef))
# upper bound for eps <= 1/N: T + rem <= eps^2 * ( c2 + (c3 + rem + c4/N + c5/N^2 + c6/N^3) * eps )
c2=float(coef[2]); 
for N in (1000, 5000, 8000, 9000, 10000, 20000):
    K=float(coef[3])+float(rem_coef)+max(float(coef[4]),0)/N+max(float(coef[5]),0)/N**2+max(float(coef[6]),0)/N**3
    print(f"N={N}: T+rem <= eps^2*({c2:.9f} + {K:.4f}*eps);  negative for all M >= N iff {K:.4f}/N < {-c2:.9f}:  {K/N < -c2}   (threshold M > {K/(-c2):.1f})")
