# UCI king-rook-king dataset: "not guaranteed correct", and correct

Status: **dead end** (searched for errors, none found). Produced with AI assistance; see the
repository README.

## The idea

The UCI Machine Learning Repository's dataset *Chess (King-Rook vs. King)* (`krkopt.data`, Michael Bain
and Arthur van Hoff, donated June 1994) lists 28,056 positions with White king, White rook and Black
king, Black to move, each labelled `draw` or with the number of moves, `zero` to `sixteen`, in which
White mates with best play. It has been a standard benchmark for thirty years. Its own description
says:

> It should be noted that our database is not guaranteed correct, but the class distribution is the
> same as Clarke's database.

A label is a mathematical fact that a small program can recompute, so every one was recomputed.

## Outcome

All 28,056 labels are right, and the file is complete:

- a retrograde analysis written from scratch (no chess library) gives the same label for every row;
  the longest win is 16 moves;
- the rows are exactly the legal Black-to-move positions with the White king in the triangle
  a1-d1-d4, one from each pair of mirror images in the long diagonal when the king stands on it:
  34,968 positions before that identification, 28,056 after it, and all 28,056 are in the file, none
  twice;
- as a second check with unrelated code and data, the draw/win split agrees for all 28,056 rows with
  the Syzygy KRvK table read by python-chess (2,796 draws). That check is not in `check.py`.

So the caveat can be dropped: the dataset has no label noise.

## Check

`python check.py` (about 20 seconds, standard library only) reads `krkopt.data` from its own folder
and prints the two class distributions, the number of mismatches (0) and the completeness counts;
`check.log` is its output. The data file is the one in
https://archive.ics.uci.edu/static/public/23/chess+king+rook+vs+king.zip, fetched 2026-11-11
(SHA-256 497b61d20d3d9e2ce310f9f4d2ca92dbdb0691d9e449d983ec6f7baf387dc7a9; licence CC BY 4.0).

## Limits

- Castling and the fifty-move rule play no part in this ending; "moves" are White moves, as in the
  dataset.
- No search was made for earlier independent verifications; with a dataset this old and this
  small, some surely exist. This page records only that the check was done here and what it gave.
- The companion dataset *King-Rook vs. King-Pawn* stores derived attributes, not positions, and was
  not checked.

## Credit

Michael Bain and Arthur van Hoff (the database); M. R. B. Clarke (1977, the earlier database whose
class distribution it matches); Ronald de Man (Syzygy tables).
