# A064169: five more exceptions inside the range that was "tested"

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the
repository README. Not submitted to the OEIS.

## The entry

[A064169](https://oeis.org/A064169): numerator minus denominator of the n-th harmonic number H_n. It
carries the remark (Gary Detlefs, 2011):

> It appears that a(n) = numerator((3*(HarmonicNumber(n) - 1)) / (n*(n^2 + 6*n + 11))), except for
> n = 5, 82, 115, and 383 (tested to 20000).

## Result

The list is incomplete within its own stated range. The exceptions up to 20000 are

    5, 82, 115, 383, 4136, 9333, 9416, 9702, 18030.

The agent that found this reports no further exception up to 30000.

## Check

    python check.py

computes H_n exactly for n <= 20000 and compares the two numerators. One second. Output in `check.log`.

## Not to be confused with

A different conjecture in the same entry (Amiram Eldar and Thomas Ordowski, 2019: n divides a(n-2) if
and only if n is prime) was disproved in 2026 at n = 16843^2 in Epoch AI's "OEIS Open" work; the entry
links it and Google DeepMind's formal-conjectures repository records it. That is someone else's result
and concerns a different statement.

## Novelty check

Checked 2026-11-11: all eleven pages of the revision history with their discussion threads; the draft
page (no pending edit); an in-depth web search with the sequence number and the new exceptions; Epoch
AI's OEIS Open list and the formal-conjectures file for this entry (both concern the other conjecture);
and the omega-institute project's issues and code. The extra exceptions are not recorded.
