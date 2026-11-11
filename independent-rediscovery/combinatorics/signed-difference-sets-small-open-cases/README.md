# Signed difference sets in 16 small cases listed as open: found here, but two projects had them in August 2026

Status: **independent rediscovery** (2026-11-11). Fabian Arévalo (9 August 2026) and Nicolas Masselot
(12 August 2026) had settled every one of these cases. Produced with AI assistance; see the repository
README.

## The source

The [La Jolla Signed Difference Set Repository](https://dmgordon.org/signed-difference-sets/) of Daniel M.
Gordon (file `sds.json`, version 1.2 of 2026-04-24; GitHub `dmgordo/signed-difference-sets`, Zenodo DOI
10.5281/zenodo.7473882) records for 70,543 pairs (parameters, abelian group) whether a signed difference
set is known; 67,823 are marked `Open`.

A signed difference set SDS(v, k, lambda) in an abelian group G of order v is a pair of disjoint subsets
P, N with |P| + |N| = k such that, with f = +1 on P, -1 on N and 0 elsewhere,

    sum over x in G of f(x) f(x + g) = lambda        for every g != 0.

The key `SDS(27,10,1,[3,9])` means v = 27, k = 10, lambda = 1 in Z3 x Z9. Gordon's paper ("Signed
difference sets", Des. Codes Cryptogr. 91 (2023), arXiv:2212.10630) says: "A search for noncyclic signed
difference sets with lambda != 0 not constructed with Theorem 4.1 turned up only one such signed
difference set: an (18, 13, 4) set in Z2 x Z3 x Z3."

## What was found here

A simulated-annealing search over all 91 cases marked `Open` with v <= 40 found a signed difference set
in 16 of them (`new_sds.json`):

    SDS(25,12,1,[5,5])
    SDS(27,10,1,[3,3,3])   SDS(27,10,1,[3,9])
    SDS(27,14,5,[3,3,3])   SDS(27,14,5,[3,9])
    SDS(27,17,8,[3,3,3])
    SDS(32,20,4,G)   for G = [2,16], [2,2,2,2,2], [2,2,2,4], [2,2,8], [2,4,4], [4,8]
    SDS(32,28,12,G)  for G = [2,4,4], [4,8]
    SDS(36,11,2,G)   for G = [3,12], [6,6]

An exhaustive search (every placement of the zeros and of the negative elements) shows that five small
open cases have no set: `SDS(9,8,1,[3,3])` (252 candidates), `SDS(20,17,8,[2,10])` (155,040) and
`SDS(27,25,16,G)` for G = [27], [3,3,3], [3,9] (105,300 each).

## Who had it first

- **Fabian Arévalo**, repository `farev/Matematica`, folder `conjectures/signed-difference-sets`, commits
  of 2026-08-09: 58 of the open cases decided by exhaustive search, 10 with a set (all those above
  except the six `(32,20,4)` cases) and 48 without, including the five negative cases above. The same
  work closes 45,328 open cases with two character criteria.
- **Nicolas Masselot**, repository `nlarch/certified-small-sds-census` (first version 2026-08-12, Zenodo
  DOI 10.5281/zenodo.21901581): all 68 open cases with v <= 36 settled, 16 with a set and 52 without.
  His 16 cases are exactly the 16 above. He proves that a signed (32,20,4) set exists in an abelian
  group of order 32 if and only if the group is not cyclic.
- Zhiwen He and Jiayan Wu (arXiv:2608.22936, 24 August 2026) published nonexistence criteria that rule
  out 45,361 open cases, the first two of which are the two criteria in Arévalo's notes.

Nothing in the list above is new. Three of the 16 cases also follow from published constructions, which
the database does not record for these groups: `SDS(27,14,5,[3,3,3])` is Gordon's Proposition 2.3 (Paley
difference set of GF(27) with N = {0}); `SDS(27,17,8,[3,3,3])` is Gordon's Theorem 4.1 with q = 3,
r = 9; `SDS(27,10,1,[3,3,3])` is the product construction of He, Chen and Ge (arXiv:2306.05631, equation
(4.1)) taken with m = 1, although their Theorem 4.1 is stated for even m (`check.py` verifies this one
instance).

## How the earlier work was missed

The first novelty pass read the repository file, its issue tracker and commit history, the Zenodo
record, the maintainer's page and the three papers, and ran two in-depth web searches with the
parameter triples. None of these shows the two projects: neither is cited in the papers or linked from
the repository, and neither repository page contains a triple written as "(27,10,1)". They appeared
only in a later in-depth search for the repository's name together with the word "error", made for a
different purpose. A search for the repository's name alone would have found them at the start.

## Check

    python check.py

needs only Python 3 and takes about 15 seconds. It checks 36 sets copied from the repository against the
definition (to show that the definition used is the repository's), the 16 sets in `new_sds.json`, the
exhaustive search for the five negative cases (after confirming on three cases with known sets that the
same loop finds them), and the m = 1 product construction. `exhaust_second.py` (numpy, numba) repeats
the exhaustive search through the character criterion; its counts in `exhaust_second.log` are the same.

A reimplementation of He and Wu's first two criteria reproduces their published counts (44,872
exclusions, then 456 more) and excludes none of the 16 cases.

## Limits

- The 16 sets are single examples, not classified up to equivalence and not compared element by element
  with the sets of the two earlier projects.
- Of the 91 open cases with v <= 40, 35 are excluded by He and Wu's first two criteria, 16 have a set,
  5 are settled negatively above, and for the remaining 35 the annealing found nothing, which proves
  nothing. Masselot's census settles all of those with v <= 36 negatively; that was not re-derived here.

## Credit

Daniel M. Gordon (definition, repository, constructions); Fabian Arévalo and Nicolas Masselot (first
resolutions of these cases); Zhiwen He, Tingting Chen, Gennian Ge and Jiayan Wu (constructions and
criteria).
