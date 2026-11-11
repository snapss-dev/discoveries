# Euler-product constants: wrong final terms in A175639 and in four continued fractions (A078076, A078077, A078086, A078088)

Status: **verified**, **new?** (2026-11-11). Five errata in entries, not new mathematics. Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

Five OEIS entries for constants defined by products over the primes end in terms that do not belong to
the constant. In three of them the listed continued fraction is exactly the continued fraction of the
constant cut off after 98 decimal places, which is how many decimals the companion entries list.

| entry | what it lists | terms listed | first wrong term | printed | correct |
|---|---|---|---|---|---|
| [A175639](https://oeis.org/A175639) | digits of Taniguchi's constant, Prod_p (1 - 3/p^3 + 2/p^4 + 1/p^5 - 1/p^6) | a(0..104) | a(99) | 8,8,8,3,2,8 | 3,3,0,6,7,7 |
| [A078076](https://oeis.org/A078076) | continued fraction of Prod_p (1 - 1/(p^2-2)) | a(0..91) | a(91) | 3 | 2 |
| [A078077](https://oeis.org/A078077) | continued fraction of Prod_p (1 + 1/(p^2+p-1)) | a(0..90) | a(83) | 3,7,1,1,3,40,6,1 | 1,1,3,14,1,1,2,2 |
| [A078086](https://oeis.org/A078086) | continued fraction of Prod_p (1 - 1/(p^2 (p^2-1))) | a(0..90) | a(85) | 2,2,3,2,6,1 | 1,8,5,1,35,1 |
| [A078088](https://oeis.org/A078088) | continued fraction of (5 Pi^2/48) Prod_{p>=3} (1 - (p+2)/p^3) | a(0..94) | a(94) | 96 | 19 |

"Printed" and "correct" give all terms from the first wrong one to the end of the DATA line.

## The entries

**A175639** (R. J. Mathar, Aug 01 2010; "More digits from Jean-François Alcover, Apr 15 2016"). The
105 digits now listed were entered in revision #13 (Alcover, Apr 15 2016) together with a Mathematica
program that sums prime zeta values with `NSum`. The last six digits are wrong:

    printed  ...22933484616 888328
    correct  ...22933484616 330677 048416995587689...

The entry's PARI line, `prodeulerrat(1-3/p^3+2/p^4+1/p^5-1/p^6)` (Amiram Eldar, Mar 04 2021), returns the
correct digits; the difference from the DATA line was not noted in the entry.

**A078076, A078077, A078086, A078088** (Benoit Cloitre, Dec 02 2002) belong to a family of fifteen
continued fractions, A078076 to A078090, for the prime products whose decimal expansions are in
A065463 to A065493. Each of the four has a PARI line `contfrac(prodeulerrat(...))` added by Amiram Eldar
in March 2021, which returns the correct terms. A078088 also carries the note "Corrected from 2nd term
on by R. J. Mathar, Sep 19 2008". The other eleven entries of the family agree with their own PARI programs
(run here at 150 digits) in every listed term.

The correct continuations, with the terms that follow:

    A078076  a(91..)  2, 5, 4, 1, 3, 1, 1, ...
    A078077  a(83..)  1, 1, 3, 14, 1, 1, 2, 2, 1, 5, 3, 1, 1, 1, ...
    A078086  a(85..)  1, 8, 5, 1, 35, 1, 4, 1, 1, 8, 1, 1, ...
    A078088  a(94..)  19, 3, 1, 1, 80, 2, 1, ...

## Why

A continued fraction computed from a decimal string is only valid as far as the string determines it.
For A078076, A078077 and A078086 the listed terms are, term for term, the continued fraction of the
rational number obtained by truncating the constant to 98 decimal places (`check.py` verifies this).
The companion decimal entries A065481, A065489 and A065471 each list 98 decimal places. With 98 decimals only about the
first 83 to 91 partial quotients are determined; the terms after that are those of the truncated
decimal, not of the constant. The same test does not reproduce the last term of A078088 for any
truncation length between 60 and 140, so the origin of its 96 is not known.

A078082 is the continued fraction of Prod_p (1 - 1/(p (p+1))), the reciprocal of the A078077 constant,
so its terms are those of A078077 shifted by one place. A078082 is correct throughout, and so already
shows the true A078077 a(83..89) = 1, 1, 3, 14, 1, 1, 2 as its a(84..90).

## Check

    python check.py

evaluates each product with certified ball arithmetic (Arb, through python-flint): the primes below 100
directly, and the rest from the series log(N/D)(x) = sum l_n x^n and the prime zeta function
P(n) = sum_k mu(k)/k log zeta(kn), with every truncation enclosed in the ball. The result is an interval
of width below 10^-200 that contains the constant. Digits and partial quotients are accepted only if
both ends of the interval give the same ones. A second evaluation with mpmath, coded separately and
using mpmath's own prime zeta function, must fall inside the interval. Output in `check.log`; it runs in
about fifteen seconds.

A third, unrelated implementation, PARI/GP 2.17.4 `prodeulerrat` at 220 digits (`pari_check.gp`, output
in `pari_check.log`), gives the same 190 digits
of Taniguchi's constant and, for each of the four continued fractions, the same first 108 partial
quotients.

The DATA lines in `check.py` are as served by oeis.org on 2026-11-11.

## Limits

- The two evaluations in `check.py` use the same decomposition of the product (they differ in the
  arithmetic and in the zeta and prime zeta code). PARI's `prodeulerrat` is the independent method.
- The companion decimal entries were compared with their PARI programs only, not with Arb; all agreed.
- No claim is made about who computed what in 2002; the 98-decimal explanation is an exact match of the
  listed terms, not a documented history.

## Novelty check

Performed 2026-11-11.

- Live entries re-fetched from oeis.org; all five still show the terms above (A175639 revision #49 of
  Sep 19 2026; A078076 and A078077 #9, A078086 #9, A078088 #11, all of Jul 05 2024).
- Every page of the five revision histories with their discussion threads, and the five draft pages (no
  pending edit). A175639: 49 revisions; threads about a MathWorld link (2011) and a name change (Sep
  2026). The four continued fractions: 9 to 11 revisions; the only threads are "Continued fraction offset
  consistency" (Andrew Howroyd, Jul 05 2024). None mentions wrong terms.
- The complete OEIS term dump was searched for the leading terms: no duplicate entry for any of the five
  (A078082, discussed above, is the reciprocal).
- In-depth web searches with the A-numbers and with 100 digits of Taniguchi's constant: other tables give
  18 digits; no report of an error.
- Google DeepMind formal-conjectures file list, Epoch AI's OEIS Open list, and the omega-institute
  project (issue and code search): no mention of any of the five.

Digits of other OEIS constants are being corrected by contributors at present (for example A341641,
corrected on Oct 19 2026), so these entries may be fixed independently at any time.
