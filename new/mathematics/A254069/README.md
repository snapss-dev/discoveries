# A254069: a new term, a(4) = 909764941

Status: **verified** as a term; minimality by one agent's two searches. No earlier record found
(2026-11-11). Produced with AI assistance; see the repository README. Not submitted to the OEIS.

## The entry

[A254069](https://oeis.org/A254069): the smallest k such that none of 4k - 4j + 2 and 4k + 4j - 2,
j = 0, ..., n, is squarefree. Listed terms: 13, 13, 1263, 837140, with the remark "a(4) > 10^8". The entry
has not changed since 2015.

## Result

    a(4) = 909764941.

The eight numbers 4k - 14, 4k - 10, ..., 4k + 14 are divisible by the squares of
5, 11, 1949, 13, 3, 23, 7, 19 in that order. Halving them, this is a run of eight consecutive odd numbers,
1819529875 to 1819529889, none of which is squarefree. The agent also found a(5) > 1.43 * 10^12.

## How minimality was established

By the agent that found the term: a sieve over runs of consecutive odd numbers, and a second sieve that
tests the literal definition for every k up to 9.2 * 10^8.

## Check

    python check.py

factors the eight values and reproduces a(0) to a(2) by brute force from the definition. Output in
`check.log`. It does not repeat the minimality search.

## Novelty check

Checked 2026-11-11: every page of the revision history with its discussion threads (43 revisions, the
last in 2015; nothing on a(4)); the draft page (no pending edit); a search of the complete OEIS term dump
for 909764941, 1819529875 and 3639059750 (no sequence contains any of them); an in-depth web search; and
the omega-institute project's issues.
