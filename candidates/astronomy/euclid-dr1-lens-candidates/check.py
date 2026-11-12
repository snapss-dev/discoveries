"""Check of the page "66 possible strong lenses in Euclid DR1 that are not in the consortium's catalogue".

    python check.py            reads candidates.csv and cutouts.npz from its own folder (a few seconds)
    python check.py --figure   also redraws grade_Bplus_1.png and grade_Bplus_2.png

What it does, without any network access:
 1. table integrity: one row per object, no two rows within 5 arcsec, grade counts as on the page;
 2. the statements about the Euclid Consortium's search (columns copied from its public ECLIPSE
    catalogues): no row is in its expert-graded object catalogue, every row has a search cutout,
    and the counts of rows flagged by its networks and shown to its volunteers are as stated;
 3. for every grade B+ candidate, from the stored Euclid VIS cutout (14 x 14 arcsec, 0.1 arcsec per
    pixel, the galaxy at the centre): subtracts a smooth model of the galaxy (the median surface
    brightness in elliptical annuli) and measures the strongest residual feature at the radius and
    direction stated for the arc: distance from the centre, direction, length along the circle, width
    across it, signal to noise.
The grades themselves were given by eye; this script only shows that the features are in the data.
"""
import csv
import os
import sys

import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
PIX = 0.1       # arcsec per VIS pixel
RNOISE = 6.6    # arcsec: the noise is measured beyond this radius (the corners of the 14 arcsec cutout)


def centre_shape(img):
    n = img.shape[0]
    c = n // 2
    sm = ndi.gaussian_filter(img, 1.5)
    w = 8
    sub = sm[c - w:c + w + 1, c - w:c + w + 1]
    iy, ix = np.unravel_index(np.argmax(sub), sub.shape)
    cy, cx = c - w + iy, c - w + ix
    yy, xx = np.mgrid[:n, :n]
    dy, dx = yy - cy, xx - cx
    edge = np.concatenate([sm[:6].ravel(), sm[-6:].ravel(), sm[:, :6].ravel(), sm[:, -6:].ravel()])
    bg = np.median(edge)
    sg = 1.4826 * np.median(np.abs(edge - bg)) + 1e-12
    q, pa = 1.0, 0.0
    for frac in (0.08, 0.2):
        thr = max(bg + 6 * sg, bg + frac * (sm[cy, cx] - bg))
        lab, _ = ndi.label(sm > thr)
        m = lab == lab[cy, cx]
        if lab[cy, cx] == 0 or m.sum() < 30 or m.sum() > 0.25 * n * n:
            continue
        f = (sm - bg) * m
        s = f.sum()
        qxx, qyy, qxy = (f * dx * dx).sum() / s, (f * dy * dy).sum() / s, (f * dx * dy).sum() / s
        pa = 0.5 * np.arctan2(2 * qxy, qxx - qyy)
        t, dl = qxx + qyy, np.sqrt((qxx - qyy) ** 2 + 4 * qxy ** 2)
        q = np.sqrt(max((t - dl) / 2, 1e-6) / max((t + dl) / 2, 1e-6))
        break
    return cy, cx, float(np.clip(q, 0.3, 1.0)), float(pa)


def residual(img):
    img = np.nan_to_num(img.astype(np.float64))
    n = img.shape[0]
    cy, cx, q, pa = centre_shape(img)
    yy, xx = np.mgrid[:n, :n]
    dy, dx = yy - cy, xx - cx
    xr = dx * np.cos(pa) + dy * np.sin(pa)
    yr = -dx * np.sin(pa) + dy * np.cos(pa)
    rell = np.sqrt(xr ** 2 + (yr / q) ** 2).ravel()
    edges = list(range(11))
    while edges[-1] < rell.max():
        edges.append(edges[-1] * 1.10 + 0.5)
    edges = np.array(edges)
    idx = np.digitize(rell, edges) - 1
    flat = img.ravel()
    prof, rc = [], []
    for b in range(len(edges) - 1):
        sel = idx == b
        if sel.any():
            prof.append(np.median(flat[sel]))
            rc.append(rell[sel].mean())
    res = img - np.interp(rell, rc, prof).reshape(n, n)
    r = np.hypot(dx, dy) * PIX
    v = res[r > RNOISE]
    sig = 1.4826 * np.median(np.abs(v - np.median(v))) + 1e-12
    return res, r, (cy, cx), sig


def features(res, r, cyx, sig, rmin=0.6, rmax=6.4):
    cy, cx = cyx
    sm = ndi.gaussian_filter(res, 1.0)
    v = sm[r > RNOISE]
    ssig = 1.4826 * np.median(np.abs(v - np.median(v))) + 1e-12
    lab, nl = ndi.label((sm > 3.0 * ssig) & (r > rmin) & (r < rmax), structure=np.ones((3, 3)))
    n = res.shape[0]
    yy, xx = np.mgrid[:n, :n]
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), 1):
        m = lab[sl] == i
        if m.sum() < 12:
            continue
        y, x = yy[sl][m] - cy, xx[sl][m] - cx
        vals = res[sl][m]
        f = np.clip(vals, 0, None)
        if f.sum() <= 0:
            continue
        rr, th = np.hypot(x, y), np.arctan2(y, x)
        w = f / f.sum()
        cth = np.arctan2((w * np.sin(th)).sum(), (w * np.cos(th)).sum())
        dth = np.angle(np.exp(1j * (th - cth)))
        rmean = float((w * rr).sum())
        lt = float(np.percentile(dth * rmean, 97.5) - np.percentile(dth * rmean, 2.5)) + 1.0
        wr = float(np.percentile(rr, 97.5) - np.percentile(rr, 2.5)) + 1.0
        # position angle north through east: east is to the left (decreasing x), north is up (increasing y)
        pa = (np.degrees(np.arctan2(-np.cos(cth), np.sin(cth)))) % 360
        out.append(dict(r=rmean * PIX, pa=float(pa), len=lt * PIX, wid=wr * PIX, snr=float(vals.sum() / (sig * np.sqrt(m.sum())))))
    return out


def yes(v):
    return str(v).strip().lower() in ("true", "yes", "1")


with open(os.path.join(HERE, "candidates.csv"), newline="", encoding="utf-8") as fh:
    rows = list(csv.DictReader(fh))
cut = np.load(os.path.join(HERE, "cutouts.npz"))
counts = {g: sum(r["grade"] == g for r in rows) for g in ("B+", "B")}
print("candidates:", len(rows), counts)
assert len(rows) == 66 and counts == {"B+": 8, "B": 58}
names = [r["name"] for r in rows]
assert len(set(names)) == len(names), "duplicate names"
ra = np.array([float(r["ra_deg"]) for r in rows])
dec = np.array([float(r["dec_deg"]) for r in rows])
near = []
for i in range(len(rows)):
    d = np.hypot((ra - ra[i]) * np.cos(np.radians(dec[i])), dec - dec[i]) * 3600
    d[i] = 1e9
    assert d.min() > 5.0, "two rows within 5 arcsec: %s" % names[i]
    near.append(d.min())
print("no two candidates within 5 arcsec of each other; nearest pair %.0f arcsec apart" % min(near))

# what the Euclid Consortium's search did with these objects
sep = np.array([float(r["eclipse_nearest_object_arcsec"]) for r in rows])
assert (sep > 10).all()
print("nearest entry of the consortium's expert-graded object catalogue: closest %.0f arcsec, median %.0f arcsec" % (sep.min(), np.median(sep)))
assert all(float(r["eclipse_cutout_offset_arcsec"]) < 1.0 for r in rows)
fl = [yes(r["eclipse_flagged_by_networks"]) for r in rows]
sw = [yes(r["eclipse_seen_by_volunteers"]) for r in rows]
sr = [yes(r["eclipse_seen_by_volunteers_second_stage"]) for r in rows]
ex = [yes(r["eclipse_seen_by_experts"]) for r in rows]
early = [yes(r["eclipse_early_search_tile"]) for r in rows]
print("every row has a consortium search cutout centred on it; flagged by its networks: %d; shown to volunteers: %d; "
      "shown to volunteers a second time: %d; shown to its experts: %d; not flagged by its networks, so seen by nobody there: %d" % (
          sum(fl), sum(sw), sum(sr), sum(ex), len(rows) - sum(fl)))
assert sum(fl) == 32 and sum(sw) == 32 and sum(sr) == 11 and sum(ex) == 0
print("in tiles of the consortium's two early searches: %d (of which not flagged: %d)" % (sum(early), sum(e and not f for e, f in zip(early, fl))))
assert sum(early) == 15
vs = [(float(r["eclipse_volunteer_score"] or "nan"), float(r["eclipse_volunteer_second_score"] or "nan")) for r in rows]
hi = sum(1 for a, b in vs if (a == a and a >= 0.5) or (b == b and b >= 0.5))
print("shown to volunteers and scored 0.5 or more in either round: %d; highest second-round score %.2f (expert inspection needed more than 0.87)" % (
    hi, max(b for a, b in vs if b == b)))
assert max(b for a, b in vs if b == b) < 0.87
ns = [float(r["eclipse_network_ensemble_score"]) for r, f in zip(rows, fl) if not f]
print("not flagged: %d with a network ensemble score above 0.5" % sum(x > 0.5 for x in ns))
bp = [r for r in rows if r["grade"] == "B+"]
print("of the 8 grade B+: flagged by the networks %d, never flagged %d" % (
    sum(yes(r["eclipse_flagged_by_networks"]) for r in bp), sum(not yes(r["eclipse_flagged_by_networks"]) for r in bp)))

print("\nthe arc of each grade B+ candidate in its stored VIS cutout: the strongest residual feature within")
print("1 arcsec of the stated radius and 40 degrees of the stated direction (north through east)")
print("%-26s %7s %7s | %6s %6s %6s %6s %6s" % ("name", "stated", "stated", "r\"", "PA", "len\"", "wid\"", "S/N"))
npass = 0
for r in bp:
    key = r["name"].replace(" ", "_")
    r0, pa0 = float(r["arc_radius_arcsec"]), float(r["arc_direction_deg"])
    res, rr, cyx, sig = residual(cut[key + "_VIS"])
    fs = [f for f in features(res, rr, cyx, sig)
          if abs(f["r"] - r0) <= 1.0 and abs((f["pa"] - pa0 + 180) % 360 - 180) <= 40]
    b = max(fs, key=lambda f: f["snr"] * f["len"]) if fs else None
    print("%-26s %6.1f\" %6.0f  | %6s %6s %6s %6s %6s" % (
        r["name"], r0, pa0, *(("%.1f" % b["r"], "%.0f" % b["pa"], "%.1f" % b["len"], "%.1f" % b["wid"], "%.0f" % b["snr"]) if b else ("-",) * 5)))
    ok = b is not None and b["snr"] >= 5 and b["len"] >= 1.0
    npass += int(ok)
    assert ok, "no significant residual feature at the stated place: " + r["name"]
print("grade B+ objects with a residual feature of S/N above 5 and at least 1 arcsec long at the stated place: %d of %d" % (npass, len(bp)))

if "--figure" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    def stretch(a, sig, soft=8, hi=None):
        hi = hi if hi is not None else max(np.percentile(a, 99.8), 30 * sig)
        x = np.clip((a + 2 * sig) / (hi + 2 * sig), 0, 1)
        return np.arcsinh(x * soft * 10) / np.arcsinh(soft * 10)

    def panels(r):
        key = r["name"].replace(" ", "_")
        img = np.nan_to_num(cut[key + "_VIS"].astype(np.float64))
        res, rr, cyx, sig = residual(img)
        col = None
        if key + "_H" in cut.files:
            def nz(b):
                b = np.kron(np.nan_to_num(b.astype(np.float64)), np.ones((3, 3)))[:img.shape[0], :img.shape[1]]  # NISP stored binned 3x3
                s = 1.4826 * np.median(np.abs(b - np.median(b))) + 1e-9
                return stretch(b, s, soft=5, hi=max(np.percentile(b, 99.6), 30 * s))
            h = nz(cut[key + "_H"])
            blue = stretch(img, sig, soft=5)
            green = nz(cut[key + "_Y"]) if key + "_Y" in cut.files else 0.5 * (h + blue)
            col = np.dstack([h, green, blue])
        return stretch(img, sig), np.clip(res / sig, -3, 10), col

    half = cut[bp[0]["name"].replace(" ", "_") + "_VIS"].shape[0] * PIX / 2
    ext = [half, -half, -half, half]
    for k in range(0, len(bp), 4):
        part = bp[k:k + 4]
        fig, axs = plt.subplots(len(part), 3, figsize=(10, 3.45 * len(part)), dpi=90)
        axs = np.atleast_2d(axs)
        for i, r in enumerate(part):
            v, rs, col = panels(r)
            axs[i, 0].imshow(v, cmap="gray", origin="lower", extent=ext, interpolation="nearest")
            axs[i, 0].set_title(r["name"] + "  VIS", fontsize=8)
            axs[i, 1].imshow(rs, cmap="gray", origin="lower", extent=ext, vmin=-3, vmax=10, interpolation="nearest")
            axs[i, 1].set_title("VIS minus galaxy model (units of noise)", fontsize=8)
            if col is not None:
                axs[i, 2].imshow(col, origin="lower", extent=ext, interpolation="nearest")
                axs[i, 2].set_title("colour: H, Y, VIS = red, green, blue", fontsize=8)
            for a in axs[i]:
                a.set_xticks([-5, 0, 5]); a.set_yticks([-5, 0, 5]); a.tick_params(labelsize=6, length=2)
            axs[i, 0].set_ylabel("arcsec (N up, E left)", fontsize=7)
        fig.subplots_adjust(left=0.05, right=0.995, top=0.975, bottom=0.025, wspace=0.08, hspace=0.16)
        fig.savefig(os.path.join(HERE, "grade_Bplus_%d.png" % (k // 4 + 1)))
        plt.close(fig)
    print("\nfigures written: grade_Bplus_1.png, grade_Bplus_2.png (each panel %.0f arcsec across, north up, east left)" % (2 * half))
print("\nALL CHECKS PASSED")
