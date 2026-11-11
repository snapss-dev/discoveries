"""Eastern islet at Cape Caledon, Devon Island (75.6495 N, 80.4590 W): yearly area on clear Sentinel-2 dates.
Reads area_series.csv in this folder (one row per scene, 10 Jul to 25 Sep, 2018 to 2026)."""
import csv, os, statistics, collections
HERE = os.path.dirname(os.path.abspath(__file__))
rows = [r for r in csv.DictReader(open(os.path.join(HERE, "area_series.csv"))) if r["clean"] == "True"]
iso = [r for r in rows if r["touches_edge"] == "False" and 0.05 < float(r["area_km2"]) < 0.14 and float(r["floe_frac"]) < 0.08]
print(len(rows), "clear scenes;", len(iso), "with the islet surrounded by water and little drift ice")
by = collections.defaultdict(list)
for r in iso: by[r["date"][:4]].append(float(r["area_km2"]))
ok = True
for y in sorted(by):
    m = statistics.median(by[y]); print(f"  {y}: {len(by[y]):2d} dates, median {m:.4f} km2, range {min(by[y]):.4f} to {max(by[y]):.4f}")
    ok &= 0.09 < m < 0.12
allv = [v for y in by for v in by[y]]
print(f"all years: median {statistics.median(allv):.4f} km2, first isolated clear date {min(r['date'] for r in iso)}")
print("PASS" if ok and len(by) == 9 else "FAIL", "- islet present in every summer 2018 to 2026 with yearly median area between 0.09 and 0.12 km2 (no trend: rock)")
