"""Replay the move sequences printed next to each <=5-man diagram and compare every move with the tablebase.
Flags: (A) a move marked ! that worsens the result; (B) a move marked ? / ?? that does not change the result;
(C) an 'only move' statement where several moves keep the result; (E) an unmarked move that worsens the result.
"""
import json, re, sys, chess, chess.syzygy

TB = chess.syzygy.open_tablebase("data/syzygy")
LANG = sys.argv[1]
MAXMEN = 5

PIECEMAP = dict(en={}, de={"D": "Q", "T": "R", "L": "B", "S": "N"}, fr={"R": "K", "D": "Q", "T": "R", "F": "B", "C": "N"},
                es={"R": "K", "D": "Q", "T": "R", "A": "B", "C": "N"})
PL = dict(en="KQRBN", de="KDTLS", fr="RDTFC", es="RDTAC")[LANG]


def clean(s):
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S)
    s = re.sub(r"<ref[^>]*/>", "", s)
    s = re.sub(r"<ref.*?</ref>", "", s, flags=re.S)
    s = re.sub(r"\{\{chesspunc\|([^}]*)\}\}", r"\1", s, flags=re.I)
    s = re.sub(r"\{\{chessAN\|([^}]*)\}\}", r"\1", s, flags=re.I)
    s = s.replace("{{=}}", "=").replace("&nbsp;", " ").replace("…", "...").replace("–", "-").replace("—", "-").replace("×", "x")
    s = s.replace("0-0-0", "O-O-O").replace("0-0", "O-O").replace("†", "+").replace("‡", "#")
    s = re.sub(r"\[\[(?:[^|\]]*\|)?([^\]]*)\]\]", r"\1", s)
    s = re.sub(r"'{2,}", "", s)
    s = re.sub(r"\{\{[^{}]*\}\}", " ", s)
    return s


SAN = rf"(?:O-O-O|O-O|[{PL}]?[a-h]?[1-8]?[-x:]?[a-h][1-8](?:=?[{PL}])?(?:\s?e\.\s?p\.)?)"
TOKEN = re.compile(rf"(?P<lp>\()|(?P<rp>\))|(?P<num>\d{{1,3}})\s*(?P<dots>\.\s*\.\.\.?|\.\.\.|\.)\s*(?P<m1>{SAN})(?P<c1>[+#]*)\s*(?P<a1>\?\?|!!|\?!|!\?|\?|!)?"
                   rf"(?:[\s,]+(?P<m2>{SAN})(?P<c2>[+#]*)\s*(?P<a2>\?\?|!!|\?!|!\?|\?|!)?)?")


def to_move(board, tok):
    t = tok
    if LANG != "en":
        t = "".join(PIECEMAP[LANG].get(ch, ch) if ch.isupper() and ch != "O" else ch for ch in t)
    t = t.replace(":", "x").replace("-", "") if not t.startswith("O") else t
    t = re.sub(r"\s?e\.\s?p\.", "", t)
    m = re.match(r"^(.*[a-h][1-8])=?([QRBN])$", t)
    if m:
        t = m.group(1) + "=" + m.group(2)
    try:
        return board.parse_san(t)
    except ValueError:
        return None


def wdl(board):
    if board.is_checkmate():
        return -2
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    if chess.popcount(board.occupied) > MAXMEN or board.castling_rights:
        return None
    try:
        return TB.probe_wdl(board)
    except Exception:
        return None


def sgn(x):
    return (x > 0) - (x < 0)


def analyse(d):
    text = clean(d["caption"] + " \n " + d["ctx_cut"])
    out = []
    boards = {}
    stack = []
    started = False
    first = None
    for m in TOKEN.finditer(text):
        if m.group("lp"):
            stack.append(dict(boards)); continue
        if m.group("rp"):
            if stack: boards = stack.pop()
            continue
        n = int(m.group("num")); side = chess.WHITE if m.group("dots").strip() == "." else chess.BLACK
        key = (n, side)
        if key in boards:
            b = boards[key].copy()
        elif not started or key == first:
            try:
                b = chess.Board(f"{d['placement']} {'w' if side else 'b'} - - 0 1")
            except ValueError:
                continue
            if not b.is_valid():
                continue
            first = first or key
        else:
            continue
        seq = [(m.group("m1"), m.group("a1"))]
        if m.group("m2") and side == chess.WHITE:
            seq.append((m.group("m2"), m.group("a2")))
        cur = key
        for tok, ann in seq:
            mv = to_move(b, tok)
            if mv is None:
                break
            started = True
            before = wdl(b)
            keep = []
            if before is not None:
                for x in b.legal_moves:
                    b.push(x); w = wdl(b); b.pop()
                    if w is not None and sgn(-w) == sgn(before):
                        keep.append(b.san(x))
            san = b.san(mv)
            boards[cur] = b.copy()
            fen = b.fen()
            b.push(mv)
            after = wdl(b)
            ctx = text[max(0, m.start() - 60):m.end() + 110].replace("\n", " ")
            out.append(dict(fen=fen, san=san, ann=ann or "", before=before, after=None if after is None else -after, keep=keep, ctx=ctx, depth=len(stack), n=cur[0]))
            cur = (cur[0], chess.BLACK) if cur[1] == chess.WHITE else (cur[0] + 1, chess.WHITE)
            boards[cur] = b.copy()
    return out


ONLY = re.compile(r"only (winning |drawing |saving |good )?(move|way)|einzige|seul coup|única", re.I)
START = re.compile(r"\{\{\s*(?:Chess diagram|Schachbrett|Diagramme d'échecs|Diagrama de ajedrez)", re.I)
nd = nm = 0
flags = []
for line in open("data/diagrams.jsonl", encoding="utf-8"):
    d = json.loads(line)
    if d["lang"] != LANG or d["men"] > MAXMEN:
        continue
    ctx = d["ctx"]
    cut = len(ctx)
    for pat in (START, re.compile(r"\n==")):
        mm = pat.search(ctx)
        if mm: cut = min(cut, mm.start())
    d["ctx_cut"] = ctx[:cut]
    res = analyse(d)
    nd += 1; nm += len(res)
    for r in res:
        if r["before"] is None or r["after"] is None:
            continue
        b, a = sgn(r["before"]), sgn(r["after"])
        kind = None
        if a < b and r["ann"] in ("!", "!!"): kind = "A !-move worsens"
        elif a < b and r["ann"] in ("", "!?"): kind = "E unmarked move worsens"
        elif a == b and r["ann"] in ("?", "??"): kind = "B ?-move keeps result"
        elif a == b and b >= 0 and len(r["keep"]) > 1 and ONLY.search(r["ctx"][60:]): kind = "C 'only' but several"
        if kind:
            flags.append((kind, d, r))
print(f"[{LANG}] diagrams {nd}, moves replayed {nm}, flags {len(flags)}")
for kind, d, r in sorted(flags, key=lambda t: t[0]):
    print(f"--- {kind} | {d['title']} #{d['idx']} | {r['fen']} | {r['n']}{'.' if ' w ' in r['fen'] else '...'}{r['san']}{r['ann']} | before {r['before']} after {r['after']} | keeps: {','.join(r['keep'][:12])}")
    print("     ", r["ctx"])
