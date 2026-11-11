# A086651: a(6k+3) = 2, with a closed form for every term

Status: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A086651](https://oeis.org/A086651) (John W. Layman, 2003): "a(1)=1, a(2)=1 and for n > 2, a(n) is the
smallest positive integer such that the third-order absolute difference gives the Fibonacci numbers".
It begins 1, 1, 2, 5, 5, 10, 23, 23, 2, 57, 57, 146, 379, 379, 2, ... and carries the comment
"It appears that a(6k+3) is always 2. Is this easy to prove?" A recurrence and generating function were
added in 2012, without proof.

**Reading of the definition.** Write d(j) = |a(j+1) - a(j)|. The listed terms are reproduced by the rule

    a(n) is the smallest positive integer with | d(n-1) - d(n-2) | = F(n-1),

where F(1) = F(2) = 1, F(3) = 2, ... (the entry counts the sequence itself as the first order). The check
script confirms that this rule gives all 21 listed terms.

## Result

For every m = 6k + 3 with k >= 0:

    a(m) = 2,
    a(m+1) = a(m+2) = 2 + F(m+1),
    a(m+3) = 2 + F(m+3),
    a(m+4) = a(m+5) = 2 + F(m+5).

Consequently a(n) = 18 a(n-6) - a(n-12) - 32 for n >= 15, which implies the recurrence and generating
function listed in the entry.

## Proof

At each step the rule leaves at most two values for the new difference, d(n-1) = d(n-2) + F(n-1) or
d(n-2) - F(n-1) or F(n-1) - d(n-2), of which only non-negative ones count, and then a(n) = a(n-1) + d(n-1)
or a(n-1) - d(n-1), of which the smallest positive one is taken.

Claim H(m), for m = 6k + 3: a(m) = 2 and d(m-1) = F(m-1). H(3) holds: d(1) = 0 forces d(2) = 1 = F(2),
and a(3) = 2. Assume H(m). The facts used below are F(m) >= 2 and F(m+1) >= 3, true for m >= 3.

| n | new difference | candidates for a(n) | result |
|---|---|---|---|
| m+1 | d(m) = F(m-1) + F(m) = F(m+1); the other choice F(m-1) - F(m) is negative | 2 + F(m+1), or 2 - F(m+1) < 1 | a(m+1) = 2 + F(m+1) |
| m+2 | d(m+1) = 0 or 2F(m+1) | a(m+1); a(m+1) + 2F(m+1); a(m+1) - 2F(m+1) = 2 - F(m+1) < 1 | a(m+2) = a(m+1), d(m+1) = 0 |
| m+3 | d(m+2) = F(m+2) | 2 + F(m+1) + F(m+2); or 2 + F(m+1) - F(m+2) = 2 - F(m) < 1 | a(m+3) = 2 + F(m+3) |
| m+4 | d(m+3) = F(m+2) + F(m+3) = F(m+4); the other choice is negative | 2 + F(m+3) + F(m+4); or 2 + F(m+3) - F(m+4) = 2 - F(m+2) < 1 | a(m+4) = 2 + F(m+5) |
| m+5 | d(m+4) = 0 or 2F(m+4) | a(m+4); a(m+4) + 2F(m+4); a(m+4) - 2F(m+4) = 2 - F(m+2) < 1 | a(m+5) = a(m+4), d(m+4) = 0 |
| m+6 | d(m+5) = F(m+5) | 2 + F(m+5) + F(m+5); or 2 + F(m+5) - F(m+5) = 2 | a(m+6) = 2, d(m+5) = F(m+5) |

The last row is H(m+6). ∎

The recurrence follows from F(j+6) = 18 F(j) - F(j-6): each of the six residue classes has the form
2 + F(6k + c), so a(n) - 2 = 18 (a(n-6) - 2) - (a(n-12) - 2).

## Check

    python check.py 3000

simulates the rule (all candidates enumerated at each step) and compares with the closed form. Output
is in `check.log`: the 21 listed terms are reproduced, a(6k+3) = 2 throughout, and the closed form and
both recurrences hold up to n = 3000.

## Novelty check

The published entry and its complete revision history (seven revisions, 2003 to 2021) contain no proof.
A web search for the sequence number found nothing further. Checked 2026-11-11.

## Weak point

The result depends on the reading of "third-order absolute difference" given above. It reproduces every
listed term, but the entry does not spell the rule out.
