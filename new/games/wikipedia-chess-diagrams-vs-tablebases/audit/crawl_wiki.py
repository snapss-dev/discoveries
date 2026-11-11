"""Fetch wikitext of every main-namespace page that embeds a chess-diagram template.
usage: crawl_wiki.py <lang> <out_dir> <template title> [<template title> ...]
"""
import sys, json, time, os, requests

lang, out = sys.argv[1], sys.argv[2]
templates = sys.argv[3:]
os.makedirs(out, exist_ok=True)
S = requests.Session()
S.headers["User-Agent"] = "open-data-research/1.0"
API = f"https://{lang}.wikipedia.org/w/api.php"


def get(params):
    for attempt in range(6):
        r = S.get(API, params=params, timeout=60)
        if r.status_code in (429, 503):
            time.sleep(10 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()
    raise RuntimeError("gave up")


titles = {}
for t in templates:
    cont = {}
    while True:
        p = dict(action="query", list="embeddedin", eititle=t, eilimit=500, einamespace=0, format="json", **cont)
        j = get(p)
        for e in j["query"]["embeddedin"]:
            titles[e["pageid"]] = e["title"]
        if "continue" not in j:
            break
        cont = j["continue"]
        time.sleep(0.5)
    print(t, len(titles), flush=True)

ids = sorted(titles)
outf = open(os.path.join(out, f"{lang}.jsonl"), "w", encoding="utf-8")
for i in range(0, len(ids), 50):
    chunk = ids[i:i + 50]
    p = dict(action="query", prop="revisions", rvprop="content|ids|timestamp", rvslots="main",
             pageids="|".join(map(str, chunk)), format="json", formatversion=2)
    j = get(p)
    for pg in j["query"]["pages"]:
        if "revisions" not in pg:
            continue
        rev = pg["revisions"][0]
        outf.write(json.dumps(dict(lang=lang, pageid=pg["pageid"], title=pg["title"], revid=rev["revid"],
                                   ts=rev["timestamp"], text=rev["slots"]["main"]["content"]), ensure_ascii=False) + "\n")
    time.sleep(0.5)
    if i % 500 == 0:
        print(i, len(ids), flush=True)
outf.close()
print("done", len(ids))
