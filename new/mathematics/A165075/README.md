# A165075: "all terms are multiples of 48" holds for odd lengths and fails for even ones

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS.

## The entry

[A165075](https://oeis.org/A165075) (Joseph Myers, 2009): fixed points of the base-7 Kaprekar map, which
sends n to (its base-7 digits in descending order) minus (the same digits in ascending order). It carries
the remark: "All terms appear to be multiples of 48, and more precisely congruent to -48 (mod 14*48),
except for the initial 0." (M. F. Hasler, 17 July 2026)

One day later (18 July 2026) the list of terms was extended to a(17) = 77852854787906052.

## Result

The remark is contradicted by that seventeenth term, and by the entry's own table of 4081 terms:

- a(17) = 77852854787906052 = 65544331066553322111 in base 7 is a fixed point and is 36 modulo 48
  (and 36 modulo 672). It is the first term with an even number of base-7 digits (20).
- a(25) = 3896245168015046400 is a multiple of 48 but is 288 modulo 672.
- Of the 4080 nonzero terms in the table, 1342 are not multiples of 48, and 1785 are not congruent to -48
  modulo 672. Those 1785 are exactly the terms with an even number of base-7 digits; their greatest common
  divisor is 12.

What is true:

- **Proved:** if n has an odd number of base-7 digits, its Kaprekar image is a multiple of 48. So every
  term with an odd number of digits is a multiple of 48.
- **Proved:** every term is a multiple of 12, and 12 cannot be improved (it is the greatest common divisor
  of the even-length terms in the table).
- **Observed, not proved:** all 2295 terms in the table with an odd number of digits are congruent to -48
  modulo 672.

## Proof of the odd-length statement

Let n have L digits and let d_0 >= d_1 >= ... >= d_(L-1) be its digits in descending order. Then

    K(n) = sum over i of (d_i - d_(L-1-i)) * 7^(L-1-i)
         = sum over i < (L-1)/2 of (d_i - d_(L-1-i)) * (7^(L-1-i) - 7^i),

by pairing position i with position L-1-i. Each bracket is 7^i * (7^(L-1-2i) - 1). If L is odd, the
exponent L-1-2i is even, and 7^2 - 1 = 48 divides 7^(even) - 1. ∎

If L is even the exponent is odd and 7^(odd) - 1 is 6 modulo 48, so for a general n only divisibility by 6
follows.

*Fixed points are multiples of 12.* For odd L this is contained in the above. Let L be even and K(n) = n.
Since 7 is 1 modulo 6, n is congruent to its digit sum s modulo 6; and n = K(n) is a multiple of 6; so s is
even. Modulo 12 each bracket 7^i * (7^(odd) - 1) is 6, so
K(n) = 6 * sum over i < L/2 of (d_i - d_(L-1-i)) modulo 12, and that sum has the parity of s. Hence
n = K(n) is 0 modulo 12. ∎

The same argument in base 5 and base 9 gives 8 and 16 for every fixed point, in agreement with the
unconditional remarks in the sister entries A165036 and A165114 (not checked numerically here); base 7 is
the odd one out because 7^(odd) - 1 is only twice an odd number.

## Check

    python check.py

- part 1: an independent enumeration runs through every multiset of base-7 digits of each length up to 40
  and keeps those reproduced by the map: 211 fixed points, identical to the first 211 terms of the
  published table. It reports a(17), and that a(17) is the first term that is not a multiple of 48;
- part 2: all 4081 terms of the table (`b165075.txt`, by Joseph Myers, copied from the entry) are re-tested
  with exact integers against the definition, and the residues are tabulated by parity of the length;
- part 3: the proved statement is tested on the Kaprekar images of 200,000 random numbers.

Output in `check.log` (under half a minute).

## Limits

Beyond 40 digits the terms are taken from the published table and only re-tested, not re-enumerated. The
congruence modulo 672 for odd lengths is an observation on that table.

## Novelty check

Performed 2026-11-11:

- both pages of the revision history (revisions 1 to 17, the last on 18 July 2026): the remark was added in
  revisions of 17 July and the longer list of terms the next day; there are no discussion threads and no
  later correction; the draft page has no pending edit;
- the sister entries named in the cross-references (bases 2 to 10) and A165071, A165076, A165078, A008722:
  bases 3, 5, 8 and 9 carry similar remarks by the same author, also dated 17 July 2026; none mentions the
  failure in base 7. The earlier agent tested the remarks for bases 3, 5 and 9 on shorter ranges and found
  no failure; they were not re-tested here;
- an in-depth web search with the sequence number, "multiples of 48" and the seventeenth term, and Zenodo's
  record search for the sequence number: nothing;
- Google DeepMind's formal-conjectures file list, Epoch AI's OEIS Open list and the omega-institute
  project: no mention.

The counterexample is in the entry's own data, so anyone reading the entry closely can see it; no record
of anyone pointing it out was found.

## Credit

The table of terms is Joseph Myers's; the remark is M. F. Hasler's. For the structure of these fixed
points in odd bases see A. Kay, "Fixed Points and Cycles of the Kaprekar Transformation: 1. Odd Bases",
Journal of Integer Sequences 25 (2022), Article 22.6.7. Its text was searched by keyword, not read in
full: it classifies fixed points and cycles by their digit counts and, as far as that search shows, states
no divisibility property of the fixed points.
