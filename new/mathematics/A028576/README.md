# A028576: n divides a(n), and n^2 divides 3 a(n)

Status: **verified**; no earlier record found (2026-11-11). Produced with AI assistance; see the repository README.
Not submitted to the OEIS.

## The entry

[A028576](https://oeis.org/A028576): a(n) = (1/(4n)) * sum_{d | n} mu(n/d) * binomial(2d, d)^2, beginning
1, 4, 33, 304, 3175, 35556, ... It carries the comment "Conjecture: a(n) is divisible by n and 3*a(n) by
n^2" (F. Chapoton, 25 February 2026).

## Result

The conjecture is true. More precisely, write c(x) = binomial(2x, x) and S(n) = sum_{d | n} mu(n/d) c(d)^2,
so a(n) = S(n)/(4n). If p^k exactly divides n with k >= 1, then p-adic valuation of S(n) is at least

    3k        for p >= 5,
    3k - 1    for p = 3,
    3k + 2    for p = 2,

and 4 divides S(n) for every n. All three bounds are attained, which is why the factor 3 is needed.

## Proof

**Step 1 (grouping).** Let n = p^k m with p not dividing m. Divisors d of n with mu(n/d) != 0 have the form
e p^k or e p^(k-1) with e | m, with opposite signs. So

    S(n) = sum_{e | m} mu(m/e) * [ c(e p^k)^2 - c(e p^(k-1))^2 ].

Each bracket is c(N)^2 - c(x)^2 with N = p x and v_p(N) = k.

**Step 2 (the ratio as a product).** Let N = p x and U = {1 <= j <= N : p does not divide j}. Splitting
the factorials in c(N) into multiples and non-multiples of p gives

    c(N) / c(x) = prod_{j in U} (N + j) / j.

The map j -> N - j permutes U, so prod_{j in U} (1 - N/j) = +1 or -1. Multiplying,

    c(N)/c(x) = +-P,     P = prod_{j in U} (1 - N^2 / j^2),

hence c(N)^2 - c(x)^2 = c(x)^2 (P^2 - 1).

**Step 3 (size of P - 1).** Expanding, P = 1 - N^2 T + N^4 (a p-adic integer), with
T = sum_{j in U} j^(-2). The set U consists of N/p^k full sets of units modulo p^k, so modulo p^k, T is
N/p^k times the sum of u^(-2) over the units u modulo p^k, which equals the sum of u^2 over those units.

- For p >= 5 choose g with g^2 not congruent to 1 modulo p. Multiplying the units by g permutes them, so
  (g^2 - 1) times the sum is 0 modulo p^k, and the sum is 0 modulo p^k. Hence v_p(P - 1) >= 3k.
- For p = 3 and p = 2 the sum of squares of the units modulo p^k has valuation k - 1. Hence
  v_p(P - 1) >= 3k - 1.

**Step 4 (from P - 1 to P^2 - 1).** For odd p, P + 1 is a p-adic unit, so v_p(P^2 - 1) = v_p(P - 1). For
p = 2, P is 1 modulo 4, so v_2(P + 1) = 1 and v_2(P^2 - 1) >= 3k; moreover c(x) is even for x >= 1, which
adds 2. This gives the three bounds for each bracket in Step 1, and so for S(n).

**Step 5 (conclusion).** 4 | S(n) because every c(d) with d >= 1 is even. Combining over the primes
dividing n: 4 n^2 | S(n), that is n | a(n); and 4 n^3 | 3 S(n), that is n^2 | 3 a(n). ∎

For p >= 5 the congruence in Steps 2 to 4 is the classical one of Jacobsthal for binomial(pa, pb).

## Check

    python check.py 3000

computes S(n) exactly for all n <= 3000 and confirms both divisibilities; it also checks the valuation
bound of Steps 2 to 4 for every prime p < 60 and every x with p x <= 3000, and reports that the smallest
slack is 0 in each of the three cases (the bounds are attained). Output in `check.log`. The agent that
found the proof ran the same checks to n = 12000.

## Novelty check

Checked 2026-11-11: every page of the entry's revision history, including its discussion threads; the draft page (no pending edit); the entries it cross-references; an in-depth web search with the sequence number; the conjecture list of Epoch AI's OEIS Open benchmark; and the issue tracker of the omega-institute project, which proves OEIS conjectures in bulk. No proof or discussion of the conjecture was found.

## Weak point

Steps 3 and 4 for p = 2 and p = 3 are an elementary argument written here, not a cited lemma. The
numerical check agrees with them exactly, including the cases of equality.
