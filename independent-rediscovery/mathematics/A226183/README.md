# A226183: the formula printed in the entry is wrong at n = 10, as its own discussion thread says

Status: **rediscovery**. Jon E. Schoenfield and Kevin Ryde pointed out the failure in the entry's
discussion thread in September 2021; the correct asymptotics are in the 2017 thread of A289183. Produced
with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A226183](https://oeis.org/A226183) (Clark Kimberling, May 30 2013): least positive integer k such that
1 + 1/2 + ... + 1/n < 1/(n+1) + ... + 1/k, that is, least k with H(k) > 2 H(n). Data: 4, 11, 22, 36, 54,
75, 100, 129, 161, **197**, 236, ... The entry gives this formula, stated without qualification:

> a(n) = round(exp(gamma)*n*(n+1) + gamma) where gamma is the Euler-Mascheroni constant 0.57714...
> (A001620). - Carl R. White, Sep 01 2021

## What was found here

On 2026-11-11 an agent, working through formula lines that the OEIS does not mark as conjectures, found
that this one contradicts the listed data: at n = 10 it gives round(196.495...) = 196, and a(10) = 197.

- The formula fails at n = 10, 123, 193, 453, 553, 559, 635, 713, 723, 724, ..., at 164906 of the first
  10^7 values of n (1.649 %). It is always one too small there.
- The reason is the constant. From H(k) = log(k + 1/2) + gamma + 1/(24 (k + 1/2)^2) - ... one gets

      a(n) = floor(e^gamma * (n^2 + n + 1/3) + 1/2 - 0.0432/(n + 1/2)^2 + ...),

  so the constant added to e^gamma * n(n+1) before taking the floor should be e^gamma/3 + 1/2 = 1.0937,
  where the formula has gamma + 1/2 = 1.0772. The two disagree when the fractional part of
  e^gamma * n(n+1) falls in an interval of length e^gamma/3 - gamma = 0.01648, which matches the
  observed 1.649 %.
- G(n) = floor(e^gamma * (n^2 + n + 1/3) - 1/2) equals A289183(n) = A226183(n) - 1 for every n from 1
  to 10^7, with no exception.

## Who had it first

- **The failure.** The discussion thread of A226183, Sep 08 2021. Schoenfield: "at n=10, the Formula
  entry gives a(n) = nint(exp(gamma)*10*11 + gamma) = nint(196.49518...) = 196, but the correct value of
  a(10) is 197." Ryde: "I have different at n=10, n=123, n=193 versus the b-file." White replied with an
  apology in the same thread. The formula nevertheless remained in the published entry.
- **The correct constant.** [A289183](https://oeis.org/A289183) (greatest m with H(m) < 2 H(n), which is
  A226183(n) - 1) has carried since July 2017 the formula f(n) = floor(n^2 * exp(gamma + 1/n) - C),
  C = 1/2 + e^gamma/6 (Schoenfield; C identified by Vaclav Kotesovec), with the exceptions n = 66, 39087,
  517345, 2013005, 10240491, 80968833 below 4 * 10^9. Expanding, f(n) has the same constant e^gamma/3 as
  above, plus a term e^gamma/(6n) that the true expansion does not have; that extra term is why f has
  exceptions.
- **The form without that term.** In the A289183 thread of Jul 18 2017 Schoenfield proposed
  f'(n) = floor(n^2 * exp(gamma + 1/n - (1/6)/n^3) - C), expecting far fewer exceptions, and Kotesovec
  gave the next coefficient, 41/360 - e^(-2 gamma)/24. Since n^2 * exp(1/n - 1/(6 n^3)) =
  n^2 + n + 1/2 + O(1/n^2), f' is G up to terms of order 1/n^2, and Kotesovec's coefficient reproduces
  the -0.0432 above. Neither f' nor G appears in the published entries.

## What is not recorded in the entries

- A226183 still prints White's formula with no warning, and does not say a(n) = A289183(n) + 1 (it only
  lists A289183 as a cross-reference).
- A289183 asks "Is there any n > 66 at which f(n) and a(n) differ?" and lists the exceptions of f. With G
  in place of f, all six listed exceptions disappear (checked here), and there is none up to 10^7.

## Check

    python check.py            (about 5 minutes; needs python-flint and mpmath)
    python check.py 100000     (a few seconds)

Part 1 uses exact rationals for n <= 60. Part 2 certifies A289183(n) for every n up to 10^7 with Arb ball
arithmetic (the sign of H(m) - 2H(n) is decided rigorously at m and at m + 1) and compares the three
formulas. Part 3 does the same at the six exceptions listed in A289183 and their neighbours. Part 4
repeats n <= 3000 with mpmath. Output in `check.log`.

## Limits

- G(n) = A289183(n) is verified for n <= 10^7 and at the six listed exceptions only. Since G(n) <= f(n)
  always, and A289183(n) <= G(n) as long as the expansion above is accurate, G would also be right at
  every n below 4 * 10^9 where f is right; that step relies on Schoenfield's scan and on the expansion,
  and was not re-verified here.
- Whether G has any exception at all is open. The expected number, from the size of the neglected term,
  is about 0.04; a proof would need information about the fractional parts of e^gamma * n(n+1) that is not
  available (it is not even known whether e^gamma is irrational).

## How the earlier work was missed, and found

The published entry carries the formula as a plain statement; the objections exist only in the history's
discussion threads. They were found when the history of A226183 and of the cross-referenced A289183 was
read on 2026-11-11 (both histories in full, with discussion threads; no pending drafts).
