"""Safety check for catalogue.json against the previous version.

Usage: python3 -I verify_catalogue.py NEW_JSON OLD_JSON
Fails (exit 1) if: invalid JSON, duplicate ids, counts wrong, any entry removed,
or any id / legacyId / status / type changed.
"""
import json, sys, collections

new, old = (json.load(open(p)) for p in sys.argv[1:3])
errors = []
ids = [x["id"] for x in new["games"] + new["otherProjects"]]
if len(ids) != len(set(ids)):
    errors.append("duplicate ids")
c = collections.Counter(g["status"] for g in new["games"])
want = {"rated": len(new["games"]), "Fully Playable": c["Fully Playable"],
        "Mostly Playable": c["Mostly Playable"], "Early Development": c["Early Development"],
        "otherProjects": len(new["otherProjects"])}
if new["counts"] != want:
    errors.append(f"counts mismatch {new['counts']} vs {want}")
for key in ("games", "otherProjects"):
    o = {x["id"]: x for x in old[key]}
    n = {x["id"]: x for x in new[key]}
    missing = set(o) - set(n)
    if missing:
        errors.append(f"{key}: removed {sorted(missing)[:5]}")
    for i in set(o) & set(n):
        for f in ("legacyId", "status", "type", "console", "title"):
            if o[i].get(f) != n[i].get(f):
                errors.append(f"{i}: {f} changed")
print("OK" if not errors else "\n".join(errors[:20]))
sys.exit(1 if errors else 0)
