"""Counterexamples to Conjecture 7 of D. Y. B. Annor, arXiv:2506.03646 (versions 1 and 2):
    v1:  gamma_t(G) >= ceil((3 gamma(G) + 2 gamma_c(G)) / 6)
    v2:  gamma_t(G) >= floor((3 gamma(G) + 2 gamma_c(G)) / 6)
for connected graphs G without isolated vertices.

The tree T_k: k "units" (an edge s_j t_j with one leaf attached to s_j and one to t_j), consecutive units
joined by a path t_j - x_j - y_j - s_(j+1).   n = 6k - 2.

Method A: dynamic programming on the tree for gamma and gamma_t; gamma_c = n - (number of leaves).
Method B: exhaustive search over vertex subsets with bit masks (numba), using only the definitions:
          no dominating / total dominating set smaller than the claimed value, one of the claimed size exists,
          and the smallest connected dominating set found by testing all 2^n subsets (n <= 28).
Extra:    all trees with at most 17 vertices (networkx generator) tested against both forms of the conjecture.
"""
import time
import numpy as np
from numba import njit, prange

INF = 10 ** 9


def family(k):
    edges = []
    nid = [0]

    def new():
        nid[0] += 1
        return nid[0] - 1

    prev_t = None
    for j in range(k):
        s, t, ls, lt = new(), new(), new(), new()
        edges += [(s, t), (s, ls), (t, lt)]
        if prev_t is not None:
            x, y = new(), new()
            edges += [(prev_t, x), (x, y), (y, s)]
        prev_t = t
    return nid[0], edges


def adj_of(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


# ---------------- Method A: tree DP
def tree_dp(n, adj):
    order = []
    parent = [-1] * n
    seen = [False] * n
    st = [0]
    seen[0] = True
    while st:
        v = st.pop()
        order.append(v)
        for w in adj[v]:
            if not seen[w]:
                seen[w] = True
                parent[w] = v
                st.append(w)
    # domination: D0 = v in the set; D1 = v out, dominated by a child; D2 = v out, not dominated yet
    D = [None] * n
    # total domination: T0 = v in, has a child in; T1 = v in, no child in (needs its parent in);
    #                   T2 = v out, has a child in; T3 = v out, no child in (needs its parent in)
    T = [None] * n
    for v in reversed(order):
        ch = [w for w in adj[v] if parent[w] == v]
        d0 = 1 + sum(min(D[c]) for c in ch)
        d2 = sum(D[c][1] for c in ch)
        d1 = INF
        if ch:
            base = sum(min(D[c][0], D[c][1]) for c in ch)
            d1 = base + min(D[c][0] - min(D[c][0], D[c][1]) for c in ch)
        D[v] = (min(d0, INF), min(d1, INF), min(d2, INF))
        # v in the set: every child has v as a neighbour in the set, so any child state is allowed
        t1 = 1 + sum(min(T[c][2], T[c][3]) for c in ch)
        t0 = INF
        if ch:
            allin = sum(min(T[c]) for c in ch)
            t0 = 1 + allin + min(min(T[c][0], T[c][1]) - min(T[c]) for c in ch)
        # v out: a child in the set must have its own child in the set (T0); a child out must be T2
        t3 = sum(T[c][2] for c in ch)
        t2 = INF
        if ch:
            bo = sum(min(T[c][0], T[c][2]) for c in ch)
            t2 = bo + min(T[c][0] - min(T[c][0], T[c][2]) for c in ch)
        T[v] = (min(t0, INF), min(t1, INF), min(t2, INF), min(t3, INF))
    r = order[0]
    return min(D[r][0], D[r][1]), min(T[r][0], T[r][2])


def invariants_A(n, edges):
    adj = adj_of(n, edges)
    g, gt = tree_dp(n, adj)
    leaves = sum(1 for v in range(n) if len(adj[v]) == 1)
    return g, gt, n - leaves


# ---------------- Method B: exhaustive bit-mask search
@njit(cache=False)
def exists_dom(n, nb, size, total):
    # is there a (total) dominating set with exactly `size` vertices?  Gosper's hack over all masks of that size.
    full = (np.int64(1) << n) - 1
    if size <= 0:
        return False
    x = (np.int64(1) << size) - 1
    while x <= full:
        cov = np.int64(0)
        for v in range(n):
            if (x >> v) & 1:
                cov |= nb[v]
                if not total:
                    cov |= np.int64(1) << v
        if cov == full:
            return True
        c = x & -x
        r = x + c
        x = (((r ^ x) >> 2) // c) | r
    return False


@njit(parallel=True, cache=False)
def min_connected_dom(n, nb):
    # size of the smallest connected dominating set, by testing all 2^n subsets
    full = (np.int64(1) << n) - 1
    nchunk = 64
    best = np.full(nchunk, n + 1, dtype=np.int64)
    total = np.int64(1) << n
    for ch in prange(nchunk):
        lo = total * ch // nchunk
        hi = total * (ch + 1) // nchunk
        b = n + 1
        for x in range(max(lo, 1), hi):
            cov = np.int64(x)
            pc = 0
            for v in range(n):
                if (x >> v) & 1:
                    cov |= nb[v]
                    pc += 1
            if cov != full or pc >= b:
                continue
            xx = np.int64(x)
            comp = xx & -xx
            while True:
                grow = comp
                for v in range(n):
                    if (comp >> v) & 1:
                        grow |= nb[v] & xx
                if grow == comp:
                    break
                comp = grow
            if comp == xx:
                b = pc
        best[ch] = b
    return best.min()


def invariants_B(n, edges, claim_g, claim_gt):
    adj = adj_of(n, edges)
    nb = np.array([sum(1 << w for w in adj[v]) for v in range(n)], dtype=np.int64)
    assert exists_dom(n, nb, claim_g, False) and not exists_dom(n, nb, claim_g - 1, False)
    assert exists_dom(n, nb, claim_gt, True) and not exists_dom(n, nb, claim_gt - 1, True)
    return claim_g, claim_gt, int(min_connected_dom(n, nb))


if __name__ == "__main__":
    import numba
    numba.set_num_threads(min(4, numba.config.NUMBA_NUM_THREADS))
    t0 = time.time()
    print(" k   n  gamma gamma_t gamma_c  floor((3g+2gc)/6)  ceil((3g+2gc)/6)  v2 form   v1 form   checked by")
    for k in range(1, 13):
        n, edges = family(k)
        g, gt, gc = invariants_A(n, edges)
        assert n == 6 * k - 2 and (g, gt, gc) == (2 * k, 2 * k, 4 * k - 2), (k, g, gt, gc)
        how = "A"
        if k <= 5:
            gB = invariants_B(n, edges, g, gt)
            assert gB == (g, gt, gc), (gB, g, gt, gc)
            how = "A and B (exhaustive)"
        fl = (3 * g + 2 * gc) // 6
        ce = -((-(3 * g + 2 * gc)) // 6)
        print("%2d  %2d   %2d     %2d      %2d          %2d                 %2d          %s  %s  %s" %
              (k, n, g, gt, gc, fl, ce, "VIOLATED" if gt < fl else "holds   ",
               "VIOLATED" if gt < ce else "holds   ", how))
        assert (gt < fl) == (k >= 5) and (gt < ce) == (k >= 3)
    n, edges = family(5)
    print("T_5 edges:", sorted(tuple(sorted(e)) for e in edges))
    print("time so far %.0f s" % (time.time() - t0))

    # ---------------- all small trees
    import networkx as nx
    NMAX = 17
    viol_floor = 0
    count = 0
    ceil_list = []
    for n in range(2, NMAX + 1):
        for Tg in nx.nonisomorphic_trees(n):
            count += 1
            ed = list(Tg.edges())
            adj = adj_of(n, ed)
            g, gt = tree_dp(n, adj)
            gc = n - sum(1 for v in range(n) if len(adj[v]) == 1) if n >= 3 else 1
            s = 3 * g + 2 * gc
            if gt < s // 6:
                viol_floor += 1
            if gt < -((-s) // 6):
                ceil_list.append((n, g, gt, gc, sorted(tuple(sorted(e)) for e in ed)))
    print("all %d trees with 2..%d vertices (method A): violations of the v2 (floor) form: %d; "
          "of the v1 (ceiling) form: %d" % (count, NMAX, viol_floor, len(ceil_list)))
    if ceil_list:
        m = min(c[0] for c in ceil_list)
        sm = [c for c in ceil_list if c[0] == m]
        print("  smallest trees violating the v1 form have %d vertices (%d of them); "
              "(gamma, gamma_t, gamma_c) = %s" % (m, len(sm), sorted(set(c[1:4] for c in sm))))
        for c in sm:
            assert invariants_B(c[0], c[4], c[1], c[2]) == c[1:4]
            print("   ", c[4])
        print("  (each of these re-checked by method B)")
        # cross-check of method A against method B on every tree with at most 11 vertices
        nchk = 0
        for n in range(3, 12):
            for Tg in nx.nonisomorphic_trees(n):
                ed = list(Tg.edges())
                a = invariants_A(n, ed)
                assert invariants_B(n, ed, a[0], a[1]) == a
                nchk += 1
        print("  methods A and B agree on all %d trees with 3..11 vertices" % nchk)
    assert viol_floor == 0
    print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
