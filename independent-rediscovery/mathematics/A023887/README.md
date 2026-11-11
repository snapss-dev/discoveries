# A023887: sigma_m(n) through sigma of a larger number

Status: **rediscovery**. Credit: the omega-institute project. Produced with AI assistance; see the
repository README.

## What was found here

On 2026-11-11 an agent proved a conjecture in [A023887](https://oeis.org/A023887) (Velin Yanev, 2017):

    sigma_m(n) = sigma(n^m * rad(n)^(m-1)) / sigma(rad(n)^(m-1))     for n, m > 0.

Both sides are multiplicative in n, and at n = p^e the right side is
sigma(p^(me + m - 1)) / sigma(p^(m-1)) = (p^(m(e+1)) - 1)/(p^m - 1) = sigma_m(p^e).

## Who had it first

- The case m = 2: Sela Fried, in a note linked from A001157.
- The general case: the [omega-institute project](https://github.com/the-omega-institute/trureturing),
  issue 7947, "settle: OEIS A023887", closed 14 September 2026, by the same multiplicative reduction.

## How it was missed at first

The entry still marks the statement as a conjecture, and its revision history has no proof. The earlier
proof appeared only when the sequence number was searched in that project's issue tracker.
