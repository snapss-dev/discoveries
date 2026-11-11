# A121860: lcm(1, ..., n) divides a(n) - 2 for every n except 4

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry and what was already known

[A121860](https://oeis.org/A121860): a(n) = sum_{d | n} n! / (d! (n/d)!), beginning 1, 2, 2, 8, 2, 122,
2, 1682, ...

- **Peter Bala** conjectured in the entry (8 August 2025) that modulo any k >= 3 the sequence is
  eventually constant, equal to 2.
- **Peter Luschny**, in the entry's discussion the next day, suggested the sharper form: a(k) - 2 is
  divisible by n for all k >= n.
- **Haobo Ma and Wenlin Zhang** proved Bala's conjecture ([Zenodo record 23971256](https://zenodo.org/records/23971256),
  5 November 2026): a(n) is 2 modulo m for all n >= 2m + 4, and for prime m already for all n >= m.

So the conjecture itself is settled, and not by this page (see
[the rediscovery page](../../../independent-rediscovery/mathematics/A121860-conjecture/README.md)). What
follows is the sharp form.

## Result

For every n other than 4, lcm(1, 2, ..., n) divides a(n) - 2. Equivalently:

    a(n) = 2 (mod m)   for all n >= m,   with the single exception m = n = 4.

This is Luschny's suggested form, which holds except at that one point (a(4) = 8), and it removes the
gap between m and 2m + 4 for composite m.

## Proof

The terms d = 1 and d = n are each 1. Take d | n with 1 < d < n and e = n/d, so d, e >= 2. For a prime p
and i >= 1 put q = p^i and

    T_i = floor(de/q) - floor(d/q) - floor(e/q),

so that the p-adic valuation of n!/(d! e!) is the sum of the T_i (Legendre's formula). We claim
T_i >= 1 whenever q <= n, unless d = e = 2 and q = 2.

- If d < q and e < q: T_i = floor(de/q) >= 1, because de = n >= q.
- If d >= q > e (or the reverse): with a = floor(d/q) >= 1, floor(de/q) >= a e >= 2a >= a + 1.
- If d >= q and e >= q: with a = floor(d/q), b = floor(e/q) >= 1, floor(de/q) >= a b q, and
  a b q - a - b >= 2ab - a - b = a(b-1) + b(a-1) >= 0, with a b q - a - b >= 1 unless a = b = 1 and
  q = 2. In that last case d, e are 2 or 3, and T_i = floor(de/2) - 2 is 0 only for d = e = 2.

Hence for n != 4 every middle term has p-adic valuation at least the number of powers of p up to n,
which is the exponent of p in lcm(1, ..., n). So lcm(1, ..., n) divides every middle term, and therefore
a(n) - 2. For n = 4 the one middle term is 4!/(2! 2!) = 6, and a(4) - 2 = 6 is not divisible by 4. ∎

## Check

    python check.py 1500

computes a(n) exactly and confirms that lcm(1, ..., n) divides every middle term and a(n) - 2 for all
n <= 1500 except n = 4. Output in `check.log`.

## Novelty check

Checked 2026-11-11: every page of the entry's revision history, including the discussion threads (which
is where Luschny's suggestion is); the draft page (no pending edit); the Ma and Zhang note, whose Lemma 6
proves the statement for primes p <= n but not for prime powers; an in-depth web search with the
sequence number; and the issue tracker and code of the omega-institute project behind that note. None
states the lcm form.
