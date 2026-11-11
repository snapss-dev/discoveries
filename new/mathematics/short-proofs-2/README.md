# Seventeen short proofs (proposed additions to "Three short proofs")

Status of each: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS. These are routine once written down; they are listed because the entries still
mark them as conjectures or open observations. Each was derived a second time, independently of the agent
that first proposed it, and checked numerically from the definition.

`python check.py` checks all of them (about two minutes); output in `check.log`.

The first four need an idea; the rest are one-line congruence arguments.

## A120566: all coefficients are odd

Entry: g.f. A(x) = A(A(x)) - x*A(A(A(x))) with a(1) = 1: 1, 1, 1, 3, 7, 33, 109, 643, ... "It appears that
all terms are odd." (Paul D. Hanna, 4 June 2026)

*Proof.* Let B(x) = x/(1 - x) = x + x^2 + x^3 + ... . Then B(B(x)) = x/(1 - 2x) and
B(B(B(x))) = x/(1 - 3x), so modulo 2, B(B) = x and B(B(B)) = B. Hence, modulo 2,

    B(B) - x*B(B(B)) = x - x*B = x + x*B = B,

because x + x*B = x + x^2/(1 - x) = B exactly. So B satisfies the equation modulo 2. The equation has only
one solution with a(1) = 1, over the integers and over the field with two elements, by the same recursion:
the coefficient of x^n in A(A(x)) is 2 a(n) + R_n with R_n depending on a(1), ..., a(n-1), so the equation
reads a(n) = T_n - R_n, with T_n the coefficient of x^(n-1) in A(A(A(x))); modulo 2 the term 2 a(n) drops
out and the same recursion results. Composition of series with integer coefficients and zero constant term
commutes with reduction modulo 2, so the integer solution reduces to the unique solution modulo 2, which
is B. Every coefficient of B is 1. ∎

The same argument proves Hanna's parity conjecture for the sister entry A091713
(A(x) = x + x*A(A(A(x)))). That case was settled earlier by Yuan Chi (August 2026) and is listed under
independent-rediscovery; his note does not mention A120566.

## A326328: a(n) is 6 modulo 9 for every n >= 1

Entry: a(n) = (2n)! [x^(2n)] cosh(x)^(-3): 1, -3, 33, -723, 25953, ... "Apparently all terms except the
initial 1 have 3-valuation 1." (F. Chapoton, 25 November 2021)

*Proof.* Let sech x = sum E_n x^n/n! (E_0 = 1, E_2 = -1, E_4 = 5, E_6 = -61). From
(sech x)'' = sech x - 2 sech^3 x, a(n) = (E_(2n) - E_(2n+2))/2. Next, sech x = 2e^x/(e^(2x) + 1)
= e^x * sum_m (-u/2)^m with u = e^(2x) - 1, so

    E_n = sum_{m >= 0} (-1/2)^m D(m, n),     D(m, n) = sum_{j=0}^{m} (-1)^(m-j) binomial(m, j) (2j + 1)^n.

D(m, n) is n! times the coefficient of x^n in e^x (e^(2x) - 1)^m; it vanishes for m > n and is divisible by
2^m m! (expand (e^(2x) - 1)^m with Stirling numbers of the second kind). So the m-th term is an integer
multiple of m!, hence 0 modulo 9 for m >= 6, and

    E_n = sum_{m=0}^{5} (-1/2)^m D(m, n)   (mod 9)     for all n.

For n >= 2, each (2j + 1)^n modulo 9 is 0 if 3 divides 2j + 1 and otherwise has period 6 in n. So E_n
modulo 9 has period 6 for n >= 2, and E_(2n) modulo 9 has period 3 for n >= 1. From E_2, E_4, E_6 = -1, 5,
-61 the residues are 8, 5, 2, repeating. Every difference E_(2n) - E_(2n+2) is therefore 3 modulo 9, and
a(n) = 3/2 = 6 modulo 9 for all n >= 1. In particular the 3-adic valuation of a(n) is exactly 1. ∎

That Euler numbers are periodic modulo odd numbers is classical (D. E. Knuth and T. J. Buckholtz, 1967,
cited in A000364 for the moduli 3 and 5); the derivation above is included to keep the proof
self-contained. The step from there to A326328 is the identity a(n) = (E_(2n) - E_(2n+2))/2.

## A068206: every term is 7 modulo 21

Entry: n such that gcd(N(2n), D(2n-2)) = 7, where N and D are the numerator and denominator of the Bernoulli
number. "Conjecture: All terms are of the form 7 + 21*j." (Vaclav Kotesovec, 29 April 2014)

*Proof.* By the von Staudt-Clausen theorem, 7 divides D(2n-2) exactly when 6 divides 2n - 2, that is when
n is 1 modulo 3. Then 6 does not divide 2n, and Kummer's congruence for the prime 7 gives
B(2n)/(2n) = B(2)/2 = 1/12 modulo 7, a unit. So the exponent of 7 in N(2n) equals the exponent of 7 in n.
A term therefore has 7 | n and n = 1 modulo 3, which is n = 7 modulo 21. ∎

## A332937: a(p + 1) = 1 for every prime p > 3

Entry: gcd of the first two terms of row n of the Wythoff array. "If seems that for all primes p > 3,
a(1+p) = 1." (sic; Antti Karttunen, 15 January 2025)

*Proof.* Let phi be the golden ratio and m = floor(n phi) = n phi - e with 0 < e < 1. Then
m phi = m + n - e/phi, so the first term of row n is floor(m phi) = m + n - 1 and the second is
floor(m phi^2) = 2m + n - 1. Hence a(n) = gcd(m + n - 1, m) = gcd(n - 1, floor(n phi)). For n = p + 1 with
p >= 5, p < floor((p + 1) phi) < 2p, so p does not divide it and the gcd is 1. ∎

## One-line arguments

**A090818** (nonprime k with 3(3^k - 1)B(2k) an integer; "It appears that a(n) is never == 2 (mod 4)"). If
k = 2 modulo 4 then 4 | 2k, so 5 divides the denominator of B(2k) (von Staudt-Clausen), while 3^k = -1
modulo 5, so 5 does not divide 3(3^k - 1). ∎

**A048868** (numbers whose reduced residue system has more primes than nonprimes; "Conjecture: all terms are
even", Michael De Vlieger, 21 May 2017). For odd n >= 3 the map x -> n - x pairs the phi(n) residues and
changes parity, so phi(n)/2 of them are even. All of those except possibly 2 are nonprime, and so is 1. So
at least phi(n)/2 residues are nonprime. ∎

**A058059** (n with x^n + x + 2 irreducible over GF(3); "Apparently all terms are even", Joerg Arndt, 28
April 2012). For odd n, x = 2 is a root: 2^n + 4 = (-1)^n + 1 = 0 modulo 3, so x + 1 is a factor. (For
n = 1 the polynomial is 2x + 2 itself; the entry starts at n = 2.) ∎

**A130061** (k dividing 3^((k-1)/2) - 2^((k-1)/2) - 1; "It appears that all terms are composite except
a(1) = 1 and a(2) = 3"). For a prime p > 3, Euler's criterion makes both powers +1 or -1 modulo p, so the
expression is -3, -1 or 1 modulo p, never 0. ∎

**A131418** (n with digitsum(n) = digitsum(n + digitsum(n)); "Conjecture: all terms are divisible by 9",
Harvey P. Dale, 28 March 2019). A number is congruent to its digit sum modulo 9, so the condition gives
n = 2n modulo 9. ∎

**A134460** (first differences of A067186, the n with (n^2 + n + 2)/2 prime; "Except for the first term
a(1)=2, this sequence contains no terms of the form 4m+2"). (n^2 + n + 2)/2 is even for n = 1 or 2 modulo
4, so apart from n = 1 the terms of A067186 are 0 or 3 modulo 4, and two such numbers never differ by
2 modulo 4. ∎

**A328881** (a(n+3) = 2^n - a(n), a(0) = a(2) = 1, a(1) = 0; "It appears that, when odd, a(n) is never a
multiple of 5", Jean-François Alcover, 28 November 2019). Applying the recurrence four times,
a(n+12) = a(n) + 455 * 2^n, so a(n) modulo 10 has period 12 for n >= 1; the residues of a(1), ..., a(12)
are 0, 1, 0, 2, 3, 8, 4, 9, 6, 4, 7, 6, and a(0) = 1. No term ends in 5. ∎

**A348158** (sum of the distinct values of phi(d) over the divisors d of n; "Apparently, all the terms are
odd"). The value 1 occurs (d = 1) and every other value of phi is even. ∎

**A342681** (primes p with p + reverse(p) a palindromic prime; "It appears that all terms have an odd number
of digits", Robert Israel, 24 March 2021). With an even number L of digits, p + reverse(p) is the sum of
d_i (10^i + 10^(L-1-i)), and each 10^i + 10^(L-1-i) is a multiple of 11 because L - 1 - 2i is odd. So the
sum is a multiple of 11 larger than 11. ∎

**A300984** (numbers whose sum of squarefree divisors and sum of nonsquarefree divisors are both squarefree;
"Conjecture: a(n) is of the form a(n) = 2^i*p^j", verified by the author to 10^7). The sum of the squarefree
divisors is the product of (1 + p) over the primes p dividing n; two odd primes make it a multiple of 4. ∎

**A044279** (k such that 31 occurs in base 9 in k but not in k - 1; "Conjecture: the sum of the digits of
the terms of the sequence is always a multiple of 9 or 1 plus a multiple of 9", Harvey P. Dale, 25 May 2025).
The decimal digit sum is congruent to k modulo 9, which is the last base-9 digit of k. Going from k - 1 to k
changes a block "d 8...8" into "(d+1) 0...0". A new occurrence of 31 must use a changed digit and cannot
contain a 0, so d + 1 = 1, preceded by a 3. Then k ends in 1 (no trailing zeros) or in 0. ∎

**A037915** (a(n) = floor((3n + 4)/4); "It appears that a(n) = number of distinct values among
Floor(i^2 / n) for i = 0, 1, 2, ..., n", Samuel Vodovoz, 15 June 2015). True for n >= 2 and false for n = 1
(the values 0 and 1 make two, while a(1) = 1); with i = 1, ..., n it holds for all n >= 1. *Proof for
n >= 2:* consecutive values of i^2/n differ by (2i + 1)/n. While this is at most 1 the floors take every
integer value up to floor(t^2/n), where t = floor((n - 1)/2) + 1; afterwards the gap exceeds 1 and each of
the n - t further values of i gives a new floor. The count floor(t^2/n) + 1 + n - t equals
floor(3n/4) + 1 in each residue class of n modulo 4 (for n = 1 the first part gives one value more). ∎
This is a well-known type of exercise.

**A002791** (a(n) = sum of d^2 over divisors d <= 4 plus 4 times the sum of the divisors d > 4). Two
formulas are marked "Conjectured" (Sean A. Irvine, May 2014). Both follow from the definition, and the first
has a misprint. The sequence is the sum over d | n of b(d) with b = 1, 4, 9, 16, 20, 24, 28, ...
(b(d) = 4d for d >= 5), and sum b(d) x^d = (x + 2x^2 + 2x^3 + 2x^4 - 3x^5)/(1 - x)^2; the entry prints the
last term as -3x^4. And a(n) = 4 sigma(n) - 3 - 4[2 | n] - 3[3 | n], which is the second formula with
f = 10, 3, 7, 6, 7, 3 for n = 0, ..., 5 modulo 6. ∎

## Novelty check

Performed 2026-11-11 for every entry above: every page of its revision history with the discussion threads
(none of them contains a proof; the mirror copy used for the quotations is the current revision in every
case); the draft page (no pending edit); Google DeepMind's formal-conjectures file list; the conjecture
list of Epoch AI's OEIS Open benchmark; and the omega-institute project's issues and code, searched by
sequence number. S. Fried's "Further proofs of conjectures from the OEIS" (arXiv:2607.24832) was searched
for all the sequence numbers: none occurs. Zenodo's record search was run for every sequence number (it
finds the note on A091713, and nothing for the entries above). Web searches were run only for A120566, A326328, A068206, A332937,
A048868 and A300984; for the other entries no web search was made.

Ten further entries from the same batch (A091713, A008474, A254074, A000680, A088883, A088884, A014865,
A065907, A125855, A034496) turned out to be settled already and are listed on the page "Short proofs that
were already known" under independent-rediscovery. Two of them, A091713 and A065907, were caught only by
reading neighbouring entries (a Zenodo note linked from A141117; remarks in A065902 to A065906). The
entries named in the cross-references of A120566 and A332937 were read; those of A326328 and A068206 were
searched for remarks on these sequences; for the other entries only a quick scan of the comment lines of
adjacent sequence numbers was made, which is not exhaustive.

## Limits

Unrefereed. The proofs for A068206 and A090818 rely on the classical theorems named. The check of the two
functional equations goes to n = 40 only.
