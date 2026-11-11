"""Smallest TREE violating the v2 (floor) form of Annor's Conjecture 7.

Facts used (proved on the page): a violation needs gamma_t >= 10, gamma_t = 11 is impossible, and gamma_t >= 12 needs
at least 24 vertices.  So a violating tree with at most 23 vertices has gamma = gamma_t = 10 and gamma_c = 18.  In a tree
gamma_c = (number of non-leaf vertices), so such a tree is a tree I on 18 vertices (its non-leaves) with pendant
leaves attached; every leaf of I must carry at least one pendant leaf, and a second pendant on the same vertex
changes neither gamma nor gamma_t, so it only adds vertices.

Search: every tree I on 18 vertices with at most LMAX leaves (networkx generator), every set P of vertices of I that
contains the leaves of I with |P| <= LMAX; T = I plus one pendant leaf on each vertex of P; n = 18 + |P|.
Reports every T with gamma = gamma_t = 10.  LMAX = 6 covers all trees with at most 24 vertices of this type.
"""
import itertools
import sys
import time
import networkx as nx
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from check import tree_dp, adj_of, invariants_B, exists_dom

LMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
t0 = time.time()
found = {}
ntrees = 0
ncand = 0
nbrute = 0
for I in nx.nonisomorphic_trees(18):
    ed = list(I.edges())
    deg = [0] * 18
    for u, v in ed:
        deg[u] += 1
        deg[v] += 1
    leaves = [v for v in range(18) if deg[v] == 1]
    if len(leaves) > LMAX:
        continue
    ntrees += 1
    others = [v for v in range(18) if deg[v] != 1]
    for extra in range(0, LMAX - len(leaves) + 1):
        for add in itertools.combinations(others, extra):
            P = leaves + list(add)
            n = 18 + len(P)
            edges = ed + [(p, 18 + i) for i, p in enumerate(P)]
            ncand += 1
            g, gt = tree_dp(n, adj_of(n, edges))
            if ncand % 250 == 0 or (g == 10 and gt == 10):
                # brute-force confirmation of the DP values on a sample and on every reported tree
                adj = adj_of(n, edges)
                nb = np.array([sum(1 << w for w in adj[v]) for v in range(n)], dtype=np.int64)
                assert exists_dom(n, nb, g, False) and not exists_dom(n, nb, g - 1, False)
                assert exists_dom(n, nb, gt, True) and not exists_dom(n, nb, gt - 1, True)
                nbrute += 1
            if g == 10 and gt == 10:
                found.setdefault(n, []).append(sorted(tuple(sorted(e)) for e in edges))
print("trees I on 18 vertices with at most %d leaves: %d; candidate trees T tested: %d" % (LMAX, ntrees, ncand))
print("gamma and gamma_t from the DP confirmed by brute force over vertex subsets for %d of them "
      "(every 250th candidate and every reported tree)" % nbrute)
for n in sorted(found):
    # reduce to isomorphism classes
    classes = []
    for e in found[n]:
        G = nx.Graph(e)
        if not any(nx.is_isomorphic(G, H) for H in classes):
            classes.append(G)
    print("n = %d: %d trees with gamma = gamma_t = 10, gamma_c = 18 (violations), %d up to isomorphism"
          % (n, len(found[n]), len(classes)))
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "trees%d.txt" % n), "w") as f:
        print("# all trees on %d vertices with gamma = gamma_t = 10 and gamma_c = 18, one edge list per line" % n, file=f)
        for G in classes:
            print(sorted(tuple(sorted(e)) for e in G.edges()), file=f)
    print("    written to trees%d.txt; the first one:" % n)
    print("   ", sorted(tuple(sorted(e)) for e in classes[0].edges()))
    for G in classes[:3]:
        e = list(G.edges())
        assert invariants_B(n, e, 10, 10) == (10, 10, 18)
    print("    the first three re-checked by exhaustive search over all 2^%d vertex subsets (method B of check.py)" % n)
if not found:
    print("no violating tree with at most %d vertices" % (18 + LMAX))
# The remaining case for 24 vertices: gamma_t >= 12 would need gamma = 12 and gamma_c >= 21, i.e. at most 3 leaves.
# Trees on 24 vertices with at most 3 leaves are the path and the spiders with three legs; none has gamma = 12.
mx = 0
for a in range(1, 22):
    for b in range(a, 23 - a):
        c = 23 - a - b
        if c < b:
            continue
        edges = []
        nxt = 1
        for leg in (a, b, c):
            prev = 0
            for _ in range(leg):
                edges.append((prev, nxt)); prev = nxt; nxt += 1
        assert nxt == 24
        mx = max(mx, tree_dp(24, adj_of(24, edges))[0])
edges = [(i, i + 1) for i in range(23)]
mx = max(mx, tree_dp(24, adj_of(24, edges))[0])
print("trees on 24 vertices with at most 3 leaves: largest gamma = %d (12 would be needed)" % mx)
assert mx < 12
assert not any(n < 24 for n in found) and 24 in found
print("done (%.0f s)" % (time.time() - t0))
