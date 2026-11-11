# A100682: the list of exceptions is incomplete

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A100682](https://oeis.org/A100682): floor of the fourth root of the pentatope numbers,
a(n) = floor(binomial(n+3, 4)^(1/4)), offset 0. It carries the comment (Charles R Greathouse IV, 2012):

> Conjecture: a(n) = floor((n - 3/2)/24^(1/4)) for n not in {0, 1, 6, 17, 2403, 5318}.

**Indexing.** The conjecture was written before the entry's offset was changed in December 2015. In its
own indexing it concerns floor(binomial(m, 4)^(1/4)) with m = n + 3. In the current offset the formula
reads floor((n + 3/2)/24^(1/4)), and the listed exceptions 6, 17, 2403, 5318 become n = 3, 14, 2400, 5315.

## Result

The exception list is incomplete. The next exceptions are

    m = 634027531  and  m = 1705327318        (n = 634027528 and n = 1705327315),

and these six are all the exceptions with n < 2 * 10^9. For example, at n = 634027528 the sequence value
is 286454272 and the formula gives 286454273. `exceptions.txt` lists 61 exceptions below 10^132, each
confirmed by exact integer arithmetic.

## Why

With u = n + 3/2,

    n(n+1)(n+2)(n+3) = (u^2 - 5/4)^2 - 1,

so 24^(1/4) * binomial(n+3, 4)^(1/4) = u - 5/(8u) + O(u^-3), which is always below u. Hence
a(n) <= formula(n) for every n, and a(n) = formula(n) - 1 exactly when an integer multiple of 24^(1/4)
falls in the gap of width about 5/(8u) just below u. Such n come from the continued fraction of
2 * 24^(1/4) = [4; 2, 2, 1, 10, 2, 1, 4, 1, 1, 3, 17, 1, 62, ...]. Exceptions should keep occurring, at a
rate of roughly one per order of magnitude; that expectation is heuristic, not proved.

## Check

Everything is exact integer arithmetic: a(n) is the largest k with 24 k^4 <= n(n+1)(n+2)(n+3), and the
formula is the largest k with 384 k^4 <= (2n+3)^4.

    python check.py                  exhaustive exact scan of n < 3,000,000, and all 61 listed values
    python check.py 2000000000       full scan to 2 * 10^9 (float pre-filter, then exact checks)

Output of the full scan is in `check.log`: the exceptions below 2 * 10^9 are exactly
3, 14, 2400, 5315, 634027528, 1705327315.

## Limits

- Completeness is claimed only below 2 * 10^9. The larger values in `exceptions.txt` were found from the
  continued fraction; each is verified, but the list between 2 * 10^9 and 10^132 is not proved complete.
- That there are infinitely many exceptions is not proved.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads (which record the
2015 offset change and nothing on further exceptions); the draft page (no pending edit); an in-depth web
search with the sequence number; Epoch AI's OEIS Open conjecture list; and the omega-institute project,
whose notes set this entry aside as a transcription problem without listing further exceptions.
