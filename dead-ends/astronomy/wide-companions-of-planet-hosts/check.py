"""Hand check of six planet hosts that the NASA Exoplanet Archive lists as single stars (sy_snum = 1)
although Gaia DR3 shows a co-moving companion that is in the El-Badry, Rix & Heintz (2021) catalogue.

Default: reads hand_check.json (the query results stored on 2026-11-11) and applies the tests.
With --fetch: asks the two public services again (no key needed) and rewrites hand_check.json.
  NASA Exoplanet Archive TAP, table pscomppars: sy_snum per host
  ESA Gaia archive TAP, table gaiadr3.gaia_source: astrometry of primary and companion
Tests per pair: parallaxes agree within 3 sigma; the proper-motion difference is below the largest
orbital motion a bound pair of total mass 5 solar masses could show at that separation (the criterion
of El-Badry et al. 2021: dmu <= 0.44 mas/yr * plx^1.5 / sqrt(theta), plus 2 sigma).
"""
import csv, io, json, math, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PAIRS = [("HD 155918", 5801950515627094400, 5801950515623082496), ("BD+63 1405", 2160951157908163968, 2160951157908689664),
         ("HD 23472", 4674216245427964416, 4674216245427964672), ("HD 109988", 6160221740968692992, 6160221736672454400),
         ("HD 109271", 3578137842709899648, 3578137911427752704), ("TOI-1824", 1675511792082576384, 1675511792082576128)]
UA = {"User-Agent": "open-data-research/1.0"}


def get(url, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers=UA)
    return urllib.request.urlopen(req, timeout=120).read().decode("utf-8", "replace")


if "--fetch" in sys.argv:
    hosts = ",".join("'%s'" % h for h, _, _ in PAIRS)
    t = get("https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
            {"query": "select hostname,sy_snum,sy_pnum from pscomppars where hostname in (%s)" % hosts, "format": "csv"})
    snum = {r["hostname"]: int(r["sy_snum"]) for r in csv.DictReader(io.StringIO(t))}
    time.sleep(1)
    ids = ",".join(str(i) for _, a, b in PAIRS for i in (a, b))
    t = get("https://gea.esac.esa.int/tap-server/tap/sync",
            {"REQUEST": "doQuery", "LANG": "ADQL", "FORMAT": "csv",
             "QUERY": "SELECT source_id,ra,dec,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,phot_g_mean_mag "
                      "FROM gaiadr3.gaia_source WHERE source_id IN (%s)" % ids})
    gaia = {r["source_id"]: {k: float(v) for k, v in r.items() if k != "source_id"} for r in csv.DictReader(io.StringIO(t))}
    json.dump({"fetched": time.strftime("%Y-%m-%d"), "sy_snum": snum, "gaia": gaia}, open(os.path.join(HERE, "hand_check.json"), "w"), indent=1)

d = json.load(open(os.path.join(HERE, "hand_check.json")))
print("query results stored on", d["fetched"])
print("host         sy_snum  sep\"   proj. au  G(comp)  dplx/sigma  dmu mas/yr  bound limit  verdict")
ok = True
for host, a, b in PAIRS:
    p, c = d["gaia"][str(a)], d["gaia"][str(b)]
    theta = 3600 * math.hypot((p["ra"] - c["ra"]) * math.cos(math.radians(p["dec"])), p["dec"] - c["dec"])
    au = theta / (p["parallax"] / 1000)
    dplx = abs(p["parallax"] - c["parallax"]) / math.hypot(p["parallax_error"], c["parallax_error"])
    dmu = math.hypot(p["pmra"] - c["pmra"], p["pmdec"] - c["pmdec"])
    sig = math.sqrt(p["pmra_error"] ** 2 + c["pmra_error"] ** 2 + p["pmdec_error"] ** 2 + c["pmdec_error"] ** 2)
    lim = 0.44 * p["parallax"] ** 1.5 / math.sqrt(theta) + 2 * sig
    good = d["sy_snum"].get(host) == 1 and dplx < 3 and dmu < lim
    ok &= good
    print("%-11s     %s    %5.1f   %6.0f    %5.1f     %5.1f      %6.2f      %6.2f     %s" % (
        host, d["sy_snum"].get(host), theta, au, c["phot_g_mean_mag"], dplx, dmu, lim,
        "listed single, companion co-moving" if good else "NOT confirmed"))
print()
print("ALL SIX CONFIRMED" if ok else "NOT ALL CONFIRMED (see table)")
sys.exit(0)
