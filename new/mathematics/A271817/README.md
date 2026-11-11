# A271817: three new terms

Status: a(10) and a(11) **verified**; a(12) verified up to a small stated gap. No earlier record found
(2026-11-11). Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A271817](https://oeis.org/A271817): the smallest k > 1 such that none of k^2, k^2 + 1, ..., k^2 + n is
squarefree. Listed terms: 2, 7, 32, 41, 239, 13982, 240761, 240761, 26220368, 93499279 (n = 0 to 9), with
the remark "a(10) > 1.2*10^8" (Giovanni Resta, 2016). The entry has not changed since 2016.

## Result

    a(10) = a(11) = 2352655113
    a(12) = 17546197568        (see the limit below)

For k = 2352655113 the numbers k^2 + j, j = 0, ..., 11, are divisible by the squares of
3, 17, 19, 2, 13, 7, 5, 2, 11, 3, 23, 2 in that order, and k^2 + 12 is squarefree. For k = 17546197568 the
numbers k^2 + j, j = 0, ..., 12, are divisible by the squares of 2, 5, 3, 421, 2, 7, 31, 11, 2, 17, 59, 3, 2,
and k^2 + 13 is squarefree.

## How minimality was established

By the agent that found the terms, with two programs: a sieve over k that marks every k^2 + j divisible
by p^2 for all primes p < 10^5 and factors exactly any k left with a single unexplained value (it
reproduces all ten listed terms); and a separate program that enumerates every k below the candidate for
which some k^2 + j is divisible by p^2 with p >= 10^5, each of which was then factored in full. None gives
a smaller k.

## Check

    python check.py

factors every value for both k and reproduces the listed terms for n <= 5 by brute force from the
definition. Output in `check.log`. It does not repeat the minimality search.

## Limits

- **a(12).** The search used primes below 10^6 and factored exactly every k with at most two values left
  unexplained. A k with three or more values whose only square factors exceed 10^12 was not excluded;
  such a k is expected about once in 10^8 searches of this size.
- Minimality for a(10) rests on two programs by the same agent and has not been repeated independently.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads (14 revisions, the
last in 2016); the draft page (no pending edit); the cross-referenced entries; a search of the complete
OEIS term dump for 2352655113 and 17546197568 (no sequence contains either); an in-depth web search; and
the omega-institute project's issues.
