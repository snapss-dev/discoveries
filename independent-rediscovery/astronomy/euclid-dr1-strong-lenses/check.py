"""Check of the page "93 Euclid DR1 strong lenses found independently of the consortium's catalogue".

    python check.py     reads rediscoveries.csv from its own folder

Verifies, without network access, that the numbers on the page follow from the table: every row lies
within 3 arcsec of an entry of the Euclid Consortium's ECLIPSE object catalogue (identifier, grade and
score copied from it), the cross-tabulation of the grades given here against the consortium's expert
grades, and the fraction the experts graded A or B.
"""
import csv
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "rediscoveries.csv"), newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
print("rows:", len(rows))
assert len(rows) == 93
assert len(set(r["eclipse_id"] for r in rows)) == 93, "two rows share a consortium identifier"
assert all(r["eclipse_id"].startswith("EUCL-DR1-L") for r in rows)
sep = [float(r["eclipse_separation_arcsec"]) for r in rows]
print("separation from the consortium's position: %d rows below 0.5 arcsec, largest %.2f arcsec" % (sum(s < 0.5 for s in sep), max(sep)))
# one system is a triple of galaxies with one arc; the consortium centres it on a different member
assert sum(s < 0.5 for s in sep) == 92 and max(sep) < 3.0
ours = ("A", "B+", "B")
theirs = ("A", "B", "C", "X")
tab = {o: {t: sum(1 for r in rows if r["grade_here"] == o and r["eclipse_grade"] == t) for t in theirs} for o in ours}
print("\ngrade here (rows) against the consortium's expert grade (columns)")
print("%-6s" % "" + "".join("%5s" % t for t in theirs) + "  total")
for o in ours:
    print("%-6s" % o + "".join("%5d" % tab[o][t] for t in theirs) + "%7d" % sum(tab[o].values()))
tot = {t: sum(tab[o][t] for o in ours) for t in theirs}
print("%-6s" % "all" + "".join("%5d" % tot[t] for t in theirs) + "%7d" % sum(tot.values()))
assert tab["A"] == {"A": 3, "B": 1, "C": 0, "X": 0}
assert tot == {"A": 32, "B": 49, "C": 11, "X": 1}
ab = tot["A"] + tot["B"]
print("\ngraded A or B by the consortium's experts: %d of %d (%.0f per cent)" % (ab, len(rows), 100.0 * ab / len(rows)))
assert ab == 81
pub = [r for r in rows if r["eclipse_earliest_publication"].strip()]
print("rows the consortium's catalogue marks as published before it: %d (%s)" % (
    len(pub), "; ".join(sorted(set(r["eclipse_earliest_publication"] for r in pub)))))
assert len(pub) == 5
print("\nALL CHECKS PASSED")
