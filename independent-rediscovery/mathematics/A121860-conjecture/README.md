# A121860: Bala's constant-tail conjecture

Status: **rediscovery**. Credit: Haobo Ma and Wenlin Zhang. Produced with AI assistance; see the
repository README.

## What was found here

On 2026-11-11 an agent proved the conjecture in [A121860](https://oeis.org/A121860) (Peter Bala,
8 August 2025): for a(n) = sum_{d | n} n!/(d! (n/d)!), the sequence modulo any k is eventually constant,
equal to 2. The argument: for a divisor d with 1 < d < n and e = n/d, the term n!/(d! e!) equals
binomial(n, d+e) * binomial(d+e, d) * (n-d-e)!, and n - d - e >= sqrt(n) - 2, so every middle term is
divisible by k once n >= (k+2)^2.

## Who had it first

Haobo Ma and Wenlin Zhang, "Proof of Bala's totient-period conjectures: OEIS A258899 and A258903",
[Zenodo record 23971256](https://zenodo.org/records/23971256), published 5 November 2026, six days
earlier. Their Corollary 4 proves the same conjecture by the same factorial-divisibility idea, with the
better bound n >= 2m + 4, and their note covers a wider family of weighted sums.

## How it was missed at first

The entry and the first page of its history showed no proof, and an ordinary web search found nothing.
The Zenodo note appeared only in an in-depth search with the sequence number.

## What remains

Reading the entry's discussion threads led to a sharper statement that the note does not contain:
[lcm(1, ..., n) divides a(n) - 2 for every n except 4](../../../new/mathematics/A121860-sharp-onset/README.md).
