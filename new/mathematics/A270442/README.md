# A270442: a new term, a(11) = 25812395459

Status: **verified**, including minimality. No earlier record found (2026-11-11). Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A270442](https://oeis.org/A270442) (Juri-Stepan Gerasimov, Apr 09 2016; keyword more): the smallest
k > 1 such that none of k^2 - 0, k^2 - 1, k^2 - 2, ..., k^2 - n is squarefree. Listed terms for n = 0 to
10: 2, 3, 10, 941, 3052, 8173, 35359, 1526009, 30167284, 46952141, 574236841, with "a(10) from Giovanni
Resta, Oct 29 2018". The last edit (January 2021) added a Mathematica program with the remark "The
program will take a long time to run". This is the mirror image of A271817 (k^2 + j), for which this
repository already has three new terms.

## Result

    a(11) = 25812395459.

k = 25812395459 is prime, and k^2 - j for j = 1, ..., 11 is divisible by the squares of
2 and 3, 7, 131, 41, 2, 5, 53, 23, 2, 3, 43 in that order:

    k^2 -  1 = 2^3 * 3^2 * 5 * 29 * 31 * 14356171 * 143402197
    k^2 -  2 = 7^2 * 41826721 * 325092328151
    k^2 -  3 = 2 * 131^2 * 997 * 19471027713167
    k^2 -  4 = 3 * 41^2 * 79 * 359 * 1039 * 14779 * 303379
    k^2 -  5 = 2^2 * 11 * 15142721802995541379
    k^2 -  6 = 5^2 * 2922653 * 9118834967159
    k^2 -  7 = 2 * 3 * 19 * 53^2 * 359243 * 5791775443
    k^2 -  8 = 23^2 * 10399 * 121118189409263
    k^2 -  9 = 2^7 * 7 * 877 * 6827 * 59077 * 2102329
    k^2 - 10 = 3^2 * 13 * 37 * 10601 * 523351 * 27741449
    k^2 - 11 = 2 * 5 * 43^2 * 1433 * 25146266774851

k^2 - 12 = 128483 * 5185742544397343 is squarefree, so a(12) > a(11).

## The idea

Brute force factors k^2 - j for every k. Instead, for each prime p and each j, the k with p^2 | k^2 - j
form at most two residue classes modulo p^2 (for odd p not dividing j), so a sieve over k can mark, for
all p < 10^5 at once, which of the twelve values have a square factor. The first k with all twelve
marked is 25812395459.

That leaves the k for which some k^2 - j has a square factor p^2 only with p >= 10^5. A second program
lists all of them below the candidate:

- for 10^5 <= p <= 2 * 10^8: the roots of x^2 = j modulo p^2 (Tonelli-Shanks, one Hensel step);
- for p > 2 * 10^8: write k^2 - j = m p^2, so m <= 16657 and (k, p) solves x^2 - m y^2 = j. A square m
  gives nothing in range. For m > 121, j < sqrt(m), so x/y in lowest terms is a convergent of sqrt(m)
  (Legendre); all convergents with numerator up to the bound are listed. For m <= 121 all solutions are
  generated from the fundamental ones, found inside Nagell's bounds, by powers of the fundamental unit.

This gives 205929 values of k. Each was tested exactly from the definition: none qualifies.

## What is proved, and how

- *25812395459 satisfies the definition for n = 11*: the factorisations above (`check.py`).
- *No smaller k does.* A smaller k would either have all of k^2 - 1, ..., k^2 - 11 divisible by squares
  of primes below 10^5, and the sieve (`search_sieve.py`, numba) shows the first such k is 25812395459
  while reproducing all eleven listed terms; or it would be one of the 205929 values of
  `search_large.py`, all excluded.
- *Second argument with another sieve.* `search_second.py` (numpy; roots and factoring by sympy; no code
  shared with the first sieve) uses primes below 2 * 10^4 and tests exactly every k with at most one of
  the eleven values unexplained: 397 values of k, and the only one that qualifies is 25812395459. The
  large-prime program run from 2 * 10^4 lists 1558638 values of k, none of which qualifies. Together
  these again cover every k below the term.

## Check

    python check.py                                         (seconds)
    python search_sieve.py -1 2.6e10 11 1e5 1               (several minutes; numba, python-flint)
    python search_large.py -1 25812395458 1e5 2e8 11        (two minutes)
    python search_second.py 11 2 25812395460 2e4            (about fifteen minutes; numpy, sympy)
    python search_large.py -1 25812395458 2e4 2e8 11        (ten minutes)

Outputs in `check.log`, `search_sieve.log`, `search_large.log`, `search_second.log` (the second sieve
was run in three ranges). `check.py` recomputes a(0) to a(5) from the definition.

## Limits

- The large-prime program is common to both arguments. It was compared with brute force on small ranges
  for this sign and for k^2 + j (first lines of `search_large.log`: nothing missing), but it is one
  program by one agent, and nobody else has repeated the search.
- python-flint was seen to return a repeated prime as two separate entries for some numbers above 2^64.
  The programs merge equal primes, multiply the factors back and test each for primality before using a
  factorisation; the large-prime runs were repeated after this was fixed.
- Following the entry, 0 would count as not squarefree and negative values by their absolute value; this
  plays no role for k > 3.
- a(12) was not determined. The sieve with primes below 10^5 found no k with all thirteen values marked
  below 2.8 * 10^10; that is not a proved bound.

## Novelty check

Performed 2026-11-11: every page of the revision history of A270442 with its discussion threads (56
revisions, 2016 to 2021; the threads concern the offset, the wording and the bound a(9) < 10^8, and two
from March and April 2016 are about counts of primes by residue class, unrelated to this definition) and the
draft page (no pending edit); the entry has no b-file; the cross-referenced entry A271817 and this
repository's page on it; a search of the complete OEIS term dump for 25812395459 (no sequence contains
it); an in-depth web search for the A-number with 25812395459 (only the entry itself, without the
value); the file list of Google DeepMind's formal-conjectures and the local copy of the Epoch AI "OEIS
Open" list (A270442 is in neither); the omega-institute project's issues and code (no mention).

## Credit

The sequence is due to Juri-Stepan Gerasimov; a(8) to Michel Marcus, a(9) to Seiichi Manyama, a(10) to
Giovanni Resta. The sieve for the companion entry A271817 was set up by an earlier agent of this project;
the treatment of large primes through Pell equations is new here.
