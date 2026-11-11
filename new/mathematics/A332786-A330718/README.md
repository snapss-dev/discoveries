# A332786 and A330718: 16843^2 is a weak pseudoprime for both

Status: **verified** by three independent computations; no earlier record found for these two entries
(2026-11-11). The number itself is well known and has been used by others on neighbouring entries.
Computed, not proved. Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entries

- [A332786](https://oeis.org/A332786): a(n) = numerator(-1/n + Sum_{k=1..n} 2^(k-1)/k). Comments by
  Thomas Ordowski (Feb 24 2020), still in the entry (revision 41): "If p > 3 is a prime, then p^2 | a(p)."
  "If p is a Wolstenholme prime (A088164), then p^3 | a(p). However, it should be noted that also
  7^3 | a(7)." "Conjecture: there are no pseudoprimes m such that m^2 | a(m)." "Is 7^2 the only weak
  pseudoprime (i.e., a composite m such that m | a(m))?"
- [A330718](https://oeis.org/A330718): b(n) = numerator(Sum_{k=1..n} (2^k-2)/k), by Amiram Eldar and
  Thomas Ordowski (Dec 28 2019). Comments, still in the entry (revision 73): "Conjecture: for n > 3, if
  n^2 | a(n), then n is prime." "Are there the weak pseudoprimes m such that m | a(m)?"

## Result

Let p = 16843, the smaller of the two known Wolstenholme primes, and m = p^2 = 283686649.

- The p-adic valuation of A332786(m) is exactly 2. So m divides a(m): 7^2 is **not** the only weak
  pseudoprime of A332786.
- The p-adic valuation of A330718(m) is exactly 2. So m divides b(m): the answer to the question in
  A330718 is **yes**.
- In both cases m^2 does not divide the term, so the two conjectures (no composite m with m^2 dividing
  the term) are untouched.
- There is no other composite m <= 20000 that divides a(m), and none at all that divides b(m), by
  exhaustive search with exact fractions. Between 20000 and 283686649 nothing was searched.

## How it was computed

The term at n = p^2 has on the order of 10^8 digits, so it is not formed. Write the rational number
as S and put T = p^2 S. Then T is a p-adic integer,

    T = p^2 A + p B + C - 1,
    A = Sum over k <= p^2, p not dividing k, of 2^(k-1)/k
    B = Sum over j < p of 2^(pj-1)/j
    C = 2^(p^2-1)

and the valuation of the numerator is v_p(T) - 2 once v_p(T) >= 2. For A330718 every 2^(k-1) becomes
2^(k-1) - 1 (half of the entry's rational, which has the same valuation at an odd prime). T is computed
modulo p^5: v_p(T) = 4 for both entries, with T/p^4 = 808 (mod p) for A332786 and 7568 (mod p) for
A330718.

Three computations of the A332786 valuation agree (the residue 808 is given by the second and third):
1. `check.gp`: PARI/GP, one plain loop over the 283686649 terms with arbitrary-precision residues;
2. `check.py`: vectorised 64-bit integers, inverses by Newton lifting from a table modulo p, products in
   15-bit limbs;
3. the first pass by a different agent (64-bit compiled loops modulo p^4, and big integers modulo p^5 with
   a different grouping of terms).

The A330718 value was computed by 1 and 2 only. Both programs are calibrated against exact rational
arithmetic for n = p^2 (check.py for p from 5 to 43, check.gp for p from 5 to 31), where they reproduce
the valuations of both entries, including the known case 49 | a(49).

## Why one might expect it

For every prime 5 <= p <= 43, and for p = 16843, the valuations satisfy

    v_p(a(p^2)) = v_p(a(p)) - 1        and        v_p(b(p^2)) = v_p(b(p)) - 1.

So p^2 divides the term at p^2 exactly when p^3 divides the term at p. For A332786 that happens at p = 7
and at the Wolstenholme primes (v_p(a(p)) = 3 for p = 7, 16843 and 2124679; `valuation_at_p.py`). For A330718
it happens at the Wolstenholme primes but not at 7 (v_7(b(7)) = 2), which is why A330718 has no small
example. This relation is an observation; it is not proved here. If it holds, 2124679^2 is a further
weak pseudoprime of both entries; that was not computed (4.5 * 10^12 terms).

## How to check

    python check.py           (about two minutes; needs numpy)
    gp -q check.gp            (PARI/GP; several minutes)
    python valuation_at_p.py  (the valuations at p itself; a few seconds)

Outputs are in `check.log`, `check_gp.log` and `valuation_at_p.log`.

## Credit

The questions are Thomas Ordowski's (with Amiram Eldar for A330718). That squares of Wolstenholme primes
defeat "only for primes" statements tied to Wolstenholme's theorem is known: A267824 lists 283686649 for
the binomial form, and Epoch AI's "OEIS Open" work (arXiv:2608.11941) used p = 16843 to disprove
conjectures in A064169 and A309391. What is added here is the computation for these two entries, where
the sums carry powers of 2 and the harmonic-number argument does not apply directly.

## Limits

- A computation, not a proof; the relation between the valuations at p and p^2 is unexplained.
- 283686649 is not shown to be the second-smallest weak pseudoprime of A332786, nor the smallest of
  A330718: the exhaustive search stops at 20000.
- The related conjecture in A108866 (n^2 divides the numerator of -2/n + Sum 2^k/k only for primes) is
  not affected: for odd n that numerator is 2 a(n), and m^2 does not divide a(m).

## Novelty check (2026-11-11)

- Every page of the revision histories of A332786 (41 revisions), A330718 (73), A330719 (44), A108866
  (37), A267824 (38), A229726 (12) and the pages served for A088164 (revisions 62 to 171), with all
  discussion threads. No answer to either question; no pending drafts. The threads on A332786 are
  about wording and about the prime case.
- The live text of A332786, A330718 and A108866, fetched today.
- The complete OEIS term dump: 283686649 occurs only in A267824.
- Epoch AI's OEIS Open list: contains the A108866 conjecture, not these questions; the paper's two
  Wolstenholme-prime disproofs concern A064169 and A309391.
- Google DeepMind's formal-conjectures file list: has A108866, not A332786 or A330718.
- The omega-institute project: no issue or code mentions A332786; A330718 appears once, in a list of
  screened-out items, in connection with A330719.
- Two in-depth web searches with the A-numbers, "weak pseudoprime", 283686649 and 16843^2: nothing.
