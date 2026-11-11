# A332102: a(n) = round(n / log(3/2) + 3) fails at a 1614-digit n

Status: counterexample **verified**, **new?** (2026-11-11). Whether it is the smallest is not proved.
Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A332102](https://oeis.org/A332102) (M. F. Hasler, 2020): the least m > 0 with
2 m^n <= sum_{k < m} k^n. It begins 3, 5, 8, 10, 13, 15, 18, 20, ... and carries the line
"Conjecture: a(n) = round(n/log(3/2) + 3)."

## Result

The conjecture is false. Let n be the 1614-digit number in `counterexample_n.txt` (it begins
270423632827570868..., and is the denominator of the convergent of index 3143 of the continued
fraction 2/log(3/2) = [4; 1, 13, 1, 5, 5, 2, 2, 9, ...]). With F = round(n/log(3/2) + 3) and
S(M, n) = sum_{k=1}^{M-1} (k/M)^n:

    S(F, n)   - 2  =  -2.0978e-3231  < 0,
    S(F+1, n) - 2  =  +3.6477e-1614  > 0,

so a(n) = F + 1. (S(M, n) increases with M, because k/M <= (k+1)/(M+1) term by term.)

## Why

This is the same mechanism as in
[A072633](../A072633-smallest-counterexample/README.md), with 2 in place of 1 on the left. The terms
(1 - j/M)^n behave like (2/3)^j when n/M is near log(3/2), and the real crossover is

    n = log(3/2) * (M - 5/2 + c/M + ...),      c = 15 log(3/2) - 73/12 = -0.0013567.

So the formula fails only when n/log(3/2) lies within about 0.0014/M below a half-integer, which forces n
to be (a multiple of) a convergent denominator of 2/log(3/2) with the right parity and side. The constant
c was obtained by formal expansion and matches a numerical fit to seven digits; it explains where to
look, and the certificate above does not depend on it.

## Check

    python check.py

certifies both inequalities with Arb ball arithmetic at 17,500 bits (about 19,500 terms each, with a
rigorous bound on the tail), and confirms that the formula agrees with the definition for n <= 300.
About half a minute. Output in `check.log`. The agent that found the number confirmed it separately in
PARI/GP at 5,142 digits.

## Limits

- **Smallest?** Under the expansion above, yes: the only earlier candidate, a 489-digit convergent
  denominator, was certified not to be a counterexample. But there is no explicit error bound for the
  expansion here, so minimality is not proved (compare the A072633 page, where it is).
- A direct check found no failure for n <= 3000.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads (a 2020 exchange
there concerns a different, withdrawn recurrence); the draft page (no pending edit); an in-depth web
search with the sequence number; Epoch AI's OEIS Open conjecture list; and the omega-institute project's
issues and code. None mentions a counterexample.
