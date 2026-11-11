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

