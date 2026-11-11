"""Coverage and calibration table of the island survey, recomputed from the per-tile logs in this folder.
tiles_<region>.csv: one row per Sentinel-2 tile (scenes used, share of valid pixels, mapped islands present and recovered).
triage_<region>.csv: candidates left after the automatic filters, before inspection by eye."""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
REG = [("sg", "South Georgia"), ("pat", "Patagonia 46-52.5 S"), ("tdf", "Tierra del Fuego 54-55.3 S"),
       ("gl_nw", "NW Greenland 72-76.7 N"), ("gl_w", "W Greenland 68-72 N"), ("gl_se", "SE Greenland 60-68.7 N"),
       ("gl_e", "E Greenland 68.7-74.5 N (part)"), ("ca_e", "SE Ellesmere, N Devon (part)"), ("ak", "Alaska 132-151 W coast"),
       ("ap", "Antarctic Peninsula 62.8-68 S")]
print(f"{'region':34s} tiles  analysed  no-coast  valid  mapped islands  recovered  recall  left for inspection")
T = A = M = F = K = 0
for key, name in REG:
    rows = list(csv.DictReader(open(os.path.join(HERE, f"tiles_{key}.csv"))))
    ok = [r for r in rows if r["status"] == "ok"]
    skip = sum(r["status"] == "skip_no_coast" for r in rows)
    bad = len(rows) - len(ok) - skip
    m = sum(int(r["osm_islands"]) for r in ok); f = sum(int(r["osm_islands_found"]) for r in ok)
    v = sum(float(r["valid_frac"]) for r in ok) / max(1, len(ok))
    p = os.path.join(HERE, f"triage_{key}.csv")
    k = len(list(csv.DictReader(open(p)))) if os.path.exists(p) else 0
    print(f"{name:34s} {len(rows):5d}  {len(ok):8d}  {skip:8d}  {v:5.2f}  {m:14d}  {f:9d}  {f / max(1, m):6.2f}  {k:6d}" + (f"   ({bad} failed)" if bad else ""))
    T += len(rows); A += len(ok); M += m; F += f; K += k
print(f"{'total':34s} {T:5d}  {A:8d}  {'':8s}  {'':5s}  {M:14d}  {F:9d}  {F / M:6.2f}  {K:6d}")
ak = list(csv.DictReader(open(os.path.join(HERE, "triage_ak.csv"))))
hit = [r for r in ak if abs(float(r["lat"]) - 59.194) < 0.02 and abs(float(r["lon"]) + 138.066) < 0.03]
print("Prow Knob, Alsek Lake (documented separation, summer 2025) recovered:", bool(hit),
      f"area {float(hit[0]['area_km2']):.2f} km2 at {hit[0]['lat']} N, {hit[0]['lon']} E" if hit else "")
nw = list(csv.DictReader(open(os.path.join(HERE, "triage_gl_nw.csv"))))
hit = [r for r in nw if abs(float(r["lat"]) - 76.2629) < 0.01 and abs(float(r["lon"]) + 61.943) < 0.02]
print("Docker Smith islet in the NW Greenland list:", bool(hit))
ca = list(csv.DictReader(open(os.path.join(HERE, "triage_ca_e.csv"))))
hit = [r for r in ca if abs(float(r["lat"]) - 75.65) < 0.01 and abs(float(r["lon"]) + 80.47) < 0.03]
print("Cape Caledon islets (Pelto 2018) in the Canadian list:", len(hit), "components")
