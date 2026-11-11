# A152212: no term is congruent to 2 modulo 4

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry

[A152212](https://oeis.org/A152212): numbers k such that sigma_0(k) divides k*sigma_1(k) - sigma_2(k),
where sigma_0 counts the divisors, sigma_1 is their sum and sigma_2 the sum of their squares. It begins
1, 3, 5, 7, 11, 12, 13, 15, 16, 17, ... Two comments ask for a proof:

- "Up to 4000000, the sequence contains no k == 2 (mod 4), which if it holds up implies that every run of
  3 starts with an odd number (in fact, k == 3 (mod 4)), and that there are no runs of 4. It appears,
  based on congruence arguments mod powers of 2, that no k == 2 (mod 4) is possible, but I am not sure that
  I can actually prove this." (Franklin T. Adams-Watters, 8 November 2009)
- "For every k == 2 (mod 4) up to 10^8, the largest power of 2 that divides sigma_0(k) is exactly twice
  the largest power of 2 that divides (k*sigma_1(k) - sigma_2(k)), so k is not a term. Can it be proved
  that this holds for all k == 2 (mod 4)?" (Jon E. Schoenfield, 9 March 2024)

## Result

Yes. Write v(x) for the exponent of 2 in x and E(k) = k*sigma_1(k) - sigma_2(k). For every k == 2 (mod 4),

    v(sigma_0(k)) = v(E(k)) + 1,

which is Schoenfield's observation. So sigma_0(k) never divides E(k), and no k == 2 (mod 4) is a term.
Consequently the sequence has no run of four consecutive integers, and every run of three starts at a
number congruent to 3 modulo 4.

## Proof

Let k = 2m with m odd. All three functions are multiplicative, so

    sigma_0(k) = 2 sigma_0(m),   sigma_1(k) = 3 sigma_1(m),   sigma_2(k) = 5 sigma_2(m),
    E(k) = 6 m sigma_1(m) - 5 sigma_2(m).

**Lemma.** For an odd prime p and e >= 0:

    (a)  v(1 + p^2 + p^4 + ... + p^(2e)) = v(e + 1),
    (b)  v(1 + p + p^2 + ... + p^e)     >= v(e + 1).

*Proof of the lemma.* If e is even, each sum has an odd number of odd terms, so it is odd, and v(e + 1) = 0.
Let e be odd, so e + 1 is even. For an odd integer q and even N, the lifting-the-exponent formula gives
v(q^N - 1) = v(q - 1) + v(q + 1) + v(N) - 1. Hence
v((q^N - 1)/(q - 1)) = v(q + 1) + v(N) - 1. With q = p^2 and N = e + 1: q is 1 modulo 8, so v(q + 1) = 1,
and the sum in (a) has valuation exactly v(e + 1). With q = p: v(p + 1) >= 1, so the sum in (b) has
valuation at least v(e + 1). ∎

Let m = product of p_i^(e_i). Multiplying over the prime powers,

    v(sigma_2(m)) = sum of v(e_i + 1) = v(sigma_0(m)),        v(sigma_1(m)) >= v(sigma_0(m)).

Put t = v(sigma_0(m)). Then v(5 sigma_2(m)) = t, while v(6 m sigma_1(m)) >= t + 1. The two terms of E(k)
have different valuations, so v(E(k)) = t (in particular E(k) is not zero), and v(sigma_0(k)) = t + 1. ∎

*Runs.* Four consecutive integers contain one that is 2 modulo 4, so there is no run of four. A run of
three avoids the residue 2, so it is {4j + 3, 4j + 4, 4j + 5}.

## Check

    python check.py

- method 1: a segmented sieve computes sigma_0, sigma_1 and sigma_2 of every k <= 400,000,000 from the
  factorisation of k itself (the reduction to the odd part is not used) and tests the valuation identity
  for all 100,000,000 values k == 2 (mod 4): no failure. The entry reports a test to 10^8. The sieve
  reproduces the 64 published terms;
- method 2: plain divisor lists for k <= 300,000: 165,894 terms, none congruent to 2 modulo 4; runs of
  consecutive terms have length at most 3, and all 24,608 runs of length 3 start at 3 modulo 4;
- the lemma is tested for 2821 odd prime powers.

Output in `check.log` (about a minute).

## Limits

Unrefereed. The proof says nothing about which k congruent to 0 modulo 4 are terms.

## Novelty check

Performed 2026-11-11:

- all four pages of the revision history (revisions 1 to 31, the last in March 2024) and its one discussion
  thread (about wording only); the draft page (no pending edit);
- the cross-referenced entries A000005, A000203, A001157 and A064987: none mentions this sequence, and no
  other entry numbered A152000 to A153999 does;
- an in-depth web search with the sequence number and its definition; it led to S. Fried, "Further proofs
  of conjectures from the OEIS", arXiv:2607.24832, whose text was searched: it does not mention A152212;
- Zenodo's record search for the sequence number, Google DeepMind's formal-conjectures file list, the
  conjecture list of Epoch AI's OEIS Open benchmark, and the issues and code of the omega-institute
  project: no mention.

No proof was found. Both questions are still open in the entry.
