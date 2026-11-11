# Three short proofs

Status of each: **verified**, **new?** (2026-11-11). Produced with AI assistance; see the repository
README. Not submitted to the OEIS. These are routine once written down; they are listed because the
entries still mark them as conjectures.

`python check.py` checks them numerically; output in `check.log`.

## A069097: a trigonometric gcd identity

Entry remark (Peter Bala, 2023): "It appears that for n odd,
Sum_{k = 1..n} (-1)^(k+1)*gcd(k,n)/cos(k*Pi/n)^2 = n."

*Proof.* Write gcd(k, n) = sum of phi(d) over the common divisors d of k and n. Putting k = d j and
m = n/d (both d and m are odd, so (-1)^(k+1) = (-1)^(j+1)):

    sum = sum_{d | n} phi(d) * sum_{j=1}^{m} (-1)^(j+1) / cos(j pi / m)^2.

In the inner sum the term j = m equals 1. For 1 <= j < m, the terms j and m - j have the same
cos^2 and, since m is odd, opposite signs, so they cancel. The inner sum is 1, and the total is
sum_{d | n} phi(d) = n. ∎

## A234307: an alternating gcd sum

Entry: a(n) = Sum_{i=1..n} gcd(2n - i, i). Conjecture (Peter Bala, 2024):
a(n) = (1/4) * Sum_{k = 1..4n} (-1)^k * gcd(k, 8n).

*Proof.* Let P(m) = sum_{k=1}^{m} gcd(k, m) (Pillai's function). The symmetry k -> m - k gives, for even m,
sum_{k=1}^{m/2} gcd(k, m) = (P(m) - m/2) / 2. Hence

    a(n) = sum_{i<=n} gcd(i, 2n) = (P(2n) - n)/2,
    sum_{k<=4n} gcd(k, 8n) = (P(8n) - 4n)/2,
    sum over even k<=4n of gcd(k, 8n) = 2 sum_{j<=2n} gcd(j, 4n) = P(4n) - 2n.

The alternating sum is twice the even part minus the whole, so the conjecture is equivalent to
P(8n) = 4 P(4n) - 4 P(2n). P is multiplicative with P(2^e) = (e+2) 2^(e-1); writing 2n = 2^e * (odd),
the identity reduces to (e+4) 2^(e+1) = 4 (e+3) 2^e - 4 (e+2) 2^(e-1), which holds. ∎

## A055210: sum of totients of the square divisors of n

Conjecture (Velin Yanev, 2019): a(n) = sigma_2(s)/sigma_1(s) with s = n/core(n), the largest square
dividing n.

*Proof.* Both sides are multiplicative, so take n = p^e and let p^(2t) be the largest even power of p
dividing it. The left side is sum_{j=0}^{t} phi(p^(2j)) = 1 + p (p^(2t) - 1)/(p + 1) =
(p^(2t+1) + 1)/(p + 1). The right side is
[(p^(4t+2) - 1)/(p^2 - 1)] / [(p^(2t+1) - 1)/(p - 1)] = (p^(2t+1) + 1)/(p + 1). ∎

## Novelty check

Checked 2026-11-11: every page of the entry's revision history, including its discussion threads; the draft page (no pending edit); the entries it cross-references; an in-depth web search with the sequence number; the conjecture list of Epoch AI's OEIS Open benchmark; and the issue tracker of the omega-institute project, which proves OEIS conjectures in bulk. No proof of these three was found. A fourth identity that was first listed here, for A023887, had already been proved elsewhere and now has its own page under [independent-rediscovery](../../../independent-rediscovery/mathematics/A023887/README.md).
