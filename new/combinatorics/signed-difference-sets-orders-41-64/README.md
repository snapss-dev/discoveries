# Explicit signed difference sets for 26 cases of order 48, 54 and 64 that the La Jolla repository lists as open

Status: **verified**; no earlier record found (2026-11-11), with the weak points stated under Limits.
Produced with AI assistance; see the repository README. Nothing was submitted to the maintainer.

## The source

The [La Jolla Signed Difference Set Repository](https://dmgordon.org/signed-difference-sets/) of Daniel M.
Gordon (file `sds.json`, version 1.2 of 2026-04-24; GitHub `dmgordo/signed-difference-sets`, Zenodo DOI
10.5281/zenodo.7473882; SHA-256 `39bab9fc...80ca85`) records for 70,543 pairs (parameters, abelian group)
whether a signed difference set is known: 67,823 are marked `Open`, 2,574 `No`, 87 `Yes`, 59 `All`.

A signed difference set SDS(v, k, lambda) in an abelian group G of order v is a pair of disjoint subsets
P, N with |P| + |N| = k such that, with f = +1 on P, -1 on N and 0 elsewhere,

    sum over x in G of f(x) f(x + g) = lambda        for every g != 0

(in the group ring, D D^(-1) = (k - lambda) + lambda G for D = P - N; D. M. Gordon, "Signed difference
sets", Des. Codes Cryptogr. 91 (2023), arXiv:2212.10630). The key `SDS(48,24,8,[4,12])` means v = 48,
k = 24, lambda = 8 in Z4 x Z12.

The small open cases have been worked on since August 2026. Fabian Arévalo (`farev/Matematica`,
2026-08-09) and Nicolas Masselot (`nlarch/certified-small-sds-census`, 2026-08-12) between them settled
every open case with v <= 36; Arévalo also settled ten cases of order 37, 43, 44, 49 and 50, all negatively. Zhiwen
He and Jiayan Wu (arXiv:2608.22936v2, 20 September 2026) rule out 45,361 open cases by four criteria and
construct sets for three (orders 64, 125 and 256), and write that "many group-specific cases in the
signed difference set database remain open".

## Result

`new_sds.json` holds an explicit signed difference set for each of the following 26 cases, all marked
`Open` in version 1.2 of the file. Groups are given by invariant factors.

    (48,24,8)  |P| = 22, |N| = 2   set found in [2,2,12], [2,2,2,6], [4,12]
                 other groups of this order: [2,24] Open; [48] Open
    (48,32,16)  |P| = 30, |N| = 2   set found in [2,2,12], [2,2,2,6], [4,12]
                 other groups of this order: [2,24] Open; [48] Open
    (54,46,10)  |P| = 35, |N| = 11   set found in [3,3,6]
                 other groups of this order: [3,18] Open; [54] Open
    (64,18,2)  |P| = 15, |N| = 3   set found in [2,2,16], [2,2,2,2,2,2], [2,2,2,2,4], [2,2,2,8], [2,2,4,4], [2,4,8], [4,4,4], [8,8]
                 other groups of this order: [2,32] Open; [4,16] Open; [64] Open
    (64,22,6)  |P| = 21, |N| = 1   set found in [2,2,2,2,4], [2,2,2,8], [2,2,4,4], [2,4,8], [4,4,4]
                 other groups of this order: [2,2,16] Open; [2,2,2,2,2,2] Open; [2,32] Open; [4,16] Open; [64] Open; [8,8] Open
    (64,46,30)  |P| = 45, |N| = 1   set found in [2,2,2,2,2,2], [2,2,2,2,4], [2,2,2,8], [2,2,4,4], [2,4,8], [4,4,4]
                 other groups of this order: [2,2,16] Open; [2,32] Open; [4,16] Open; [64] Open; [8,8] Open

For each parameter triple the second line gives the status in the file of the same triple in the other
abelian groups of that order; for those marked `Open` the search here found nothing, which proves
nothing.

One of the 26 follows from the literature: the set found for `SDS(64,46,30,[2,2,2,2,2,2])` is, after a
translation, a partial difference set with parameters (64,45,32,30) as P and the identity as N. A regular
partial difference set with lambda - mu = 2 always gives a signed difference set in this way (this is
how Theorem 5.3 of He and Wu works), and partial difference sets with these
parameters in Z2^6 are classical (negative Latin square type). The other ten sets with |N| = 1, for
(64,22,6) and (64,46,30) in groups that are not elementary abelian, are not of this form: there P,
translated so that N is the identity, is not closed under inversion. Whether partial difference sets
with lambda - mu = 2 are known in those groups, which would also give existence, was not checked.
A second observation of the same kind: the support P u N of the set found for
`SDS(64,18,2,[2,2,2,2,2,2])` has only two unsigned difference counts, 2 and 6, as a partial difference
set with parameters (64,18,2,6) would; in the seven other groups the supports show three or more
counts. So in Z2^6 this set may be a known partial difference set with three signs changed.

The search also returned a set for `SDS(64,22,6,[2,2,2,2,2,2])`, which He and Wu had settled (their
Theorem 5.3 with m = 3); it is not counted and not included.

None of these cases is excluded by the first two criteria of He and Wu (self-conjugate prime; C2
quotient), reimplemented here from the description in their README; the reimplementation reproduces
their published counts on the 67,823 open cases (44,872 exclusions, then 456 more).

## How the sets were found

Simulated annealing on E = sum over g != 0 of (A(g) - lambda)^2, where A is the autocorrelation of f; a
move exchanges the values of f at two positions, so |P| = (k + s)/2 and |N| = (k - s)/2 with
s^2 = k + lambda (v - 1) are kept (Gordon's Lemma 1.1). All 105 open cases with 41 <= v <= 50 were
tried for 25 seconds each, and the 148 open cases with 51 <= v <= 64 that pass the two criteria (of
316 open) for 12 seconds each. Every set above appeared within 12 seconds, most within one. The same
program, run on the 91 open cases with v <= 40, found sets in exactly the 16 cases where Arévalo and Masselot
report existence (see the page `signed-difference-sets-small-open-cases`), and none where they or He and
Wu prove nonexistence.

## Check

    python check.py

needs only Python 3 and runs in a few seconds. It first checks 36 sets copied from the repository against
the definition above, to show that the definition used is the repository's, then checks every set in
`new_sds.json` by computing all v - 1 autocorrelation values with integer arithmetic. Output is in
`check.log`. The search program (numpy, numba) shares no code with `check.py`.

`check_characters.py` (needs numpy) tests the same sets by a different criterion,
|sum of f(x) chi(x)|^2 = k - lambda for every nontrivial character chi; all 26 pass
(`check_characters.log`).

## Limits

- **Novelty is the weak point.** Two independent projects settled the same kind of case for v <= 36 three
  months ago and neither is linked from the repository or cited in the papers; they were found here only
  by a late web search. A third project covering these orders may exist. What was checked is listed
  below.
- The sets are single examples, not classified up to equivalence, and apart from the test described
  under Result no closed-form description was looked for. A set with the same parameters appearing
  in several groups of one order suggests a simple construction, which an expert may recognise.
- Nothing is claimed about nonexistence. The annealing finds the repository's known sets for v <= 31
  within seconds but misses most known cyclic cases with v >= 35 in 3 seconds, so its failures carry
  little weight.
- He and Wu's program was not run; their first two criteria were reimplemented from its README. Their
  third and fourth criteria need k = v - 1 or an elementary abelian p-group with p odd, which no case
  in the table satisfies.
- The status fields of the file were taken as given.

## Novelty check

Done on 2026-11-11:

- status `Open` for each case in `sds.json` version 1.2; GitHub and Zenodo hold the same latest version
  (2026-04-24); the repository has no issues and its last commit is of that date; the maintainer's page
  (site last updated 2026-09-03) lists no further results;
- Arévalo's decided cases (`data/values.csv`, 58 rows: nothing of order 48, 54 or above 50) and his notes;
  his write-up page (fabianarevalo.com/signed-difference-sets), which reports no existence result
  above order 36 and lists the cells still open past order 36 as an open question;
  Masselot's census (orders up to 36 only), its final report and research ledger;
- the theorem statements of Gordon (arXiv:2212.10630), He, Chen and Ge (arXiv:2306.05631) and He and Wu
  (arXiv:2608.22936v2). For v between 41 and 64 their constructions apply only to odd prime powers
  (Gordon's Propositions 2.2, 2.3 and Theorem 3.2; the Paley-type and cyclotomic constructions of He,
  Chen and Ge), to v = 55 = 4 * 16 - 9 (Gordon's Theorem 4.1) and to `SDS(64,22,6)` in Z2^6 (He and Wu);
  none is stated for a group of order 48 or 54, or for the other triples of order 64 in the table
  (but see the remark on partial difference sets under Result);
- in-depth web searches for "signed difference set" with the triples (48,24,8), (48,32,16), (54,46,10),
  (64,18,2), (64,22,6), (64,46,30), and for the repository name; a GitHub code search for the triple
  (48,24,8). None returned these cases.

Not checked: MathSciNet, zbMATH, and the literature on ternary sequences and arrays with two-level
autocorrelation under other names.

## Credit

Daniel M. Gordon (definition, repository, list of open cases). Fabian Arévalo and Nicolas Masselot for the
censuses of the smaller orders, against which the search was calibrated. Zhiwen He and Jiayan Wu for the
nonexistence criteria used as a filter.
