# A123855: 2^k divides a(2^k - 1)

Status: **proved** here, unrefereed; no earlier proof found (2026-11-11). Elementary. Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A123855](https://oeis.org/A123855) (Alexander Adamchuk, 2006):

    a(n) = Sum_{j=1..n} Sum_{i=1..n} prime(i)^j.

It carries the remark "It appears that 2^k divides a(2^k-1) for all k > 0 (confirmed for 0 < k < 10)."

## Proof

Let n = 2^k - 1, and for a prime q let S_q = q + q^2 + ... + q^n, so that a(n) is the sum of S_q over
the first n primes.

**Odd q.** S_q + 1 = 1 + q + ... + q^(2^k - 1) = (1 + q)(1 + q^2)(1 + q^4) ... (1 + q^(2^(k-1))).
Each of the k factors is even, so 2^k divides S_q + 1. Hence S_q = -1 modulo 2^k.

**q = 2.** S_2 = 2^(n+1) - 2 = 2^(2^k) - 2, and 2^k >= k, so S_2 = -2 modulo 2^k.

The first n primes are 2 and n - 1 = 2^k - 2 odd primes. Therefore, modulo 2^k,

    a(n) = -2 - (2^k - 2) = -2^k = 0.  ∎

The argument uses nothing about the primes except that one of them is 2 and the others are odd.

## Check

    python check.py 13

computes a(2^k - 1) exactly for k up to 13 and prints the power of 2 in it. Output in `check.log`. The
agent that found the proof also checked the congruence up to k = 26.

## Novelty check

Checked 2026-11-11: all 21 revisions of A123855 with their discussion threads, and the histories of the
companion entries A123856 and A123857; the three draft pages (no pending edits); an in-depth web search
with the sequence number; Sela Fried's two papers; Epoch AI's OEIS Open list; Google DeepMind's
formal-conjectures repository; the omega-institute project; the Foundation-0 math0 repository. The
remark is still unproved in the entry and no proof was found elsewhere.
