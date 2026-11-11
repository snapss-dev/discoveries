"""Extract every chess diagram with at most 7 men from the crawled wikitext.
Writes data/diagrams.jsonl with: lang, title, revid, idx, placement (FEN board field), men, header, caption.
"""
import json, re, sys, os

NAMES = r"(?:Diagramma scacchi|Diagram schaken|Szachownica|Diagrama de xadrez(?: pequeno)?|Шахова діаграма(?: мала)?|Šachovnice|Schackdiagram|Sakkállás|Chess diagram(?: small)?)"
START = re.compile(r"\{\{\s*" + NAMES + r"\s*(?=[|\n])", re.I)
PIECE = re.compile(r"^[kqrbnp][ld]$")


def template_end(text, i):
    depth = 0
    j = i
    n = len(text)
    while j < n - 1:
        two = text[j:j + 2]
        if two == "{{":
            depth += 1; j += 2
        elif two == "}}":
            depth -= 1; j += 2
            if depth == 0:
                return j
        else:
            j += 1
    return -1


def split_top(body):
    parts, cur, d1, d2 = [], [], 0, 0
    j = 0
    while j < len(body):
        two = body[j:j + 2]
        if two == "{{": d1 += 1; cur.append(two); j += 2; continue
        if two == "}}": d1 -= 1; cur.append(two); j += 2; continue
        if two == "[[": d2 += 1; cur.append(two); j += 2; continue
        if two == "]]": d2 -= 1; cur.append(two); j += 2; continue
        c = body[j]
        if c == "|" and d1 == 0 and d2 == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(c)
        j += 1
    parts.append("".join(cur))
    return parts


def strip_comments(s):
    return re.sub(r"<!--.*?-->", "", s, flags=re.S)


def to_placement(cells):
    rows = []
    for r in range(8):
        row, empty = "", 0
        for c in cells[r * 8:(r + 1) * 8]:
            c = c.strip().lower()
            if PIECE.match(c):
                if empty: row += str(empty); empty = 0
                ch = c[0]
                row += ch.upper() if c[1] == "l" else ch
            else:
                empty += 1
        if empty: row += str(empty)
        rows.append(row)
    return "/".join(rows)


def parse_template(body):
    body = strip_comments(body)
    parts = split_top(body)[1:]
    named, pos = {}, []
    for p in parts:
        m = re.match(r"^\s*([A-Za-zÀ-ÿА-я0-9_ ]{1,20}?)\s*=(.*)$", p, re.S)
        s = p.strip()
        if s.startswith("="):
            continue  # de row separators
        if m and not PIECE.match(s):
            named[m.group(1).strip()] = m.group(2).strip()
        else:
            pos.append(p)
    if "Z8" in named:  # German named-row format
        cells = []
        for r in "87654321":
            row = [x for x in named.get("Z" + r, "").split("/")]
            row = (row + [""] * 8)[:8]
            cells += row
        return to_placement(cells), named.get("Titel", ""), named.get("Beschreibung", "")
    if len(pos) < 66:
        return None
    header = pos[1].strip()
    cells = pos[2:66]
    caption = " | ".join(x.strip() for x in pos[66:] if x.strip())
    return to_placement(cells), header, caption


def main():
    out = open("data/diagrams2.jsonl", "w", encoding="utf-8")
    stats = {}
    for lang in sys.argv[1:]:
        ntpl = nbad = nsmall = 0
        for line in open(f"data/wiki2/{lang}.jsonl", encoding="utf-8"):
            d = json.loads(line)
            text = d["text"]
            for idx, m in enumerate(START.finditer(text)):
                e = template_end(text, m.start())
                if e < 0:
                    nbad += 1; continue
                ntpl += 1
                res = parse_template(text[m.start() + 2:e - 2])
                if res is None:
                    nbad += 1; continue
                placement, header, caption = res
                men = sum(ch.isalpha() for ch in placement)
                if placement.count("K") != 1 or placement.count("k") != 1 or men > 7:
                    continue
                nsmall += 1
                # text following the diagram, for context
                ctx = text[e:e + 4000]
                out.write(json.dumps(dict(lang=lang, title=d["title"], revid=d["revid"], idx=idx, placement=placement,
                                          men=men, header=header, caption=caption, ctx=ctx), ensure_ascii=False) + "\n")
        stats[lang] = (ntpl, nbad, nsmall)
    print(stats)


main()
