# A332786: 16843^2 is a second "weak pseudoprime"

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the
repository README. Not submitted to the OEIS.

## The entry

[A332786](https://oeis.org/A332786) (Thomas Ordowski, 2020): a(n) is the numerator of

    S(n) = -1/n + Sum_{k=1..n} 2^(k-1) / k.

The entry notes that p^2 divides a(p) for every prime p > 3, and then asks:

- "Is 7^2 the only weak pseudoprime (i.e., a composite m such that m | a(m))?"
- "Conjecture: there are no pseudoprimes m such that m^2 | a(m)."

## Result

**No, 7^2 is not the only one.** m = 16843^2 = 283686649 is composite and m divides a(m).

The exact power of 16843 in a(m) is 2, so m^2 does not divide a(m). The conjecture in the second line
is untouched.

16843 is the smaller of the two known Wolstenholme primes. The entry already says that p^3 divides
a(p) for Wolstenholme primes and for p = 7, and these are exactly the primes whose squares turn up here.

## Check

    python check.py 7
    python check.py 16843

For n = p^2, write T = p^2 S(n). T is a p-adic integer, and it is computed modulo a power of p term by
term: a term with p not dividing k contributes p^2 2^(k-1) / k, a term k = p j with j < p contributes
p 2^(k-1) / j, the term k = n contributes 2^(n-1), and -1/n contributes -1. The power of p in S(n)
is the power of p in T, minus 2; when that is not negative, it is also the power of p in the numerator
a(n).

Two implementations that share no arithmetic code agree at p = 16843:

| method | result |
|---|---|
| A: numba, 64-bit arithmetic modulo p^4, 2.8 * 10^8 terms in parallel blocks | T = 0 modulo p^4 |
| B: gmpy2 big integers modulo p^5, terms grouped as k = p q + r | T = 0 modulo p^4, and T / p^4 = 808 modulo p |

So p^4 divides T exactly, and p^2 divides a(p^2) exactly. For p = 5, 7, 11 and 13 both methods agree with
exact rational arithmetic (the power of p in a(p^2) is 1, 2, 1, 1), which includes the known case 49.
The output is in `check.log`.

## A pattern, not proved

In every case computed, the power of p in a(p^2) is one less than the power of p in a(p). If that
holds in general, the weak pseudoprimes of the form p^2 are the squares of the primes with p^3 dividing
a(p): 7, 16843, and presumably the other known Wolstenholme prime 2124679, whose square was not
computed (4.5 * 10^12 terms).

## Credit for the mechanism

The square of a Wolstenholme prime has refuted several "only for primes" remarks in 2026: Epoch AI's
"OEIS Open" work for A064169 and A309391, and
[A000846 and A051924](../A000846-A051924/README.md) in this repository. Trying it on A332786 is what
is added here.

## Novelty check

Checked 2026-11-11: all 41 revisions of the entry with their discussion threads; the draft page (no
pending edits); an in-depth web search with the sequence number and 283686649; Sela Fried's two papers
of proofs of OEIS conjectures; Google DeepMind's formal-conjectures repository (no file for this entry);
the omega-institute project's issues and code (no mention); the Foundation-0 math0 repository (no
mention). In Epoch AI's OEIS Open list the entry itself is not a problem. A neighbouring conjecture
from A108866 is: that for n > 3 the numerator of -2/n + Sum 2^k/k is divisible by n^2 only when n is
prime. The number found here does not contradict it, because only the second power of 16843 divides,
not the fourth.

## Limits

Only squares of primes were tried. Nothing is claimed about other composite m, or about whether 16843^2
is the smallest weak pseudoprime after 49.
