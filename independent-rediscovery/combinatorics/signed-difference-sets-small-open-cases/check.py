"""Independent check of signed difference sets (pure Python, integer arithmetic only).

A signed difference set SDS(v,k,lambda) in an abelian group G = Z_n1 x ... x Z_nr is a pair of
disjoint subsets P, N of G with |P|+|N| = k such that, writing f = +1 on P, -1 on N, 0 elsewhere,

    sum_{x in G} f(x) f(x+g) = lambda      for every g != 0.

(Equivalently D D^(-1) = (k-lambda) + lambda G in the group ring, D = P - N.)

Reads new_sds.json and known_examples.json from its own folder. known_examples.json holds sets
copied from the La Jolla Signed Difference Set Repository; they are checked with the same code to
show that the definition used here is the repository's.
"""
import itertools
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def parse(key):
    m = re.fullmatch(r"SDS\((\d+),(\d+),(-?\d+),\[([\d,]+)\]\)", key)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), tuple(int(x) for x in m.group(4).split(","))


def as_tuple(e):
    return (e,) if isinstance(e, int) else tuple(e)


def check(key, P, N):
    v, k, lam, ns = parse(key)
    order = 1
    for n in ns:
        order *= n
    assert order == v, "group order"
    P = [as_tuple(e) for e in P]
    N = [as_tuple(e) for e in N]
    for e in P + N:
        assert len(e) == len(ns) and all(0 <= x < n for x, n in zip(e, ns)), "element out of range"
    assert len(set(P)) == len(P) and len(set(N)) == len(N) and not set(P) & set(N), "P, N not disjoint sets"
    assert len(P) + len(N) == k, "support size"
    f = {e: 1 for e in P}
    f.update({e: -1 for e in N})
    values = set()
    for g in itertools.product(*[range(n) for n in ns]):
        if not any(g):
            continue
        total = 0
        for x, fx in f.items():
            y = tuple((a + b) % n for a, b, n in zip(x, g, ns))
            total += fx * f.get(y, 0)
        values.add(total)
    return values == {lam}, sorted(values), len(P), len(N)


def run(fn, label):
    data = json.load(open(os.path.join(HERE, fn)))
    ok_all = True
    print("%s: %d sets" % (label, len(data)))
    for row in data:
        ok, values, p, n = check(row["key"], row["P"], row["N"])
        ok_all &= ok
        print("  %-28s |P|=%2d |N|=%2d  autocorrelation values off the identity: %s  %s"
              % (row["key"], p, n, values, "OK" if ok else "FAIL"))
    return ok_all


if __name__ == "__main__":
    a = run("known_examples.json", "calibration (sets copied from the repository)")
    b = run("new_sds.json", "new signed difference sets")
    print("ALL OK" if a and b else "FAILURE")


# ---------------------------------------------------------------------------------------------
# Exhaustive search in five very small open cases (no signed difference set exists).
# Every choice of the zero positions and of the negative positions is tried; a candidate is
# rejected at the first nonzero g whose autocorrelation differs from lambda.

def exhaustive_count(key):
    v, k, lam, ns = parse(key)
    s2 = k + lam * (v - 1)
    s = int(round(s2 ** 0.5))
    assert s * s == s2 and (k + s) % 2 == 0
    q = (k - s) // 2                       # |N|; |P| = (k + s) / 2  (Gordon, Lemma 1.1, up to overall sign)
    elems = list(itertools.product(*[range(n) for n in ns]))
    idx = {e: i for i, e in enumerate(elems)}
    shift = [[idx[tuple((a + b) % n for a, b, n in zip(x, g, ns))] for x in elems] for g in elems]
    nz = [g for g in range(v) if any(elems[g])]
    found = tried = 0
    for zeros in itertools.combinations(range(v), v - k):
        support = [x for x in range(v) if x not in zeros]
        for neg in itertools.combinations(support, q):
            tried += 1
            f = [0] * v
            for x in support:
                f[x] = 1
            for x in neg:
                f[x] = -1
            ok = True
            for g in nz:
                sg = shift[g]
                if sum(f[x] * f[sg[x]] for x in support) != lam:
                    ok = False
                    break
            found += ok
    return tried, found


SMALL_OPEN = ["SDS(9,8,1,[3,3])", "SDS(20,17,8,[2,10])", "SDS(27,25,16,[27])", "SDS(27,25,16,[3,3,3])", "SDS(27,25,16,[3,9])"]
SMALL_KNOWN = ["SDS(9,8,-1,[3,3])", "SDS(11,6,1,[11])", "SDS(13,12,-1,[13])"]   # calibration: these exist

if __name__ == "__main__":
    print()
    print("exhaustive search (candidates tried, signed difference sets found):")
    for key in SMALL_KNOWN + SMALL_OPEN:
        tried, found = exhaustive_count(key)
        print("  %-24s %8d tried, %4d found" % (key, tried, found))


# ---------------------------------------------------------------------------------------------
# The product construction of He, Chen and Ge (arXiv:2306.05631, eq. (4.1)), taken with m = 1:
# G = Z3 x Z3 x Z3, D = (1,0,Z3) + (0,Z3,0) + (0,D',D') with D' = {1} - {2} the (3,2,-1) set.
# Their Theorem 4.1 is stated for even m; this instance is checked directly.

def hcg_m1():
    chi = {1: 1, 2: -1}
    coef = {}
    for g in range(3):
        coef[(1, 0, g)] = 1
        coef[(0, g, 0)] = 1
    for a in (1, 2):
        for b in (1, 2):
            coef[(0, a, b)] = chi[a] * chi[b]
    P = [list(e) for e, c in coef.items() if c == 1]
    N = [list(e) for e, c in coef.items() if c == -1]
    return check("SDS(27,10,1,[3,3,3])", P, N)


if __name__ == "__main__":
    print()
    print("He-Chen-Ge product construction with m = 1 in Z3^3: (ok, values, |P|, |N|) =", hcg_m1())
