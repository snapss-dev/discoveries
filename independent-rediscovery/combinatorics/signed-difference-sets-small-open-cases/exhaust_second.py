"""Second, independent exhaustive search for the five small cases (numpy + numba, different method:
the autocorrelation is tested through the group's characters, |sum_x f(x) chi(x)|^2 = k - lambda for
every nontrivial character chi, with floating point and a tolerance of 1e-6)."""
import itertools, re, cmath, math
import numpy as np
from numba import njit


def parse(key):
    m = re.fullmatch(r"SDS\((\d+),(\d+),(-?\d+),\[([\d,]+)\]\)", key)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), [int(x) for x in m.group(4).split(",")]


@njit(cache=True)
def count(v, k, q, n, cre, cim, zeros_list, comb_idx):
    found = 0
    tried = 0
    f = np.zeros(v)
    support = np.zeros(k, dtype=np.int64)
    for zi in range(zeros_list.shape[0]):
        j = 0
        for x in range(v):
            isz = False
            for z in range(zeros_list.shape[1]):
                if zeros_list[zi, z] == x:
                    isz = True
            if not isz:
                support[j] = x
                j += 1
        for ci in range(comb_idx.shape[0]):
            tried += 1
            f[:] = 0.0
            for x in range(k):
                f[support[x]] = 1.0
            for x in range(q):
                f[support[comb_idx[ci, x]]] = -1.0
            ok = True
            for c in range(1, v):
                re_ = 0.0
                im_ = 0.0
                for x in range(v):
                    re_ += f[x] * cre[c, x]
                    im_ += f[x] * cim[c, x]
                if abs(re_ * re_ + im_ * im_ - n) > 1e-6:
                    ok = False
                    break
            if ok:
                found += 1
    return tried, found


def run(key):
    v, k, lam, ns = parse(key)
    s = math.isqrt(k + lam * (v - 1))
    q = (k - s) // 2
    elems = list(itertools.product(*[range(m) for m in ns]))
    cre = np.zeros((v, v)); cim = np.zeros((v, v))
    for c, a in enumerate(elems):
        for x, e in enumerate(elems):
            z = cmath.exp(2j * cmath.pi * sum(ai * ei / m for ai, ei, m in zip(a, e, ns)))
            cre[c, x] = z.real; cim[c, x] = z.imag
    zeros_list = np.array(list(itertools.combinations(range(v), v - k)), dtype=np.int64)
    comb_idx = np.array(list(itertools.combinations(range(k), q)), dtype=np.int64).reshape(-1, q)
    return count(v, k, q, float(k - lam), cre, cim, zeros_list, comb_idx)


if __name__ == "__main__":
    for key in ["SDS(9,8,-1,[3,3])", "SDS(11,6,1,[11])", "SDS(13,12,-1,[13])",
                "SDS(9,8,1,[3,3])", "SDS(20,17,8,[2,10])", "SDS(27,25,16,[27])", "SDS(27,25,16,[3,3,3])", "SDS(27,25,16,[3,9])"]:
        tried, found = run(key)
        print("%-24s %8d tried, %4d found" % (key, tried, found))
