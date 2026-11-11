"""Contact sheet for triage: one false-colour chip (SWIR/NIR/green; water black, ice cyan, rock brown) per candidate,
OSM land edge in yellow. Usage: python -I sheet.py <region> [min_area_km2] [max_n] [suffix]"""
import sys, os, json, pickle, warnings
import numpy as np, pandas as pd, rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform as wt, transform_geom
from rasterio.enums import Resampling
from shapely.geometry import box, shape
from shapely.strtree import STRtree
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor
warnings.filterwarnings("ignore")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("GDAL_HTTP_USERAGENT", "open-data-research/1.0")
name = sys.argv[1]; amin = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05; maxn = int(sys.argv[3]) if len(sys.argv) > 3 else 40
suffix = sys.argv[4] if len(sys.argv) > 4 else ""
d = pd.read_csv(f"out/cand_{name}{suffix}.csv")
t = pd.read_csv(f"out/tiles_{name}{suffix}.csv").set_index("tile")
c = d[d.cls.isin(["IN_MAPPED_LAND", "AMBIG"]) & (d.bare_frac >= 0.3) & (d.area_km2 >= amin)
      & (((d.adj_sea_px > 2000) & (d.ring_new_frac >= 0.15)) | ((d.adj_sea_px <= 2000) & (d.adj_water_px > 2500)))].copy()
# drop duplicates from overlapping tiles (same place within ~300 m)
c = c.sort_values("area_km2", ascending=False)
keep = []
for _, r in c.iterrows():
    if all(abs(r.lat - k.lat) > 0.004 or abs(r.lon - k.lon) * np.cos(np.radians(r.lat)) > 0.004 for k in keep):
        keep.append(r)
c = pd.DataFrame(keep).head(int(os.environ.get('PRE', '160'))).reset_index(drop=True)
items = {x["id"]: x for x in json.load(open(f"data/stac_{name}.json"))}
osm = pickle.load(open(f"data/osm_{name}.pkl", "rb")); tree = STRtree(osm)

from scipy import ndimage as ndi
import math

def ring_slope(sw, nr, gr, crs, b, half, r):
    """Median Copernicus DEM slope (deg) under the water pixels within 100 m of the central land component.
    Terrain shadow misread as water lies on steep slopes; sea, lakes and former glacier tongues are gentle."""
    try:
        water = ((gr - nr) / (gr + nr + 1e-6) > 0.15) & (nr < 0.12)
        lab, n = ndi.label(~water, structure=np.ones((3, 3)))
        yy, xx = np.nonzero(lab); c0 = lab.shape[0] // 2
        k = np.argmin((yy - c0) ** 2 + (xx - c0) ** 2)
        comp = lab == lab[yy[k], xx[k]]
        if comp.mean() > 0.5: return 99.0
        ring = ndi.binary_dilation(comp, structure=np.ones((3, 3)), iterations=5) & water
        ys, xs = np.nonzero(ring)
        if len(ys) < 10: return 99.0
        X = b[0] + (xs + 0.5) * 20; Y = b[3] - (ys + 0.5) * 20
        lo, la = wt(crs, "EPSG:4326", list(X), list(Y)); lo = np.array(lo); la = np.array(la)
        latf = math.floor(r.lat); lonf = math.floor(r.lon)
        nm = f"Copernicus_DSM_COG_10_{'N' if latf >= 0 else 'S'}{abs(latf):02d}_00_{'E' if lonf >= 0 else 'W'}{abs(lonf):03d}_00_DEM"
        with rasterio.open(f"/vsicurl/https://copernicus-dem-30m.s3.amazonaws.com/{nm}/{nm}.tif") as ds:
            w = from_bounds(max(lonf, lo.min() - 0.01), max(latf, la.min() - 0.005), min(lonf + 1, lo.max() + 0.01), min(latf + 1, la.max() + 0.005), ds.transform)
            w = w.round_offsets().round_lengths()
            z = ds.read(1, window=w).astype(float); tr = ds.window_transform(w)
        dy = abs(tr.e) * 111320.0; dx = tr.a * 111320.0 * math.cos(math.radians(r.lat))
        gy, gx = np.gradient(z, dy, dx)
        sl = np.degrees(np.arctan(np.hypot(gx, gy)))
        cc = ((lo - tr.c) / tr.a).astype(int); rr = ((la - tr.f) / tr.e).astype(int)
        ok = (cc >= 0) & (cc < z.shape[1]) & (rr >= 0) & (rr < z.shape[0])
        if ok.sum() < 10: return 99.0
        return float(np.median(sl[rr[ok], cc[ok]]))
    except Exception as e:
        return -1.0

def chip(r):
    it = items[t.loc[r.tile, "scenes"].split("|")[0]]
    half = max(3000.0, 4 * np.sqrt(r.area_km2) * 1000)
    B = []
    for k in ("swir16", "nir", "green"):
        with rasterio.open("/vsicurl/" + it["assets"][k]) as ds:
            X, Y = wt("EPSG:4326", ds.crs, [r.lon], [r.lat])
            b = (X[0] - half, Y[0] - half, X[0] + half, Y[0] + half)
            n = int(2 * half / 20)
            B.append(ds.read(1, window=from_bounds(*b, ds.transform), boundless=True, fill_value=0, out_shape=(n, n),
                             resampling=Resampling.bilinear).astype(float) / 1e4)
            crs = ds.crs
    img = np.clip(np.dstack(B) / 0.6, 0, 1) ** 0.8
    lines = []
    ll = wt(crs, "EPSG:4326", [b[0], b[2], b[0], b[2]], [b[1], b[1], b[3], b[3]])
    qb = box(min(ll[0]), min(ll[1]), max(ll[0]), max(ll[1])); bb = box(*b)
    for i in tree.query(qb):
        g0 = osm[i].intersection(qb.buffer(0.01))
        if g0.is_empty or g0.geom_type not in ("Polygon", "MultiPolygon"): continue
        try:
            gg = shape(transform_geom("EPSG:4326", crs, g0.__geo_interface__)).buffer(0).intersection(bb)
        except Exception:
            continue
        for poly in getattr(gg, "geoms", [gg]):
            if poly.geom_type != "Polygon": continue
            for ring in [poly.exterior] + list(poly.interiors):
                x, y = np.array(ring.coords).T
                lines.append(((x - b[0] - half) / 1000, (y - b[1] - half) / 1000))
    sw, nr, gr = B
    slope = ring_slope(sw, nr, gr, crs, b, half, r)
    ice = float((((gr - sw) / (gr + sw + 1e-6) > 0.4) & (gr > 0.25)).mean())
    return img, half, lines, it["id"], ice, slope

print('prefilter', len(c), flush=True)
with ThreadPoolExecutor(6) as ex:
    res = list(ex.map(lambda r: chip(r), [r for _, r in c.iterrows()]))
c["ice_frac"] = [x[4] for x in res]; c["ring_slope"] = [round(x[5], 1) for x in res]
ok = ((c.ice_frac >= 0.02) & (c.ring_slope < 8)).values
res = [x for x, o in zip(res, ok) if o][:maxn]; c = c[ok].head(maxn).reset_index(drop=True)
c.to_csv(f"out/triage_{name}{suffix}.csv", index=False)
print(c[["tile", "lon", "lat", "area_km2", "bare_frac", "f_in_osm", "adj_sea_px", "adj_water_px", "ring_new_frac", "ice_frac", "ring_slope"]].to_string())
n = len(res); cols = 6; rows = max(1, (n + cols - 1) // cols)
fig, axs = plt.subplots(rows, cols, figsize=(3.6 * cols, 3.75 * rows), squeeze=False)
for ax in axs.ravel(): ax.axis("off")
for j, ((img, half, lines, iid, _ice, _sl), (_, r)) in enumerate(zip(res, c.iterrows())):
    ax = axs[j // cols, j % cols]; ax.axis("on")
    e = half / 1000
    ax.imshow(img, extent=[-e, e, -e, e], interpolation="nearest")
    for x, y in lines: ax.plot(x, y, "-", color="yellow", lw=0.7)
    ax.plot([0], [0], "r+", ms=14, mew=1)
    ax.set_xlim(-e, e); ax.set_ylim(-e, e)
    ax.set_title(f"#{j} {r.lat:.4f},{r.lon:.4f} {r.area_km2:.2f}km2 new{r.ring_new_frac:.2f} s{r.ring_slope:.0f} {"SEA" if r.adj_sea_px > 2000 else "lake"}\n{iid}", fontsize=7)
    ax.tick_params(labelsize=6)
plt.tight_layout(); plt.savefig(f"out/sheet_{name}{suffix}.png", dpi=75); print("wrote sheet", n)
