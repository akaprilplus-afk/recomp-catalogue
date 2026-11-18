"""Classify (ids in tools/ignore_tags.json are always sent to needs-look) tag-check results into: same / update / vague-fill / needs-look / no-tags / unreachable.

Usage: python3 -I tools/classify.py CATALOGUE_JSON RESULTS_JSON [RESULTS_JSON...] OUT_JSON
"""
import json, os, re, sys

cat = {g["id"]: g for g in json.load(open(sys.argv[1]))["games"]}
ins, out = sys.argv[2:-1], sys.argv[-1]
_ign = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ignore_tags.json")
IGNORE = json.load(open(_ign)) if os.path.exists(_ign) else {}

CLEAN = re.compile(r"^[vV]?(\d+(?:\.\d+)*)(?:[-.]?(alpha|beta|rc|preview|hotfix)[\w.-]*)?$", re.I)

def ver(tag):
    m = CLEAN.match(tag)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None

def cat_ver(release):
    text = re.sub(r"\b(19|20)\d\d(-\d\d){0,2}\b", " ", release)  # drop years/dates
    m = re.search(r"\b[vV]?(\d+(?:\.\d+)+|\d+)\b", text)
    return tuple(int(x) for x in m.group(1).split(".")) if m else None

def pad(t, n=5):
    return t + (0,) * (n - len(t))

rows = []
for path in ins:
    for r in json.load(open(path)):
        g = cat[r["id"]]
        r["status"] = g["status"]
        newest = r.get("newest") or []
        if r["id"] in IGNORE:
            r["kind"] = "needs-look"; r["why"] = IGNORE[r["id"]]
        elif "error" in r:
            r["kind"] = "unreachable"
        elif not newest:
            r["kind"] = "no-tags"
        elif r.get("catalogueMentionsNewest"):
            r["kind"] = "same"
        else:
            clean = [t for t in newest if ver(t["tag"])]
            if not clean:
                r["kind"] = "needs-look"; r["why"] = "no clean version label"
            else:
                best = max(clean, key=lambda t: (t["date"], pad(ver(t["tag"]))))
                r["best"] = best
                cv = cat_ver(g["release"])
                nv = ver(best["tag"])
                if best["tag"].lower().lstrip("v") in g["release"].lower():
                    r["kind"] = "same"
                elif cv is None:
                    r["kind"] = "vague-fill"
                elif pad(nv) > pad(cv):
                    r["kind"] = "update"
                else:
                    r["kind"] = "needs-look"; r["why"] = "GitHub label is not higher than catalogue"
        rows.append(r)

json.dump(rows, open(out, "w"), indent=1)
