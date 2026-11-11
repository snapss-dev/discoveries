# A059923 and A207976: two formulas of the form floor(x^n) fail from n = 24 and n = 27

Status: **verified** (exact integer arithmetic); no earlier record found (2026-11-11). Produced with AI
assistance; see the repository README. Not submitted to the OEIS.

## The entries

[A059923](https://oeis.org/A059923) (Rainer Rosenthal, Mar 03 2001): a(1) = 1, and a(n+1) is the smallest
number with a(n+1)^n > a(n)^(n+1). Terms: 1, 2, 3, 5, 8, 13, 20, 31, 48, 74, ... The entry states:

> a(n) = floor(x^n), where x=1.53885131519173... - Paul D. Hanna, Feb 21 2003

[A207976](https://oeis.org/A207976) (Thomas Ordowski, Feb 20 2012): a(1) = 2, and for n > 1, a(n) is the
largest integer such that a(n)^(1/n) is decreasing. Terms: 2, 3, 5, 8, 13, 21, 34, 56, 92, ... The entry
states (added by the author, Apr 20 2012):

> a(n) = 1 + floor(q^n), where q = lim a(n+1)/a(n) = 1.652213...

Neither line is marked as a conjecture. In both cases the constant is the limit of a(n)^(1/n).

## Result

Both formulas are false.

- **A059923.** x = 1.538851315191734898742089155195..., and x^24 = 31097.096..., but a(24) = 31096. The
  formula holds for n <= 23 and fails for n = 24, 30-35, 42-45, 52-54, 57-62, ...: at 106 of the first 300
  values of n. At every failure floor(x^n) = a(n) + 1. The value a(24) = 31096 lies within the range of the
  entry's b-file (n = 1..300) and was among the terms listed in the entry's earliest recorded revision.
- **A207976.** q = 1.652212713506639616678637286048..., and q^27 = 772290.888..., so the formula gives
  772291, but a(27) = 772292. The formula holds for n <= 26 and fails for n = 27, 28, 29, 55, 76, 81,
  85-88, 98, ...: at 35 of the first 300 values of n. At every failure it gives a(n) - 1.
- **Control.** A080869(n) + 1 obeys the same rule as A059923 with first term 2. Its formula,
  a(n) = floor(t^n) - 1 with t = 2.3055... (same author, same date), passes the same test for every
  n <= 300.

## Why

Take A059923. By definition a(n+1) = a(n)^(1+1/n) + theta(n) with 0 < theta(n) <= 1. Let
u(n) = x^n - a(n) > 0. Raising a(n) + u(n) to the power 1 + 1/n gives

    u(n+1) = (1 + 1/n) * a(n)^(1/n) * u(n) - theta(n) + (smaller terms),

so, reading it backwards, u(n) is close to theta(n)/x + theta(n+1)/x^2 + theta(n+2)/x^3 + ... This lies
between 0 and 1/(x - 1). The formula a(n) = floor(x^n) says u(n) < 1.

- If x > 2 then 1/(x - 1) < 1 and the formula cannot fail. That is the situation of A080869 and A080870.
- Here x = 1.5389 and 1/(x - 1) = 1.856. Whenever a few consecutive theta are large, u(n) exceeds 1. This
  first happens at n = 24, and then about a third of the time.

For A207976 the same argument applies with a(n) - q^n in place of u(n) and 1/(q - 1) = 1.533.

What does hold, for all n <= 300: floor(x^n) - 1 <= A059923(n) <= floor(x^n), and
floor(q^n) + 1 <= A207976(n) <= floor(q^n) + 2.

## Check

    python check.py            (about 1 minute, standard library only)

Everything is a comparison of integers. With N = 420:

- a(N)^(1/N) < x <= (a(N) + 2)^(1/N). The lower bound is the definition (a(n)^(1/n) increases). The upper
  bound holds because (a(n) + 2)^(1/n) never increases for n >= 3: by Bernoulli's inequality
  (a + 2)^(1+1/n) >= a^(1+1/n) + 2(1 + 1/n) a^(1/n) >= a^(1+1/n) + 3 >= a(n+1) + 2, using
  (1 + 1/n) a(n)^(1/n) >= 3/2. The script also checks this monotonicity directly up to N.
- So the formula fails at n if a(N)^n >= (a(n) + 1)^N, and holds at n if (a(N) + 2)^n < (a(n) + 1)^N.
  For every n <= 300 one of the two is the case.
- For A207976 the bounds are (a(N) - 2)^(1/N) <= q < a(N)^(1/N), by the mirror-image argument (it needs
  a(n)^(1/n) >= 3/2, true since the limit is 1.65).

The sequences themselves are generated with exact integer roots, and the defining inequalities are
asserted for every term. The output is in `check.log`.

    python check2.py           (a few seconds; needs mpmath and python-flint)

is an independent second computation (FLINT integer roots, 400-digit floating point for x and q). It
gives the same failure lists for n < 150; output in `check2.log`.

## Limits

- The lists of failures are complete for n <= 300 only.
- That the formulas fail for infinitely many n, and the fraction of n at which they fail, are not proved.
- "The formula cannot fail when x > 2" is the heuristic above; for A080869 it was only tested to n = 300,
  and A080870 was not tested.

## Novelty check

Done 2026-11-11: all three pages of the revision history of each entry, with their discussion threads
(one thread, unrelated) and the draft pages (no pending edits); the cross-referenced entries A080869,
A080870 and A059842; an in-depth web search with both A-numbers and constants; the file list of Google
DeepMind's formal-conjectures; the conjecture list of Epoch AI's OEIS Open; an issue search of the
omega-institute project. None mentions a failure of either formula.
