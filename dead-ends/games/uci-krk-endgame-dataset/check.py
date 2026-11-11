"""Recompute the UCI 'Chess (King-Rook vs. King)' labels by retrograde analysis (no chess library)."""
import sys, collections

import os
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "krkopt.data")
WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve",
         "thirteen", "fourteen", "fifteen", "sixteen"]


def kmoves(s):
    f, r = s % 8, s // 8
    return [(r + dr) * 8 + f + df for dr in (-1, 0, 1) for df in (-1, 0, 1)
            if (dr or df) and 0 <= f + df < 8 and 0 <= r + dr < 8]


KM = [kmoves(s) for s in range(64)]
ADJ = [set(k) for k in KM]


def rook_reach(wr, wk, bk=None):
    """squares the rook attacks/moves to; the white king blocks; a black king blocks but its square is attacked"""
    out = []
    f, r = wr % 8, wr // 8
    for df, dr in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        x, y = f + df, r + dr
        while 0 <= x < 8 and 0 <= y < 8:
            s = y * 8 + x
            if s == wk:
                break
            out.append(s)
            if s == bk:
                break
            x += df; y += dr
    return out


def rook_attacks_through(wr, wk, sq):
    """does the rook attack sq, the black king being transparent (it is the piece moving)?"""
    return sq in rook_reach(wr, wk, None)


# black-to-move positions: (wk, wr, bk) legal if distinct, kings not adjacent
def btm_legal(wk, wr, bk):
    return wk != wr and wk != bk and wr != bk and bk not in ADJ[wk]


def wtm_legal(wk, wr, bk):
    return btm_legal(wk, wr, bk) and bk not in rook_reach(wr, wk, bk)


def black_moves(wk, wr, bk):
    """list of successors: ('cap',) if the rook can be taken, else wtm positions"""
    res = []
    for t in KM[bk]:
        if t in ADJ[wk] or t == wk:
            continue
        if t == wr:
            res.append("cap")  # rook not defended (t not adjacent to wk)
            continue
        if rook_attacks_through(wr, wk, t):
            continue
        res.append((wk, wr, t))
    return res


def white_moves(wk, wr, bk):
    res = []
    for t in KM[wk]:
        if t == wr or t == bk or t in ADJ[bk]:
            continue
        res.append((t, wr, bk))
    for t in rook_reach(wr, wk, bk):
        if t == bk:
            continue
        res.append((wk, t, bk))
    return res


B = {}  # btm position -> depth (white moves to mate)
W = {}
btm = [(a, b, c) for a in range(64) for b in range(64) for c in range(64) if btm_legal(a, b, c)]
wtm = [p for p in btm if wtm_legal(*p)]
bsucc = {p: black_moves(*p) for p in btm}
for p in btm:
    if not bsucc[p] and p[2] in rook_reach(p[1], p[0], p[2]):
        B[p] = 0
wsucc = {p: white_moves(*p) for p in wtm}
n = 0
while True:
    n += 1
    neww = [p for p in wtm if p not in W and any(B.get(q) == n - 1 for q in wsucc[p])]
    for p in neww:
        W[p] = n
    newb = [p for p in btm if p not in B and bsucc[p] and all(q != "cap" and q in W for q in bsucc[p])]
    for p in newb:
        B[p] = max(W[q] for q in bsucc[p])
        assert B[p] == n
    if not neww and not newb:
        break
print("max depth (white moves), black to move:", max(B.values()))

mis = []
dist_file, dist_mine = collections.Counter(), collections.Counter()
seen = set()
for line in open(path):
    a = line.strip().split(",")
    if len(a) != 7:
        continue
    sq = lambda f, r: (int(r) - 1) * 8 + "abcdefgh".index(f)
    p = (sq(a[0], a[1]), sq(a[2], a[3]), sq(a[4], a[5]))
    seen.add(p)
    mine = WORDS[B[p]] if p in B else "draw"
    if not btm_legal(*p):
        mine = "ILLEGAL"
    dist_file[a[6]] += 1; dist_mine[mine] += 1
    if mine != a[6]:
        mis.append((line.strip(), mine))
print("rows:", sum(dist_file.values()), "distinct positions:", len(seen))
print("label distribution in file :", [dist_file[w] for w in ["draw"] + WORDS])
print("label distribution computed:", [dist_mine[w] for w in ["draw"] + WORDS])
print("mismatches:", len(mis))
for m in mis[:40]:
    print("  ", m)
# completeness: positions with the white king in the a1-d1-d4 triangle, up to the diagonal reflection
tri = [p for p in btm if p[0] % 8 <= 3 and p[0] // 8 <= p[0] % 8]
print("legal black-to-move positions with white king in a1-d1-d4 triangle:", len(tri))
flip = lambda s: (s % 8) * 8 + s // 8
canon = set()
for p in tri:
    q = tuple(flip(s) for s in p)
    if p[0] // 8 == p[0] % 8:
        canon.add(min(p, q))
    else:
        canon.add(p)
print("after identifying diagonal mirror images when the king is on a1-d4:", len(canon))
print("file positions inside that canonical family:", len(seen & set(tri)), "of", len(seen))
canon_of = lambda p: min(p, tuple(flip(s) for s in p)) if p[0] // 8 == p[0] % 8 else p
print("distinct mirror classes among the file's positions:", len({canon_of(p) for p in seen}),
      "| all of them among the", len(canon), "classes:", {canon_of(p) for p in seen} == canon)
