# Adjacent digits differing by d or less: 29 conjectured generating functions, already proved by others

Status: **verified**, and **found earlier by others** (checked 2026-11-11). Produced with AI assistance; see
the repository README. Nothing here is new except that the finite verification is carried out and
recorded for each of the 29 entries.

## The entries

R. H. Hardin's family "Number of base b (circular) n-digit numbers with adjacent digits differing by d or
less" (2006) has several hundred OEIS entries. In 29 of them, between A124698 and A126531, the formula
section still reads "Conjectures from Colin Barker" or "Empirical G.f." (2012 to 2017), for example

- A124698 (base 5, circular, d = 1): "G.f.: (1 - 6*x^2 - 4*x^3 + 12*x^4) / ((1 - x)*(1 - 2*x)*(1 - 2*x - 2*x^2))";
- A126531 (base 10, d = 5): "G.f.: (1 - x)*(1 + 3*x - x^3) / ((1 + x)*(1 - 9*x + 6*x^2 + 3*x^3 - 2*x^4))".

The full list, with the formulas as published, is in `conjectures.json`.

## Result

All 29 generating functions are correct, together with the recurrences and the seven closed forms
a(n) = 1 + alpha^n + beta^n that accompany them.

## Who had it first

- **Rafał Wiktorowicz, August 2026**: "Proofs of the conjectured recurrences and generating functions for
  the adjacent-digits family", a five-page note attached to the neighbouring entry A126371 and linked from
  28 of the 29 entries (and from several hundred others in the family) since 10 August 2026. It gives the
  argument below once for the whole family, with two worked examples (A126371 and A125327), and describes
  the finite verification so that it can be repeated for any entry.
- **Robert Israel, 23 January 2018**, in A126474, the 29th entry: "a(n) = e^T M^(n-1) e ... The fact that
  (M^3-5*M^2-M+2I) e = 0 implies Colin Barker's recursion, and the G.f. follows." He did the same for A126360
  and A126362 on 12 August 2019.
- The OEIS Wiki page for the circular family states the transfer-matrix principle.

## The argument

Let M be the b x b matrix with M(i, j) = 1 when |i - j| <= d and 0 otherwise. Words with leading zeros
allowed are walks, so for n >= 1 the linear count is the sum of all entries of M^(n-1) and the circular
count is trace(M^n); a(0) = 1 by the entries' convention. By the Cayley-Hamilton theorem both sequences
satisfy, for n >= 1, the recurrence of order b given by the characteristic polynomial of M. The
coefficients g(n) of a rational function P/Q with Q(0) = 1 or -1 satisfy the recurrence given by Q from
n = deg P + 1 on. The difference a(n) - g(n) therefore satisfies a recurrence of order b + deg Q from
n = deg P + 1 on, and vanishes identically as soon as it vanishes for 0 <= n <= deg P + b + deg Q.

## How the earlier work was missed

The first pass judged novelty from the formula lines, which still say "Conjectures". The proof is in a
link line of each entry, pointing to a file stored under a different sequence number. The second pass
found it only when it listed the link lines of the entries, after the proof had been re-derived.

## Check

    python check.py

For each of the 29 entries: builds M; compares the matrix formula with brute-force enumeration of digit
strings (all n with b^n <= 300,000); compares with every published term; expands the published generating
function with exact integers and compares it with the matrix sequence for 0 <= n <= 60, which exceeds
deg P + b + deg Q + 1 in every case (the largest requirement is 28); and tests the published recurrences
and closed forms on the same range. Output in `check.log` (seconds).

## Limits

Only the 29 entries whose formulas are worded as conjectures were treated. Many other entries of the
family carry generating functions by the same author without that wording; they were not examined. The
order of the recurrences is not shown to be minimal here (the note by Wiktorowicz discusses minimality).

## Novelty check

Performed 2026-11-11: both pages of the revision history of each of the 29 entries (the link to the 2026
note appears in a revision of 10 August 2026 in 28 of them; A126474 has Israel's remark instead); the
draft pages (no pending edits); the note itself, read in full.
