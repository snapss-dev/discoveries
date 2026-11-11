# Covering-design records: no entry beaten, and the table is already being swept by the same method

Status: **dead end** (2026-11-11). Searched and not found. Produced with AI assistance; see the repository
README.

## The table

A (v,k,t) covering design is a set of k-subsets (blocks) of {1..v} such that every t-subset lies in a
block; C(v,k,t) is the least number of blocks. The best known coverings for v < 100, k <= 25, t <= 8 were
kept for thirty years in Dan Gordon's La Jolla Covering Repository. State on 2026-11-11:

- Gordon froze his database in March 2026 and published it as a dataset ("La Jolla Coverings
  Repository", Zenodo, version 1.2.1 of 2026-11-10: `coverdata.json` with sizes, lower bounds and the
  history of improvements for 9,482 parameter sets, and `covers.json`, 4.2 GB, with the block lists). His
  README: "In March, 2026, I froze the database, and in August shut down my database."
- The live table is now Giovanni Acerbi's coveringrepository.com, which states "historical data up to the
  end of March 2026 are imported from the Dan Gordon Covering Repository" and counts 9,490 (v,k,t)
  coverings. Its list of latest (v,k,t) improvements showed 100 entries, all dated November 2026.
  Current sizes can be read without an account; block lists of entries improved after March could not
  be downloaded anonymously (the download links answer with a browser challenge).

## What was tried

1. **Shrinking by simulated annealing.** Start from the record covering in the frozen dataset, delete the
   block that covers the fewest t-subsets alone, and repair with single-point exchanges (cost: number of
   uncovered t-subsets; half of the moves aimed at an uncovered t-subset). One entry was run,
   C(60,16,4) = 559 in the frozen data (a doubled (30,8,4) covering): two attempts of 5 million moves
   each left 136 and 128 of the 144 and 176 uncovered 4-subsets uncovered. No improvement. The live
   table already had 547 for this entry (26 September 2026).
2. **Coverings with a prescribed cyclic group.** Choose m base blocks in Z_v whose v translates cover
   every t-subset, and anneal on the number of uncovered orbits. Two entries: C(83,8,3) = 2082 would
   need m <= 25 base blocks; the search left 73 of 1107 orbits uncovered with m = 25, 63 with m = 26 and
   18 with m = 30. C(45,16,6) = 4066 would need m <= 90; with m = 80 the search stalled near 1,350 of
   181,006 orbits uncovered. No improvement.
3. **Dropping superfluous blocks** from coverings built by constructions. The scan read one covering,
   C(44,25,8) = 851 (dynamic programming construction): no block can be dropped; the block with the
   fewest 8-subsets covered by it alone has 240 of them.

Denominator: four parameter sets attacked, about 15 minutes of single-core search in total, no record
beaten. This is a shallow attempt, not evidence that the table is hard.

## Why the lane was closed

The live table shows who is already doing this. In October 2026 Wynand van Staden uploaded many
improvements (his repository speaks of more than 600 records) with the note "Weighted local search v2 (SAT-style t-set weighting + tabu),
shrinking the previous record", and published the code (`WynandVStaden/covering-design-records`,
written "with AI assistance (Claude)"). The README reports a run over 3,251 table entries that improved
312, a zero-coverage cleanup of constructed covers, and derived coverings from product constructions,
and it states that parallel tempering and simulated annealing "found no records" in their tests and
that the oldest table entries (1996 to 2005) did not improve. That is method 1 above, done better and at the scale of the
whole table; method 3 is part of it. The entries left unimproved are the ones their solver already
failed on.

The one idea here that differs from theirs, prescribing a group, failed for a clear reason: at k = 8,
t = 3 the records have density about 1.27 (blocks times C(k,t) over C(v,t)), and a covering problem
with only 25 base blocks cannot reach that; at t = 6 the records have density near 4, but random-like
base blocks leave a fraction of orbits uncovered that annealing does not remove.

## Useful by-products

- The frozen dataset can be read one covering at a time with HTTP range requests: the file is ordered
  by (t, k, v), so a byte offset can be estimated from the sizes in `coverdata.json` and corrected from
  the keys found nearby.
- The live table answers its ordinary search form for a fixed (k, t), which is enough to compare sizes.

## Limits

- Nothing here was verified against the block lists of the live table, only against its sizes.
- The cyclic search used no multipliers and no fixed points; other groups were not tried.

## Credit

Dan Gordon and the contributors to the La Jolla Covering Repository; Giovanni Acerbi (coveringrepository.com);
Wynand van Staden (weighted local search records and code).
