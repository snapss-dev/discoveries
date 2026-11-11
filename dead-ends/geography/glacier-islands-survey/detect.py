"""Detect land that is water-enclosed in recent Sentinel-2 imagery but drawn inside a much larger OpenStreetMap
land polygon (i.e. mapped as attached to the mainland or to a glacier).

Usage: python -I detect2.py <region> [tile ...]
Reads data/stac_<region>.json and data/osm_<region>.pkl.
Writes out/cand_<region>.csv (all enclosed components), out/tiles_<region>.csv (per-tile coverage and
recall of mapped islands).

Water mask: a 20 m pixel is water if it is water (NDWI > 0.15 and NIR < 0.12) in ANY of up to three
low-cloud scenes of different dates; drifting ice therefore does not bridge channels, rock does.
"""
import sys, os, json, pickle, csv, warnings, threading
import numpy as np
import rasterio
from rasterio.enums import Resampling
from rasterio.features import rasterize
from rasterio.warp import transform_geom, transform as wtransform
from scipy import ndimage as ndi
from shapely.geometry import box, mapping
from shapely.strtree import STRtree
from concurrent.futures import ThreadPoolExecutor

warnings.filterwarnings("ignore")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_USERAGENT", "open-data-research/1.0")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")
os.environ.setdefault("GDAL_HTTP_MAX_RETRY", "4")
os.environ.setdefault("GDAL_HTTP_RETRY_DELAY", "3")
N = 5490
PX_KM2 = 0.0004
ST8 = np.ones((3, 3), bool)
MAXSC = int(os.environ.get("MAXSC", "3"))
LOCK = threading.Lock()
ISL = []


def read_band(href):
    with rasterio.open("/vsicurl/" + href) as ds:
        return ds.read(1, out_shape=(N, N), resampling=Resampling.nearest)


def header(href):
    with rasterio.open("/vsicurl/" + href) as ds:
        return ds.transform * ds.transform.scale(ds.width / N, ds.height / N), ds.crs


def pick(items):
    items = sorted(items, key=lambda d: d["cloud"] + 0.3 * (d["nodata"] or 0))
    out, days = [], set()
    for d in items:
        day = d["datetime"][:10]
        if day in days:
            continue
        if (d["nodata"] or 0) > 50 and out:
            continue
        out.append(d); days.add(day)
        if len(out) == MAXSC:
            break
    return out


def process(tile, items, osm, tree):
    sel = pick(items)
    tr, crs = header(sel[0]["assets"]["scl"])
    x0, y1 = tr * (0, 0); x1, y0 = tr * (N, N)
    lons, lats = wtransform(crs, "EPSG:4326", [x0, x1, x0, x1, (x0 + x1) / 2, (x0 + x1) / 2], [y0, y0, y1, y1, y0, y1])
    tb = box(min(lons) - 0.3, min(lats) - 0.05, max(lons) + 0.3, max(lats) + 0.05)
    geoms = [transform_geom("EPSG:4326", crs, mapping(osm[i])) for i in tree.query(tb)]
    osml = (rasterize(geoms, out_shape=(N, N), transform=tr, fill=0, default_value=1, dtype="uint8")
            if geoms else np.zeros((N, N), np.uint8)).astype(bool)
    lf = float(osml.mean())
    info = dict(tile=tile, osm_land_frac=round(lf, 4), scenes="", valid_frac=0, osm_islands=0, osm_islands_found=0,
                cand=0, status="")
    if lf < 0.003 or lf > 0.9995:
        info["status"] = "skip_no_coast"; return [], info
    water = np.zeros((N, N), bool); valid = np.zeros((N, N), bool); bare = np.zeros((N, N), bool)
    used = []
    for it in sel:
        try:
            g = read_band(it["assets"]["green"]); n = read_band(it["assets"]["nir"])
            s = read_band(it["assets"]["swir16"]); scl = read_band(it["assets"]["scl"])
        except Exception as e:
            print("  read fail", it["id"], str(e)[:80], flush=True); continue
        gg = g[::37, ::37]; gg = gg[gg > 0]
        off = 1000 if gg.size and gg.min() >= 1000 else 0
        for r0 in range(0, N, 610):
            q = slice(r0, r0 + 610)
            ok = (g[q] > 0) & ~np.isin(scl[q], (0, 1, 3, 8, 9, 10))
            gf = (g[q].astype(np.float32) - off) / 1e4; nf = (n[q].astype(np.float32) - off) / 1e4
            sf = (s[q].astype(np.float32) - off) / 1e4
            w = ok & ((gf - nf) / (gf + nf + 1e-6) > 0.15) & (nf < 0.12)
            b = ok & ~w & ((gf - sf) / (gf + sf + 1e-6) < 0.4)
            water[q] |= w; valid[q] |= ok; bare[q] |= b
        used.append(it["id"])
        del g, n, s, scl
    if not used:
        info["status"] = "read_fail"; return [], info
    with LOCK:
        return analyse(tile, tr, crs, osml, water, valid, bare, used, info)


def analyse(tile, tr, crs, osml, water, valid, bare, used, info):
    land = valid & ~water
    if os.environ.get("SAVENPZ"):
        np.savez_compressed(f"data/dbg_{tile}.npz", water=water, valid=valid, bare=bare, osml=osml, tr=np.array(tr)[:6], crs=str(crs))
    bare &= land
    info["scenes"] = "|".join(used); info["valid_frac"] = round(float(valid.mean()), 3)
    olab, on = ndi.label(osml, structure=ST8)
    oarea = np.bincount(olab.ravel())
    edge = np.unique(np.concatenate([olab[0], olab[-1], olab[:, 0], olab[:, -1]]))
    oarea_eff = oarea.astype(float); oarea_eff[edge[edge > 0]] = 1e9
    landd = ndi.binary_dilation(land, structure=ST8)
    lab, n = ndi.label(landd, structure=ST8)
    del landd
    lab[~land] = 0
    unk_d = ndi.binary_dilation(~valid, structure=ST8, iterations=3)
    area = np.bincount(lab.ravel(), minlength=n + 1)
    barea = np.bincount(lab[bare].ravel(), minlength=n + 1)
    touch_unk = np.bincount(lab[unk_d].ravel(), minlength=n + 1) > 0
    eb = np.zeros((N, N), bool); eb[:3] = eb[-3:] = True; eb[:, :3] = eb[:, -3:] = True
    touch_edge = np.bincount(lab[eb].ravel(), minlength=n + 1) > 0
    inosm = np.bincount(lab[osml].ravel(), minlength=n + 1)
    objs = ndi.find_objects(lab)
    wlab, wn = ndi.label(water, structure=ST8)
    wsea = np.bincount(wlab[~osml & water].ravel(), minlength=wn + 1)
    wtot = np.bincount(wlab.ravel(), minlength=wn + 1)
    rows = []; found = set()
    for i in range(1, n + 1):
        A = area[i]
        if A < 60 or A > 2.5e6 or touch_unk[i] or touch_edge[i] or objs[i - 1] is None:
            continue
        sl = objs[i - 1]
        sub = lab[sl] == i
        ol = olab[sl][sub]; ol = ol[ol > 0]
        if len(ol):
            k = np.bincount(ol).argmax(); kA = oarea_eff[k]
        else:
            k, kA = 0, 0
        f_in = inosm[i] / A; bf = barea[i] / A; ratio = kA / A
        if f_in > 0.5 and ratio > 4: cls = "IN_MAPPED_LAND"
        elif f_in > 0.3 and ratio <= 4: cls = "KNOWN_ISLAND"; found.add(int(k))
        elif f_in < 0.1: cls = "IN_MAPPED_SEA"
        else: cls = "AMBIG"
        yy, xx = np.nonzero(sub)
        cy, cx = yy.mean() + sl[0].start, xx.mean() + sl[1].start
        X, Y = tr * (cx + 0.5, cy + 0.5)
        lon, lat = wtransform(crs, "EPSG:4326", [X], [Y])
        r = dict(tile=tile, id=i, cls=cls, lon=round(lon[0], 5), lat=round(lat[0], 5), area_km2=round(A * PX_KM2, 4),
                 bare_frac=round(bf, 3), f_in_osm=round(f_in, 3), osm_comp_km2=round(kA * PX_KM2, 2),
                 adj_sea_px=-1, adj_water_px=-1, ring_new_frac=-1)
        if cls in ("IN_MAPPED_LAND", "AMBIG") and bf >= 0.3:
            s2 = (slice(max(0, sl[0].start - 6), sl[0].stop + 6), slice(max(0, sl[1].start - 6), sl[1].stop + 6))
            comp = lab[s2] == i
            ring = ndi.binary_dilation(comp, structure=ST8, iterations=3) & ~comp & water[s2]
            wl = np.unique(wlab[s2][ring]); wl = wl[wl > 0]
            r["adj_sea_px"] = int(wsea[wl].sum()); r["adj_water_px"] = int(wtot[wl].sum())
            r["ring_new_frac"] = round(float((ring & osml[s2]).sum() / max(1, ring.sum())), 3)
        rows.append(r)
    # recall of mapped islands (calibration): OSM components, not at tile edge, 0.05-100 km2, fully in valid data
    oobjs = ndi.find_objects(olab)
    no = nf = 0
    for k in range(1, on + 1):
        if oarea_eff[k] > 250000 or oarea[k] < 125 or oobjs[k - 1] is None:
            continue
        sl = oobjs[k - 1]
        s2 = (slice(max(0, sl[0].start - 4), sl[0].stop + 4), slice(max(0, sl[1].start - 4), sl[1].stop + 4))
        if unk_d[s2].any():
            continue
        no += 1; nf += k in found
        ISL.append((tile, k, round(oarea[k] * PX_KM2, 4), int(k in found)))
    info.update(osm_islands=no, osm_islands_found=nf, status="ok",
                cand=sum(1 for r in rows if r["cls"] in ("IN_MAPPED_LAND", "AMBIG") and r["bare_frac"] >= 0.3))
    return rows, info


if __name__ == "__main__":
    name = sys.argv[1]
    items = json.load(open(f"data/stac_{name}.json"))
    osm = pickle.load(open(f"data/osm_{name}.pkl", "rb"))
    tree = STRtree(osm)
    tiles = {}
    for d in items:
        tiles.setdefault(d["tile"], []).append(d)
    sel = sys.argv[2:] or sorted(tiles)
    allrows, infos = [], []

    def run(t):
        try:
            r, info = process(t, tiles[t], osm, tree)
        except Exception as e:
            r, info = [], dict(tile=t, osm_land_frac=-1, scenes="", valid_frac=0, osm_islands=0, osm_islands_found=0, cand=0,
                               status="FAIL " + str(e)[:100])
        print(t, info["status"], "landfrac", info["osm_land_frac"], "valid", info["valid_frac"], "osm_islands",
              info["osm_islands_found"], "/", info["osm_islands"], "cand", info["cand"], flush=True)
        return r, info

    suffix = os.environ.get("SUFFIX", "")
    FIELDS = ["tile", "id", "cls", "lon", "lat", "area_km2", "bare_frac", "f_in_osm", "osm_comp_km2", "adj_sea_px", "adj_water_px", "ring_new_frac"]
    IF = ["tile", "osm_land_frac", "scenes", "valid_frac", "osm_islands", "osm_islands_found", "cand", "status"]
    fc = open(f"out/cand_{name}{suffix}.csv", "w", newline=""); wc = csv.DictWriter(fc, fieldnames=FIELDS); wc.writeheader()
    ft = open(f"out/tiles_{name}{suffix}.csv", "w", newline=""); wtl = csv.DictWriter(ft, fieldnames=IF); wtl.writeheader()
    skip = set(os.environ.get("SKIP", "").split(","))
    sel = [t for t in sel if t not in skip]
    with ThreadPoolExecutor(int(os.environ.get("NTHREADS", "3"))) as ex:
        for r, info in ex.map(run, sel):
            allrows += r; infos.append(info)
            wc.writerows(r); wtl.writerow(info); fc.flush(); ft.flush()
    fc.close(); ft.close()
    with open(f"out/osmisl_{name}{suffix}.csv", "w") as f:
        print("tile,osm_comp,osm_area_km2,found", file=f)
        for r in ISL: print(",".join(map(str, r)), file=f)
    print("total", len(allrows), "tiles ok", sum(i["status"] == "ok" for i in infos))
