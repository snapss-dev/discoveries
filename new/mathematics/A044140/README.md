# A044140: a guessed recurrence fails at the 58th term

Status: **verified**; no earlier record found (2026-11-11). A small correction. Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A044140](https://oeis.org/A044140): numbers k such that the string "02" occurs in the base-7
representation of k but not of k - 1. It begins 51, 100, 149, 198, 247, 296, ... and lists 42 terms. In
2019 a generating function was added as a conjecture, with the recurrence
a(n) = a(n-1) + a(n-8) - a(n-9) for n > 9.

## Result

The recurrence, and with it the generating function, first fails at n = 58: the true a(58) is 2499
(10200 in base 7), and the recurrence predicts 2501. The conjecture was fitted to terms below 7^4 = 2401;
past that point "02" can appear one digit position further left, which no recurrence of that shape
models. More generally, a formula of this kind cannot survive each new power of 7.

## Check

    python check.py

generates the sequence from the definition, reproduces the listed start, and reports the first index
where the recurrence fails. Output in `check.log`.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads; the draft page (no
pending edit); an in-depth web search with the sequence number; Epoch AI's OEIS Open list; Google
DeepMind's formal-conjectures repository; and the omega-institute project's issues and code. No
refutation is recorded.
