# A229324: not every term is a multiple of 5

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the
repository README. Not submitted to the OEIS.

## The entry

[A229324](https://oeis.org/A229324): composite squarefree numbers n such that p + tau(n) divides
n - phi(n) for every prime p dividing n. It begins 115, 205, 295, 565, ... and carries two remarks:
"All terms are apparently multiple of 5" and "It appears that a(n) = 5*A061240(n+1)"
(Michel Marcus, 2013). Its table of terms stops at n = 500.

## Result

Both remarks are false. The term

    10419754 = 2 * 59 * 227 * 389

is in the sequence (tau = 16, n - phi(n) = 5333850, divisible by 18, 75, 243 and 405) and is 4 modulo 5.
The agent that found it places it at index 25842 and reports nine terms below 2 * 10^9 that are not
multiples of 5, among 3,556,179 terms; one of them, 188371849 = 17 * 29 * 137 * 2789, is odd.

## Why it held for so long

For a term with two prime factors the condition forces one of them to be 5, which is exactly the second
remark. Both remarks fail at the first term with four prime factors.

## Check

    python check.py

confirms from the definition that 10419754 and 188371849 are terms, and that all 708 terms below 200,000
are multiples of 5. Output in `check.log`. The index and the count below 2 * 10^9 come from the agent's
sieve and were not recomputed.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads; the draft page (no
pending edit); an in-depth web search with the sequence number and the counterexample; Epoch AI's OEIS
Open list; Google DeepMind's formal-conjectures repository; and the omega-institute project's issues and
code. No counterexample is recorded.
