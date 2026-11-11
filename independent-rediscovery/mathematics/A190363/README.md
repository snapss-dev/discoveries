# A190363: a guessed recurrence fails at the 161st term

Status: **rediscovery**. Credit: a contributor to Google DeepMind's formal-conjectures repository, and
Daniel Veljjanoski. Produced with AI assistance; see the repository README.

## What was found here

On 2026-11-11 an agent found that the recurrence conjectured in [A190363](https://oeis.org/A190363)
(2025), a(n) = a(n-4) + a(n-17) - a(n-21), holds for 22 <= n <= 160 and first fails at n = 161: the true
a(161) is 542, and a(157) + a(144) - a(140) = 528 + 484 - 471 = 541. Here
a(n) = n + floor(n sqrt(5)/2) + floor(5n/4). No recurrence with constant coefficients can hold, since
it would make floor(n sqrt(5)/2) eventually quasi-polynomial.

## Who had it first

- The counterexample was already recorded in Google DeepMind's
  [formal-conjectures](https://github.com/google-deepmind/formal-conjectures) repository
  (`FormalConjectures/OEIS/190363.lean`).
- Daniel Veljjanoski proposed it to the OEIS on 11 November 2026 (revision history, revisions 15 and 16),
  noting that source and a Lean proof.

## How it was missed at first

The agent read the entry's history and draft page a little before that edit was made, and did not search
the formal-conjectures repository. A second pass found both.

## Check

    python check.py

computes the sequence exactly and reports the first failure. Output in `check.log`.
