# A276531: every term is an integer

Status: **rediscovery**. Produced with AI assistance; see the repository README.

## The entry

[A276531](https://oeis.org/A276531) (Seiichi Manyama, 16 November 2016):

    a(n) a(n-6) = a(n-1) a(n-5) + a(n-2) a(n-3) a(n-4),     a(0) = ... = a(5) = 1.

It carries "Conjecture: a(n) is an integer for all n. It has been checked by computer for
0 <= n <= 50."

## Who had it first

Michael Somos, five days later, in the same entry: "The recursion has the Laurent property. If a(0),
..., a(5) are variables, then a(n) is a Laurent polynomial (a rational function with a monomial
denominator)." (21 November 2016.) A Laurent polynomial with integer coefficients, evaluated at
a(0) = ... = a(5) = 1, is an integer, so this settles the conjecture. The entry gives no proof of the
Laurent property and still lists the conjecture.

## What is added here

An explicit certificate for the Laurent property, from the theory of cluster algebras.

- Take the skew-symmetric matrix B below. Mutating it at its first node and then relabelling the nodes
  cyclically gives B again (a period-1 quiver in the sense of Fordy and Marsh, 2011).

      0  1 -1 -1 -1  1
     -1  0  2  0  0 -1
      1 -2  0  2  0 -1
      1  0 -2  0  2 -1
      1  0  0 -2  0  1
     -1  1  1  1 -1  0

- The exchange relation at the first node is x1 x1' = x2 x6 + x3 x4 x5, which is the recurrence.
- By the Laurent phenomenon (Fomin and Zelevinsky, 2002), every cluster variable is a Laurent
  polynomial with integer coefficients in the initial ones. All terms are positive, so no division by
  zero occurs.

## Check

    python check.py 40

builds B by the Fordy-Marsh rule, verifies the period-1 property with exact integer arithmetic, and
checks integrality directly for n <= 40. Output in `check.log`.

## How the earlier work was missed

The agent read Somos's comment and reported the conjecture as proved by its own argument, on the
ground that the comment "gave no proof". The comment is the result; a supporting certificate does not
make it new. Caught when the revision history was read in full on 2026-11-11.
