"""Conjectured generating functions for "number of base-b (circular) n-digit numbers with adjacent digits
differing by d or less" (29 OEIS entries between A124698 and A126531; formulas by Colin Barker, 2012-2017).

For each entry (read from conjectures.json, which holds the formulas and terms as published):
  1. the true sequence is computed by a transfer matrix M (M[i][j] = 1 iff |i - j| <= d):
         linear:   a(n) = sum of all entries of M^(n-1)   (leading zeros allowed)
         circular: a(n) = trace(M^n)
     and a(0) = 1 by the entries' convention;
  2. the matrix model is compared with brute-force enumeration of digit strings for all n with b^n <= 3*10^5;
  3. the published terms are compared with the matrix values;
  4. the conjectured g.f. P/Q is expanded with exact integers and compared with the true sequence for
     0 <= n <= N.  This is a proof as soon as N >= deg P + 1 + b + deg Q (see the page), which is asserted;
  5. the conjectured recurrence and closed form, where given, are tested for n <= N.
"""
import itertools
import json
import os
import re
import time
import sympy

N = 60
HERE = os.path.dirname(os.path.abspath(__file__))
x = sympy.symbols("x")


def matmul(A, B):
    n = len(A)
    return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]


def true_sequence(b, d, circular, nmax):
    M = [[1 if abs(i - j) <= d else 0 for j in range(b)] for i in range(b)]
    out = [1]
    P = [[1 if i == j else 0 for j in range(b)] for i in range(b)]      # M^(n-1)
    for n in range(1, nmax + 1):
        if circular:
            Pn = matmul(P, M)
            out.append(sum(Pn[i][i] for i in range(b)))
            P = Pn
        else:
            out.append(sum(sum(r) for r in P))
            P = matmul(P, M)
    return out


def brute(b, d, circular, n):
    c = 0
    for w in itertools.product(range(b), repeat=n):
        ok = all(abs(w[i] - w[i + 1]) <= d for i in range(n - 1))
        if ok and circular:
            ok = abs(w[-1] - w[0]) <= d
        c += ok
    return c


def series(Pc, Qc, nmax):
    # coefficients of P/Q, exact; Pc, Qc lists of ints by ascending degree, Qc[0] = +-1
    assert abs(Qc[0]) == 1
    out = []
    for n in range(nmax + 1):
        s = Pc[n] if n < len(Pc) else 0
        for j in range(1, min(n, len(Qc) - 1) + 1):
            s -= Qc[j] * out[n - j]
        assert s % Qc[0] == 0
        out.append(s // Qc[0])
    return out


t0 = time.time()
E = json.load(open(os.path.join(HERE, "conjectures.json")))
print("%-8s %4s %-8s %2s  %-22s %-9s %-9s %-10s %s" % ("entry", "base", "kind", "d", "published terms", "brute", "g.f.", "needed N", "recurrence / closed form"))
allok = True
for e in E:
    b, d, circ = e["base"], e["d"], e["circular"]
    t = true_sequence(b, d, circ, N)
    # 2. brute force
    nb = 0
    n = 1
    while b ** n <= 300000:
        assert brute(b, d, circ, n) == t[n], (e["A"], n)
        nb = n
        n += 1
    # 3. published terms
    data = e["data"]
    assert data == t[:len(data)], e["A"]
    # 4. generating function
    expr = sympy.sympify(e["gf"].replace("^", "**"))
    num, den = sympy.fraction(sympy.together(expr))
    Pp = sympy.Poly(sympy.expand(num), x)
    Qp = sympy.Poly(sympy.expand(den), x)
    Pc = [int(c) for c in reversed(Pp.all_coeffs())]
    Qc = [int(c) for c in reversed(Qp.all_coeffs())]
    g = series(Pc, Qc, N)
    need = (len(Pc) - 1) + 1 + b + (len(Qc) - 1)
    assert N >= need
    okg = g == t
    # 5. recurrence and closed form
    extra = []
    if e["recurrence"]:
        rhs, n0 = e["recurrence"]
        terms = re.findall(r"([+-]?\s*\d*)\*?a\(n-(\d+)\)", rhs)
        coef = {}
        for c, k in terms:
            c = c.replace(" ", "")
            coef[int(k)] = int(c) if c not in ("", "+", "-") else (1 if c in ("", "+") else -1)
        okr = all(t[n] == sum(c * t[n - k] for k, c in coef.items()) for n in range(n0 + 1, N + 1))
        extra.append("recurrence for n > %d: %s" % (n0, "ok" if okr else "FAILS"))
        allok &= okr
    if e["closed_form"]:
        m = re.match(r"1 \+ \(+(\d+)-sqrt\((\d+)\)\)(/2\))?\^n", e["closed_form"])
        A_, B_, half = int(m.group(1)), int(m.group(2)), bool(m.group(3))
        # alpha, beta = (A -+ sqrt B) or (A -+ sqrt B)/2 ; s(n) = alpha^n + beta^n
        p = A_ if half else 2 * A_
        q4 = A_ * A_ - B_
        assert (not half) or q4 % 4 == 0
        q = q4 // 4 if half else q4
        s = [2, p]
        for n in range(2, N + 1):
            s.append(p * s[n - 1] - q * s[n - 2])
        okc = all(t[n] == 1 + s[n] for n in range(1, N + 1))
        extra.append("closed form: %s" % ("ok" if okc else "FAILS"))
        allok &= okc
    allok &= okg
    print("%-8s %4d %-8s %2d  %-22s %-9s %-9s %-10d %s" % (
        e["A"], b, "circular" if circ else "linear", d, "%d terms ok" % len(data), "n <= %d" % nb,
        "ok to %d" % N if okg else "FAILS", need, "; ".join(extra)))
assert allok
print("all %d generating functions agree with the transfer-matrix sequence for 0 <= n <= %d, beyond the number "
      "of terms that makes the agreement a proof" % (len(E), N))
print("ALL CHECKS PASSED  (%.0f s)" % (time.time() - t0))
