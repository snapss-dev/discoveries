# A261114 and A333507: two decimal expansions with wrong digits, settled by integer arithmetic

Status: **verified**, **new?** (2026-11-11). Two errata in entries, not new mathematics. Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

Both constants can be computed with exact integers, so anyone can confirm the digits below without
trusting floating point.

| entry | constant | terms listed | first wrong term | printed | correct | extent |
|---|---|---|---|---|---|---|
| [A261114](https://oeis.org/A261114) DATA | Sum_{n>=0} 1/(n!)^n | a(1..87) | a(43) | 6 | 5 | the 45 terms a(43..87) are not digits of the constant |
| A261114 b-file | same | a(1..440) | a(43) | 6 | 5 | 357 of the 398 terms from a(43) on differ from the true digit |
| [A333507](https://oeis.org/A333507) DATA | 1 - 365!/(342! * 365^23) | a(0..119) | a(84) | 2 | 3 | one extra digit inserted; a(85..119) are the true a(84..118) |

## A261114: Sum_{n>=0} 1/(n!)^n

The entry (Daniel Suteu, Sep 20 2015) gives

> 2.2546326437516075174660917619423624873602862427910816970143008652092...

and links a b-file "Table of n, a(n) for n = 1..440" whose first 87 terms are the DATA terms.

The true value is

    2.25463264375160751746609176194236248736028 58728774975406353663042726797704291927465...

The listed digits are right for 42 terms (the leading 2 and 41 decimals) and wrong from a(43) on. The
number printed in the b-file exceeds the true sum by 3.70 * 10^-43, so none of its digits after the
42nd carries information about the constant; 357 of those 398 digits differ from the true digit, which
is the rate expected of unrelated digits. The correct a(1..440) are printed in `check.log`.

Why this is certain: the partial sum up to n = 30 is an exact rational number, and since each term is at
most half the one before, the rest of the series is below 2/(31!)^31 < 10^-1000. The digits therefore
follow from one integer division.

The entry's own programs do not agree with its data. The PARI line `suminf(k=0, 1/k!^k)` (Michel
Marcus, Sep 20 2022) returns the true value; the editing note that came with it says "suminf gives a
better result than sumpos; I don't know why", and the data were left as they were. The Mathematica line
`N[Sum[1/((n!)^n), {n, 0, Infinity}], 120]` (Michael De Vlieger, Sep 22 2015) was not run here.

## A333507: the birthday probability for 23 people

The entry (Kritsada Moomuang, Mar 25 2020) is the "Decimal expansion of
1 - ((365!) / ((365 - 23)! * 365^23))", the probability that at least two of 23 people share a birthday. A
comment by Charles R Greathouse IV (Jul 11 2020) notes: "This is a rational number; numerator and
denominator both have 53 digits." Indeed the value is

    38093904702297390785243708291056390518886454060947061 / 75091883268515350125426207425223147563269805908203125.

Its expansion and the listed terms, from a(80):

    correct a(80..119):  5992 331680537053201186483284776542468600
    printed a(80..119):  5992 2 33168053705320118648328477654246860

The DATA line has one extra digit 2 at a(84). Every later term is the true digit of the position before
it, so 32 of the 36 terms a(84..119) are wrong as listed. The extra digit is already in the first
submitted draft (revision #2, Mar 25 2020) and was never changed. The entry's Mathematica line
`RealDigits[1- ((365!) / ((365 - 23)! * 365^23)), 10, 120]` works on an exact rational (it was not run
here), which points to a slip in copying the digits.

## Check

    python check.py

computes both constants three ways each (exact rationals; Arb ball arithmetic through python-flint;
mpmath, or for A333507 a long division that uses neither factorials nor fractions), requires the three
to agree, and compares with the DATA lines and with `b261114.txt`, both as served by oeis.org on
2026-11-11. Output in `check.log`. The entries' own PARI lines, run at 500 digits in PARI/GP 2.17.4
(`pari_check.gp`, output in `pari_check.log`), give the same digits.

## How these were found

All 14474 entries with keyword `cons` or `cofr` and a name about a decimal expansion, a continued
fraction or a constant, in a local copy of the OEIS (complete to about A352000), were screened. Where a
small translator could parse it, the closed form in the name, the entry's Mathematica expression and the
entry's PARI program were each evaluated to about 40 digits beyond the listed terms and compared
with the DATA lines. For 9767 entries at least one evaluation reproduced every listed term (median 99
terms, about 950000 terms in all); for 6709 of them two or more did. 4281 entries could not be evaluated. The
disagreements that began after three or more correct terms were examined one by one; nearly all were
programs less accurate than the data they sit beside, and 23 were left unsettled (see Limits). These two entries and the five on the page
"Euler-product constants" are the ones where the data are wrong. The b-files of 184 entries with a closed form (those of at most 1000 terms; 176240 digits) were also
compared in full; all agreed.

## Limits

- Only the DATA lines were screened for most entries; b-files were fetched for A261114 and for the
  184 entries mentioned above. Entries after about A352000 were not screened.
- The screen cannot see an error in an entry whose definition the translator could not parse (roots of
  equations, most integrals, slowly convergent series).
- A confirmed entry was confirmed by its own name or program, evaluated by mpmath or PARI at higher
  precision; that is a screen, not a certified computation. Only the entries on these two pages were
  recomputed with ball arithmetic.
- For 23 entries the PARI program in the entry and the DATA line disagree and it was not settled which
  is right (prime sums, multiple integrals and iterations where the program is probably the weaker
  side). Twelve entries end in a digit that is rounded up instead of truncated; these were not counted
  as errors.
- Why the A261114 digits are wrong was not established. An error of 3.7 * 10^-43 is what a computation
  carried at about 43 significant digits and printed to 440 would give, but that is a guess.

## Novelty check

Performed 2026-11-11.

- Live entries re-fetched from oeis.org: both still show the digits above (A261114 revision #41 of
  Sep 20 2022, A333507 revision #19 of Jul 27 2022).
- Every page of both revision histories, with the discussion threads, and both draft pages (no pending
  edit). A261114: 41 revisions; the threads concern recycling the A-number, the b-file offset
  (R. J. Mathar, Sep 30 2015) and the PARI remark quoted above; none says the digits are wrong.
  A333507: 19 revisions; the threads ask for an example line and a cross-reference.
- The complete OEIS term dump was searched for the leading digits of both constants: no other entry
  lists either constant.
- In-depth web searches with the A-numbers and the digit strings: no report of an error.
- Google DeepMind formal-conjectures file list, Epoch AI's OEIS Open list, and the omega-institute
  project (issue and code search): no mention of either entry.

Cross-referenced entries (A036740, A014088, A343015) were not read beyond their names.
