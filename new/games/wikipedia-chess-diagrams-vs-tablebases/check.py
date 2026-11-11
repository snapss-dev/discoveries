"""Check seven statements in Wikipedia chess articles against endgame tablebases.

    python check.py                     uses tablebase_2026-11-11.json (answers of the public Lichess tablebase
                                        service, saved on 2026-11-11) and replays the game scores and lines
    python check.py --online            asks the Lichess tablebase service again and compares with the saved answers
    python check.py --syzygy DIR        also probes local Syzygy WDL files (*.rtbw) in DIR with python-chess, for every
                                        position whose table is present (3-4-5-man set, KQPPvKQ for case B)

Needs: python-chess ("pip install chess"); "requests" only for --online.
A move "keeps the result" when the position after it has the same game-theoretic value for the mover.
Wins and losses are taken without the fifty-move rule; every position below is an unconditional win, loss or draw.
"""
import json, os, sys, time
import chess

HERE = os.path.dirname(os.path.abspath(__file__))
claims = json.load(open(os.path.join(HERE, "claims.json"), encoding="utf-8"))
saved = json.load(open(os.path.join(HERE, "tablebase_2026-11-11.json"), encoding="utf-8"))
online = "--online" in sys.argv
syz = None
if "--syzygy" in sys.argv:
    import chess.syzygy
    syz = chess.syzygy.open_tablebase(sys.argv[sys.argv.index("--syzygy") + 1])

NEG = {"win": "loss", "loss": "win", "draw": "draw"}
ok_all = True


def key(fen):
    return " ".join(fen.split()[:2])


def from_api_json(j):
    """(category for side to move, sorted list of moves keeping it) from a Lichess tablebase answer"""
    cat = j["category"]
    keep = sorted(m["san"] for m in j["moves"] if m["category"] == NEG.get(cat))
    return cat, keep


def from_saved(fen):
    return from_api_json(saved[key(fen)])


def from_online(fen):
    import requests
    for attempt in range(5):
        r = requests.get("https://tablebase.lichess.ovh/standard", params={"fen": fen},
                         headers={"User-Agent": "open-data-research/1.0"}, timeout=60)
        if r.status_code == 429:
            time.sleep(60)
            continue
        break
    time.sleep(2.5)
    return from_api_json(r.json())


def from_syzygy(fen):
    def val(b):
        if b.is_checkmate():
            return -2
        if b.is_stalemate() or b.is_insufficient_material():
            return 0
        return syz.probe_wdl(b)
    name = {2: "win", 0: "draw", -2: "loss"}
    b = chess.Board(fen)
    try:
        w = val(b)
        keep = []
        for m in list(b.legal_moves):
            san = b.san(m)
            b.push(m)
            v = -val(b)
            b.pop()
            if v == w:
                keep.append(san)
    except (KeyError, chess.syzygy.MissingTableError):
        return None
    return name.get(w, f"wdl {w}"), sorted(keep)


def report(label, got, c):
    global ok_all
    if got is None:
        print(f"      {label:8s}: table not present, skipped")
        return
    cat, keep = got
    good = cat == c["category"] and ("keep" not in c or keep == sorted(c["keep"]))
    ok_all &= good
    extra = f"; moves keeping it: {' '.join(keep)}" if "keep" in c else ""
    print(f"      {label:8s}: {cat} for the side to move{extra}   [{'agrees' if good else 'DISAGREES'}]")


def replay(spec, target_key):
    """replay a move list from a FEN; return True if the target position (board + side to move) occurs"""
    b = chess.Board(spec["fen"])
    hit = key(b.fen()) == target_key
    for san in spec["moves"].split():
        b.push_san(san)          # raises on an illegal move
        hit |= key(b.fen()) == target_key
    return hit, b


for cl in claims:
    print(f"[{cl['id']}] {cl['wiki']}.wikipedia.org, \"{cl['article']}\", revision {cl['revid']}")
    print(f"    statement: {cl['statement']}")
    print(f"    verdict  : {cl['verdict']}")
    for name in ("game", "line"):
        if name in cl:
            spec = cl[name]
            target = spec.get("must_pass_through") or spec.get("must_reach")
            hit, b = replay(spec, target)
            ok_all &= hit
            print(f"    {name} replayed ({spec.get('label', 'printed solution')}): all moves legal; position {target} "
                  f"{'occurs' if hit else 'DOES NOT OCCUR'}")
            if name == "game":
                # every position of the replayed score, with local tables if present
                if syz is not None:
                    b = chess.Board(spec["fen"])
                    for san in spec["moves"].split():
                        got = from_syzygy(b.fen())
                        if got:
                            mark = "" if b.san(b.parse_san(san)) in got[1] else "   <-- changes the result"
                            print(f"        {b.fullmove_number}{'.' if b.turn else '...'}{san:7s} {got[0]:4s} for the mover; keeping moves: {' '.join(got[1])}{mark}")
                        b.push_san(san)
    for c in cl["checks"]:
        b = chess.Board(c["fen"])
        assert b.is_valid(), c["fen"]
        print(f"    {c['what']}: {key(c['fen'])}  ({chess.popcount(b.occupied)} men)")
        print(f"      expected: {c['category']}" + (f"; moves keeping it: {' '.join(sorted(c['keep']))}" if "keep" in c else ""))
        report("saved", from_saved(c["fen"]), c)
        if online:
            report("online", from_online(c["fen"]), c)
        if syz is not None:
            report("syzygy", from_syzygy(c["fen"]), c)
    print()

print("ALL CHECKS AGREE" if ok_all else "SOME CHECK DISAGREES")
sys.exit(0 if ok_all else 1)
