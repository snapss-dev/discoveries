# Five OEIS constants whose program line computes a different number

Status: **verified**, **new?** (2026-11-11). Errata in program lines; the listed digits are correct.
Produced with AI assistance; see the repository README. Not submitted to the OEIS.

In each of these entries the DATA line agrees with the constant in the name, but a program printed in
the entry does not produce it.

| entry | constant (name) | program line | what the line gives |
|---|---|---|---|
| [A036665](https://oeis.org/A036665) | 1/9801980198019801 | PARI: `1/9801980198019800.` | 1/9801980198019800; agrees with the constant for 16 significant digits |
| [A134877](https://oeis.org/A134877) | Sum_{k>=1} 1/(k!!)^(k!!) = 1.28703709... | Mathematica: `Sum[1/n^n, {n, 1, 100}]` | Sum 1/n^n = 1.29128599... |
| [A194657](https://oeis.org/A194657) | (4 Pi^6 log 2 - 90 Pi^4 zeta(3) + 1350 Pi^2 zeta(5) - 5715 zeta(7))/1536 = 0.11757583... | Mathematica: `... - 5715 Pi^2*Zeta[7]` | -33.159125..., because of an extra factor Pi^2 |
| [A221363](https://oeis.org/A221363) | the Pythagorean comma 531441/524288 = 1.0136432647705078125 | Mathematica: `31441/524288` | 0.0599689..., the leading 5 of the numerator is missing |
| [A238273](https://oeis.org/A238273) | Sum_{n>=1} mu(n)/n^n | PARI: `suminf(n=1, moebius(n)/n^n)` | the sum of the first 47 terms; right for 86 digits only, at any precision |

## The instructive one: A238273

PARI's `suminf` stops as soon as three consecutive terms are negligible. Here the terms are
mu(n)/n^n, and mu(48) = mu(49) = mu(50) = 0 because 48, 49 and 50 are divisible by 16, 49 and 25: the
first run of three consecutive integers that are not squarefree. The summation therefore ends at
n = 47 whatever the working precision, and the first term it never sees is 1/51^51 = 8.2 * 10^-88.
`pari_check.log` shows that `suminf(n=1, moebius(n)/n^n)` at 150 digits equals the sum up to n = 47
digit for digit and differs from the true sum from the 87th digit on. The line was added on
Apr 09 2026 (Charles R Greathouse IV); at the default precision of 38 digits its output is correct,
so the defect shows only when someone asks for more digits than 86.

## The other four

- A036665 (PARI line, Charles R Greathouse IV, Aug 17 2026): the last digit of the denominator is 0
  instead of 1. The Mathematica line of the same entry has the right denominator.
- A134877 (entry by Artur Jasinski, Nov 14 2007): the Mathematica line sums 1/n^n, which is the
  constant of A073009, not 1/(n!!)^(n!!).
- A194657 (entry by Seiichi Kirikami, Sep 01 2011): the last term of the Mathematica line carries a factor Pi^2
  that the name and the data do not have.
- A221363 (entry by Jonathan Sondow, Jan 19 2013): the Mathematica line has 31441 for 531441.

## Check

    python check.py

evaluates the constant in each name and the expression in each program line, with exact rational
arithmetic where the number is rational or the series converges fast enough to bound the tail
(A036665, A134877, A221363, A238273), and with mpmath and Arb balls for A194657, and counts how many
of the listed digits each reproduces. Output in `check.log`. `pari_check.gp` and `pari_check.log` show
the behaviour of `suminf` in PARI/GP 2.17.4. Mathematica was not available; the Mathematica lines were
read, not run.

## Limits

These were noticed as a by-product of a screen of about 14500 constant entries for wrong digits (see the
page "A261114 and A333507"). The screen compares programs with data, so it finds a wrong program only
when a second route to the constant exists; it is not a complete audit of program lines.

## Novelty check

Performed 2026-11-11.

- Live entries re-fetched from oeis.org: all five still show the program lines quoted above (A036665
  revision #15, A134877 #11, A194657 #18, A221363 #28, A238273 #18).
- Every page of the five revision histories with their discussion threads, and the five draft pages (no
  pending edit). A036665: 15 revisions, no thread. A134877: 11 revisions, one thread (2013) about where
  to print the value. A194657: 18 revisions; the author corrected the name and the Mathematica line
  several times on Sep 01 2011 (5717 to 5715, the missing division by 1536), and the extra Pi^2 stayed.
  A221363: 28 revisions, threads about trailing zeros and keywords (2013). A238273: 18 revisions, one
  thread ("OK?", 2014). None mentions the program lines discussed here.
- Google DeepMind formal-conjectures file list, Epoch AI's OEIS Open list, and the omega-institute
  project (issue and code search): no mention of any of the five.
- No web search was made for these five entries.
