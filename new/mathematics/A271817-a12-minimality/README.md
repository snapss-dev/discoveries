# A271817: the gap in a(12) = 17546197568 is closed

Status: **supplement to the existing page `new/mathematics/A271817`** (not a new finding of its own). That
page gives a(12) = 17546197568 "verified up to a small stated gap". The gap is now closed: a(12) is
verified, including minimality. Checked 2026-11-11. Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry and the open point

[A271817](https://oeis.org/A271817): the smallest k > 1 such that none of k^2, k^2 + 1, ..., k^2 + n is
squarefree. The existing page reports a(10) = a(11) = 2352655113 (minimality proved) and
a(12) = 17546197568 with this limit: "The search used primes below 10^6 and factored exactly every k
with at most two values left unexplained. A k with three or more values whose only square factors exceed
10^12 was not excluded".

## Result

There is no k with 1 < k < 17546197568 for which k^2, ..., k^2 + 12 all have a square factor. So

    a(12) = 17546197568

without the proviso.

## How

The two programs written for the mirror entry A270442 (k^2 - j; see that page) take the sign as a
parameter.

- `search_sieve.py` (primes below 10^5): the first k with all thirteen values marked is 17546197568. On
  the way it reproduces the ten listed terms and a(10) = a(11) = 2352655113.
- `search_large.py`: the complete list of k <= 17546197567 for which some k^2 + j, 1 <= j <= 12, is
  divisible by p^2 with p >= 10^5. For 10^5 <= p <= 2 * 10^8 the roots of x^2 = -j modulo p^2; for
  p > 2 * 10^8 the equation k^2 + j = m p^2 with m <= 7697, solved through the convergents of sqrt(m)
  for m > 144 (Legendre, since then j <= 12 < sqrt(m)) and through fundamental solutions inside Nagell's
  bounds for m <= 144. The list has 170864 values of k. Each was tested exactly from the definition:
  none qualifies.

Every k below 17546197568 is of one of the two kinds, so none qualifies.

## Check

    python check.py                                      (seconds)
    python search_sieve.py 1 1.76e10 12 1e5 1            (several minutes; numba, python-flint)
    python search_large.py 1 17546197567 1e5 2e8 12      (three minutes)

Outputs in `check.log`, `search_sieve.log`, `search_large.log`.

## Limits

- The sieve here is a new implementation, independent of the one behind the existing page, and gives the
  same thirteen terms. The large-prime program exists once; it was compared with brute force on a small
  range (first lines of `search_large.log`).
- Same remark on python-flint factorisations as on the A270442 page (equal primes are merged, products
  and primality are checked).

## Novelty check

As on the existing page (history, draft, term dump, web search, all 2026-11-11); in addition the local
term dump still shows the entry ending at a(9) = 93499279.

## Credit

The term a(12) and the sieve were found by an earlier agent of this project; this supplement only
removes the proviso.
