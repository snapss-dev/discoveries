# A285563: an empirical generating function fails at n = 36

Status: **verified**; no earlier record found (2026-11-11). Low interest: a formula fitted to a chaotic
cellular automaton. Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A285563](https://oeis.org/A285563) (Robert Price, 2017): the diagonal from the origin to the corner
of the n-th stage of the two-dimensional cellular automaton "Rule 51" on the 5-cell von Neumann
neighbourhood, started from a single ON cell, read as a binary number.

The entry carries an "Empirical g.f." (Colin Barker, 2017):

    (1 + x - x^2 + 2x^3 - 6x^4 - 64x^8 + 128x^9 + 64x^10 - 128x^11)
    / ((1 - x)(1 + x)(1 - 2x)(1 - 2x^2)(1 + 2x^2))

## Result

The generating function matches the 33 terms printed in the entry and the next three, and first fails
at n = 36:

- the automaton gives a(36) = 120257773568 (binary 1101111111111111011000000000000000000);
- the generating function gives 137437642752.

After that it fails at every even n tried. The odd terms stay 2^(n+1) - 1.

The contradiction was already inside the entry: its own b-file (n = 0..126) lists the automaton's
value at n = 36. Nobody had compared the two.

## Check

    python check.py 60

simulates the automaton from the rule (a cell is ON at the next step when exactly 0 or 2 of its four
neighbours are ON, which makes the empty background flip every step), reads the diagonal, expands the
generating function, and compares. Output in `check.log`. The agent that found this used two further
simulations (a dense grid and a sparse set of cells that differ from the background) and compared 331
stages; this script is a third, written separately.

## How it was found

By a mechanical screen: 4,235 rational generating functions marked as conjectured or empirical in the
OEIS were expanded and compared with the entries' b-files.

## Novelty check

Checked 2026-11-11: all 11 revisions of the entry and its discussion; the draft page (no pending
edits); an in-depth web search with the sequence number; Epoch AI's OEIS Open list; Google DeepMind's
formal-conjectures repository; the omega-institute project; the Foundation-0 math0 repository. No
mention of the failure.
