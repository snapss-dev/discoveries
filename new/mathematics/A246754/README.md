# A246754: the listed term a(8) is one too large, and so is the formula at n = 8, 52, 200, 226, 849, ...

Status: **verified** (exact integer arithmetic, two programs); no earlier record found (2026-11-11).
Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A246754](https://oeis.org/A246754) (Derek Orr, Nov 15 2014; more terms from Alois P. Heinz, Nov 15 2014):

> Least positive number k such that k^k is at least 10^n digits long.

Data, offset 0: 1, 10, 57, 387, 2890, 22934, 189482, 1611056, **13993960**, 123579654, 1105747503,
10000000000, ... (22 terms). The entry gives a formula, stated without qualification:

> a(n) = ceiling(exp(LambertW(10^n*log(10)))) for n > 0. - Charles R Greathouse IV, Nov 16 2014

and an exact program, `a(n)= my(k=sqrtint(10^n)); while(#digits(k^k)<10^n,k++);k`.

## Result

1. **a(8) = 13993959, not 13993960.** The number 13993959^13993959 has exactly 10^8 = 100000000 decimal
   digits, and 13993958^13993958 has fewer:

       13993958 * log10(13993958) = 99999992.15...
       13993959 * log10(13993959) = 99999999.73...     (floor + 1 = 100000000 digits)
       13993960 * log10(13993960) = 100000007.31...

   The other 21 listed terms agree with the definition.

2. **The formula answers a slightly different question.** A number has at least 10^n digits when it is at
   least 10^(10^n - 1). The formula solves k^k = 10^(10^n), so it returns the least k for which k^k has at
   least 10^n + 1 digits. The formula that matches the definition is

       a(n) = ceiling(exp(LambertW((10^n - 1) * log(10)))).

   The two differ, by exactly 1, for n = **8, 52, 200, 226, 849** and for no other n <= 1000. All 22 listed
   terms agree with the formula as printed, which is how the wrong a(8) fits the entry.

## Why

Write x(T) for the real solution of x * log10(x) = T. The definition asks for ceiling(x(10^n - 1)), the
formula gives ceiling(x(10^n)). Since d(x log10 x)/dx = log10(x) + 1/log(10), the two real numbers differ by
about 1/(log10(x) + 0.434), which is roughly 1/n. The formula is wrong exactly when an integer lies between
them. That has probability about 1/n for each n, so failures should continue forever, at a rate of about
one per factor e in n (five were found below 1000, where this estimate predicts about seven). That
expectation is heuristic.

When x(10^n) is itself an integer (k = 10^j with j * 10^j = 10^n, so n = 1, 11, 102, ...) the two values
agree. A floating-point evaluation of the printed formula can still be off by one at those n.

## A detail from the revision history

The history of the entry shows that on Nov 15 2014 the data briefly held the correct value: revision 13
changed a(8) from 13993960 to 13993959, and revision 15, ten minutes later, changed it back. No reason is
recorded. The formula was added the next day.

## Check

    python check.py            (under a minute; needs python-flint and mpmath)

- Part 1 computes 13993958^13993958 and 13993959^13993959 as exact integers (FLINT) and compares them with
  10^(10^8 - 1) and 10^(10^8).
- Part 2 computes, for every n from 1 to 1000, the least k with k * log10(k) >= 10^n - 1 (the definition)
  and the least k with k * log10(k) >= 10^n (the formula). Each value k is certified with Arb ball
  arithmetic: the sign of k*log(k) - T*log(10) is decided rigorously at k and at k - 1.
- Part 3 repeats Part 2 with mpmath, sharing no code with Part 2.
- `check.gp` is a second exact computation of Part 1 in PARI/GP (`gp -q check.gp`, about 6 s, needs about
  300 MB of stack); its output is in `check_gp.log`.

## Limits

- For n >= 9 the values are certified through logarithms in ball arithmetic, not by forming k^k.
- The list of n at which the formula fails is complete only for n <= 1000.
- That the formula fails for infinitely many n is not proved.
- Why revision 15 restored 13993960 is not known.

## Novelty check

Done 2026-11-11: all four pages of the revision history of A246754 with every discussion thread (the
threads discuss only how to program the search); the draft page (no pending edit; the latest revision is
#35 of Mar 25 2026, which still lists 13993960); the cross-referenced entries A000312 and A011557; the
complete OEIS term dump (the number 13993959 occurs in no entry); an in-depth web search for the A-number
with 13993959 and 13993960; the file list of Google DeepMind's formal-conjectures; the conjecture list
of Epoch AI's OEIS Open; and an issue and code search of the omega-institute project. None mentions the
discrepancy.
