"""Find a game in a PGN file and evaluate every position with at most N men with local Syzygy tables."""
import sys, chess, chess.pgn, chess.syzygy
pgn, tbdir, white, black, maxmen = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5])
TB = chess.syzygy.open_tablebase(tbdir)
def val(b):
    if b.is_checkmate(): return -2
    if b.is_stalemate() or b.is_insufficient_material(): return 0
    return TB.probe_wdl(b)
sg = lambda x: (x > 0) - (x < 0)
f = open(pgn, encoding="latin-1")
while True:
    g = chess.pgn.read_game(f)
    if g is None: break
    if white in g.headers.get("White", "") and black in g.headers.get("Black", ""):
        print({k: g.headers[k] for k in ("Event", "Site", "Date", "Round", "White", "Black", "Result")})
        b = g.board()
        for mv in g.mainline_moves():
            san = b.san(mv)
            if chess.popcount(b.occupied) <= maxmen:
                try:
                    w = val(b); keep = []
                    for x in b.legal_moves:
                        s = b.san(x); b.push(x); v = val(b); b.pop()
                        if sg(-v) == sg(w): keep.append(s)
                    b.push(mv); after = -val(b); b.pop()
                    flag = "" if sg(after) == sg(w) else "   <== RESULT CHANGES"
                    print(f"{b.fullmove_number}{'.' if b.turn else '...'}{san:8s} | {b.board_fen()} {'w' if b.turn else 'b'} | WDL for side to move {w:+d} | moves keeping it: {' '.join(keep)}{flag}")
                except Exception as e:
                    print(f"{b.fullmove_number}{'.' if b.turn else '...'}{san:8s} | {b.board_fen()} | no table ({type(e).__name__})")
            b.push(mv)
        print("final:", b.board_fen(), g.headers["Result"])
        break
