# A125314: a new term, a(11) = 10892793

Status: **verified**, including minimality by two searches that share no code. No earlier record found
(2026-11-11). Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A125314](https://oeis.org/A125314) (Alexander Adamchuk, Jan 18 2007; keywords hard, more): the smallest
number k > 1 such that Sum_{i=1..k} i^n divides Product_{i=1..k} i^n, that is, such that
1^n + 2^n + ... + k^n divides (k!)^n. Listed terms for n = 1 to 10:
3, 7, 3, 31, 13, 1556, 733, 89037, 1441, 668073, with the comment
"a(11) > 1091730. - Robert G. Wilson v, Jan 25 2007". The entry has six revisions, the last in 2015, and
none touches the data.

## Result

    a(11) = 10892793.

For k = 10892793 = 3 * 67 * 54193, with k + 1 = 2 * 11 * 149 * 3323,

    1^11 + ... + k^11 = k^2 (k+1)^2 g(k) / 24
      = 3 * 11^2 * 67^2 * 149^2 * 367 * 487^2 * 619 * 701 * 829 * 3323^2 * 3559 * 6121 * 17851 * 20717
        * 54193^2 * 235537 * 465929 * 1557103 * 4598233,

where g(k) = 2k^8 + 8k^7 + 4k^6 - 16k^5 - 5k^4 + 26k^3 - 3k^2 - 20k + 10. Every prime factor is below k,
so the sum divides (k!)^11. No smaller k > 1 works.

## Why the term was out of reach, and the idea

The program in the entry tests each k with one modular power of k!. But the sum is a polynomial in k
(Faulhaber), and a prime q > k that divides it can never divide k!. So k can only work if k + 1 is
composite and the 57-digit number g(k) has no prime factor above k, which is rare (g is irreducible of
degree 8). Such k can be found without factoring anything:

- **Sieve.** For each prime p below the search limit, find the roots of g modulo p, lift them to the
  prime powers that can occur, and add log p along each residue class. The k where the logarithms add up
  to log g(k) are the only candidates. Up to 1.1 * 10^7 there are 53 of them, 10892793 included (the linear
  factors k and k + 1 are sieved in the same way), and each is settled by an exact factorisation.
- **Batch test (independent).** Let P be the product of all primes up to 10892793. With a product tree
  and a remainder tree compute P mod g(k) for every k at once; then g(k) has no prime factor above
  10892793 exactly when g(k) divides (P mod g(k))^256. This uses no roots and no sieve. It leaves 108
  candidates below 10892793 plus 10892793 itself. Each of the 108 is rejected either because k + 1 is
  prime or by an explicit common factor of g(k) with the product of the primes between k and 10892793.

Both searches end with the same single survivor.

## What is proved, and how

- *10892793 satisfies the definition*: computed literally in `check.py` (the sum of the 11th powers as an
  exact integer, k! reduced modulo it, then the 11th power), and again from the factorisation above.
- *No smaller k does*: for every k from 2 to 10892792 the batch test either shows that g(k) has a prime
  factor above 10892793, which is above k, or produces one of the two rejections above. In all cases a
  prime larger than k divides the sum: it divides k + 1 or g(k), and for k >= 4 it is larger than 3, so
  the division by 24 does not remove it (`check.py` tests k = 2 to 60 literally). The sieve reaches the same conclusion by a different route and
  also reproduces a(8) = 89037 and a(10) = 668073 as the first hits for n = 8 and n = 10.

## Check

    python check.py                               (about one minute)
    python search_sieve.py 11 1.1e7               (about two minutes; python-flint, numba, sympy)
    python search_batch.py 2 5500000 10892793     (three minutes; python-flint)
    python search_batch.py 5500000 10892794 10892793

`check.py` finds a(1) to a(7) and a(9) by brute force from the definition, confirms that the definition
holds at the listed a(8) and a(10), tests k = 10892793 literally, and prints the factorisation. Outputs
are in `check.log`, `search_sieve.log` and `search_batch.log`.

## Limits

- Both searches were written by the same AI agent in one session. They share no code and no method, but
  nobody else has repeated them.
- The batch test relies on python-flint (FLINT) big-integer arithmetic and the sieve on its root finding
  modulo p; the final statement for k = 10892793 does not (plain Python integers).
- Nothing is claimed about a(12). For even n the sum has the factor 2k + 1 next to a factor of degree
  n - 2, and the same search would have to go very much further.

## Novelty check

Performed 2026-11-11: the full revision history of A125314 (6 revisions, 2007 to 2015, one page, no
discussion beyond two server notes) and the draft page (no pending edit); the entry has no b-file, no
links and no cross-references; a search of the complete OEIS term dump for 10892793 (no sequence
contains it); an in-depth web search for the A-number together with 10892793 (nothing); the file list
of Google DeepMind's formal-conjectures and the local copy of the Epoch AI "OEIS Open" list (A125314 is
in neither); the omega-institute project's issues and code (no mention).

## Credit

The sequence is due to Alexander Adamchuk; a(8) to a(10) and the bound a(11) > 1091730 are due to
Robert G. Wilson v (2007).
