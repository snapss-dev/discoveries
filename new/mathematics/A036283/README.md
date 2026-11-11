# A036283: two wrong values in the b-file, and a proof of a(n) = 6 A202318(n)

Status: the two data errors are **verified** and no earlier record of them was found (2026-11-11). The
relation itself is **not new as a statement**: it is asserted without proof in A202318. The proof is
short, standard and unrefereed. Produced with AI assistance; see the repository README. Not submitted
to the OEIS.

## The entries

- [A036283](https://oeis.org/A036283): denominator of (2^(2n-1) - 1) B_{2n} / n, the coefficients of
  the expansion of cosec x. It carries "Apparently a(n) = 6*A202318(n)" (Hugo Pfoertner, 2022).
- [A202318](https://oeis.org/A202318) (Shevelev and Moses, 2011) is defined prime by prime: the powers
  of 2 and 3 in a(n) are those in n; a prime p >= 5 appears, with exponent 1 + v_p(2n / (p - 1)),
  exactly when p - 1 divides 2n. It carries "a(n) = A036283(n)/6" (Pfoertner, 2022) as a formula.

Here v_p(m) is the exponent of p in m.

## Two wrong values

The b-file of A036283 (n = 1..10000) disagrees with the definition in two places.

| n | b-file | correct | ratio |
|---|---|---|---|
| 6951 = 3 * 7 * 331 | 346793879715066 | 1047715648686 | 331 |
| 8308 = 4 * 31 * 67 | 2162760 | 32280 | 67 |

In both, the b-file keeps a prime q that divides n. It cannot be in the denominator: q - 1 does not
divide 2n, so by Adams's theorem (step 4 below) q divides the numerator of B_{2n} and cancels. The
b-file of A202318 has no such error; at these n it gives 174619274781 and 5380, one sixth of the
correct values.

## Proof of the relation

Write r(n) = (2^(2n-1) - 1) B_{2n} / n. The exponent of p in its denominator is max(0, -v_p(r(n))).
Two classical facts are used.

- **von Staudt-Clausen.** v_p(B_{2n}) = -1 when p - 1 divides 2n, and v_p(B_{2n}) >= 0 otherwise.
- **Adams.** If p - 1 does not divide 2n, then B_{2n} / (2n) is p-integral.

1. p = 2. Here v_2(B_{2n}) = -1 and 2^(2n-1) - 1 is odd, so the exponent is 1 + v_2(n).
2. p = 3. Here v_3(B_{2n}) = -1, and 2^(2n-1) = 2 * 4^(n-1) is 2 modulo 3, so 3 does not divide
   2^(2n-1) - 1. The exponent is 1 + v_3(n).
3. p >= 5 with p - 1 dividing 2n. Then v_p(B_{2n}) = -1. By Fermat 2^(2n) = 1 modulo p, so
   2 (2^(2n-1) - 1) = -1 modulo p, and p does not divide 2^(2n-1) - 1. The exponent is 1 + v_p(n),
   which equals 1 + v_p(2n / (p - 1)) because p divides neither 2 nor p - 1.
4. p >= 5 with p - 1 not dividing 2n. By Adams, B_{2n} / n is p-integral, hence so is r(n). The
   exponent is 0.

Multiplying over all primes gives 2 * 3 * A202318(n). ∎

## Check

    python check.py 10000

computes the denominator directly from FLINT's Bernoulli numbers for every n up to 10000, compares it
with 6 A202318(n) from the definition, and recomputes the two disputed values with a second Bernoulli
implementation (sympy). Output in `check.log`.

## Novelty check

Checked 2026-11-11: all 30 revisions of A036283 and all revisions of A202318 with their discussion
threads; both draft pages (no pending edits); a web search with both sequence numbers; Sela Fried's two
papers; Epoch AI's OEIS Open list; Google DeepMind's formal-conjectures repository; the omega-institute
project; the Foundation-0 math0 repository. The b-file of A036283 dates from 2016 and has not been
replaced. No proof of the relation and no note about the two values was found.
