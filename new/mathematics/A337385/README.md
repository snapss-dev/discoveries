# A337385: not every term is divisible by 255255

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the
repository README. Not submitted to the OEIS.

## The entry

[A337385](https://oeis.org/A337385): odd numbers k with sigma(A003961(k)) >= 2 * A003961(k), where
A003961 replaces each prime in the factorisation of k by the next prime. It carries the remark
"Apparently, all terms are divisible by 255255 = 3*5*7*11*13*17" (Hugo Pfoertner, 2020). The listed terms
stop at about 4.35 * 10^9.

## Result

The remark is false. The odd number

    k = 8562829275 = 3^3 * 5^2 * 7 * 11 * 13 * 19 * 23 * 29

has no factor 17, and A003961(k) = 307877945375 has sigma = 619531960320, which exceeds
2 * 307877945375 = 615755890750. The agent that found it places it at index 45 and reports that 68 of the
931 terms below 10^11 are not divisible by 255255.

## Check

    python check.py

computes A003961(k) and its sigma from the factorisation. Output in `check.log`. The index and the count
below 10^11 come from the agent's search and were not recomputed.

## A caveat on novelty

307877945375 already appears in the published table of a related sequence (A115414, odd abundant-type
numbers), so the refutation could have been read off existing data. It is not stated anywhere that was
checked.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads; the draft page (no
pending edit); an in-depth web search with the sequence number and the counterexample; Epoch AI's OEIS
Open list; Google DeepMind's formal-conjectures repository; and the omega-institute project's issues and
code. No counterexample is recorded.
