# A218049: two new terms, a(6) = 5990500988 and a(7) = 20106639730

Status: **verified**, including minimality. No earlier record found (2026-11-11). Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A218049](https://oeis.org/A218049) (Michel Lagneau, Oct 19 2012; keywords hard, more): the smallest k
such that the n numbers k^2 + 1, (k+1)^2 + 1, ..., (k+n-1)^2 + 1 are each divisible by a square (larger
than 1). Listed terms for n = 1 to 5: 7, 117, 5742, 455356, 35952791, with "a(5) from Giovanni Resta,
Oct 21 2012". The data have not changed since 2012; the edits of January 2026 only reformat the example.

## Result

    a(6) = 5990500988
    a(7) = 20106639730

    5990500988^2+1 = 5 * 29^2 * 73 * 116906168739853
    5990500989^2+1 = 2 * 13^2 * 41 * 10645853 * 243245753
    5990500990^2+1 = 37 * 53^2 * 345281114864297
    5990500991^2+1 = 2 * 17^2 * 661 * 3461 * 27139096889
    5990500992^2+1 = 5 * 13 * 109^2 * 46468637236121
    5990500993^2+1 = 2 * 5^2 * 10729 * 66895520826049

    20106639730^2+1 = 13^2 * 113 * 1229 * 17225108320577
    20106639731^2+1 = 2 * 101^2 * 197 * 2366389 * 42506357
    20106639732^2+1 = 5^2 * 109 * 31013 * 4783752552569
    20106639733^2+1 = 2 * 5 * 29^2 * 881 * 54564111606049
    20106639734^2+1 = 17^2 * 61 * 89 * 257668487631697
    20106639735^2+1 = 2 * 409 * 433^2 * 977 * 2698083169
    20106639736^2+1 = 41^2 * 240497894987087537

The values just before and after each run are squarefree, so the runs have length exactly 6 and 7.

## Why the terms were out of reach, and the idea

The program in the entry factors k^2 + 1 for every k. A sieve needs no factoring: p^2 divides k^2 + 1
only for primes p = 1 mod 4, and then exactly for two residue classes of k modulo p^2. Marking those
classes for all p < 10^5 and looking for runs of marked k takes seconds per 10^10.

The sieve alone proves nothing about square factors p^2 with p >= 10^5. These are handled completely by
a second program that lists every k up to the bound with such a factor:

- for 10^5 <= p <= 10^8, the two roots of x^2 = -1 modulo p^2 (Tonelli-Shanks and one Hensel step);
- for p > 10^8, write k^2 + 1 = m p^2. Then m <= (k / 10^8)^2 is small and k^2 - m p^2 = -1, so k/p is a
  convergent of the continued fraction of sqrt(m) (Legendre's theorem, since 1 < sqrt(m)); all
  convergents with numerator up to the bound are listed for every non-square m (a square m gives no
  solution with k > 0).

Below 20106639740 there are 16720 such k. For each, the maximal run of consecutive non-squarefree values
through it was computed by exact factorisation: the longest has length 4.

## What is proved, and how

- *The two values satisfy the definition*: exact factorisations, `check.py`.
- *No smaller k does.* A run of n values that starts below the stated term either consists of k that are
  all marked by primes below 10^5, or contains a k with a square factor p^2, p >= 10^5.
  The first kind: the sieve (`search_sieve.py`, numba) finds its first run of 6 at 5990500988 and of 7 at
  20106639730, and reproduces a(1) to a(5) on the way. The second kind: none, by the list above
  (`search_large.py`).
- *Second implementation.* `search_second.py` (numpy; roots and factoring by sympy; no shared code)
  marks the same classes, then factors exactly every window of 6 consecutive k with at most one unmarked
  member (4820 windows). Up to 20106639731 it finds runs of 6 starting at 5990500988, 6312851589,
  7327934032, 9609773415, 12626645282, 17035061318, 18233931290, 18623636307, 20106639730 and
  20106639731, hence the same first run of 6 and the same first run of 7.

## Check

    python check.py                                      (under a minute)
    python search_sieve.py 2.02e10 7 1e5                 (about a minute; numba, python-flint)
    python search_large.py 1 20106639740 1e5 1e8 1 runs7
    python search_second.py 6 1 20106639732 1e5          (about eight minutes; numpy, sympy)

Outputs in `check.log`, `search_sieve.log`, `search_large.log`, `search_second.log`. `check.py` also
recomputes a(1) to a(4) from the definition.

## Limits

- The large-prime program is used by both arguments. It was compared with brute force on a small range
  (first lines of `search_large.log`: no pair missing), and its list for 10^5 <= p <= 10^8 can be
  rechecked value by value, but it is one program by one agent.
- python-flint was seen to return a repeated prime as two separate entries for some numbers above 2^64
  (for example 112297 twice in the factorisation of 6186303945^2 + 1). The programs merge equal primes,
  multiply the factors back and test each for primality before using a factorisation; an earlier version
  that did not was discarded and its runs repeated.
- a(8) was not determined. A run of the sieve alone (primes below 10^5) found no run of 8 below
  7.9 * 10^11; that is not a proved bound.

## Novelty check

Performed 2026-11-11: every page of the revision history of A218049 with its discussion threads (23
revisions; the two threads are from October 2012 and concern the wording) and the draft page (no pending
edit); the entry has no b-file; the cross-referenced entries A217798 and A218048 (lists of k with runs
of 2 and 3, far below these values); a search of the complete OEIS term dump for 5990500988, 5990500989
and 20106639730 (no sequence contains any of them); an in-depth web search for the A-number with
5990500988 (nothing); the file list of Google DeepMind's formal-conjectures and the local copy of the
Epoch AI "OEIS Open" list (A218049 is in neither); the omega-institute project's issues and code (no
mention).

## Credit

The sequence is due to Michel Lagneau; a(5) to Giovanni Resta (2012).
