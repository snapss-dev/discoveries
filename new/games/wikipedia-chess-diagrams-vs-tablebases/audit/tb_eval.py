"""Tablebase result of every extracted diagram, for both sides to move.
<=5 men: local Syzygy WDL tables (python-chess).  6-7 men: Lichess tablebase API (cached).
Output data/tb.json: { "<placement> <stm>": {"res": "W"|"D"|"B"|"illegal", "cat": ..., "src": ...} }
res is from White's point of view; cursed wins / blessed losses count as wins / losses (50-move rule ignored),
the raw category is kept in cat.
"""
import json, os, sys, time, requests, chess, chess.syzygy

mode = sys.argv[1]  # local | api
TB = chess.syzygy.open_tablebase("data/syzygy")
path = f"data/tb_{mode}.json"
tb = json.load(open(path)) if os.path.exists(path) else {}
S = requests.Session(); S.headers["User-Agent"] = "open-data-research/1.0"

seen = {}
for line in open("data/diagrams.jsonl", encoding="utf-8"):
    d = json.loads(line)
    seen[d["placement"]] = d["men"]


def api(fen):
    for attempt in range(8):
        r = S.get("https://tablebase.lichess.ovh/standard", params={"fen": fen}, timeout=60)
        if r.status_code in (429, 503):
            time.sleep(30 * (attempt + 1)); continue
        if r.status_code == 400:
            return None
        r.raise_for_status()
        return r.json()
    raise RuntimeError("gave up")


n = 0
for placement, men in sorted(seen.items(), key=lambda kv: kv[1]):
    for stm in "wb":
        key = f"{placement} {stm}"
        if key in tb:
            continue
        fen = f"{placement} {stm} - - 0 1"
        try:
            b = chess.Board(fen)
        except ValueError:
            tb[key] = dict(res="illegal", cat="badfen"); continue
        if not b.is_valid():
            tb[key] = dict(res="illegal", cat=str(b.status())); continue
        if men <= 5 and mode == "local":
            w = TB.probe_wdl(b)  # from side to move
            ww = w if stm == "w" else -w
            tb[key] = dict(res="W" if ww > 0 else "B" if ww < 0 else "D", cat=w, src="syzygy-local")
        elif men > 5 and mode == "api":
            j = api(fen)
            time.sleep(1.3)
            if j is None:
                tb[key] = dict(res="illegal", cat="api400"); continue
            cat = j["category"]
            sgn = 1 if cat in ("win", "cursed-win", "syzygy-win", "maybe-win") else -1 if cat in ("loss", "blessed-loss", "syzygy-loss", "maybe-loss") else 0
            if cat == "unknown":
                tb[key] = dict(res="?", cat=cat, src="lichess-api"); continue
            ww = sgn if stm == "w" else -sgn
            best = [(m["san"], m["category"]) for m in j["moves"][:40]]
            tb[key] = dict(res="W" if ww > 0 else "B" if ww < 0 else "D", cat=cat, dtz=j.get("dtz"), dtm=j.get("dtm"), moves=best, src="lichess-api")
            n += 1
            if n % 25 == 0:
                json.dump(tb, open(path, "w")); print(n, flush=True)
json.dump(tb, open(f"data/tb_{mode}.json", "w"))
print("done", len(tb))
