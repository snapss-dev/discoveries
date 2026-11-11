"""Second, independent computation for the search in smallest_tree.py.  It does not use the dynamic program.

1. The generator: the trees on 18 vertices produced by networkx are reduced to a canonical form (AHU string
   from the centre); they must be pairwise different and their number must be 123,867 (OEIS A000055), so
   the list is complete.
2. The domination numbers: a candidate tree T (18 non-leaves plus at most 6 single leaves) can only violate
   the conjecture if gamma(T) = gamma_t(T) = 10.
   - A greedy algorithm (deepest vertex first; if it is not dominated, take its parent) builds a dominating
     set, which is then checked against the definition.  If it has at most 9 vertices, gamma <= 9 is
     certified and T is not a violator.
   - Otherwise gamma and gamma_t are computed by integer linear programming (scipy / HiGHS).
   The trees found with gamma = gamma_t = 10 must be the 138 trees with 24 vertices of smallest_tree.py.
"""
import itertools
import os
import sys
import time
import numpy as np
import networkx as nx
from scipy.optimize import milp, LinearConstraint, Bounds

LMAX = 6


def adj_of(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def canon(n, adj):
    # canonical string of a free tree: AHU encoding rooted at the centre (minimum over the two centres)
    d = [len(a) for a in adj]
    layer = [v for v in range(n) if d[v] <= 1]
    removed = len(layer)
    while removed < n:
        nxt = []
        for v in layer:
            for w in adj[v]:
                d[w] -= 1
                if d[w] == 1:
                    nxt.append(w)
        removed += len(nxt)
        layer = nxt

    def enc(v, p):
        return "(" + "".join(sorted(enc(w, v) for w in adj[v] if w != p)) + ")"
    return min(enc(c, -1) for c in layer)


def greedy_dominating_set(n, adj):
    parent = [-1] * n
    order = [0]
    seen = [False] * n
    seen[0] = True
    for v in order:
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                parent[w] = v
                order.append(w)
    S = set()
    for v in reversed(order):                      # deepest first (reverse breadth-first order)
        if v not in S and not any(w in S for w in adj[v]):
            S.add(parent[v] if parent[v] >= 0 else v)
    # check against the definition
    assert all(v in S or any(w in S for w in adj[v]) for v in range(n))
    return S


def ilp_gamma(n, adj, total):
    A = np.zeros((n, n))
    for v in range(n):
        for w in adj[v]:
            A[v, w] = 1
        if not total:
            A[v, v] = 1
    res = milp(c=np.ones(n), constraints=LinearConstraint(A, lb=np.ones(n), ub=np.inf),
               integrality=np.ones(n), bounds=Bounds(0, 1))
    assert res.success
    return int(round(res.fun))


t0 = time.time()
forms = set()
ntrees = ncand = ncert = nilp = 0
found = {}
found_forms = set()
other = {}
for I in nx.nonisomorphic_trees(18):
    ed = list(I.edges())
    adjI = adj_of(18, ed)
    forms.add(canon(18, adjI))
    ntrees += 1
    leaves = [v for v in range(18) if len(adjI[v]) == 1]
    if len(leaves) > LMAX:
        continue
    others = [v for v in range(18) if len(adjI[v]) != 1]
    for extra in range(0, LMAX - len(leaves) + 1):
        for add in itertools.combinations(others, extra):
            P = leaves + list(add)
            n = 18 + len(P)
            adj = adj_of(n, ed + [(p, 18 + i) for i, p in enumerate(P)])
            ncand += 1
            if len(greedy_dominating_set(n, adj)) <= 9:
                ncert += 1
                continue
            nilp += 1
            g, gt = ilp_gamma(n, adj, False), ilp_gamma(n, adj, True)
            if g == 10 and gt == 10:
                found[n] = found.get(n, 0) + 1
                found_forms.add(canon(n, adj))
            else:
                other[(g, gt)] = other.get((g, gt), 0) + 1
print("trees on 18 vertices from the generator: %d; distinct canonical forms: %d (A000055(18) = 123867)"
      % (ntrees, len(forms)))
assert ntrees == len(forms) == 123867
print("candidates: %d; gamma <= 9 certified by an explicit dominating set: %d; decided by integer programming: %d"
      % (ncand, ncert, nilp))
print("integer programming, (gamma, gamma_t) other than (10, 10):", dict(sorted(other.items())))
print("trees with gamma = gamma_t = 10, by number of vertices:", dict(sorted(found.items())),
      "; up to isomorphism:", len(found_forms))
assert found == {24: 138} and len(found_forms) == 99
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
