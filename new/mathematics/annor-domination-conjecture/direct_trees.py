"""Direct test of the version 2 (floor) form of Annor's Conjecture 7 on EVERY tree with a given number of
vertices, without the reduction used in smallest_tree.py.   Usage: python direct_trees.py 18 19 20 21

gamma and gamma_t by the dynamic program of check.py; gamma_c = number of non-leaves.  The number of trees
produced by the generator is compared with the known counts (OEIS A000055).
"""
import os
import sys
import time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import networkx as nx
from check import tree_dp, adj_of

A000055 = {14: 3159, 15: 7741, 16: 19320, 17: 48629, 18: 123867, 19: 317955, 20: 823065, 21: 2144505, 22: 5623756}
for n in map(int, sys.argv[1:]):
    t0 = time.time()
    count = 0
    viol = 0
    best = None
    for T in nx.nonisomorphic_trees(n):
        count += 1
        adj = adj_of(n, list(T.edges()))
        g, gt = tree_dp(n, adj)
        gc = n - sum(1 for v in range(n) if len(adj[v]) == 1)
        slack = 6 * gt - (3 * g + 2 * gc)          # violation of the floor form  <=>  slack <= -6
        if best is None or slack < best:
            best = slack
        if gt < (3 * g + 2 * gc) // 6:
            viol += 1
    assert count == A000055[n], (n, count)
    print("n = %d: %d trees (matches A000055), violations of the floor form: %d, smallest 6*gamma_t - 3*gamma - 2*gamma_c = %d"
          " (a violation needs -6 or less)   [%.0f s]" % (n, count, viol, best, time.time() - t0), flush=True)
