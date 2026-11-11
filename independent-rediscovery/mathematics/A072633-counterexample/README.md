# A072633: the 330-digit counterexample

Status: **rediscovery**. Credit: Antonio Sanso. Produced with AI assistance; see the repository README.

## What was found here

On 2026-11-11 an agent found that the conjecture in [A072633](https://oeis.org/A072633),
a(n) = 1 + round(n / log 2) for the smallest m with 1^n + ... + m^n >= (m+1)^n, fails at a 330-digit n
(the denominator of the convergent of index 641 of 2/log 2), where the true value is one larger. It was
confirmed with three independent systems.

## Who had it first

Antonio Sanso posted the same n on 22 July 2026
([X post](https://x.com/asanso/status/2079999623507198242)) and proposed it to the OEIS the same day
(A072633 revision history, revisions 21 to 25), with rigorous interval-arithmetic bounds that agree with
ours to every digit shown. An editor asked for a formatting change, and the edit was reverted on
9 August 2026 when no reply came. The published entry therefore still shows only the conjecture.

## How it was missed at first

The check had read the published entry and run one ordinary web search. The edit was visible only in the
entry's revision history, and the post only to an in-depth search.

## What remains

A proof that Sanso's n is the smallest counterexample, the bound F(n) <= a(n) <= F(n) + 1, and four
further counterexamples:
[A072633, smallest counterexample](../../../new/mathematics/A072633-smallest-counterexample/README.md).
The verification scripts for the counterexample itself are on that page.
