# A202194 and A202202: binary arrays avoiding 001 and 101

Status: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entries

[A202202](https://oeis.org/A202202) (R. H. Hardin, 2011) is the table T(n, k) = number of
(n+2) x (k+2) binary arrays avoiding the patterns 001 and 101 in rows and columns (three consecutive
entries, read left to right and top to bottom). [A202194](https://oeis.org/A202194) is its diagonal:
108, 640, 3500, 18144, ...

Both carry only empirical or conjectured formulas: an "Empirical" recurrence (2011) and
"Conjecture: a(n) = 4*(n+2)^2 * (2*n+1)!/(n! * (n+1)!)" (Michael Somos, 2020) in A202194, and
"Empirical" column formulas in A202202.

## Result

The number of R x C binary arrays (R, C >= 1) with no consecutive 001 or 101 in any row or column is

    2 R C binomial(R + C - 2, R - 1).

With R = C = n + 2 this is 2 (n+2)^2 binomial(2n+2, n+1) = 4 (n+2)^2 (2n+1)! / (n! (n+1)!), which is the
conjectured formula for A202194. In the indexing of A202202, T(n, k) = 2 (n+2)(k+2) binomial(n+k+2, n+1).

## Proof

A row contains 001 or 101 exactly when it contains "01" starting at its second position or later, because
the entry before that "01" can be anything. So a row avoids both patterns exactly when its entries from
the second one on are non-increasing; its first entry is unconstrained by the row. The same holds for
columns.

The conditions therefore are: (a) every row, restricted to columns 2..C, is non-increasing; (b) every
column, restricted to rows 2..R, is non-increasing. These split the array into four independent parts:

| part | constraint | choices |
|---|---|---|
| the corner entry (1,1) | none | 2 |
| the rest of row 1 | non-increasing (from its row only) | C |
| the rest of column 1 | non-increasing (from its column only) | R |
| the block of rows 2..R and columns 2..C | non-increasing along rows and down columns | binomial(R + C - 2, R - 1) |

The last count is the number of 0/1 fillings of an (R-1) x (C-1) box whose ones form a Young diagram in
the corner, that is, the number of lattice paths across the box. Multiplying gives the formula. ∎

## A typo in A202202

The entry's general formula, "T(n,k)=2*(k+2)*(n+2)*product{i=2..k+2}(n+i)/n!", gives 216 for T(1,1), whose
listed value is 108. Dividing by (k+1)! instead of n! gives the formula above.

## Check

    python check.py 7

counts the arrays straight from the definition (testing every consecutive triple) for all
3 <= R, C <= 7 and compares with the formula. Output in `check.log`.

## Novelty check

The published entries still say "Empirical" and "Conjecture". The first page of each revision history
(the ten most recent revisions, to October 2025) shows no proof; a contributor proved the individual
columns A202195 to A202201 in 2026, not the table or its diagonal. A web search found nothing further.
Older history pages were not read. Checked 2026-11-11.
