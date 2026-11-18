"""Apply automatic factual updates (kinds 'update' and 'vague-fill') to catalogue.json.

Usage: python3 -I apply_updates.py CATALOGUE_JSON CLASSIFIED_JSON RUN_DATE
Writes CATALOGUE_JSON in place. Never touches id, legacyId, status, or removes entries.
"""
import json, sys, collections

cat_path, cls_path, run_date = sys.argv[1:4]
d = json.load(open(cat_path))
by_id = {g["id"]: g for g in d["games"]}
applied = 0
for r in json.load(open(cls_path)):
    if r["kind"] not in ("update", "vague-fill"):
        continue
    g = by_id[r["id"]]
    tag, tdate = r["best"]["tag"], r["best"]["date"]
    base = g["projectUrl"].rstrip("/")
    source = f"{base}/releases/tag/{tag}"
    new_release = f"{tag} ({tdate})"
    changes = []
    if g["release"] != new_release:
        changes.append(("release", g["release"], new_release))
        g["release"] = new_release
    if g.get("filesUrl") != source:
        changes.append(("filesUrl", g.get("filesUrl"), source))
        g["filesUrl"] = source
    if changes:
        g.setdefault("history", [])
        for field, old, new in changes:
            g["history"].append({
                "date": run_date, "field": field, "old": old, "new": new,
                "source": source,
                "note": "Newest version tag on GitHub; date is the tagged code's date (approximate release date).",
            })
        g["verified"] = run_date
        applied += 1

c = collections.Counter(g["status"] for g in d["games"])
d["counts"] = {"rated": len(d["games"]), "Fully Playable": c["Fully Playable"],
               "Mostly Playable": c["Mostly Playable"], "Early Development": c["Early Development"],
               "otherProjects": len(d["otherProjects"])}
d["catalogueVersion"] = run_date.replace("-", ".") + "-1"
d["updated"] = run_date
json.dump(d, open(cat_path, "w"), ensure_ascii=False, indent=2)
open(cat_path, "a").write("\n")
print("entries updated:", applied)
