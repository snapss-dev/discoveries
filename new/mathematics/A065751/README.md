# A065751: the empirical generating function fails at the first six-digit term

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry

[A065751](https://oeis.org/A065751) (Reinhard Zumkeller, 2001): numbers whose decimal digits consist of
nested and/or concatenated ordered pairs 0-9, 1-8, 2-7, 3-6 and 4-5. Reading 0, 1, 2, 3, 4 as five kinds
of opening bracket and 9, 8, 7, 6, 5 as the matching closing brackets, the terms are the well-formed
bracket words that do not begin with 0. The entry lists 43 terms, a(0) = 18 to a(42) = 4536, and the
formula

"Empirical g.f.: -9*(100*x^19 + x^15 + 50*x^14 - 10*x^13 - 10*x^12 - 10*x^11 - 9*x^10 - 156*x^9 - 11*x^8
- 11*x^7 - 11*x^6 - 12*x^5 - 117*x^4 - x^3 - x^2 - x - 2) / ((x - 1)^2 * (x + 1)^2 *
(x^4 - x^3 + x^2 - x + 1)^2 * (x^4 + x^3 + x^2 + x + 1))." (Colin Barker, 29 March 2013)

## Result

The generating function reproduces a(0), ..., a(43) and is wrong from n = 44 on:

    n            43     44      45      46
    g.f.       4545   5094    5184    5274
    true a(n)  4545 100998  101898  102798

The value 5094 is not a term at all: it begins with 5, a closing digit.

## Why

The number of terms with 2m digits is 4 * 5^(m-1) * Catalan(m): 4, 40, 500, 7000, 105000, ... (the first
bracket is one of four kinds, the other m - 1 pairs are free). There are 44 terms with two or four digits,
and the formula fits exactly those. A rational function with that denominator has coefficients that grow
at most linearly along each residue class of n modulo 10, while the true terms jump by a factor of about
100 each time the length increases and the lengths' populations grow geometrically, so no formula of this
shape can hold.

## Check

    python check.py

- method 1: a stack parser applied to every integer below 10^8 finds 7544 terms;
- method 2: the bracket words with 1 to 5 pairs generated from the grammar; the terms below 10^8 are the
  same 7544 numbers, and the counts by length are 4, 40, 500, 7000, 105000;
- the 43 published terms are reproduced;
- the generating function is expanded with exact rational arithmetic and compared: first disagreement at
  n = 44 (5094 against 100998).

Output in `check.log` (under half a minute).

## Limits

This is a correction of an extrapolation from 43 terms, not new mathematics. The "Why" paragraph is an
explanation, not a proof that no rational generating function exists; the failure at n = 44 is exact.

## Novelty check

Performed 2026-11-11:

- both pages of the revision history (revisions 1 to 11, the last in June 2025), which have no discussion
  threads; the draft page (no pending edit). The formula has stood unchanged since 2013;
- A065752 (the squares in the sequence), the only entry it refers to apart from the digital root: no remark
  on the formula;
- an in-depth web search with the sequence number, the formula's author and the value 100998, and Zenodo's
  record search for the sequence number: nothing;
- Google DeepMind's formal-conjectures file list, Epoch AI's OEIS Open list and the omega-institute
  project: no mention.

## Credit

A sister case with the same cause (a formula fitted to the terms below a digit-length boundary) is on the
page for A044140 in this repository.
