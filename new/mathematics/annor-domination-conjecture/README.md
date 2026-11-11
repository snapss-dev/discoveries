# A withdrawn conjecture on three domination numbers is false: the smallest tree counterexamples have 24 vertices

Status: **verified**; no earlier record of a counterexample found (2026-11-11). The conjecture was removed
from the latest version of its source without comment, so its author may know it to be false. Produced
with AI assistance; see the repository README. Not sent to the author or to any journal.

## The source

Dickson Y. B. Annor, "A Note on Inequalities for Three Domination Parameters", arXiv:2506.03646. For a
connected graph G without isolated vertices, gamma(G) is the domination number, gamma_t(G) the total
domination number and gamma_c(G) the connected domination number. The paper exists in three versions.

- Version 1 (4 June 2025), abstract: "we propose the following conjecture: for every connected
  isolated-free graph G," gamma_t(G) >= ceil((3 gamma(G) + 2 gamma_c(G))/6) (the formula is transcribed here
  in plain text). This is Conjecture 7.
- Version 2 (14 February 2026): the same Conjecture 7 with a floor in place of the ceiling,
  gamma_t(G) >= floor((3 gamma(G) + 2 gamma_c(G))/6), and a new Figure 3, captioned as a tree T with
  gamma(T) = gamma_t(T) = 6 and gamma_c(T) = 10, given as a case of equality. Those three values violate
  the version 1 form (38/6 rounds up to 7).
- Version 3 (5 June 2026): the conjecture, the figure and the supporting results (Theorem 8, Propositions
  10 to 16) are gone; the abstract no longer mentions a conjecture; the weaker Theorem with
  3 gamma + gamma_c remains. No reason is given, in the text or on the arXiv page.

## Result

Both forms of the conjecture are false, already for trees.

1. **A family.** Let T_k consist of k "units", each an edge s_j t_j with one leaf attached to s_j and one
   to t_j, with consecutive units joined by a path t_j - x_j - y_j - s_(j+1) through two new vertices. T_k
   has 6k - 2 vertices and

       gamma(T_k) = gamma_t(T_k) = 2k,     gamma_c(T_k) = 4k - 2.

   The right-hand side of the version 2 form is floor((14k - 4)/6), which exceeds 2k for every k >= 5. So
   T_5, with 28 vertices, has gamma_t = 10 < 11, and the gap grows like k/3. The version 1 form fails from
   k = 3 (16 vertices; 6 < 7).
2. **Smallest trees.** No tree with fewer than 24 vertices violates the version 2 form. Exactly 99 trees
   with 24 vertices do; all have gamma = gamma_t = 10 and gamma_c = 18. One of them: the path
   v_1 v_2 ... v_20 with one extra leaf attached to each of v_3, v_10, v_11 and v_18. All 99 are in
   `trees24.txt`.
3. **Version 1 form.** The smallest trees violating it have 14 vertices (five trees, all with
   gamma = gamma_t = 6 and gamma_c = 10), for example the path v_1 ... v_12 with an extra leaf on v_3 and
   on v_10.
4. **Any graph.** A counterexample to the version 2 form, tree or not, has gamma_t >= 10, cannot have
   gamma_t = 11, and has at least 20 vertices. Whether a graph that is not a tree can do it with 20 to 23
   vertices was not determined.

## Why

*The family.* T_k has 2k leaves, and the closed neighbourhoods {leaf, its neighbour} are pairwise disjoint,
so every dominating set has at least 2k vertices. The 2k vertices s_j, t_j form a total dominating set:
s_j and t_j are adjacent, each leaf is next to its s_j or t_j, x_j is next to t_j and y_j next to s_(j+1).
Hence gamma = gamma_t = 2k. In a tree with at least 3 vertices, a connected dominating set must contain
every non-leaf v: otherwise the set lies in one component of T - v, and no vertex of another component is
in it or next to a member of it. The non-leaves form a connected dominating set, so gamma_c equals their
number, 6k - 2 - 2k = 4k - 2.

*The general bounds.* Let S be a smallest total dominating set and c the number of components of the
subgraph it induces; each has at least 2 vertices, so c <= gamma_t/2. If c > 1, take a shortest path
between two different components. If it had length 4 or more, its third vertex would be next to some
vertex of S, and that would give a shorter path between two different components. So its length is at most
3, and adding its at most 2 inner vertices merges two components. Repeating, gamma_c <= gamma_t + 2(c - 1),
which is at most 2 gamma_t - 2, and at most 2 gamma_t - 3 when gamma_t is odd. (This is a standard
argument.) A violation of the version 2 form needs 3 gamma + 2 gamma_c >= 6 gamma_t + 6. With
gamma <= gamma_t this gives 7 gamma_t - 4 >= 6 gamma_t + 6, so gamma_t >= 10, with gamma = 10 and
gamma_c = 18 if gamma_t = 10; and for gamma_t = 11 it would need 33 + 38 >= 72, which is false. A connected
graph with gamma_c = 18 has at least 20 vertices. If gamma_t >= 12, then gamma >= 12 and gamma_c >= 21 are
needed, and since gamma <= n/2 this takes at least 24 vertices.

*The search for the smallest trees.* By the last paragraph a violating tree with at most 23 vertices has
gamma = gamma_t = 10 and exactly 18 non-leaves. The non-leaves form a tree I on 18 vertices; every leaf of
I carries at least one leaf of T; a second leaf on the same vertex changes neither gamma nor gamma_t, so a
violating tree with such a doubled leaf would contain a smaller violating tree. So it is enough to take every tree I on 18 vertices with at most 6 leaves (10,910 trees), attach single leaves to
every set of at most 6 vertices containing the leaves of I (92,099 trees T in all), and compute gamma and
gamma_t. None with at most 23 vertices has gamma = gamma_t = 10; 99 with 24 vertices do. With 24 vertices
the case gamma_t >= 12 would need gamma = 12 and at most 3 leaves; trees with at most 3 leaves on 24
vertices have gamma at most 9.

## Check

    python check.py
    python smallest_tree.py

`check.py` computes the three numbers for T_1, ..., T_12 by dynamic programming on the tree (method A) and,
for T_1 to T_5, by exhaustive search over vertex subsets using only the definitions (method B: no
dominating or total dominating set of size 2k - 1 exists, one of size 2k does, and the smallest connected
dominating set among all 2^n subsets has 4k - 2 vertices). It then runs method A over all 81,136 trees
with 2 to 17 vertices: no violation of the version 2 form, 350 of the version 1 form, the smallest with
14 vertices. Methods A and B agree on all 434 trees with 3 to 11 vertices. About a minute.

`smallest_tree.py` runs the search described above (about a minute), writes `trees24.txt`, confirms gamma
and gamma_t by brute force for every 250th candidate and for all reported trees (506 trees), and confirms
gamma_c = 18 by exhaustive search for the first three. Outputs in `check.log` and `smallest_tree.log`.

    python second_method.py

`second_method.py` repeats the search without the dynamic program. It reduces the 123,867 trees on 18
vertices to canonical forms and confirms that they are pairwise different, so the list is complete (the
number is OEIS A000055(18)). For 88,831 of the 92,099 candidates a greedy algorithm exhibits a dominating
set with at most 9 vertices, checked against the definition, which rules them out; for the remaining 3,268
gamma and gamma_t are computed by integer linear programming (HiGHS). Result: the same 138 labelled trees,
99 up to isomorphism, all with 24 vertices. About three minutes; output in `second_method.log`.

    python direct_trees.py 18 19 20 21 22

`direct_trees.py` tests the version 2 form on every tree with the given numbers of vertices, without the
reduction to 18 non-leaves: 9,033,148 trees with 18 to 22 vertices (the counts match OEIS A000055), no
violation; the closest any of them comes is 6 gamma_t - 3 gamma - 2 gamma_c = -4, where a violation needs
-6. About half an hour, most of it for 22 vertices; output in `direct_trees.log`. Together with `check.py`
this covers all trees with at most 22 vertices directly; 23 vertices rest on the reduction.

## Limits

- The count of 99 and the absence of violating trees with 23 vertices rest on the reduction argument
  and on one tree generator (networkx), whose output for 18 vertices was shown to be complete by canonical
  forms. The domination numbers were computed by two methods that share no code. A second, independent
  generator was not used.
- Graphs that are not trees were not searched beyond the bounds in item 4. An earlier exhaustive run over
  all connected graphs with at most 9 vertices found no violation, as the bound of 20 vertices predicts.
- It is not known why the conjecture was withdrawn. The author may have a counterexample; none is published.

## Novelty check

Performed 2026-11-11:

- the arXiv record of 2506.03646 and the full text of versions 1, 2 and 3, read and compared (see above);
  the record has no comment, journal reference or withdrawal note;
- in-depth web searches for the title, the arXiv number and the inequality with "counterexample": no
  follow-up, citing paper or counterexample found;
- Google DeepMind's formal-conjectures repository (code and issue search for the author and the arXiv
  number): nothing;
- the omega-institute project: two issues mention Annor, both about a different conjecture (Conjecture 14
  of his paper on graph covers, arXiv:2502.14341), which that project refuted in September 2026;
- Zenodo's record search for the arXiv number and the title: nothing;
- not reached: Google Scholar, MathSciNet, zbMATH, and any journal version of the note.

## Credit

The conjecture, its withdrawal, and the tree of Figure 3 in version 2 (whose three values already
contradict the version 1 form) are D. Y. B. Annor's. Whether that tree is T_3 was not checked; the figure
was not extracted. The inequality gamma_c <= 2 gamma_t - 2 is a standard fact about total and connected
domination.
