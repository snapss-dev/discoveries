# A072633: Sanso's counterexample to a(n) = 1 + round(n / log 2) is the smallest one

Written 2026-11-11 and revised after an independent check. Produced with AI assistance (see the
repository README). Not submitted to the OEIS or to a journal.

## Credit and scope

**The counterexample is not ours.** Antonio Sanso found it and posted it on 22 July 2026
([X post](https://x.com/asanso/status/2079999623507198242)), and proposed it to the OEIS the same day
(A072633 history, revisions 21 to 25). An editor asked for a formatting change and reverted the edit on
9 August 2026 when no reply came, so the published entry (revision 27) still shows only the conjecture.
The same number was found independently here on 2026-11-11, before the revision history had been read.
Priority is Sanso's; see [the rediscovery page](../../../independent-rediscovery/mathematics/A072633-counterexample/README.md).

What this note adds, as far as could be checked:

1. a proof that Sanso's n is the **smallest** counterexample. It rests on one refereed theorem (Gallot,
   Moree & Zudilin 2011), one elementary lemma proved here, and two finite computations;
2. the two-sided bound F(n) <= a(n) <= F(n) + 1 for every n, and a necessary condition for a(n) != F(n);
3. the next counterexamples (451 digits, and three of 638 to 639 digits), complete below q_1301;
4. the link to the older literature, which already contains the constant that explains everything.

## 1. Statement

For an integer n >= 0 let a(n) be the smallest m >= 1 with

    1^n + 2^n + ... + m^n >= (m+1)^n            (OEIS A072633)

and let F(n) = 1 + round(n / log 2), the formula conjectured by Herbert Kociemba in 2020 and verified
there for n <= 700. Write L = log 2 and theta = 2/L = [2; 1, 7, 1, 2, 1, 1, 1, 3, 2, 4, ...], with
convergents p_k/q_k (p_0/q_0 = 2/1).

**Theorem.**

1. F(n) <= a(n) <= F(n) + 1 for every n >= 0.
2. If a(n) = F(n) + 1, then n > 693,200,000, and n = t*q_k and 2F(n) - 1 = t*p_k for some odd k and odd
   t with p_k odd, and mu < 1/250, where mu = M*(M - 3/2 - n/L) and M = F(n) + 1.
3. The smallest n with a(n) != F(n) is n = q_641, the 330-digit number in `counterexample_n.txt`.
   There a(n) = F(n) + 1. The only other such n below q_1301 (a 666-digit number) are q_871 (451 digits)
   and q_1251, 3*q_1251, 5*q_1251 (638 to 639 digits).

## 2. Earlier work

- **Erdős 1949** (Amer. Math. Monthly 56, Advanced Problem 4347) compared the same crossover with the
  integer m = m_E(n) defined by (1 - 1/m)^n > 1/2 > (1 - 1/(m-1))^n. As restated in van de Lune's report,
  the problem asks for a proof that m_E - 1 <= a(n) <= m_E, and that both values occur infinitely often.
- **van de Lune 1975** and **van de Lune & te Riele 1975** (Mathematisch Centrum reports ZW 54/75 and
  ZW 56/75) proved a(n) >= m_E - 1 and that a(n) = m_E for almost all n.
- **Best & te Riele 1976** (report NW 23/76) proved a(n) <= m_E and found the first 33 known n with
  a(n) = m_E - 1, from the continued fraction of 2/log 2; the smallest is n = 777451915729368. Whether
  there are infinitely many is open. Their Theorem 6 (stated without proof) gives the crossover as
  n = (M - 3/2 - (25/12 - 3 log 2 + o(1))/M) log 2.
- **Gallot, Moree & Zudilin 2011** (Math. Comp. 80, 1221-1237, Theorem 1) proved that expansion with
  c1 = 25/12 - 3 log 2 = 0.0038918 and made it effective for M > 10^9. That theorem is used below.

In these terms there are three quantities of the form ceiling(n/L + 1/2 + (const)/n):

| quantity | constant | first n where it differs from a(n) |
|---|---|---|
| Kociemba's formula F(n) | 0 | n = q_641, 330 digits (Sanso 2026; smallest: this note) |
| the true value a(n) | L*c1 = 0.0026976 | |
| Erdős's threshold m_E(n) | L/12 = 0.0577623 | n = 777451915729368 (smallest known; Best & te Riele 1976) |

F(n) sits about twenty times closer to the truth than m_E(n), which is why it agrees with a(n) for 315
orders of magnitude longer. It differs only when n/L lies within about 0.0027/n below a half-integer.

## 3. Proof

Notation: for integers M >= 2 and real n > 0 put S(M, n) = sum_{k=1}^{M-1} (k/M)^n. Then
1^n + ... + (M-1)^n >= M^n iff S(M, n) >= 1, and a(n) = min{M : S(M, n) >= 1} - 1. For fixed M,
S(M, n) is strictly decreasing in n. For n = 0 the theorem is trivial: a(0) = 1 = F(0). Let n >= 1.

### Ingredient A: the formula never overshoots (Lemma A, proved here)

*Let M >= 2 and let n be an integer with n >= L(M - 3/2). Then 1^n + ... + (M-1)^n < M^n.*

*Proof.* Since S(M, n) decreases in n, it suffices to treat the real exponent nu = L(M - 3/2).

For 2 <= M <= 10^4 the inequality was verified by machine at the smallest integer n >= nu: with exact
integers for M <= 600 and with certified Arb balls above that (`verify_arb.py`, section 1).

Let M >= 10^4 and eps = 1/M.

*Step 1.* For 0 < x < 1, log(1 - x) <= -x - x^2/2 - x^3/3. With x = j*eps and nu = L(1/eps - 3/2):

    nu * log(1 - j*eps) <= -L*j + L*g_j,
    g_j = eps*j(3-j)/2 + eps^2*j^2(9-4j)/12 + eps^3*j^3/2.

Hence (1 - j/M)^nu <= 2^(-j) * exp(y_j) with y_j = L*g_j.

*Step 2.* y_1 = L(eps + 5 eps^2/12 + eps^3/2) > 0 and y_2 = L(eps + eps^2/3 + 4 eps^3) > 0. For
3 <= j <= M-1 we have y_j <= 0: with x = j*eps < 1, g_j/(j*eps) = (3-j)/2 + x(9-4j)/12 + x^2/2, which is
x(x/2 - 1/4) <= 0 for j = 3 (as x <= 1/2), and is below -1/2 + 1/2 = 0 for j >= 4.

*Step 3.* e^y <= 1 + y + y^2/2 for y <= 0, and e^y <= 1 + y + y^2/2 + (y^3/6)e^y for y >= 0. Since
y_1, y_2 <= 1.001*L*eps, the two cubic remainders together are at most
rho = (1/2 + 1/4) * (1.001 L eps)^3 * 1.001 / 6 <= 0.042 eps^3.

*Step 4.* Put q_j = y_j + y_j^2/2 (defined for all j >= 1 by the polynomial g_j) and
T(eps) = sum_{j>=1} 2^(-j) q_j. Since q >= -1/2 for every real y, sum_{j>=M} 2^(-j) q_j >= -2^(-M). So

    S(M, nu) <= sum_{j=1}^{M-1} 2^(-j) (1 + q_j) + rho
             <= (1 - 2^(1-M)) + T(eps) + 2^(-M) + rho  <  1 + T(eps) + rho.

*Step 5.* With sum_{j>=1} j^k / 2^j = 1, 2, 6, 26, 150, 1082, 9366 for k = 0, ..., 6
(`lemmaA_polynomial.py` computes this exactly):

    T(eps) = -(25/6 - 6L) L eps^2 + (13 L + (235/3) L^2) eps^3
             + (6433/48) L^2 eps^4 - (4621/4) L^2 eps^5 + (4683/4) L^2 eps^6,

where (25/6 - 6L) L = 0.00539516..., 13 L + (235/3) L^2 = 46.6463..., and the last three terms add at
most 64.4 eps^4. For eps <= 10^(-4):

    T(eps) + rho <= eps^2 (-0.0053951 + 46.70 eps) <= eps^2 (-0.0053951 + 0.00467) < 0.

So S(M, nu) < 1. ∎

(The hand argument already works from M >= 8655, so it overlaps the machine-checked range.) The leading
coefficient is -2 L c1 with c1 = 25/12 - 3 log 2, in agreement with ingredient C, which also implies
Lemma A for M > 10^9.

### Ingredient B: direct computation for n <= 693,200,000

*For every 1 <= n <= 693,200,000 we have a(n) = F(n).*

By Lemma A, a(n) >= F(n), so it is enough to show S(F+1, n) >= 1, and since all terms are positive it is
enough that a partial sum reaches 1. `direct_check.py` does this in two stages: a float64 pass over the
first 64 terms that accepts n only if the partial sum is at least 1 + 10^(-12) (the accumulated rounding
error is below 10^(-14)) and n/L is at least 10^(-6) away from a half-integer; and a certified Arb pass
for every n the first stage does not accept (250,766 values). No failure was found. The largest M = F + 1
covered is 1,000,076,204 > 10^9.

### Ingredient C: Gallot, Moree & Zudilin 2011, Theorem 1 (quoted)

*For an integer M > 10^9 and real nu > 0 with 1^nu + ... + (M-1)^nu = M^nu we have
nu = L (M - 3/2 - C_M/M) with 0 < C_M < 0.004.*

Since S(M, n) is continuous and strictly decreasing in n, from M - 1 at n = 0 to 0, this nu = nu(M) exists
and is unique, and for an integer n:

    S(M, n) >= 1   iff   n <= nu(M)   iff   mu >= C_M,     where mu = M (M - 3/2 - n/L).

In particular, for M > 10^9: mu >= 1/250 implies S(M, n) >= 1.

*Remark.* Theorem 3 of Best & te Riele (1976) states the same with 1/256 in place of 1/250 and for all
M >= 2. It is an unrefereed report, so the proof below does not use it; `verify_arb.py` (section 2)
re-verifies its conclusion at the largest admissible n for every 2 <= M <= 10^4, and everything found here
is consistent with it.

### Proof of the Theorem

Let n >= 1 and r = round(n/L), so F = r + 1 and r - 1/2 < n/L < r + 1/2 (n/L is irrational); r >= 1.

*(1), lower bound.* For every 2 <= M <= F we have L(M - 3/2) <= L(r - 1/2) < n, so S(M, n) < 1 by
Lemma A. Hence a(n) >= F.

*(1), upper bound.* If n <= 693,200,000 then a(n) = F by ingredient B. Otherwise M = F + 2 > 10^9 and
mu = M (r + 3/2 - n/L) > M > 1/250, so S(F+2, n) >= 1 by ingredient C. Hence a(n) <= F + 1.

*(2).* Let a(n) = F + 1. By ingredient B, n > 693,200,000, so M = F + 1 = r + 2 > n/L + 3/2 > 10^9. Put
delta = M - 3/2 - n/L = r + 1/2 - n/L, so 0 < delta < 1 and mu = M*delta. As S(F+1, n) < 1, ingredient C
gives mu < C_M < 1/250. Put p = 2r + 1 = 2F - 1. Then

    0 < p/n - theta = 2 delta / n < 1/(125 M n) < 1/(2 n^2)        (because M > n/L > n).

By Legendre's theorem p/n equals a convergent p_k/q_k of theta, and k is odd because p/n > theta. So
n = t q_k and p = t p_k with t = gcd(p, n); p is odd, hence t and p_k are odd.

*(3).* By (2), any n with a(n) != F(n) has the form t*q_k with k odd, p_k odd, t odd and mu < 1/250,
where mu = M(M - 3/2 - n/L) and M = (t p_k + 3)/2. `verify_arb.py` (sections 4 and 5) computes the first
1302 partial quotients of theta with certified balls at two precisions and evaluates mu for every odd
k <= 1300 and every odd t (mu increases with t). The only pairs with mu < 1/250 are

    (k, t) = (641, 1), (871, 1), (1251, 1), (1251, 3), (1251, 5),

and all five are genuine failures (certified individually). As q_k increases with k for k >= 1, every
n < q_641 has a(n) = F(n), and the list is complete for n < q_1301. At n = q_641 certified ball
arithmetic gives

    S(F+1, n) - 1 in [-2.87907963530e-663 +/- 1.4e-675]  < 0,
    S(F+2, n) - 1 in [ 1.16341156346e-330 +/- 4.5e-342]  > 0,

so a(n) = F(n) + 1. ∎

As a calibration of indexing and arithmetic, the same code reproduces Best & te Riele's Table 2 exactly:
the 33 values of k <= 599 with 1/256 < mu < 1/12, with mu to five decimals.

## 4. Near misses and counterexamples

Convergents of 2/log 2 with odd numerator and |mu| < 0.012, for k <= 1300. A negative sign means n/L lies
just *above* a half-integer, where the formula cannot fail. Asymptotically the formula fails when
0 < mu < c1 = 0.0038918 and holds when mu > c1; the verdict in each row is certified directly.

| k | digits of n = q_k | b_(k+1) | mu | side | formula at n |
|---:|---:|---:|---:|:---|:---|
| 70 | 32 | 65 | -0.010939 | above | holds |
| 91 | 44 | 65 | +0.010867 | below | holds |
| 95 | 48 | 105 | +0.006854 | below | holds |
| 274 | 142 | 108 | -0.006596 | above | holds |
| 300 | 154 | 155 | -0.004625 | above | holds |
| 481 | 244 | 78 | +0.009126 | below | holds |
| 542 | 281 | 526 | -0.001368 | above | holds |
| 590 | 306 | 89 | -0.008004 | above | holds |
| 612 | 318 | 212 | -0.003387 | above | holds |
| **641** | **330** | **764** | **+0.000943** | below | **fails** |
| 817 | 422 | 64 | +0.011007 | below | holds |
| 844 | 434 | 84 | -0.008465 | above | holds |
| **871** | **451** | **185** | **+0.003883** | below | **fails** |
| 903 | 470 | 155 | +0.004617 | below | holds |
| 919 | 478 | 109 | +0.006537 | below | holds |
| 1059 | 542 | 140 | +0.005112 | below | holds |
| 1084 | 555 | 62 | -0.011470 | above | holds |
| 1231 | 630 | 158 | +0.004533 | below | holds |
| **1251** | **638** | **5491** | **+0.000131** | below | **fails** (also 3n and 5n) |
| 1274 | 651 | 99 | -0.007215 | above | holds |

Two near misses are worth a look: k = 542 was close enough (|mu| = 0.0014) but on the harmless side, and
k = 871 fails by a hair (mu = 0.003883 against c1 = 0.003892). The five counterexamples found are listed
in full in `counterexamples.txt`.

*Heuristic frequency.* If the fractional parts of n/L are equidistributed, the chance that a given n fails
is about L*c1/n, so the expected number of failures below N is about 0.0027 ln N: 2.0 below 10^330 (one
found), 2.8 below 10^451 (two found), 4.0 below 10^639 (five found). This is not a theorem.

## 5. Reproducing the computations

Python 3.13 with python-flint (Arb), mpmath, sympy and numba; PARI/GP 2.17.4 for `check.gp`.

| command | what it checks | time |
|---|---|---|
| `python lemmaA_polynomial.py` | exact coefficients of T(eps) in Lemma A | 1 s |
| `python verify_arb.py 1300` | Lemma A for M <= 10^4, the continued fraction, all candidates, the certificates | 2 min |
| `python direct_check.py` | ingredient B: a(n) = F(n) for all n <= 693,200,000 | 4 min on 6 threads |
| `python verify_mpmath.py counterexample_n.txt` | the counterexample again, with mpmath intervals, no shared code | 20 s |
| `gp -q check.gp` | the counterexample in PARI/GP at 1500 digits (not interval arithmetic) | 5 s |
| `python tables.py 1300` | the table in section 4 and `counterexamples.txt` | 1 min |

The three systems agree on both margins to 12 digits, and with the values in Sanso's OEIS draft
(-2.87907963529867284035e-663 and 1.16341156346440987194e-330).

## 6. What this note depends on and does not claim

- Parts (1) to (3) rest on Theorem 1 of Gallot, Moree & Zudilin (Math. Comp. 2011), used as published.
- Lemma A for M >= 10^4 is a hand proof. It was re-derived once independently (symbolic recomputation of
  every coefficient and inequality, numerical tests up to M = 10^100) with no error found in the argument;
  it has not been refereed.
- Ingredient B is a computation. Its first stage uses float64 with a 100-fold guard band and a rounding
  error estimate made by hand, not a machine-checked bound; all borderline cases are decided with
  certified balls.
- The list of counterexamples is complete only below q_1301.
- The counterexample itself is Sanso's. Whether Sanso also established minimality is not known here; the
  X post and the OEIS draft claim only "a counterexample".

## 7. The same conjecture in A332101

[A332101](https://oeis.org/A332101) (M. F. Hasler, 2020) is the least m with m^n <= sum_{k<m} k^n, so
A332101(n) = A072633(n) + 1. Its formula line "a(n) = round(n / log(2)) + 2. (Conjectured; verified up to
10^4 ...)" is therefore the same conjecture, and it fails at the same 330-digit n. That entry also says
"a(n) = A078607(n) + 2 for almost all n > 1. (n = 777451915729368 might be an exception to this equality
or the above one.)", and a June 2026 exchange in its history asks which of the two fails there. By
ingredient B above, round(n/log 2) + 2 is correct at n = 777451915729368, so the exception is to the
A078607 equality; this is the first of the pairs found by Best & te Riele in 1976. Neither the entry nor
its history mentions A072633, Best & te Riele, or Sanso's counterexample.

## 8. Novelty check

Checked 2026-11-11: every page of the revision histories of A072633 and A332101 with their discussion
threads; both draft pages (no pending edits); the cross-referenced entries A078607, A078608 and A129935;
an in-depth web search with the sequence numbers, which is how Sanso's post was found; Epoch AI's OEIS
Open conjecture list; and the issue tracker and code of the omega-institute project. Apart from Sanso's
counterexample, no statement of minimality, of the two-sided bound, or of further counterexamples was
found.

## References

1. P. Erdős, Advanced Problem 4347, Amer. Math. Monthly 56 (1949), 343.
2. J. van de Lune, On a conjecture of Erdős (I), Mathematisch Centrum, Amsterdam, Report ZW 54/75, 1975.
3. J. van de Lune and H. J. J. te Riele, On a conjecture of Erdős (II), Report ZW 56/75, 1975.
4. M. R. Best and H. J. J. te Riele, On a conjecture of Erdős concerning sums of powers of integers,
   Mathematisch Centrum, Amsterdam, Report NW 23/76, 1976. https://ir.cwi.nl/pub/9046
5. Y. Gallot, P. Moree and W. Zudilin, The Erdős-Moser equation 1^k + 2^k + ... + (m-1)^k = m^k revisited
   using continued fractions, Math. Comp. 80 (2011), 1221-1237. https://arxiv.org/abs/0907.1356
6. A. Sanso, post of 22 July 2026, https://x.com/asanso/status/2079999623507198242, and OEIS A072633
   revision history, https://oeis.org/history?seq=A072633
7. R. K. Guy, Unsolved Problems in Number Theory, D10.
