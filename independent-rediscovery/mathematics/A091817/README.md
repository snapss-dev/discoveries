# A091817: Quet's integrality conjecture

Status: **rediscovery**. Produced with AI assistance; see the repository README.

## The entry

[A091817](https://oeis.org/A091817) (Bouayoun and Stephan, 2004): for a prime p >= 5, write the
harmonic number H(p-3) = u/v in lowest terms; the term is (2u - 3v)/p. The entry says: "Leroy Quet
conjectures that the terms are always integral. This is true for p < 3*10^4."

## Who had it first

- **Foundation-0's math0 project** published a machine-checked (Lean) proof on 18 October 2026, in an
  open pull request to its repository
  ([results/oeis-a091817](https://github.com/Foundation-0/math0/pull/1)). It classes the result as a
  first formal proof of a known result, and traces it to the congruence H(p-k) = H(k-1) modulo p in
  Z.-W. Sun and L.-L. Zhao, "Arithmetic theory of harmonic numbers (II)", Colloq. Math. 130 (2013).
- **The omega-institute project** screened the entry out in September 2026 as a classical corollary.

The OEIS entry itself still shows the conjecture as open.

## The argument found here

For a prime p >= 5, pairing k with p - k gives 1/k + 1/(p-k) = p / (k(p-k)), so H(p-1) = 0 modulo p.
Then

    H(p-3) = H(p-1) - 1/(p-1) - 1/(p-2) = 0 + 1 + 1/2 = 3/2   modulo p.

The denominator v divides lcm(1, ..., p-3), so p does not divide v, and
2u - 3v = v (2 H(p-3) - 3) = 0 modulo p. ∎

The agent that found it checked all primes up to 3 * 10^5 as well.

## How the earlier work was missed

The agent's novelty check read the entry, its eight revisions and a standard web search. The math0
pull request and the omega-institute note turned up only in the full check: an in-depth web search
with the sequence number, and a search of the omega-institute project's issues.
