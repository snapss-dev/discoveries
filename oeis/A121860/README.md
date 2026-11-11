# A121860: modulo any k, the sequence is eventually constant, equal to 2

Status: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A121860](https://oeis.org/A121860): a(n) = sum_{d | n} n! / (d! (n/d)!), beginning 1, 2, 2, 8, 2, 122,
2, 1682, ... It carries the comment "Conjecture: the sequence a(n) taken modulo a positive integer
k >= 3 eventually becomes constant equal to 2" (Peter Bala, 8 August 2025).

## Result

For every k >= 1 and every n >= (k+2)^2, a(n) is congruent to 2 modulo k. In fact a(n) - 2 is divisible
by m! for m = ceiling(sqrt(n)) - 2.

## Proof

The terms d = 1 and d = n each equal 1. Take a divisor d with 1 < d < n and put e = n/d, so d, e >= 2
and d + e <= d e = n. Then

    n! / (d! e!) = binomial(n, d+e) * binomial(d+e, d) * (n - d - e)!,

so the term is divisible by (n - d - e)!. With d <= e (the term is symmetric in d and e):

    n - d - e = (d-1)(e-1) - 1 >= (e-1) - 1 = e - 2 >= sqrt(n) - 2.

So every middle term is divisible by m! with m = ceiling(sqrt(n)) - 2. If n >= (k+2)^2 then m >= k, and
k divides m!. ∎

## Check

    python check.py 2000 40

computes a(n) exactly for n <= 2000, confirms the divisibility of each middle term for n <= 600, and
confirms the congruence for all 3 <= k <= 40 and (k+2)^2 <= n <= 2000. It also shows that the bound
(k+2)^2 is far from sharp: for k = 3, 11, 37 the last exception is n = 1, 10, 36. Output in `check.log`.

## Novelty check

The published entry and the first page of its revision history (to November 2025) show the conjecture
and one discussion remark with numerical observations, and no proof. A web search found nothing further.
Older history pages were not read. Checked 2026-11-11.
