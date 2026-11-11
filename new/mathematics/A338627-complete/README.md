# A338627 is complete: there is no a(8)

Status: **proved** (elementary), checked numerically to 3 * 10^6. No earlier record found (2026-11-11).
Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A338627](https://oeis.org/A338627) (Ilya Gutkovskiy, Nov 04 2020; keywords nonn, more): a(n) is the
smallest positive number k such that n consecutive integers starting at k have the same smallest number
of squares needed to represent them (A002828). Listed terms: 1, 11, 42, 75, 138, 713, 1672. The keyword
"more" asks for further terms, and the entry says nothing about whether they exist.

## Result

No eight consecutive positive integers have the same value of A002828. So a(n) is defined only for
n = 1, ..., 7, and the seven listed terms are the whole sequence.

More precisely, the longest runs of consecutive integers with A002828 equal to 1, 2, 3, 4 have lengths
1, 3, 7, 2.

## Proof

By Lagrange and Legendre, A002828(m) = 4 exactly when m = 4^a (8b + 7), and otherwise A002828(m) <= 3.

1. Any eight consecutive integers contain some m = 7 mod 8, and A002828(m) = 4. So a run of eight equal
   values would be a run of eight values 4.
2. Three consecutive integers cannot all be of the form 4^a (8b + 7): at least two of them are not
   divisible by 4, a number of this form that is not divisible by 4 is 7 mod 8, and two numbers that are
   7 mod 8 differ by at least 8.

Hence no run has length 8 or more. Length 7 does occur (1672, ..., 1678, between 1671 = 8 * 208 + 7 and
1679), so a(7) exists and a(8) does not.

For the other values: a run of value 3 lies strictly between two consecutive numbers that are 7 mod 8,
so has length at most 7; a number that is 3 mod 4 is not a sum of two squares, so runs of value 2 have
length at most 3 (72, 73, 74 is one); two consecutive squares above 0 never occur; 111, 112 is a run of
value 4.

## Check

    python check.py      (about ten seconds; numpy)

computes A002828 up to 3 * 10^6 by brute force from sums of squares (without the three-square theorem),
recovers the seven listed terms as the first runs of each length, finds no run longer than 7, and
confirms the two facts used above on that range. Output in `check.log`.

## Limits

The statement is a two-line consequence of classical theorems, and it may well be known to people who
have looked at the entry; the claim here is only that the entry and its history do not record it.

## Novelty check

Performed 2026-11-11: the full revision history of A338627 (4 revisions, all of Nov 04 2020, no
discussion thread) and the draft page (no pending edit); the entry has no b-file; the cross-referenced
entry A002828 (no comment on runs of equal values) and A178615 (pairs of consecutive numbers that are
not sums of three nonzero squares; a different condition); the names of all OEIS entries for a companion
sequence on runs of A002828 (none); a web search for the A-number with the run-length statement
(nothing); the file list of Google DeepMind's formal-conjectures (not present).

## Credit

The sequence is due to Ilya Gutkovskiy (2020).
