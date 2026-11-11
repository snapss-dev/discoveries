"""V627 Peg on Harvard plates: an independent measurement from the plate pixels.

For every digitised Harvard plate that covers V627 Peg in a time window, this script downloads a
20-arcminute cutout from the public DASCH DR7 service and measures the image at the star's position.
It does not use the DASCH pipeline's photometry.

Stage 1 (every plate): is there an image at the position? The sky-subtracted aperture sum is compared
with the scatter of the same sum at star-free places on the same cutout (z).
Stage 2 (plates with a detection, and plates within 12 days of one): four neighbouring cutouts are added
and the image is compared with isolated catalogue stars on the same plate (Tycho-2 and APASS DR9 B
magnitudes from VizieR). Two estimates come out: a straight-line calibration where at least six comparison
stars are detected, and a bracket, the catalogue magnitudes of the comparison stars whose images are just
stronger and just weaker than the target's. For a plate without a detection the same stars give a limit.

Run:  python check.py 1905-06-25 1905-10-10 out_1905
      python check.py 1942-11-01 1943-01-15 out_1942      (control: the superoutburst known from Sonneberg)

Writes <out>/plates.csv, <out>/lightcurve.png and <out>/montage.png; downloads are kept in <out>/cache.
"""
import base64
import csv
import gzip
import io
import json
import os
import sys
import time
import warnings

import numpy as np
import requests
from astropy.io import fits
from astropy.time import Time

warnings.filterwarnings("ignore")        # astropy's "dubious year" note for dates before 1960

API = "https://api.starglass.cfa.harvard.edu/public/dasch/dr7/"
VIZ = ["https://vizier.cfa.harvard.edu/viz-bin/asu-tsv", "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"]
UA = {"User-Agent": "open-data-research/1.0"}
RA0, DEC0 = 324.52762, 26.33223          # V627 Peg, J2000
PIX = 1.44                               # arcsec per cutout pixel (the cutouts have CD = 0.0004 deg)
R_AP, R_IN, R_OUT = 20, 50, 70           # aperture and sky annulus, pixels
STEP = 16.0                              # arcmin between the centres of neighbouring cutouts
NEIGHBOURS = [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]
DETECT_Z = 5.0


def cached(path, fetch):
    if os.path.exists(path):
        return open(path, "rb").read()
    data = fetch()
    if data is not None:
        with open(path, "wb") as f:
            f.write(data)
    return data


def dasch(endpoint, payload):
    """POST to the DASCH API. Returns the body, b"null" if the request cannot be served, None on failure."""
    wait = 15
    for _ in range(7):
        try:
            r = requests.post(API + endpoint, json=payload, headers=UA, timeout=180)
            if r.status_code == 200:
                time.sleep(0.7)
                return r.content
            if r.status_code in (400, 404):
                return b"null"
        except requests.RequestException:
            pass
        time.sleep(wait)
        wait = min(wait * 2, 240)
    return None


def vizier(source):
    q = {"-source": source, "-c": f"{RA0} {DEC0}", "-c.rm": "34", "-out.all": "", "-out.max": "20000"}
    for base in VIZ:
        try:
            r = requests.get(base, params=q, headers=UA, timeout=180)
            if r.status_code == 200 and "\t" in r.text:
                return r.content
        except requests.RequestException:
            continue
    raise SystemExit("VizieR unreachable")


def parse_tsv(raw, cols):
    """Rows of the named columns from a VizieR tab-separated table (blank cells become NaN)."""
    head, rows = None, []
    for line in raw.decode("utf-8", "replace").splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("\t")]
        if head is None:
            head = parts
            idx = [head.index(c) for c in cols]
            continue
        try:
            rows.append([float(parts[i]) if parts[i] else np.nan for i in idx])
        except (ValueError, IndexError):
            continue                      # the units and separator lines
    return np.array(rows, dtype=float).reshape(-1, len(cols))


def sep(ra1, de1, ra2, de2):
    """Small-angle separation in arcseconds."""
    return 3600 * np.hypot((ra1 - ra2) * np.cos(np.radians(de1)), de1 - de2)


def catalogue(cache):
    """(ra, dec, B) of catalogue stars: Tycho-2 at the bright end, APASS DR9 below it."""
    ty = parse_tsv(cached(f"{cache}/tycho2_wide.tsv", lambda: vizier("I/259/tyc2")),
                   ["RA(ICRS)", "DE(ICRS)", "BTmag", "VTmag"])
    ap = parse_tsv(cached(f"{cache}/apass9_wide.tsv", lambda: vizier("II/336/apass9")),
                   ["RAJ2000", "DEJ2000", "Bmag", "Vmag"])
    stars = [(ra, dec, bt - 0.24 * (bt - vt)) for ra, dec, bt, vt in ty      # Johnson B from BT, VT
             if np.isfinite(bt) and np.isfinite(vt)]
    bright = np.array(stars)
    for ra, dec, b, _ in ap:
        if np.isfinite(b) and b > 10.5 and np.min(sep(ra, dec, bright[:, 0], bright[:, 1])) > 5:
            stars.append((ra, dec, b))                                     # APASS saturates above this
    return np.array(stars)


def centre(dx, dy):
    return RA0 + dx * STEP / 60 / np.cos(np.radians(DEC0)), DEC0 + dy * STEP / 60


def to_pix(ra, dec, n, ra_c, dec_c):
    """Cutouts are resampled to a north-up tangent plane centred on the requested position."""
    c = (n - 1) / 2
    return c - (ra - ra_c) * np.cos(np.radians(dec_c)) * 3600 / PIX, c + (dec - dec_c) * 3600 / PIX


def cutout(cache, pid, sol, dx, dy):
    ra_c, dec_c = centre(dx, dy)
    tag = "" if (dx, dy) == (0, 0) else f"_{dx:+d}{dy:+d}"
    raw = cached(f"{cache}/{pid}_{sol}{tag}.b64", lambda: dasch("cutout", {
        "plate_id": pid, "solution_number": sol, "center_ra_deg": float(ra_c), "center_dec_deg": float(dec_c)}))
    try:
        payload = json.loads(raw) if raw else None
        img = fits.open(io.BytesIO(gzip.decompress(base64.b64decode(payload))))[0].data.astype(float)
    except Exception:
        return None
    img[img == 0] = np.nan                # BLANK: off the plate
    return img


def measure(img, x, y):
    """Sky-subtracted aperture sum and the offset of its centroid (pixels)."""
    n = img.shape[0]
    if not (R_OUT + 1 < x < n - R_OUT - 2 and R_OUT + 1 < y < n - R_OUT - 2):
        return None
    x0, y0 = int(round(x)) - R_OUT - 1, int(round(y)) - R_OUT - 1
    sub = img[y0:y0 + 2 * R_OUT + 3, x0:x0 + 2 * R_OUT + 3]
    yy, xx = np.mgrid[0:sub.shape[0], 0:sub.shape[1]]
    xx, yy = xx + x0, yy + y0
    r = np.hypot(xx - x, yy - y)
    sky_px = sub[(r > R_IN) & (r < R_OUT)]
    sky_px = sky_px[np.isfinite(sky_px)]
    ap = (r <= R_AP) & np.isfinite(sub)
    if sky_px.size < 500 or ap.sum() < 0.9 * np.pi * R_AP ** 2:
        return None
    d = sub[ap] - np.median(sky_px)
    w = np.clip(d, 0, None)
    if w.sum() > 0:
        dx, dy = (w * (xx[ap] - x)).sum() / w.sum(), (w * (yy[ap] - y)).sum() / w.sum()
    else:
        dx = dy = np.nan
    return d.sum(), dx, dy


def sky_scatter(img, stars_xy, rng, tries=400):
    """Scatter of the aperture sum at star-free places on this cutout (robust)."""
    n = img.shape[0]
    sums = []
    for _ in range(tries):
        x, y = rng.uniform(R_OUT + 5, n - R_OUT - 5, 2)
        if np.hypot(x - (n - 1) / 2, y - (n - 1) / 2) < 3 * R_AP:
            continue
        if stars_xy.size and np.min(np.hypot(stars_xy[:, 0] - x, stars_xy[:, 1] - y)) < 2.2 * R_AP:
            continue
        m = measure(img, x, y)
        if m:
            sums.append(m[0])
    sums = np.array(sums)
    if sums.size < 15:
        return np.nan
    return 1.4826 * np.median(np.abs(sums - np.median(sums)))


def comparison(img, stars, ra_c, dec_c):
    """Aperture sums of isolated catalogue stars on one cutout: rows of (B, sum, centroid offset arcsec)."""
    out = []
    n = img.shape[0]
    for i, (ra, dec, b) in enumerate(stars):
        if sep(ra, dec, RA0, DEC0) < 100 or b > 13.5:
            continue
        x, y = to_pix(ra, dec, n, ra_c, dec_c)
        if not (R_OUT + 1 < x < n - R_OUT - 2 and R_OUT + 1 < y < n - R_OUT - 2):
            continue
        d = sep(ra, dec, stars[:, 0], stars[:, 1])
        d[i] = 1e9
        if np.any((d < 90) & (stars[:, 2] < b + 2.0)):
            continue                      # a similar or brighter neighbour within 90 arcsec
        m = measure(img, x, y)
        if m:
            out.append((b, m[0], np.hypot(m[1], m[2]) * PIX))
    return out


def calibrate(sums, cat):
    """Catalogue B against instrumental magnitude: a robust straight line with a free slope, because a
    photographic plate is not linear. Returns (coefficients, rms, number of stars) or None."""
    inst = -2.5 * np.log10(sums)
    keep = np.ones(inst.size, bool)
    for _ in range(5):
        if keep.sum() < 6:
            return None
        co = np.polyfit(inst[keep], cat[keep], 1)
        res = cat - np.polyval(co, inst)
        s = 1.4826 * np.median(np.abs(res[keep] - np.median(res[keep]))) + 1e-6
        new = np.abs(res) < max(3 * s, 0.35)
        if (new == keep).all():
            break
        keep = new
    return co, float(np.sqrt(np.mean(res[keep] ** 2))), int(keep.sum())


def bracket(target_sum, good):
    """Catalogue B of the detected comparison stars with the nearest stronger and nearest weaker image."""
    stronger = good[good[:, 1] >= target_sum]
    weaker = good[good[:, 1] < target_sum]
    b_bright = float(stronger[np.argmin(stronger[:, 1]), 0]) if len(stronger) else np.nan
    b_faint = float(weaker[np.argmax(weaker[:, 1]), 0]) if len(weaker) else np.nan
    return b_bright, b_faint


def depth(comp, scat):
    """How deep the plate goes at this place: going down the comparison stars in order of catalogue
    magnitude, the last one before the first that is not detected."""
    last = np.nan
    for b, s, _ in comp[np.argsort(comp[:, 0])]:
        if s <= DETECT_Z * scat:
            break
        last = float(b)
    return last


def main(t0, t1, out):
    cache = f"{out}/cache"
    os.makedirs(cache, exist_ok=True)
    rng = np.random.default_rng(1905)
    stars = catalogue(cache)
    near = [(round(float(sep(RA0, DEC0, s[0], s[1])), 1), round(float(s[2]), 2)) for s in stars
            if sep(RA0, DEC0, s[0], s[1]) < 120]
    print(f"catalogue stars within 34': {len(stars)}; within 2' of the target (sep\", B): {near}")

    lines = json.loads(cached(f"{cache}/queryexps.json", lambda: dasch("queryexps", {"ra_deg": RA0, "dec_deg": DEC0})))
    sel, seen = [], set()
    for r in csv.DictReader(io.StringIO("\n".join(lines))):
        if not (t0 <= r["expdate"][:10] <= t1) or r["solnum"] in ("", None) or int(float(r["solnum"])) < 0:
            continue
        if r["series"] == "ai" and not (r["limMagApass"] or r["limMagAtlas"]):
            continue                      # the widest-field patrol camera; too shallow without a calibration
        key = (r["series"], r["platenum"], r["solnum"])
        if key not in seen:
            seen.add(key)
            sel.append(r)
    sel.sort(key=lambda r: r["expdate"])
    print(f"plates with an astrometric solution covering the position, {t0} to {t1}: {len(sel)}")

    # stage 1: is there an image at the position?
    rows = []
    for r in sel:
        pid, sol = f"{r['series']}{int(r['platenum']):05d}", int(float(r["solnum"]))
        img = cutout(cache, pid, sol, 0, 0)
        if img is None:
            print(f"{pid}: no cutout")
            continue
        n = img.shape[0]
        sxy = np.array([to_pix(s[0], s[1], n, RA0, DEC0) for s in stars if s[2] < 14.5])
        scat = sky_scatter(img, sxy, rng)
        tgt = measure(img, (n - 1) / 2, (n - 1) / 2)
        if tgt is None or not np.isfinite(scat) or scat <= 0:
            print(f"{pid}: target area unusable")
            continue
        z = tgt[0] / scat
        rows.append(dict(plate=pid, sol=sol, date=r["expdate"][:16],
                         jd=Time(r["expdate"].replace("Z", ""), format="isot", scale="utc").jd,
                         z=float(z), sum=float(tgt[0]), scat=float(scat), img=img,
                         offset=float(np.hypot(tgt[1], tgt[2]) * PIX) if z > DETECT_Z else np.nan))
    det_jd = [x["jd"] for x in rows if x["z"] > DETECT_Z]

    # stage 2: magnitudes and limits on the plates in and around the detections
    for x in rows:
        x.update(B=np.nan, rms=np.nan, ncomp=0, lim5=np.nan, comp_offset=np.nan,
                 brighter_than=np.nan, fainter_than=np.nan, depth=np.nan, note="")
        if not det_jd or min(abs(x["jd"] - j) for j in det_jd) > 12:
            continue
        comp = []
        for dx, dy in NEIGHBOURS:
            img = x["img"] if (dx, dy) == (0, 0) else cutout(cache, x["plate"], x["sol"], dx, dy)
            if img is not None:
                comp += comparison(img, stars, *centre(dx, dy))
        comp = np.array(comp).reshape(-1, 3)
        good = comp[comp[:, 1] > DETECT_Z * x["scat"]]       # stars that are themselves detected
        cal = calibrate(good[:, 1], good[:, 0]) if len(good) >= 6 else None
        x["depth"] = depth(comp, x["scat"]) if len(comp) else np.nan
        if len(good):
            x["comp_offset"] = float(np.median(good[:, 2]))
        if cal:
            co, x["rms"], x["ncomp"] = cal
            x["lim5"] = float(np.polyval(co, -2.5 * np.log10(DETECT_Z * x["scat"])))
            if x["z"] > DETECT_Z:
                x["B"] = float(np.polyval(co, -2.5 * np.log10(x["sum"])))
        if x["z"] > DETECT_Z and len(good):
            x["fainter_than"], x["brighter_than"] = bracket(x["sum"], good)
        if not np.isfinite(x["depth"]):
            x["note"] = "too shallow: the brightest comparison star is not detected either"

    cols = ["plate", "date", "jd", "z", "B", "rms", "ncomp", "fainter_than", "brighter_than", "lim5", "depth",
            "offset", "comp_offset", "note"]
    fmt = dict(jd="{:.4f}", z="{:.1f}", B="{:.2f}", rms="{:.2f}", lim5="{:.2f}", offset="{:.1f}",
               comp_offset="{:.1f}", fainter_than="{:.1f}", brighter_than="{:.1f}", depth="{:.1f}")
    for x in rows:
        for c in cols:
            x.setdefault(c, np.nan if c in fmt else "")
    table = [{c: (fmt[c].format(x[c]) if c in fmt and np.isfinite(x[c]) else ("" if c in fmt else x[c]))
              for c in cols} for x in rows]
    print("B, rms, n: straight-line calibration, its scatter and its number of stars. bracket: catalogue B of the")
    print("comparison stars with the nearest stronger and weaker image. lim5: 5-sigma limit from the calibration.")
    print("depth: faintest comparison star in an unbroken run of detected ones. Offsets in arcseconds.")
    print("plate     date                   z      B   rms   n    bracket    lim5  depth  offset  comp.offset")
    for t in table:
        br = f"{t['fainter_than']:>4s}-{t['brighter_than']:<4s}" if t["fainter_than"] or t["brighter_than"] else " " * 9
        print(f"{t['plate']:9s} {t['date']}  {t['z']:>6s} {t['B']:>6s} {t['rms']:>5s} {t['ncomp']:>3}  {br}  "
              f"{t['lim5']:>6s} {t['depth']:>6s}  {t['offset']:>6s}  {t['comp_offset']:>6s}  {t['note']}")
    print(f"detected (z > {DETECT_Z:g}): {[x['plate'] for x in rows if x['z'] > DETECT_Z]}")
    others = [x["z"] for x in rows if x["z"] <= DETECT_Z]
    print(f"largest z among the other {len(others)} plates: {max(others):.1f}")
    with open(f"{out}/plates.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(table)
    figures(rows, out)


def figures(rows, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    for x in rows:
        x["B_plot"], x["B_err"], x["lim_plot"] = np.nan, np.nan, np.nan
        if x["z"] > DETECT_Z:
            if np.isfinite(x["B"]):
                x["B_plot"], x["B_err"] = x["B"], max(x["rms"], 0.1)
            elif np.isfinite(x["fainter_than"]) and np.isfinite(x["brighter_than"]):
                x["B_plot"] = (x["fainter_than"] + x["brighter_than"]) / 2
                x["B_err"] = abs(x["brighter_than"] - x["fainter_than"]) / 2
        else:
            x["lim_plot"] = x["lim5"] if np.isfinite(x["lim5"]) else x["depth"]
    det = [x for x in rows if np.isfinite(x["B_plot"])]
    lim = [x for x in rows if np.isfinite(x["lim_plot"])]
    fig, ax = plt.subplots(figsize=(9, 4.4), dpi=130)
    if det:
        ax.errorbar([Time(x["jd"], format="jd").datetime for x in det], [x["B_plot"] for x in det],
                    yerr=[x["B_err"] for x in det], fmt="o", color="#b3261e", capsize=3, label="detected")
    if lim:
        ax.plot([Time(x["jd"], format="jd").datetime for x in lim], [x["lim_plot"] for x in lim], "v",
                color="#555555", label="not detected: fainter than this")
    ax.invert_yaxis()
    ax.set_ylabel("B magnitude")
    ax.set_title("V627 Peg on Harvard plates, measured from the plate pixels")
    ax.grid(alpha=0.3)
    ax.legend(loc="lower center")
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(f"{out}/lightcurve.png")
    plt.close(fig)

    det_jd = [x["jd"] for x in rows if x["z"] > DETECT_Z]
    show = [x for x in rows if det_jd and min(abs(x["jd"] - j) for j in det_jd) <= 16] or rows[:18]
    ncol = 6
    nrow = int(np.ceil(len(show) / ncol))
    fig, axes = plt.subplots(nrow, ncol, figsize=(2.3 * ncol, 2.55 * nrow + 0.5), dpi=110, squeeze=False)
    half = 170                               # the stamps are about 8 arcminutes across
    for a in axes.ravel():
        a.axis("off")
    for a, x in zip(axes.ravel(), show):
        c = (x["img"].shape[0] - 1) // 2
        cut = x["img"][c - half:c + half + 1, c - half:c + half + 1]
        lo, hi = np.nanpercentile(cut, [5, 99.7])
        a.imshow(cut, origin="lower", cmap="gray_r", vmin=lo, vmax=hi)
        hit = x["z"] > DETECT_Z
        a.add_patch(plt.Circle((half, half), 30, fill=False, lw=1.3, color="#d93025" if hit else "#1a73e8"))
        if hit:
            label = f"B about {x['B_plot']:.1f}" if np.isfinite(x["B_plot"]) else "detected"
        elif np.isfinite(x["lim_plot"]):
            label = f"fainter than {x['lim_plot']:.1f}"
        else:
            label = "too shallow" if x.get("note") else "not detected"
        a.set_title(f"{x['plate']}  {x['date'][:10]}\n{label}", fontsize=8, color="#b3261e" if hit else "black")
    fig.suptitle("V627 Peg: plate cutouts 8 arcminutes across, north up, east left. "
                 "DASCH DR7, Harvard College Observatory.", fontsize=10, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.965), h_pad=2.2)
    fig.savefig(f"{out}/montage.png")
    plt.close(fig)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
