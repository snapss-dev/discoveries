"""Second check of new_sds.json by a different criterion (needs numpy): f is a signed difference set
SDS(v,k,lambda) exactly when it has k nonzero values and |sum_x f(x) chi(x)|^2 = k - lambda for every
nontrivial character chi of the group. Floating point, tolerance 1e-6."""
import json, os, re
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(HERE, "new_sds.json")))
good = 0
for r in rows:
    v, k, lam = map(int, re.match(r"SDS\((\d+),(\d+),(-?\d+)", r["key"]).groups())
    ns = [int(x) for x in re.search(r"\[([\d,]+)\]", r["key"]).group(1).split(",")]
    f = np.zeros(ns)
    for e in r["P"]:
        f[tuple(e)] = 1
    for e in r["N"]:
        f[tuple(e)] = -1
    spec = (np.abs(np.fft.fftn(f)) ** 2).ravel()
    ok = int(np.count_nonzero(f)) == k and np.allclose(spec[1:], k - lam, atol=1e-6) and abs(spec[0] - (k + lam * (v - 1))) < 1e-6
    good += ok
    print("%-28s %s" % (r["key"], "OK" if ok else "FAIL"))
print("%d of %d sets pass the character criterion" % (good, len(rows)))
