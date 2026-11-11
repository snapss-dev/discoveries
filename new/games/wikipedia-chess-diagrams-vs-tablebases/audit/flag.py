"""Compare caption claims with tablebase results; print flagged diagrams for manual reading."""
import json, re, sys, os

tb = {}
for f in ("data/tb_local.json", "data/tb_api.json"):
    if os.path.exists(f):
        for k, v in json.load(open(f)).items():
            if k not in tb or tb[k]["res"] == "illegal" and "src" in v:
                tb[k] = v
            if "src" in v:
                tb[k] = v

KW = dict(
    en=dict(w=r"white (is )?(to|on) (move|play)|white moves|white plays|with white to", b=r"black (is )?(to|on) (move|play)|black moves|black plays|with black to",
            win=r"\bwins?\b|winning|\bwon\b|\bloses?\b|\blost\b|\bmates?\b|checkmate", draw=r"\bdraws?\b|drawn|drawing|fortress|stalemate"),
    de=dict(w=r"weiß (ist )?am zug|weiß zieht|weiß am zuge|anzug", b=r"schwarz (ist )?am zug|schwarz zieht|schwarz am zuge|nachzug",
            win=r"gewinn|verlier|verloren|matt", draw=r"remis|unentschieden|festung|patt"),
    fr=dict(w=r"trait aux blancs|blancs (jouent|au trait)|aux blancs de jouer", b=r"trait aux noirs|noirs (jouent|au trait)|aux noirs de jouer",
            win=r"gagne|gain|perd|\bmat\b", draw=r"nulle|annul|\bpat\b|forteresse"),
    es=dict(w=r"juegan (las )?blancas|blancas juegan|mueven (las )?blancas|turno de(l)? blanc", b=r"juegan (las )?negras|negras juegan|mueven (las )?negras|turno de(l)? negr",
            win=r"\bgana|ganan|pierde|\bmate\b", draw=r"tablas|empat|ahogado|fortaleza"),
    ru=dict(w=r"ход белых|белые начинают|белых", b=r"ход ч[её]рных|ч[её]рные начинают|ч[её]рных", win=r"выигр|побе|проигр|мат\b", draw=r"нич"),
)


def clean(s):
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"'{2,}", "", s)
    return re.sub(r"\s+", " ", s).strip()


def judge(lang, txt, rw, rb):
    k = KW[lang]
    t = txt.lower()
    flags = []
    clauses = [c for c in re.split(r"[.;]|, (?=black|white|schwarz|weiß)", t) if c.strip()]
    for c in clauses + ([t] if len(clauses) > 1 else []):
        sw, sb = bool(re.search(k["w"], c)), bool(re.search(k["b"], c))
        hw, hd = bool(re.search(k["win"], c)), bool(re.search(k["draw"], c))
        if hw == hd:
            continue
        if sw != sb:
            r = rw if sw else rb
            if r in ("illegal", "?"):
                continue
            if hd and r != "D": flags.append(f"claim draw, TB {r} ({'w' if sw else 'b'} to move): {c.strip()[:80]}")
            if hw and r == "D": flags.append(f"claim win, TB draw ({'w' if sw else 'b'} to move): {c.strip()[:80]}")
        elif not sw and not sb and c is t or len(clauses) == 1:
            rs = [r for r in (rw, rb) if r not in ("illegal", "?")]
            if not rs: continue
            if hd and all(r != "D" for r in rs): flags.append(f"claim draw, TB {rs} for either side to move")
            if hw and all(r == "D" for r in rs): flags.append("claim win, TB draw for either side to move")
    return flags


maxmen = int(sys.argv[1]) if len(sys.argv) > 1 else 5
minmen = int(sys.argv[2]) if len(sys.argv) > 2 else 2
n = nf = 0
for line in open("data/diagrams.jsonl", encoding="utf-8"):
    d = json.loads(line)
    if not (minmen <= d["men"] <= maxmen):
        continue
    a, b = tb.get(d["placement"] + " w"), tb.get(d["placement"] + " b")
    if a is None or b is None:
        continue
    n += 1
    txt = clean(d["header"] + " . " + d["caption"])
    fl = judge(d["lang"], txt, a["res"], b["res"])
    if fl:
        nf += 1
        print(f"=== [{d['lang']}] {d['title']} #{d['idx']}  {d['placement']}  men={d['men']}  TB: wtm={a['res']}({a.get('cat')}) btm={b['res']}({b.get('cat')})")
        print("   CAPTION:", txt[:500])
        for f in dict.fromkeys(fl):
            print("   FLAG:", f)
print("checked", n, "flagged", nf)
