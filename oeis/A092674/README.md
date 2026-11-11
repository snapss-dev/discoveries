# A092674 is never negative

Status: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A092674](https://oeis.org/A092674) (Jon Perry, 2004) is defined through a recursion with an
indeterminate x:

    s(1) = x,
    s(n) = binomial(n+1, 2) - sum_{i=1}^{n-1} s(i) * floor(n/i)      for n >= 2,

and a(n) is the constant term of s(n). The entry begins 0, 3, 3, 1, 5, 0, 7, 4, 6, 2, 11, 5, ... and
carries the comment "It is conjectured that a(n) is never less than 0 (tested to n=2000)".

## Result

    a(n) = phi(n) - mu(n) + [n even] * mu(n/2),

where phi is Euler's totient function and mu is the Möbius function. Hence a(n) >= 0 for every n, and
a(n) = 0 only for n = 1 and n = 6.

## Proof

Move the i = n term of the sum to the left. Since floor(n/n) = 1, the recursion says that for n >= 2

    sum_{i=1}^{n} s(i) * floor(n/i) = n(n+1)/2,

while for n = 1 the left side is s(1) = x. Now sum_{i=1}^{n} s(i) floor(n/i) = sum_{k=1}^{n} D(k), where
D(k) = sum_{d | k} s(d), because floor(n/i) counts the multiples of i up to n. Taking differences of
consecutive n:

    D(1) = x,    D(2) = 3 - x,    D(n) = n(n+1)/2 - (n-1)n/2 = n   for n >= 3.

So D(n) = n + e(n) with e(1) = x - 1, e(2) = 1 - x, and e(n) = 0 otherwise. Möbius inversion gives

    s(n) = sum_{d | n} mu(n/d) D(d)
         = phi(n) + (x - 1) mu(n) + (1 - x) [n even] mu(n/2),

using sum_{d | n} mu(n/d) d = phi(n). The constant term is the formula above.

For n >= 3 we have phi(n) >= 2, and -mu(n) + [n even] mu(n/2) >= -2, so a(n) >= 0. Equality needs
phi(n) <= 2, that is n in {1, 2, 3, 4, 6}, and checking these five values leaves n = 1 and n = 6. ∎

## Check

    python check.py 5000

computes s(n) from the recursion (as a constant and an x-coefficient) and compares the constant term with
the formula for every n up to 5000. Output:

    first terms: [0, 3, 3, 1, 5, 0, 7, 4, 6, 2, 11, 5, 13, 4, 7, 8, 17, 6, 19, 9]
    formula matches the recursion for 1 <= n <= 5000: True
    zeros at n = [1, 6]

## Novelty check

The published entry and its full revision history (two revisions, 2004 and 2012) contain no proof or
formula. A web search for the sequence number found nothing further. Checked 2026-11-11.
