# A139394: the conjecture a(n) > 0 fails where the prime race modulo 3 changes leader

Status: **rediscovery**. Credit: Carter Bays and Richard Hudson (1978). Produced with AI assistance; see
the repository README.

## What was found here

[A139394](https://oeis.org/A139394) is a(n) = A024899(n) - A024898(n): the n-th k with 6k + 1 prime minus
the n-th k with 6k - 1 prime. The entry says (Zak Seidov, 2008): "Conjecture: a(n) > 0, except
n=1,2,3,6,24, when a(n)=0." On 2026-11-11 an agent computed

    a(11669295395) = 101496968836 - 101496968854 = -18,

using two independent prime-counting methods that agree up to 10^9 and across the window around
6.09 * 10^11.

## Who had it first

A negative value of a(n) means that the n-th prime of the form 6k + 1 comes before the n-th prime of the
form 6k - 1, that is, the primes that are 1 modulo 3 have taken the lead. Bays and Hudson showed in 1978
that in the race modulo 3 this first happens at 608981813029, thirty years before the conjecture was
written. For the forms 6k + 1 and 6k - 1, which leave out the prime 2, the lead changes one prime
earlier, at 608981813017 = 6 * 101496968836 + 1, which is the value above. The crossover is a standard
example in the literature on prime number races (for instance Granville and Martin, "Prime number
races", 2006).

## What is not recorded

The entry itself still carries the conjecture and the keyword marking the sequence as non-negative, and
its history has no comment on this.

## Limit

The value above comes from the agent's computation and was not recomputed in a second pass. It agrees
with the published crossover and with published counts of both kinds of primes up to that point.
