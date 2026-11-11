# A000846 and A051924: two "only for primes" remarks fail at the square of a Wolstenholme prime

Status: **verified**; no earlier record found for these two entries (2026-11-11). The mechanism is
known and has been used by others on a neighbouring entry. Produced with AI assistance; see the
repository README. Not submitted to the OEIS.

## The entries

- [A000846](https://oeis.org/A000846): a(n) = C(3n, n) - C(2n, n). Remark (Gary Detlefs, 2013): "It
  appears that, with the exception of n = 49, a(n) == 1 (mod n^2) only if n is prime. (Tested to 10,000.)"
- [A051924](https://oeis.org/A051924): a(n) = C(2n, n) - C(2n-2, n-1). Remark (Gary Detlefs, 2013):
  "Conjecture: a(n) mod n^2 = n+2 iff n is an odd prime."

## Result

Both fail at n = 16843^2 = 283686649, which is composite, and likewise at 2124679^2. These are the squares
of the two known Wolstenholme primes.

## Why

For a prime p, the Jacobsthal-Kazandzidis congruence gives
C(pa, pb) = C(a, b) modulo p^(3 + v), where v is the p-adic valuation of a b (a - b). Taking a = 3p or 2p
and b = p gives v = 3, so modulo p^4

    C(3p^2, p^2) = C(3p, p)   and   C(2p^2, p^2) = C(2p, p).

For a Wolstenholme prime, C(2p, p) = 2 and C(3p, p) = 3 modulo p^4. Hence with n = p^2:

- A000846(n) = 3 - 2 = 1 modulo n^2;
- A051924(n) = C(2n, n)(3n - 2)/(2(2n - 1)) = (3n - 2)/(2n - 1) = n + 2 modulo n^2.

## Check

    python check.py

verifies C(2p, p) = 2 and C(3p, p) = 3 modulo p^4 for p = 16843 with exact binomials, shows that two
ordinary primes fail the same test, and confirms both remarks for n <= 600 (where 49 is the only
exception for A000846). The lift from p to p^2 uses the congruence above, a published theorem; the agent
that found this also checked n = 283686649 directly, by multiplying out the factorials modulo p^4.

## Credit for the mechanism

The same number disproved a conjecture in A064169 and A309391 in 2026 (Epoch AI's "OEIS Open" work,
recorded in MathWorld's Wolstenholme prime article). Applying it to A000846 and A051924 is what is added
here.

## Novelty check

Checked 2026-11-11: every page of both revision histories with their discussion threads; both draft
pages (no pending edits); an in-depth web search with the sequence numbers and 283686649; Epoch AI's
OEIS Open list; Google DeepMind's formal-conjectures repository; and the omega-institute project's issues
and code. Neither entry's remark is recorded as refuted.

## Limit

No search was made for a smaller counterexample between 10^4 and 2.8 * 10^8.
