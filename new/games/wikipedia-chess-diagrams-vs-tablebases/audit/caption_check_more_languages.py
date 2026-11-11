"""Second wave (more languages): result-level check of captions that state a win or a draw."""
import json, re, os, sys, time, requests, chess, chess.syzygy
TB = chess.syzygy.open_tablebase("data/syzygy")
S = requests.Session(); S.headers["User-Agent"] = "open-data-research/1.0"
CACHE = "data/api_cache2.json"; cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
WIN = re.compile(r"vince|vincono|vittoria|wint\b|winst|wygryw|wygran|ganham|vencem|ganha\b|vitória|виграш|виграють|виграє|vyhr|výhra|vinner|vinst|nyer", re.I)
DRAW = re.compile(r"patta|remise|remis|empat|нічи|remíz|döntetlen", re.I)
BTM = re.compile(r"nero muove|muove il nero|tratto al nero|zwart aan zet|zwart speelt|ruch czarnych|czarne zaczynaj|posunięcie czarnych|pretas jogam|jogam as pretas|хід чорних|чорні починають|černý na tahu|černý táhne|svart drar|svart vid draget|sötét lép|sötét indul", re.I)
def clean(s):
    s = re.sub(r"<ref[^>]*/>", "", s); s = re.sub(r"<ref.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s); s = re.sub(r"'{2,}", "", s)
    return re.sub(r"\s+", " ", s).strip()
def res(placement, stm, allow_api):
    fen = f"{placement} {stm} - - 0 1"
    try: b = chess.Board(fen)
    except ValueError: return None
    if not b.is_valid(): return None
    try:
        w = TB.probe_wdl(b); return "win" if w > 0 else "loss" if w < 0 else "draw"
    except Exception: pass
    if not allow_api: return None
    k = f"{placement} {stm}"
    if k not in cache:
        for a in range(5):
            r = S.get("https://tablebase.lichess.ovh/standard", params={"fen": fen}, timeout=60)
            if r.status_code == 429: time.sleep(60); continue
            break
        cache[k] = r.json().get("category") if r.status_code == 200 else None
        json.dump(cache, open(CACHE, "w")); time.sleep(2.0)
    c = cache[k]
    return None if c in (None, "unknown") else "win" if "win" in c else "loss" if "loss" in c else "draw"
n = nclaim = napi = 0; stats = {}
for line in open("data/diagrams2.jsonl", encoding="utf-8"):
    d = json.loads(line); n += 1
    stats[d["lang"]] = stats.get(d["lang"], 0) + 1
    txt = clean(d["header"] + " . " + d["caption"])
    hw, hd = bool(WIN.search(txt)), bool(DRAW.search(txt))
    if hw == hd: continue
    stm = "b" if BTM.search(txt) else "w"
    r = res(d["placement"], stm, True)
    if r is None: continue
    nclaim += 1
    if (hw and r == "draw") or (hd and r != "draw"):
        other = res(d["placement"], "b" if stm == "w" else "w", True)
        print(f"=== [{d['lang']}] {d['title']} #{d['idx']} rev {d['revid']} | {d['placement']} | men {d['men']} | assumed {stm} to move: {r}; other side to move: {other}")
        print("    ", txt[:420])
print("diagrams <=7 men:", n, stats, "| captions with one claim:", nclaim)
