# A202194 and A202202: binary arrays avoiding 001 and 101

Status: **rediscovery**. Credit: Christian Krause. Produced with AI assistance; see the repository
README.

## What was found here

On 2026-11-11 an agent proved that the number of R x C binary arrays with no consecutive 001 or 101 in
any row or column is

    2 R C binomial(R + C - 2, R - 1).

The argument: a row avoids both patterns exactly when its entries from the second one on are
non-increasing, and likewise for columns, so the array splits into a free corner entry (2 choices), the
rest of the first row (C choices), the rest of the first column (R choices), and a block that is
non-increasing along rows and down columns (binomial(R + C - 2, R - 1) choices).

This formula would settle the conjecture in [A202194](https://oeis.org/A202194) (Michael Somos, 2020),
which is the case R = C, and the "Empirical" formulas of the table [A202202](https://oeis.org/A202202)
(R. H. Hardin, 2011). Both entries still carry those words.

## Who had it first

Christian Krause, 24 June 2026: a proof file attached to the neighbouring entry
[A202195](https://oeis.org/A202195) ("Proof of formula") establishes a(n) = 2 w (n+2) binomial(n+w, w-1)
for arrays with n + 2 rows and w columns by the same decomposition. It is stated for the columns
A202195 to A202201 (w = 3 to 9), but the argument does not depend on w, and with R = n + 2, C = w it is
the formula above.

## How it was missed at first

The check read A202194 and A202202 and the first page of their histories. The proof sits in a file
linked from a different entry of the same family, which only a reading of the cross-referenced entries
finds.

## Small remainders

- Nobody appears to have recorded that Krause's argument settles the conjecture in A202194 and the
  empirical lines in A202202.
- The general formula printed in A202202, "T(n,k)=2*(k+2)*(n+2)*product{i=2..k+2}(n+i)/n!", gives 216 for
  T(1,1), whose listed value is 108; dividing by (k+1)! instead of n! gives the correct formula.

## Check

    python check.py 7

counts the arrays straight from the definition for all 3 <= R, C <= 7 and compares with the formula.
Output in `check.log`.
