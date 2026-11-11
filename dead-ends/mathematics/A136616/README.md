# A136616: no failure of Cantrell's harmonic-number formula below 10^10000

Status: **searched for and not found**. The formula is not proved either. Produced with AI assistance;
see the repository README. Not submitted to the OEIS.

## The entry

[A136616](https://oeis.org/A136616) (Rainer Rosenthal, Jan 13 2008): a(n) = largest m with
H(m) - H(n) <= 1, where H is the harmonic number. The entry gives, stated without qualification:

> a(n) = floor(e*n + (e-1)/2 + (e - 1/e)/(24*(n + 1/2))), after a suggestion by David Cantrell.

The companion entry A136617 calls the same expression "David Cantrell's heuristics". A103762 is the same
sequence shifted (A103762(n) = A136616(n-1) + 1), the sequence of E. R. Bobo (College Math. J. 26, 1995).

## Why it looked like a target

Formulas of the shape floor(c*n + d) for a sequence defined by a threshold have repeatedly turned out to
fail at an astronomically large n (see the pages on A072633, A332102 and A338857 in this repository). The
same analysis applies here. With N = n + 1/2, the real number M solving
digamma(M + 1/2) = 1 + digamma(N + 1/2) is

    M = e*N + (e - 1/e)/(24 N) + c3/N^3 + O(N^-5),
    c3 = e*((1 - e^-2)/(288 e^2) - 7(1 - e^-4)/960 + (1 - e^-2)^2/1152) = -0.0165891...

and a(n) = floor(M - 1/2). Cantrell's formula F(n) keeps the first two terms, so it is correct through
order 1/N, and it can fail only if an integer falls in a gap of width about 0.0166/N^3 just below
e*n + (e-1)/2 + (e - 1/e)/(24N). (The value of c3 was confirmed numerically: (M - eN - (e-1/e)/(24N)) * N^3
is -0.0165889 at N = 200.5 and -0.01658913 at N = 2000.5.)

Put q = 2n + 1 and beta = (e-1)/2 = [0; 1, 6, 10, 14, 18, ...]. A failure needs an integer r with

    kappa/2 - 0.1327/q^2  <  q*(r - q*beta)  <=  kappa/2,        kappa/2 = (e - 1/e)/12 = 0.195867.

Since kappa/2 < 1/2, r/q must equal a convergent R/S of beta lying above beta, possibly unreduced:
q = t*S, r = t*R, with t^2 * S*(R - S*beta) inside that window. For each convergent only the two integers
t next to sqrt((kappa/2) / (S*(R - S*beta))) can qualify, and q must be odd.

## Result

No failure.

- F(n) = a(n) for every n from 1 to 10^7 (direct, certified).
- For every convergent of (e-1)/2 with denominator below 10^10000 and both admissible multipliers t, the
  number n = (t*S - 1)/2 was tested directly with certified arithmetic: F(n) = a(n) in every case
  (475 candidates below 10^3000, 1384 below 10^10000).
- Nothing comes close. The quantity D = t^2 * S*(R - S*beta) - kappa/2 must be within about 0.13/q^2 of
  zero for a failure. The smallest |D| met among the candidates beyond the direct range is 7.8 * 10^-6,
  at a q of 5256 digits, where a failure would need |D| below about 10^-10512.

The smallest candidates are n = 35, 27133, 15586534, 15934198633, 25466579385586, ... . They come from
the same continued fraction as the "exceptional Bobo numbers" 36, 9045, 5195512, 5311399545,
8488859795196, 25466579385587 of S. J. Kifowit and his students (A277603; 35 + 1 and
25466579385586 + 1 are on that list). According to a comment in A103762 (Jon E. Schoenfield, 2018) those
are the n at which the simpler formula round(e*(n - 1/2)) is off by one; Cantrell's extra term
(e - 1/e)/(24(n + 1/2)) is what accounts for them.

## Why this is filed as a dead end

This search was looking for an unmarked formula that fails at a huge n. This one does not fail anywhere that
can be reached, and the reason is structural: the gap shrinks like 1/n^3, while continued-fraction
candidates of size q miss by a fixed amount, not by 1/q^2. A failure would require t^2 times
S*(R - S*beta) to agree with (e - 1/e)/12 to about 2*log10(q) digits, which amounts to e nearly satisfying
the quadratic equation (1 + 6 t^2 S^2) x^2 - 6 t^2 S (2R + S) x - 1 = 0 with an error far smaller than
general transcendence measures for e exclude. We found no way to rule that out for all (S, t), so the
formula remains unproved: true for n <= 10^7, without counterexample among all continued-fraction
candidates below 10^10000, and heuristically true for all n.

## Check

    python check.py                    (about 20 s: direct to 10^6, candidates below 10^3000)
    python check.py 10000000 10000     (the run reported above; output in check_large.log)

Part 1 certifies a(n) with Arb ball arithmetic by deciding the signs of
digamma(m+1) - digamma(n+1) - 1 at m = F(n) and m = F(n) + 1. Part 2 enumerates the convergents and tests
each candidate the same way at a precision of four times the size of q. Part 3 repeats n <= 20000 and
the candidates below 10^60 with mpmath. Needs python-flint and mpmath.

## Limits

- The statement "a failure beyond the direct range must be one of the enumerated candidates" rests on the
  expansion above, in particular on e*N < M <= e*N + (e - 1/e)/(24N) for N > 10^7. This follows from the
  standard two-sided bounds for digamma(x + 1/2) - log(x); that derivation was done by hand and is not
  machine-checked here.
- Nothing is claimed beyond q = 2n + 1 < 10^10000.
- Kifowit, Mitchell and Zandi's work on exceptional Bobo numbers was announced in 2016 as "in
  preparation". Only Kifowit's preprint "Bobo Numbers, Bobbers, and Bears" (2016) was read; the article of
  Clancy and Kifowit (College Math. J. 45, 2014) was not. Whether either proves Cantrell's formula was not
  established.

## Novelty check

Done 2026-11-11: both pages of the revision history of A136616 (the formula was added on Mar 06 2020 by
Jinyuan Wang; there is no discussion of its status) and the draft page (no pending edit); the entries
A136617, A103762, A277603; Kifowit's 2016 preprint; a web search on Bobo's sequence. No proof and no
counterexample of the formula was found.
