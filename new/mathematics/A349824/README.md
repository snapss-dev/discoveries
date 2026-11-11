# A349824: n divides a(n) only for primes and for 1, 4, 16, 27, 30

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry

[A349824](https://oeis.org/A349824) (N. J. A. Sloane, 1 January 2022): a(n) = Omega(n) * sopfr(n), the
number of prime factors of n times their sum, both counted with repetition; a(0) = 0. For example
a(12) = 3 * (2 + 2 + 3) = 21. The entry carries the remark: "It appears that with the exception of
{1,4,16,27,30}, n divides a(n) iff n is prime." (Gary Detlefs, 11 January 2022)

## Result

The remark is true. For n >= 1, n divides a(n) exactly when n is prime or n is one of 1, 4, 16, 27, 30.

## Proof

If n is prime, a(n) = n. If n = 1, a(n) = 0. Let n be composite, with k = Omega(n) >= 2 prime factors,
largest prime factor P, and m = n/P >= 2. Write s(x) for sopfr(x). Assume n divides a(n) = k * s(n).

1. Every prime factor is at most P, so s(n) <= k P. Since a(n) > 0, n <= a(n) <= k^2 P, that is m <= k^2.
2. m is a product of k - 1 primes, so m >= 2^(k-1). With step 1, 2^(k-1) <= k^2, which forces k <= 6.
   Hence m <= 36.
3. P divides n, so P divides k * s(n) = k * (P + s(m)), so P divides k * s(m). This number is positive, and
   s(m) <= m (a sum of integers >= 2 is at most their product), so P <= k * s(m) <= 6 * 36 = 216.

So n = P m <= 216 * 36 = 7776. Among the composite n <= 7776, direct computation finds that n divides
a(n) only for 4, 16, 27 and 30 (a = 8, 32, 27, 30). ∎

## Check

    python check.py

- method 1: a segmented sieve computes Omega and sopfr for every n <= 10^9; the non-prime n with
  n | a(n) are exactly 1, 4, 16, 27, 30; it also counts 50,847,534 primes, the known value of pi(10^9), and
  confirms a(p) = p for each;
- method 2: trial division for n <= 200,000, sharing no code with method 1: the same five exceptions; the
  74 published terms are reproduced; the inequalities of steps 1 to 3 are asserted for every composite n.

Output in `check.log` (about two minutes). The proof needs the computation only up to 7776.

## Limits

Unrefereed. This settles only the divisibility remark. The entry's other conjecture (Mike Klein: every
trajectory of n -> a(n) ends in a fixed point or in the loop 28, 33) is not addressed here; the
omega-institute project lists it as an open problem (its issue 24177, 30 October 2026).

## Novelty check

Performed 2026-11-11:

- all five pages of the revision history (revisions 1 to 44, the last in May 2025) with their discussion
  threads, which concern formatting only; the draft page (no pending edit);
- the cross-referenced entries A001222 and A001414 (neither mentions this sequence) and the four entries
  numbered A349000 to A351999 that cite it, A349825, A349826, A349827 and A350747 (trajectories of the map; none has the divisibility
  remark or a proof);
- an in-depth web search with the sequence number and the list 1, 4, 16, 27, 30, and Zenodo's record
  search for the sequence number;
- Google DeepMind's formal-conjectures file list and the conjecture list of Epoch AI's OEIS Open benchmark:
  no mention;
- the omega-institute project: two issues mention A349824, both about Klein's convergence conjecture (the
  text of issue 24177 was read; it does not mention the divisibility remark); five files in a backfill
  folder with hashed names also match and were not opened.

No proof of the remark was found.
