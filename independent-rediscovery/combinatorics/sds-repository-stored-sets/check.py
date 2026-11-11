"""Check the sets stored in the La Jolla Signed Difference Set Repository (sds.json, version 1.2).

A signed difference set SDS(v,k,lambda) in the cyclic group Z_v is a pair of disjoint sets P, N with
|P|+|N| = k such that the signed differences x - y (x != y in P u N, sign f(x)f(y), f = +1 on P and
-1 on N) hit every nonzero residue with total exactly lambda.

failing_sets.json lists every stored cyclic set that does not satisfy this, copied from sds.json, and,
where one was found, a corrected N on the same support. This program
  1. recomputes the signed difference counts of each stored set (pure integer arithmetic),
  2. checks that each corrected set is a signed difference set,
  3. if a copy of sds.json is placed next to this file, audits every stored cyclic set in it and
     compares the list of failures with failing_sets.json.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))


def parse(key):
    m = re.fullmatch(r"SDS\((\d+),(\d+),(-?\d+),\[([\d,]+)\]\)", key)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), m.group(4)


def difference_values(v, P, N):
    """Set of signed difference counts over the nonzero residues."""
    assert len(set(P)) == len(P) and len(set(N)) == len(N) and not set(P) & set(N)
    assert all(0 <= x < v for x in list(P) + list(N))
    f = [(x, 1) for x in P] + [(x, -1) for x in N]
    cnt = [0] * v
    for x, sx in f:
        for y, sy in f:
            if x != y:
                cnt[(x - y) % v] += sx * sy
    return sorted(set(cnt[1:]))


def main():
    rows = json.load(open(os.path.join(HERE, "failing_sets.json")))
    entries = {}
    bad = 0
    for r in rows:
        v, k, lam, G = parse(r["key"])
        assert len(r["P"]) + len(r["N"]) == k
        vals = difference_values(v, r["P"], r["N"])
        stored_fails = vals != [lam]
        fixed = None
        if r["repaired_N"] is not None:
            S = sorted(set(r["P"]) | set(r["N"]))
            P2 = [x for x in S if x not in r["repaired_N"]]
            fixed = difference_values(v, P2, r["repaired_N"]) == [lam]
        e = entries.setdefault(r["key"], {"n": 0, "fail": 0, "fixed": 0, "supports": set(), "repairs": set(), "status": r["status"]})
        e["n"] += 1
        e["fail"] += stored_fails
        e["fixed"] += bool(fixed)
        e["supports"].add(tuple(sorted(set(r["P"]) | set(r["N"]))))
        if r["repaired_N"] is not None:
            e["repairs"].add(tuple(r["repaired_N"]))
        if not stored_fails or fixed is False:
            bad += 1
        print("%-22s set %2d  lambda %3d  values as stored %s  stored N %s  corrected N %s%s"
              % (r["key"], r["set_index"], lam, vals, r["N"] if len(r["N"]) <= 4 else "(%d elements)" % len(r["N"]),
                 r["repaired_N"], "" if fixed is None else ("  -> OK" if fixed else "  -> FAIL")))
    print()
    print("entry                  status  stored sets  failing  distinct supports  corrected  distinct corrected N")
    for key, e in entries.items():
        print("%-22s %-6s  %11d  %7d  %17d  %9d  %s" % (key, e["status"], e["n"], e["fail"], len(e["supports"]), e["fixed"],
                                                        sorted(e["repairs"]) if e["repairs"] else "-"))
    print()
    print("failing stored sets: %d in %d entries; corrected on the same support: %d sets in %d entries"
          % (sum(e["fail"] for e in entries.values()), len(entries), sum(e["fixed"] for e in entries.values()),
             sum(1 for e in entries.values() if e["fixed"])))
    full = os.path.join(HERE, "sds.json")
    if os.path.exists(full):
        d = json.load(open(full))
        tot = ok = 0
        failing = set()
        for key, e in d.items():
            v, k, lam, G = parse(key)
            if "sets" not in e or "," in G:
                continue
            for i, (P, N) in enumerate(e["sets"]):
                tot += 1
                if difference_values(v, P, N) == [lam]:
                    ok += 1
                else:
                    failing.add((key, i))
        listed = set((r["key"], r["set_index"]) for r in rows)
        print("audit of sds.json: %d stored cyclic sets, %d satisfy the definition, %d do not; same list as failing_sets.json: %s"
              % (tot, ok, len(failing), failing == listed))
        if failing != listed:
            bad += 1
    else:
        print("sds.json not present: full audit skipped (place the repository file next to check.py to run it)")
    print("ALL OK" if bad == 0 else "FAILURE")


if __name__ == "__main__":
    main()
