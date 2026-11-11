# English Wikipedia: four integer lists that differ from recomputation (prime quadruplets, perfect totient numbers, divisors of 1002, happy primes)

Status: **verified** by recomputation; no earlier report found on the talk pages (2026-11-11). For
items 1, 2 and 4 the correct values are in the OEIS entries the articles themselves cite, so nothing
here is new mathematics: the finding is that the articles disagree with their own sources. Produced with AI assistance; see the
repository README. Nothing was edited or reported.

## What was done

Every comma-separated list of seven or more integers, and every table row or column of integers, in
4,464 English Wikipedia articles on number theory, combinatorics, special functions and individual
numbers was compared with the local OEIS mirror. 3,188 lists (38,881 terms) occur verbatim in an OEIS
entry. 120 lists matched an entry except for one or two insertions, deletions or substitutions. Those
whose only difference was at the first or last element (usually a row label in a table) were set aside
by rule; the rest, about 40, were inspected one by one. Most are legitimate (a different sequence, an
excluded case, a different convention). Four are errors, each confirmed by computing the numbers from the definition. Revision ids are those current
on 2026-11-11.

## 1. Prime quadruplet: there are 26 five-digit prime quadruplets, not 27

Article [Prime quadruplet](https://en.wikipedia.org/wiki/Prime_quadruplet), revision 1381299776:

> The number of prime quadruplets with n digits in base 10 for n = 2, 3, 4, ... is
> 1, 3, 7, 27, 128, 733, 3869, 23620, 152141, 1028789, 7188960, 51672312, 381226246, 2873279651
> (OEIS A120120).

The fourth term should be 26, as in A120120. The 26 quadruplets {p, p+2, p+6, p+8} with five digits
start at

    13001, 15641, 15731, 16061, 18041, 18911, 19421, 21011, 22271, 25301, 31721, 34841, 43781,
    51341, 55331, 62981, 67211, 69491, 72221, 77261, 79691, 81041, 82721, 88811, 97841, 99131.

The other terms up to eight digits (1, 3, 7, 128, 733, 3869) were recomputed and agree.

History: the article had 26 from at least 2013 until 2020-05-24, when revision 958582482 changed it to
27 with the edit summary "Fixed mistake". It has read 27 for six years.

## 2. Perfect totient number: the exponent 885 is missing

Article [Perfect totient number](https://en.wikipedia.org/wiki/Perfect_totient_number), revision
1379070377:

> Venkataraman (1975) found another family of perfect totient numbers: if p = 4 × 3^k + 1 is prime,
> then 3p is a perfect totient number. The values of k leading to perfect totient numbers in this way
> are 0, 1, 2, 3, 6, 14, 15, 39, 201, 249, 1005, 1254, 1635, ... (OEIS A005537).

Between 249 and 1005 the list omits k = 885. The number 4 × 3^885 + 1 has 423 digits and is prime;
`check.py` proves it with a Lucas test (p − 1 = 2² × 3^885 is completely factored) and then verifies
directly that the iterated totients of 3p sum to 3p. A005537 lists 885, and its revision history shows
885 in the data in the earliest revisions kept (2005 and before), so the omission is not inherited from
an older state of that entry. The list has been in the
article in this form since 2007-02-07 (revision 106363306).

## 3. 1002 (number): the divisor 3 is missing

Article [1002 (number)](https://en.wikipedia.org/wiki/1002_(number)), revision 1384107444, infobox:
"divisor = 1, 2, 6, 167, 334, 501, 1002". Since 1002 = 2 × 3 × 167, the divisors are 1, 2, 3, 6, 167,
334, 501, 1002.

The infobox divisor lists, factorizations and base representations of 403 number articles were checked
the same way (294 fields that could be parsed); this is the only wrong one.

## 4. List of prime numbers: 1039 appears twice among the happy primes

Article [List of prime numbers](https://en.wikipedia.org/wiki/List_of_prime_numbers), revision
1383567456, section "Happy primes": "... 937, 1009, 1033, 1039, 1039, 1093". A duplicated entry; the set
of numbers is right.

## Check

    python check.py

reads `wikitext_excerpts.json` (the quoted wikitext with its revision id) and recomputes all four
items: the quadruplet counts by a sieve to 10^8 and, independently, by a direct primality test up to
six digits; the exponents k < 1700 with two libraries, plus the primality proof for k = 885; the
divisors of 1002; the happy primes below 1100. About 40 seconds. Output in `check.log`.

## Limits

- Wikipedia changes; the findings are tied to the revision ids given.
- The scan only sees lists it can parse (comma-separated integers, and plain integer table cells), and
  only compares against OEIS entries that share four consecutive terms with the list. 1,690 lists
  matched no OEIS entry at all and were not examined; an error in the first few terms of a list would
  land there.
- The quadruplet counts beyond eight digits were not recomputed.
- For item 2 the larger printed exponents (1005, 1254, 1635) were confirmed as probable primes by two
  libraries, not proved.

## Novelty check

Performed 2026-11-11. For "Prime quadruplet" and "Perfect totient number": the revision that introduced
the current text was located by bisection over the revision history and the neighbouring revisions were
read; the current talk page was fetched and searched; a full-text search of the talk pages and archives
was run for the sequence numbers and the key values (A120120, "27, 128"; A005537, 885). Nothing found.
An in-depth web search for the two versions of the quadruplet list found the article, its copies, and
an older mirror that still shows 26; no report of the discrepancy.
For "1002 (number)" and "List of prime numbers" only the talk-page search was done. The correct values
have been in OEIS A120120 and A005537 throughout (their revision histories, 20 and 79 revisions, were
fetched and searched for the two term strings; neither has a pending draft); credit for them belongs to the contributors of those
entries.
