# 147 of the 280 sets stored in the La Jolla Signed Difference Set Repository fail its own definition (found earlier by F. Arévalo)

Status: **independent rediscovery** (2026-11-11). Fabian Arévalo found the same 147 failing sets on
9 August 2026. New here, as far as the check below goes: corrected sets for three further entries.
Produced with AI assistance; see the repository README. Not reported to the maintainer.

## The source

The [La Jolla Signed Difference Set Repository](https://dmgordon.org/signed-difference-sets/) of Daniel M.
Gordon: file `sds.json`, version 1.2 of 2026-04-24 (GitHub `dmgordo/signed-difference-sets`, Zenodo DOI
10.5281/zenodo.7473882, SHA-256 `39bab9fc...80ca85`). An entry such as `SDS(20,11,2,[20])` has a
`status` (`Yes`, `All`, `No`, `Open`) and, when sets are known, a field `sets`, a list of pairs [P, N].
The repository's code describes it as "a list of [P,N] sets for each known signed difference set".

A signed difference set SDS(v, k, lambda) in Z_v is a pair of disjoint sets P, N with |P| + |N| = k such
that the differences x - y of distinct elements of P u N, counted with sign +1 when x and y lie in the
same set and -1 otherwise, give every nonzero residue exactly lambda times.

## Result

The file stores 280 sets in 144 entries: 269 in cyclic groups and 11 in noncyclic groups.

- **122 of the 269 cyclic sets satisfy the definition. The other 147, in 21 entries, do not.** Example:
  `SDS(20,11,2,[20])` stores P = {0,4,6,7,8,11,12,13,15}, N = {1,9}. The difference 10 arises only from
  the pairs (11,1) and (1,11), both with sign -1, so its count is -2, not 2. The counts over the nonzero
  residues take the values -2, 0, 2, 4.
- In every failing set the sizes |P| and |N| are right. **For 62 of the failing sets, in 15 entries,
  keeping the stored support P u N and choosing other elements as N gives a signed difference set.**
  For `SDS(20,11,2,[20])` the choice N = {1, 11} works; for `SDS(167,84,40,[167])` the stored N = {162}
  fails and N = {132} works.
- In six entries marked `All` with more than one stored set (v = 20, 35, 51, 78, 104, 200), every stored set has the same
  support and differs only in N. `SDS(104,29,4,[104])` stores 24 sets on one support, none of which
  satisfies the definition; N = {8, 34, 60, 86} does. So the number of sets stored for these entries is
  not a count of signed difference sets.

The 21 entries (stored sets / failing / distinct supports / sets corrected on the same support):

    SDS(20,11,2,[20])        4 /  4 / 1 /  4     N = {1,11}
    SDS(35,21,10,[35])       4 /  4 / 1 /  4     N = {13}
    SDS(51,19,3,[51])        4 /  4 / 1 /  4     N = {6,23,40}
    SDS(61,49,36,[61])       1 /  1 / 1 /  1     N = {39}
    SDS(78,53,28,[78])      12 / 12 / 1 / 12     N = {21,47,73}
    SDS(104,29,4,[104])     24 / 24 / 1 / 24     N = {8,34,60,86}
    SDS(111,66,17,[111])     6 /  6 / 3 /  0     not searched (|N| = 11)
    SDS(167,84,40,[167])     1 /  1 / 1 /  1     N = {132}
    SDS(181,136,11,[181])    1 /  1 / 1 /  0     not searched (|N| = 45)
    SDS(182,38,2,[182])     12 / 12 / 4 /  0     not searched (|N| = 9)
    SDS(182,101,20,[182])   25 / 25 / 6 /  0     not searched (|N| = 20)
    SDS(191,96,46,[191])     1 /  1 / 1 /  1     N = {32}
    SDS(199,100,48,[199])    1 /  1 / 1 /  1     N = {152}
    SDS(200,151,102,[200])  40 / 40 / 1 /  0     not searched (|N| = 4 on a support of 151)
    SDS(247,127,63,[247])    4 /  4 / 2 /  4     N = {62} or {61}
    SDS(277,208,17,[277])    1 /  1 / 1 /  0     not searched (|N| = 69)
    SDS(347,174,85,[347])    1 /  1 / 1 /  1     N = {48}
    SDS(379,190,93,[379])    1 /  1 / 1 /  1     N = {5}
    SDS(443,222,109,[443])   1 /  1 / 1 /  1     N = {304}
    SDS(491,246,121,[491])   1 /  1 / 1 /  1     N = {337}
    SDS(499,250,123,[499])   2 /  2 / 2 /  2     N = {318}, {403}

One further remark: the single set of `SDS(18,13,4,[3,6])` is stored as triples of Z2 x Z3 x Z3 (the form
in Theorem 6.1 of Gordon's paper), while the key names Z3 x Z6 and the entry has no `G_rep` field. Read
in Z2 x Z3 x Z3 it is a signed difference set. The ten other noncyclic sets are correct as stored.

## Who had it first

Fabian Arévalo, repository `farev/Matematica`, folder `conjectures/signed-difference-sets` (commits of
2026-08-09): "147 of the 280 stored witness sets do not satisfy the SDS equation", in the same 21
entries, with the remark that `SDS(18,13,4,[3,6])` is stored in undeclared coordinates. His note
re-enumerates `SDS(20,11,2,[20])` completely (40 labelled sets in 2 translation classes) and repairs 22
of the 147 sets by exchanging at most two elements between P and N, which gives a valid set for 12 of
the 21 entries. His draft report to the maintainer is marked "not yet sent". Nicolas Masselot's census
(`nlarch/certified-small-sds-census`, 2026-08-12) builds on the same file and credits that repository.

What this page adds is small: the search here keeps the stored support and tries every choice of N of
the right size, which also corrects the entries `SDS(51,19,3,[51])`, `SDS(78,53,28,[78])` and
`SDS(104,29,4,[104])` (15 entries instead of 12), and it shows that in six entries all stored sets share
one support. His write-up lists nine entries whose stored sets he could not repair, these three among
them. Arévalo's file `data/repaired_witnesses.csv` was not read, so the overlap was judged from the
summaries in his notes and write-up only.

The earlier work was missed at first because it is not linked from the repository, its issue tracker or
the papers; it surfaced in an in-depth web search for the repository's name with the word "error".

## Why it matters

The existence statements are not in doubt for the 15 entries where a corrected set is given here: a
signed difference set with those parameters exists. What is wrong is the stored data, so a program that
reads P and N from the file gets objects that fail the defining equation in 147 of 280 cases, and the
number of stored sets overstates the number of distinct sets for the entries with a single support.
The pattern (support right, negative elements wrong) looks like an error in how N was written out, but
that is a guess; only the maintainer can say what happened.

## Check

    python check.py

needs only Python 3. `failing_sets.json` holds the 147 failing sets exactly as stored (entry, index, P,
N) and the corrected N where one was found. The program recomputes the signed difference counts of each
stored set with integer arithmetic, checks every corrected set, and prints the table above. If a copy of
`sds.json` version 1.2 is placed next to `check.py`, it also audits all 269 stored cyclic sets and
confirms that the failing ones are exactly those listed; `check.log` was produced that way (the 5 MB file
is not copied here).

The 11 noncyclic sets were checked with the program on the page `signed-difference-sets-small-open-cases`.

## Limits

- A corrected N was searched only where |N| <= 3, or |N| = 4 on a support of at most 60 elements, by
  trying every choice. For the six entries marked "not searched" nothing is known here beyond the
  failure of the stored sets.
- The corrected N is the first one found; other choices on the same support may also work.
- Nothing is claimed about the status fields (`Yes`, `All`, `No`, `Open`). In particular it is not
  checked whether `All` entries really list every set.
- It is possible that these entries were written in a convention that the repository's documentation
  does not describe. Under the documented one, which the other 122 cyclic sets follow, they fail.
- The counts in He and Wu (arXiv:2608.22936), who use this file, depend only on the status fields and
  are not affected.

## Novelty check

Done on 2026-11-11, before the earlier work was found: the issue trackers of `dmgordo/signed-difference-sets` and of
`zhiwenhe94/sds-open-case-verification`, which redistributes the same file (no issues in either); the
commit history of the repository (last change 2026-04-24, "Updates to dataset, other files"); the Zenodo
record (latest version 1.2); the maintainer's page; the README of the He and Wu verification package,
which describes the `sets` field without remark; an in-depth web search for the repository name with
"error", "erratum", "incorrect", which found the two projects named above.

## Credit

The repository and all the sets are Daniel M. Gordon's; the supports used for the corrected sets are his.
The finding that 147 stored sets fail is Fabian Arévalo's (2026-08-09).
