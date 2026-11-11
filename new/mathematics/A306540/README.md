# A306540: a(n) <= 231 for every n, and 231 is attained

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry

[A306540](https://oeis.org/A306540) (Robert Israel, 22 February 2019): a(n) is the least k >= 1 such that
the decimal expansion of n^k starts with 99 or 100. Digits after the decimal point are allowed, so
a(1) = a(10) = 1. The entry says: "a(n) always exists and is bounded: see proof at A217157" and
"Conjecture: a(n) <= 231." The table of terms covers n <= 10000.

The proof linked from A217157 (Robert Israel, 21 February 2019) uses compactness of an interval and gives
no explicit bound.

## Result

The conjecture is true: a(n) <= 231 for every n >= 1. The bound is attained: a(101) = 231, and likewise
a(101 * 10^j) = 231 for every j >= 0.

## Proof

Write x = log10(n) and let {y} be the fractional part of y. The leading digits of n^k are 99 or 100
exactly when the mantissa of n^k lies in [9.9, 10) or in [1, 1.01), that is, when

    {k x} >= log10(9.9) = 0.99563519...     or     {k x} < log10(1.01) = 0.00432137... .

(This is the test in the entry's Maple program.) So k works whenever k x is within distance
d = 0.0043213 of an integer on either side, because 1 - log10(9.9) = 0.0043648... is larger than d.

*Dirichlet's approximation theorem, in the form with Q + 1:* for every real x and every integer Q >= 1
there is an integer k with 1 <= k <= Q such that k x is within 1/(Q + 1) of an integer. (Place the Q + 2
numbers 0, {x}, {2x}, ..., {Qx}, 1 in [0, 1]. They cut it into Q + 1 intervals, so two of the numbers that
are neighbours in size differ by at most 1/(Q + 1). If the two are {ix} and {jx} with i < j, take
k = j - i; if one of them is 0 or 1, take k to be the index of the other.)

Take Q = 231. Then some k <= 231 has k x within 1/232 = 0.0043103... of an integer, and

    1/232 < log10(1.01)        (equivalently 1.01^232 = 10.058... > 10),
    1/232 < 1 - log10(9.9)     (equivalently 9.9^232 < 10^231).

If the nearest integer is below or equal to k x, then {k x} <= 1/232 < log10(1.01) and n^k starts with
100. If it is above, then {k x} >= 1 - 1/232 > log10(9.9) and n^k starts with 99. Either way
a(n) <= k <= 231. ∎

*Sharpness.* For n = 101, x = 2 + log10(1.01). For k = 1 the mantissa is exactly 1.01, which does not
start with 100. For 2 <= k <= 230, {k x} = k log10(1.01) lies between 0.0086 and 0.99392, outside both
windows, because 1.01^231 < 10. For k = 231, {k x} = 0.998237... >= log10(9.9). So a(101) = 231. The
same computation applies to 101 * 10^j.

The argument also shows why the conjectured constant is 231: it is the least Q with 1/(Q + 1) < log10(1.01),
that is, the least Q with 1.01^(Q+1) > 10.

## Check

    python check.py

- certifies the four inequalities used above, with interval arithmetic (python-flint) and again with
  integers only (101^232 > 10 * 100^232, 101^231 < 10 * 100^231, 99^232 < 10^463);
- method 1: computes a(n) for n <= 30000 with exact integer powers; reproduces the 69 published terms;
  the maximum is 231, attained at 101, 1010 and 10100;
- method 2: computes a(n) for n <= 20,000,000 from fractional parts of k log10(n) in floating point,
  re-deciding with exact integers every case within 10^-9 of a window edge (35 cases); the maximum is 231,
  attained for 411 values of n; methods 1 and 2 agree on all n <= 30000.

Output in `check.log` (about 90 seconds).

## Limits

The proof is elementary and complete, but unrefereed. The values of n other than 101 * 10^j for which
a(n) = 231 were counted, not characterised.

## Novelty check

Performed 2026-11-11:

- both pages of the revision history of A306540 (revisions 1 to 15, the last in March 2019), which have no
  discussion threads, and the draft page (no pending edit);
- the cross-referenced entry A217157 and the proof file attached to it (read in full: a compactness
  argument, no explicit constant). The history shows the reference was first written as A324295 and then
  corrected to A217157; the present A324295 is an unrelated sequence. No other entry numbered A306000 to
  A307999 mentions A306540;
- an in-depth web search for the sequence number with "starts with 99 or 100" and the bound 231, and
  Zenodo's record search for the sequence number;
- Google DeepMind's formal-conjectures file list, the conjecture list of Epoch AI's OEIS Open benchmark, and
  the issues and code of the omega-institute project: no mention.

No proof of the bound was found. The ingredients are standard, so it may well be known to the entry's
author; it is not recorded.
