# A320065: the Lambert W formula first fails at n = 3431, then at the end of every block

Status: **verified** (two independent implementations, one with certified ball arithmetic); no earlier
record found (2026-11-11). Produced with AI assistance; see the repository README. Not submitted to the
OEIS.

## The entry

[A320065](https://oeis.org/A320065) (David Lewis, Oct 22 2018): a(n) is the smallest integer i such that
binomial(2i, i) > n. So a(n) = i for binomial(2i-2, i-1) <= n < binomial(2i, i).

The entry gives this formula, stated without qualification:

> For n>1, a(n) = ceiling((-LambertW(-1, -4*log(2)/(Pi*n^2)) / (4*log(2))) * (1 + 2*log(2)/(3*log(2) +
> (2 + log(2))*LambertW(-1, -4*log(2)/(Pi*n^2)) + 2*LambertW(-1, -4*log(2)/(Pi*n^2))^2))).
> - Ryan Jean and Vaclav Kotesovec, Jan 04 2025

The discussion thread of that date records how it was obtained (one Newton step applied to
4^x * (1/sqrt(Pi x) - 1/(8 sqrt(Pi) x^(3/2))) = n) and that it was compared with the sequence for
n <= 1000. The Mathematica line in the entry checks n <= 100.

## Result

Write g(n) for the expression inside the ceiling.

- **The first failure is n = 3431 = binomial(14, 7) - 1**: a(3431) = 7 and the formula gives 8.
- The next failures are n = 12867, 12868, 12869 (a = 8, formula 9), n = 48611, ..., 48619 (a = 9,
  formula 10) and n = 184726, ..., 184755 (a = 10, formula 11). These 43 values are all the failures
  below 200000.
- For every i from 7 to 400 the formula is wrong at n = binomial(2i, i) - 1, the last n of the block where
  a(n) = i: it gives i + 1. The number of wrong values at the end of each block grows quickly: 1, 3, 9, 30,
  95, 305, 996, 3306, 11112, ... for i = 7, 8, 9, ..., and is 5511115 for i = 20. As a fraction of the
  block it shrinks slowly (4 * 10^-4 at i = 7, 5 * 10^-5 at i = 20).
- At n = binomial(2i, i) itself the formula is right for every i from 2 to 400.

## Why

g is a smooth increasing approximation to the inverse of i -> binomial(2i, i). For the ceiling to be exact
at both ends of a block one needs

    i < g(binomial(2i, i))    and    g(binomial(2i, i) - 1) <= i.

Near C = binomial(2i, i) the function g has slope about 1/(C log 4), so the two conditions leave a window
of width about 1/(C log 4), which shrinks like 4^-i, for the error g(C) - i. The error of the
approximation shrinks only like a power of i: numerically i^2 * (g(C) - i) decreases from 0.0127 at
i = 7 to 0.0113 at i = 400. (A limit of 1/(64 log 4) = 0.01127 would correspond to the first omitted term
of the Stirling series; this identification is an observation, not derived here.) From i = 7 on the error
is larger than the window, and it stays positive, so the formula overshoots on a final stretch of about
(g(C) - i) * C * log 4 values of n in each block.

No formula of this type, with finitely many correction terms, can be exact for all n; the true inverse
at the points n = binomial(2i, i) would be needed to within 4^-i.

## Check

    python check.py            (about 1 minute; needs mpmath and python-flint)
    python check.py NSCAN IMAX (defaults 200000 and 400)

- Part 1 compares the formula (mpmath, 30 digits) with the definition for every n from 2 to NSCAN and
  lists every failure.
- Part 2 evaluates g at binomial(2i, i) - 1 and at binomial(2i, i) with Arb ball arithmetic (its own
  Lambert W code) for 2 <= i <= IMAX and decides the signs of g - i rigorously.
- Part 3 finds, by bisection with Arb, the first failing n of each block for 7 <= i <= 20.

The output is in `check.log`.

## Limits

- "Every block from i = 7 on" is verified for i <= 400 only. For larger i it rests on the error staying
  positive and of order 1/i^2, which is observed, not proved.
- The scan of all n covers n < 200000; beyond that only the ends of the blocks were examined.
- The first formula of the entry, a(n) = log(n)/log(4) + log(log(n))/log(16) + O(1), is not affected.

## Novelty check

Done 2026-11-11: all five pages of the revision history of A320065 with every discussion thread (the
thread of Jan 04 2025 reports agreement for n <= 1000 and nothing beyond); the draft page (no pending
edit); the cross-referenced entry A000984, whose inverse formula (D. W. Cantrell, 2007) applies only at
the central binomial coefficients themselves and was found correct here for n < 3000; an in-depth web
search with the A-number, "LambertW" and 3431; the file list of Google DeepMind's formal-conjectures;
the conjecture list of Epoch AI's OEIS Open; and an issue and code search of the omega-institute
project. None mentions a failure.
