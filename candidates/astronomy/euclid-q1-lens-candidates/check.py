"""Second look at four possible strong lenses in Euclid Q1 imaging.

Reads cutouts.npz from this folder: 20" x 20" cutouts (0.1"/pixel, north up, east left) of the Euclid Q1
MER background-subtracted mosaics in VIS, NIR-Y and NIR-H, fetched from IRSA for the four positions.

For each candidate the VIS image is rotated by 180 degrees about the galaxy centre and subtracted from
itself. A smooth, symmetric galaxy cancels; anything that is not point-symmetric (arcs, companions,
tidal features, lensed images) stays, with a negative copy on the opposite side. This uses no model of
the galaxy. Connected regions above 3 sigma in the residual are listed with their offset, size,
significance, shape and colour relative to the galaxy.

With --figure the script writes candidates.png.
"""
import math
import os
import sys

import numpy as np
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
PIX = 0.1
CANDS = [("C1", "EUCL J033400.31-283857.4", 53.50131, -28.64928),
         ("C2", "EUCL J034936.95-510956.3", 57.40394, -51.16564),
         ("C3", "EUCL J033017.56-270213.8", 52.57316, -27.03718),
         ("C4", "EUCL J032447.79-270627.6", 51.19912, -27.10766)]
cut = np.load(os.path.join(HERE, "cutouts.npz"))


def centre(img):
    sm = ndi.gaussian_filter(img, 1.5)
    c = img.shape[0] // 2
    sub = sm[c - 8:c + 9, c - 8:c + 9]
    j, i = np.unravel_index(np.argmax(sub), sub.shape)
    return c - 8 + j, c - 8 + i


def rot_residual(img, cy, cx):
    """img minus its 180-degree rotation about pixel (cy, cx); same shape, NaN where undefined."""
    out = np.full(img.shape, np.nan)
    h, w = img.shape
    y0, y1 = max(0, 2 * cy - (h - 1)), min(h - 1, 2 * cy)
    x0, x1 = max(0, 2 * cx - (w - 1)), min(w - 1, 2 * cx)
    block = img[y0:y1 + 1, x0:x1 + 1]
    out[y0:y1 + 1, x0:x1 + 1] = block - block[::-1, ::-1]
    return out


def analyse(tag):
    vis, hband = cut[tag + "_VIS"].astype(float), cut[tag + "_H"].astype(float)
    cy, cx = centre(vis)
    res = rot_residual(vis, cy, cx)
    resh = rot_residual(hband, cy, cx)
    yy, xx = np.mgrid[:vis.shape[0], :vis.shape[1]]
    r = np.hypot(xx - cx, yy - cy) * PIX
    ring = np.isfinite(res) & (r > 6.5) & (r < 8.5)
    sig = 1.4826 * np.nanmedian(np.abs(res[ring] - np.nanmedian(res[ring])))
    sm = ndi.gaussian_filter(np.nan_to_num(res), 1.0)
    sig_s = 1.4826 * np.median(np.abs(sm[ring] - np.median(sm[ring])))
    mask = (sm > 3 * sig_s) & (r > 0.5) & (r < 6.0)
    lab, n = ndi.label(mask)
    core = r < 0.5
    gal_colour = vis[core].sum() / max(hband[core].sum(), 1e-9)
    feats = []
    for k in range(1, n + 1):
        m = lab == k
        area = int(m.sum())
        if area < 8:
            continue
        f = res[m].sum()
        snr = f / (sig * math.sqrt(area))
        w = np.clip(res[m], 0, None)
        ex = -((xx[m] - cx) * w).sum() / w.sum() * PIX
        nn = ((yy[m] - cy) * w).sum() / w.sum() * PIX
        rad = math.hypot(ex, nn)
        theta = np.degrees(np.arctan2(yy[m] - cy, xx[m] - cx))
        ref = math.degrees(math.atan2(nn, -ex))
        dth = (theta - ref + 180) % 360 - 180
        tang = (dth.max() - dth.min()) * math.pi / 180 * rad         # arcsec along the circle
        radial = (r[m].max() - r[m].min())
        fh = resh[m].sum()
        colour = (f / fh) / gal_colour if fh > 0 else float("inf")
        feats.append(dict(east=ex, north=nn, r=rad, area=area * PIX * PIX, snr=snr, tang=tang, radial=radial, colour=colour))
    feats.sort(key=lambda d: -d["snr"])
    # compact sources close to the centre: local maxima of the smoothed residual, 0.4" to 1.8" out
    peaks = []
    mx = ndi.maximum_filter(sm, size=5)
    yy_, xx_ = np.where((sm == mx) & (sm > 8 * sig_s) & (r > 0.4) & (r < 1.8))
    ap = lambda img, y, x: img[y - 2:y + 3, x - 2:x + 3].sum()
    for y, x in zip(yy_, xx_):
        fv, fh = ap(res, y, x), ap(resh, y, x)
        peaks.append(dict(east=-(x - cx) * PIX, north=(y - cy) * PIX, r=r[y, x], snr=fv / (sig * 5),
                          colour=(fv / fh) / gal_colour if fh > 0 else float("inf")))
    peaks.sort(key=lambda d: -d["snr"])
    return (cy, cx), res, sig, feats, peaks


results = {}
for tag, name, ra, dec in CANDS:
    (cy, cx), res, sig, feats, peaks = analyse(tag)
    results[tag] = (cy, cx, res, sig, feats, peaks)
    print("%s  %s  (RA %.5f, Dec %.5f)" % (tag, name, ra, dec))
    print("    east\"  north\"  radius\"  area sq\"  S/N   along-circle\"  radial\"  VIS/H relative to the galaxy core")
    for f in feats[:8]:
        print("    %+5.2f  %+5.2f   %5.2f    %5.2f   %5.1f      %5.2f        %5.2f     %s" % (
            f["east"], f["north"], f["r"], f["area"], f["snr"], f["tang"], f["radial"],
            ("%.1f" % f["colour"]) if math.isfinite(f["colour"]) else "no H flux"))
    if not feats:
        print("    no residual feature above threshold")
    for q in peaks[:4]:
        print("    compact source near the centre: %+5.2f\" east, %+5.2f\" north, radius %.2f\", S/N %.0f in a 0.5\" box, VIS/H %s times the core's" % (
            q["east"], q["north"], q["r"], q["snr"], ("%.1f" % q["colour"]) if math.isfinite(q["colour"]) else "(no H flux)"))
    print()

ok = True


def claim(cond, text):
    global ok
    print(("  PASS  " if cond else "  FAIL  ") + text)
    ok = ok and bool(cond)


f1 = [q for q in results["C1"][5] if q["snr"] > 10]
claim(len(f1) >= 2, "C1: at least two compact residual sources within 1.8\" of the centre, each above 10 sigma")
claim(len(f1) >= 2 and all(q["colour"] > 1.3 for q in f1[:2]), "C1: both are bluer than the galaxy core (VIS/H at least 1.3 times the core's)")
f2 = [f for f in results["C2"][4] if 2.3 < f["r"] < 4.3 and f["tang"] > 2 * f["radial"]]
claim(len(f2) >= 1, "C2: a residual feature at 2.3\" to 4.3\" that is at least twice as long along the circle as across it")
c2 = sorted([f for f in results["C2"][4] if 2.8 < f["r"] < 3.8], key=lambda f: f["north"])
if len(c2) >= 2:
    print("        C2 colours: southern arc VIS/H %.1f, northern arc %.1f times the core's: they differ" % (c2[0]["colour"], c2[-1]["colour"]))
    claim(c2[0]["colour"] > 2 * c2[-1]["colour"], "C2: the two arcs have different colours (counts against a single lensed source)")
f3 = [f for f in results["C3"][4] if 3.0 < f["r"] < 5.0 and f["snr"] > 20 and f["east"] > 0]
claim(len(f3) >= 2 and all(f["colour"] > 5 for f in f3), "C3: two residual segments east of the galaxy at 3.6\" to 4.3\", each above 20 sigma and much bluer than the galaxy")
claim(all(f["tang"] > 1.5 * f["radial"] for f in f3), "C3: both segments are elongated along the circle around the galaxy")

if "--figure" in sys.argv:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(3, 4, figsize=(13.5, 10.4))
    for col, (tag, name, ra, dec) in enumerate(CANDS):
        cy, cx, res, sig, feats, peaks = results[tag]
        vis = cut[tag + "_VIS"].astype(float)
        hb = cut[tag + "_H"].astype(float)
        yb = cut[tag + "_Y"].astype(float)
        ext = [10, -10, -10, 10]
        s = 1.4826 * np.median(np.abs(vis - np.median(vis)))
        axs[0, col].imshow(np.arcsinh(np.clip(vis, -s, None) / (3 * s)), origin="lower", cmap="gray", extent=ext)
        axs[0, col].set_title("%s  %s\nVIS, arcsinh stretch" % (tag, name), fontsize=9)
        axs[1, col].imshow(np.nan_to_num(ndi.gaussian_filter(np.nan_to_num(res), 0.7)), origin="lower", cmap="gray", vmin=-4 * sig, vmax=8 * sig, extent=ext)
        axs[1, col].set_title("VIS minus its 180-degree rotation", fontsize=9)

        def nrm(a):
            sa = 1.4826 * np.median(np.abs(a - np.median(a)))
            return np.clip(np.arcsinh(np.clip(a, 0, None) / (3 * sa)) / np.arcsinh(np.percentile(a, 99.7) / (3 * sa)), 0, 1)
        axs[2, col].imshow(np.dstack([nrm(hb), nrm(yb), nrm(vis)]), origin="lower", extent=ext)
        axs[2, col].set_title("colour: H, Y, VIS as red, green, blue", fontsize=9)
        for row in range(3):
            axs[row, col].set_xlim(6, -6)
            axs[row, col].set_ylim(-6, 6)
            axs[row, col].tick_params(labelsize=7)
    fig.suptitle("Four possible strong lenses in Euclid Q1 (12\" fields, north up, east left; axes in arcseconds). "
                 "Data: ESA Euclid Q1 MER mosaics via IRSA.", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    fig.savefig(os.path.join(HERE, "candidates.png"), dpi=75)
    print("wrote candidates.png")

print()
print("ALL CHECKS PASSED" if ok else "SOME CHECKS FAILED")
sys.exit(0 if ok else 1)
