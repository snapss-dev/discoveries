# A227728: the b-file is wrong from n = 643 on

Status: **verified** data error; no earlier record found (2026-11-11). The entry's conjectured
recurrence is **not proved**; it holds for the corrected terms up to n = 1000. Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A227728](https://oeis.org/A227728) (Clark Kimberling, 2013). With H(k) the harmonic numbers: a(1) is
the greatest k with H(k) - H(2) < 1/1 + 1/2, a(2) is the greatest k with H(k) - H(a(1)) < H(a(1)) - H(2),
and after that a(n) is the greatest k with

    H(k) - H(a(n-1)) < H(a(n-1)) - H(a(n-2)).

The sequence begins 10, 43, 179, 740, 3054, 12599. The entry conjectures the recurrence

    a(n) = 5a(n-1) - 4a(n-2) + 2a(n-3) - 2a(n-4) + 2a(n-5) - 2a(n-6) + 2a(n-7) - 2a(n-8) + 2a(n-9) - 2a(n-10)

and has a b-file for n = 1..1000.

## Result

A screen that tested conjectured recurrences against b-files reported that this one fails from
n = 643. It is the b-file that fails.

- Recomputed with enough precision, the terms agree with the b-file for n <= 642 and differ from it at
  every n from 643 to 1000: 358 wrong entries.
- At n = 643 the two values have 397 digits and share the first 396. The pattern fits a calculation
  that ran out of working precision near 400 digits.
- The recomputed terms satisfy the conjectured recurrence for every n from 11 to 1000. The b-file
  itself breaks it from n = 643.

## Check

    python check.py 1000 b227728.txt

with the b-file downloaded from the entry. The script finds each "greatest k" by Newton's method on
the harmonic function and then tests H(k) < T <= H(k+1) directly, at a working precision of three
times the number of digits of the term. The closest any decision comes to a tie is 0.005 of the gap
between consecutive harmonic numbers, far above the rounding error. Output in `check.log`.

The agent that found this had computed the 1000 terms twice, once with mpmath's harmonic function and
once with its own asymptotic series for H(k); the script here is a third implementation, and all three
agree.

## Novelty check

Checked 2026-11-11: all 20 revisions of the entry and its discussion (a 2017 thread corrects the name,
not the data); the draft page (no pending edits); an in-depth web search with the sequence number;
Epoch AI's OEIS Open list; Google DeepMind's formal-conjectures repository; the omega-institute
project; the Foundation-0 math0 repository. No mention of the b-file error.

## Limit

The recurrence remains a conjecture. Agreement up to n = 1000 is evidence, not a proof.
