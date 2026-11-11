# A006579: a 2025 conjecture is refuted by a number already in a neighbouring entry

Status: **known counterexample**, applied to a second entry. Not an independent find: the number was
taken from A018804. Produced with AI assistance; see the repository README.

## The entry

[A006579](https://oeis.org/A006579): a(n) = Sum_{k=1..n-1} gcd(n, k). It carries "Conjecture:
a(n) != -1 (mod n) for a composite n." (Thomas Ordowski, 11 June 2025).

## Who had it first

**Varun Vejalla**, 19 June 2025, in [A018804](https://oeis.org/A018804) (Pillai's function, which
equals a(n) + n). Ordowski had conjectured there in 2014 that n > 1 divides A018804(n) + 1 only for
primes, and Vejalla gave the counterexample

    n = 3 * 37 * 43 * 42307 * 116341 = 23492890653051.

Since A018804(n) + 1 and a(n) + 1 differ by n, the two conjectures say the same thing, and the same n
refutes the one in A006579: a(n) = 587322266326274 = 25 n - 1. Epoch AI's "OEIS Open" paper uses this
number for a third Ordowski conjecture, in A340079.

A006579 was last edited in November 2025 and does not mention it.

## Check

    python check.py

evaluates a(n) by two formulas, confirms a(n) + 1 = 25 n, and finds no composite n up to 200000 with
the property. Output in `check.log`.

Two small remarks: if q^2 divides n then a(n) + 1 = 1 modulo q, so a counterexample must be squarefree;
and a product of two primes never works.
