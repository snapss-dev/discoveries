"""Tables for the note: near-miss convergents of 2/log 2 and the counterexamples found.
Run:  python tables.py 1300"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from flint import arb, ctx
from verify_arb import continued_fraction, certify, certain_int, log2

kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 1300
bits = kmax * 12 + 7000
b = continued_fraction(kmax, bits)
P = [b[0]]; Q = [1]; pm, qm = 1, 0
for a in b[1:kmax + 1]:
    p = a * P[-1] + pm; q = a * Q[-1] + qm
    pm, qm = P[-1], Q[-1]; P.append(p); Q.append(q)
ctx.prec = bits
L = log2()
rows = []
for k in range(1, kmax + 1):
    p, q = P[k], Q[k]
    if p % 2 == 0: continue
    # signed distance of n/L from the half-integer p/2, scaled:  d = M * (p/2 - n/L),  M = (p+3)/2
    M = (p + 3) // 2
    d = arb(M) * (arb(p) / 2 - arb(q) / L)
    dv = float(d.mid())
    if abs(dv) < 0.012:
        rows.append((k, len(str(q)), b[k + 1], dv))
print("| k | digits of n = q_k | b_(k+1) | mu | side | formula at n |")
print("|---:|---:|---:|---:|:---|:---|")
out = []
for k, dig, bk, dv in rows:
    if dv > 0:
        sgn, _ = certify((P[k] + 3) // 2, Q[k])
        verdict = "holds" if sgn > 0 else "**fails**"
        side = "below a half-integer"
    else:
        verdict = "holds (cannot fail on this side)"; side = "above a half-integer"
    print(f"| {k} | {dig} | {bk} | {dv:+.6f} | {side} | {verdict} |")
    if dv > 0 and "fails" in verdict: out.append(k)
with open("counterexamples.txt", "w", newline="\n") as f:
    f.write("# A072633: values of n with a(n) = 2 + round(n/log 2) (certified with Arb), for convergent index k <= %d\n" % kmax)
    f.write("# of 2/log 2 = [2; 1, 7, 1, 2, ...] (b_0 = 2 is k = 0) and odd multiples t.  Format: k t n\n")
    for k in out:
        t = 1
        while True:
            n = t * Q[k]; M = (t * P[k] + 3) // 2
            ctx.prec = bits
            mu = arb(M) * (arb(M) - arb(3) / 2 - arb(n) / L)
            if not (mu < arb(1) / 250): break
            sgn, _ = certify(M, n)
            if sgn < 0: f.write(f"{k} {t} {n}\n")
            t += 2
print("counterexample indices:", out)
