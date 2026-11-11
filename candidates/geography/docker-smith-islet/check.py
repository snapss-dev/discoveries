"""Check of the islet at the front of Docker Smith Gletscher, Melville Bay (76.263 N, 61.943 W).

Reads only files in its own folder:
  chip_YYYY-MM-DD.npz  3 km x 3 km Sentinel-2 L2A chips at 10 m (reflectance), centred on 76.26288 N, 61.94343 W
  area_series.csv      one row per Sentinel-2 scene (10 Jul to 25 Sep, 2018 to 2026, scene cloud < 35 %)
  dem_heights.csv      ArcticDEM strip heights sampled over the islet and the sea around it

Part 1 re-measures three dates from the pixels with code that shares nothing with the series script
(4-connected flood fill from the centre instead of 8-connected labelling).
Part 2 recomputes the yearly table and the separation bracket from the per-scene table.
Part 3 prints islet heights above the adjacent sea surface.
"""
import os, csv, collections, statistics
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ok_all = True


def check(name, cond):
    global ok_all
    ok_all &= bool(cond)
    print(("PASS  " if cond else "FAIL  ") + name)


def measure(fn):
    z = np.load(os.path.join(HERE, fn))
    g, n, s = z["green"].astype(float), z["nir"].astype(float), z["swir16"].astype(float)
    if np.percentile(n, 2) > 0.08:          # scenes stored with the +1000 DN offset
        g, n, s = g - 0.1, n - 0.1, s - 0.1
    water = ((g - n) / (g + n + 1e-6) > 0.15) & (n < 0.12)
    land = ~water
    H = land.shape[0]; c = H // 2
    ys, xs = np.nonzero(land)
    k = np.argmin((ys - c) ** 2 + (xs - c) ** 2)
    seen = np.zeros_like(land); stack = [(ys[k], xs[k])]; seen[ys[k], xs[k]] = True
    while stack:                             # 4-connected flood fill
        y, x = stack.pop()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yy, xx = y + dy, x + dx
            if 0 <= yy < H and 0 <= xx < H and land[yy, xx] and not seen[yy, xx]:
                seen[yy, xx] = True; stack.append((yy, xx))
    edge = seen[0].any() or seen[-1].any() or seen[:, 0].any() or seen[:, -1].any()
    bright = ((g - s) / (g + s + 1e-6) > 0.4) & (g > 0.25)
    area = seen.sum() * 1e-4
    return area, bool(edge), float((seen & ~bright).sum() * 1e-4)


print("Part 1: three dates re-measured from pixels (10 m, 4-connected)")
res = {}
for d in ("2020-09-04", "2021-07-19", "2026-08-30"):
    a, e, r = measure(f"chip_{d}.npz"); res[d] = (a, e, r)
    print(f"  {d}: component at the centre = {a:.4f} km2, reaches the window edge (joined to the glacier) = {e}, "
          f"free of snow and ice = {r:.4f} km2")
check("2020-09-04: still joined to the glacier front", res["2020-09-04"][1])
check("2021-07-19: surrounded by water, area 0.40 to 0.55 km2", (not res["2021-07-19"][1]) and 0.40 < res["2021-07-19"][0] < 0.55)
check("2026-08-30: surrounded by water, area 0.30 to 0.36 km2", (not res["2026-08-30"][1]) and 0.30 < res["2026-08-30"][0] < 0.36)
check("the islet lost area between 2021 and 2026", res["2026-08-30"][0] < res["2021-07-19"][0])
check("its snow- and ice-free part grew between 2021 and 2026", res["2026-08-30"][2] > res["2021-07-19"][2])

print("\nPart 2: per-scene table")
rows = list(csv.DictReader(open(os.path.join(HERE, "area_series.csv"))))
clean = [r for r in rows if r["clean"] == "True"]
print(f"  {len(rows)} scenes, {len(clean)} with < 1 % cloud and < 2 % cloud shadow within 700 m")
joined = [r for r in clean if r["touches_edge"] == "True" and float(r["area_km2"]) < 1.5 and r["date"][5:7] in ("08", "09")]
iso = [r for r in clean if r["touches_edge"] == "False" and float(r["area_km2"]) < 1.5]
last_joined = max(r["date"] for r in joined); first_iso = min(r["date"] for r in iso)
print(f"  last clear August-September date joined to the glacier: {last_joined}")
print(f"  first clear date surrounded by water:                   {first_iso}")
check("bracket is 2020-09-04 to 2021-07-19", last_joined == "2020-09-04" and first_iso == "2021-07-19")
check("no clear date after the bracket shows it joined again in August or September",
      not [r for r in joined if r["date"] > first_iso])
by = collections.defaultdict(list)
for r in iso:
    by[r["date"][:4]].append(r)
print("  year  dates  median area  min    max    median ice-free  median bright fraction   (km2; dates with drift ice against the shore removed)")
med = {}
for y in sorted(by):
    m0 = statistics.median(float(r["area_km2"]) for r in by[y])
    good = [r for r in by[y] if float(r["floe_frac"]) < 0.08 and 0.8 * m0 < float(r["area_km2"]) < 1.25 * m0]
    a = [float(r["area_km2"]) for r in good]; k = [float(r["rock_km2"]) for r in good]; b = [float(r["ice_frac"]) for r in good]
    med[y] = (statistics.median(a), statistics.median(k))
    print(f"  {y}  {len(a):5d}  {statistics.median(a):.4f}       {min(a):.4f} {max(a):.4f} {statistics.median(k):.4f}           {statistics.median(b):.3f}")
ys = sorted(med)
check("six summers of isolated dates (2021 to 2026)", ys == ["2021", "2022", "2023", "2024", "2025", "2026"])
check("median area falls from about 0.43 (2021) to about 0.34 km2 (2026)", 0.41 < med["2021"][0] < 0.46 and 0.32 < med["2026"][0] < 0.36)
check("median ice-free area rises from about 0.06 to about 0.10 km2", med["2021"][1] < 0.07 and med["2026"][1] > 0.095)

print("\nPart 3: ArcticDEM strips, height above the sea surface around the islet (m)")
print("  date        whole islet median / 90th pct   bright part median   ice-free rim median / 90th pct")
keep = []
for r in csv.DictReader(open(os.path.join(HERE, "dem_heights.csv"))):
    if not (10 < float(r["sea_med"]) < 30):   # cross-track strips of 2019 are tens of metres off and are left out
        continue
    keep.append(r)
    print(f"  {r['date']}  {float(r['island_med_above_sea']):6.1f} / {float(r['island_p90_above_sea']):5.1f}"
          f"               {float(r['ice_med_above_sea']):6.1f}               {float(r['rock_med_above_sea']):6.1f} / {float(r['rock_p90_above_sea']):5.1f}")
p90 = [float(r["island_p90_above_sea"]) for r in keep]
check("eight usable strips, 2020 to 2024", len(keep) == 8)
check("90th-percentile height stays between 50 and 60 m in every strip", all(50 < v < 60 for v in p90))
check("ice-free southern rim reaches about 25 to 32 m (90th percentile)", all(25 <= float(r["rock_p90_above_sea"]) <= 33 for r in keep))
print("\nALL CHECKS PASSED" if ok_all else "\nSOME CHECKS FAILED")
