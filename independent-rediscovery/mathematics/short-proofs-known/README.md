# Short proofs that were already known

Status: **verified**, and **found earlier by others** (checked 2026-11-11). Produced with AI assistance; see
the repository README. Nothing here is new. These were proposed as new by an earlier pass that read only
the published entry; the fuller novelty check found each of them recorded elsewhere. They are kept so that
the credit is on record and the same ground is not covered again.

`python check.py` checks the statements numerically (seconds); output in `check.log`.

## A091713: all coefficients are odd

Entry: g.f. A(x) = x + x*A(A(A(x))): 1, 1, 3, 15, 99, 781, ... "Conjecture: all terms are odd." (Paul D.
Hanna, 1 December 2024)

**Who had it first:** Yuan Chi, "Proof of the Modulo 4 Conjecture for OEIS A141117 and of the Parity
Conjecture for OEIS A091713", Zenodo, doi:10.5281/zenodo.22026845 (note dated 18 August 2026, published
20 August 2026). The note is linked from A141117, the entry for A(A(x)), and not from A091713, whose
comment still reads "Conjecture". Its main result is stronger: the coefficients of A(A(x)) modulo 4.

*The argument, as re-derived here.* The equation has a unique solution over any commutative ring, the
coefficient of x^n on the right depending only on a(1), ..., a(n-1). Modulo 2, B(x) = x/(1 - x) satisfies
it, because B(B(B(x))) = x/(1 - 3x) = B modulo 2 and x + x*B = B. So the integer solution reduces to B
modulo 2. Chi's note uses the same uniqueness lemma. (The same argument applied to the sister entry
A120566 is on the page of new short proofs.)

## A008474: iterating n -> sum of (p + k) reaches 5

Entry: if n is the product of p_j^k_j then a(n) = sum of (p_j + k_j). "Conjecture: for m > 4, by iterating
the map m -> A008474(m) one always reaches 5 [tested up to m = 320000]." (Ivan N. Ianakiev, 10 November
2014)

**Who had it first:** the omega-institute project (repository the-omega-institute/trureturing, issues 7647
and 7660, opened and closed on 13 September 2026, with a Lean formalisation). The entry itself still shows
the conjecture as open.

*The argument, as re-derived here.* 5 -> 6 -> 7 -> 8 -> 5 is a cycle. For a composite m > 8, a(m) < m: for a
prime power p^k with k >= 2, p + k < p^k except for 4; for two or more coprime prime powers x_i,
sum (x_i + 1) < product x_i except for {2, 3}, and p + k <= p^k + 1. For a prime p >= 7, a(p) = p + 1 is
even and a(p + 1) < p (write p + 1 = 2^a y with y odd and use a(y) <= y + 1; the two exceptions 6 and 10
are not of the form p + 1 with p >= 7 prime). The only m with a(m) <= 4 are 1, 2, 3, 4. So every
trajectory from m >= 9 descends until it enters {5, 6, 7, 8}. The issue title describes the same proof:
one-step descent for composites, two-step descent for primes.

## A254074: no term is a multiple of 5

Entry: k such that k and k^2 both have smallest digit 5 and largest digit 9. "Conjecture: no term is a
multiple of 5." (Chai Wah Wu, 10 September 2017)

**Who had it first:** the omega-institute project (issues 7909 and 7953, 14 September 2026, with a Lean
formalisation). Argument: such a k would end in 5, so k^2 ends in 25 and contains the digit 2.

## A000680: (2n+1) divides (2n)!/2^n + 2^n exactly when 2n+1 is prime

Entry conjecture by Werner Schulte, 5 October 2025.

**Who had it first:** Sela Fried, 24 November 2025 (proof file attached to the entry; also in "Further
proofs of conjectures from the OEIS", arXiv:2607.24832, pp. 2-4). The omega-institute project formalised it
on 15 September 2026 (issues 8173 and 8196). Argument: Wilson's theorem and Fermat's little theorem for a
prime; an odd composite m divides (m - 1)!, which leaves the unit 2^n.

## A088883 and A088884: concat(p, reverse(p)) + 2 or - 2 prime

Entries: primes p for which N + 2 (A088883) or N - 2 (A088884) is prime, N being p followed by its
reversal. Remarks: N + 2 and N - 2 are never both prime; "Conjecture: All these primes are of the form
6*k + 1" and "except for 3, all these primes are of the form 6*k - 1" (Davide Rotondo, 29 April 2025).

**Who had it first:** Robert Israel, in the discussion thread of A088883 on 29 April 2025: "If p == 2
(mod 3), p||reverse(p) + 2 is divisible by 3, so yes it is true." The same remark settles all three
statements: N has digit sum twice that of p, so N = 2p modulo 3, and one of N - 2, N + 2 is a multiple of
3 unless p = 3. The entries still show the statements as conjectures.

## A014865: Dale's three divisibility claims

Entry: k dividing s(k), with s(1) = 1, s(j) = 15 s(j-1) + j. "Conjecture: all terms are odd, all terms
greater than 7 are composite, and all terms greater than 1 are divisible by 3 or 5 or 7" (Harvey P. Dale,
4 December 2020).

**Who had it first:** the omega-institute project (issue 25683, "resolve Dale's three A014865 divisibility
claims", 2 November 2026), nine days before this page.

*The argument, as re-derived here.* s(k) = (15^(k+1) - 14k - 15)/196, so k is a term exactly when 196k
divides T = 15(15^k - 1) - 14k. (a) For even k with 2-adic valuation v, the first part of T has valuation
v + 4 and the second v + 1, so T has valuation v + 1, less than that of 196k. (b) For a prime p other than
2 and 7, T = 15^2 - 15 = 210 modulo p, so p is 3 or 5; with 7 these are the only prime terms. (c) If k > 1 is odd and prime to 105, let p be its
least prime factor; then 15^k = 1 modulo p and the order of 15 divides gcd(k, p - 1) = 1, so p divides 14,
which is impossible. Whether the project's proof follows the same lines was not checked.

## A065907: no value occurs more than three times

Entry (Klaus Brockhaus, 2001): the least solution x of x^4 = 2 modulo p, for the primes p for which there
are exactly two solutions. "Conjecture: no integer occurs more than three times in this sequence." The same
conjecture stands in A065908, A065909 and A065910.

**Who had it first:** the author himself, in the companion entries A065902 to A065906, written at the same
time: "n is a solution mod p of x^4 = 2 iff p is a prime factor of n^4 - 2 and p > n. n^4 - 2 has at most
three prime factors > n". Four primes larger than n cannot all divide n^4 - 2 < n^4, and that settles all
four conjectures at once. The version derived here (the least solution is below p/2, so p > 2x) is the same
argument.

## Two that the entries already answer

- A125855 (k with k+1, k+3, k+7, k+9 all prime): "It seems that, with the exception of 4, all terms are
  multiples of 10" (Emeric Deutsch, 2006) is answered in the entry: "In fact, all terms except 4 are
  congruent to 10 (mod 30)" (Franklin T. Adams-Watters, 5 June 2014).
- A034496 (sum of the n-th powers of the divisors of 8): "Conjecture: No primes in this sequence" (Artur
  Jasinski, 2008) is answered in the entry: a(n) = (1 + 2^n)(1 + 4^n) (T. D. Noe, 26 April 2010).

## How the earlier work was missed

The first pass worked from a local copy of the entries and judged novelty from the text of each entry. The
omega-institute results are recorded only in that project's issue tracker and code, not in the OEIS; Yuan
Chi's note is on Zenodo and linked only from a neighbouring entry (an in-depth web search with the sequence
number did not find it either); Robert Israel's proof is in a discussion thread of the revision history,
not in the entry; Sela Fried's proof and the two older answers are in the entries and were overlooked; and
the remark that settles A065907 is in five neighbouring entries, not in the entry that carries the
conjecture.

## Novelty check

Performed 2026-11-11: every page of each entry's revision history with the discussion threads; draft
pages; the omega-institute project's issues and code by sequence number (issue titles and dates read; the
proofs and Lean files themselves were not opened); the text of arXiv:2607.24832; the Zenodo note, read in
full (it mentions only A141117 and A091713); the entries A065902 to A065910.
