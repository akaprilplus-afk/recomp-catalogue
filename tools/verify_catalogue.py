"""Safety check for catalogue.json against the previous version.

Usage: python3 -I tools/verify_catalogue.py NEW_JSON OLD_JSON [--owner-change ID ...]
Fails (exit 1) if: duplicate ids, counts wrong, any entry removed, any id / legacyId /
type / console / title changed, a rating changed without a matching history entry, or a
rating set by the owner (ownerRated: true) changed. Only pass --owner-change for entries the
owner rated in this same session, when the owner asked for it.
"""
import argparse, collections, json, sys

ap = argparse.ArgumentParser()
ap.add_argument("new"); ap.add_argument("old")
ap.add_argument("--owner-change", nargs="*", default=[])
a = ap.parse_args()
new, old = json.load(open(a.new)), json.load(open(a.old))
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
bad = [g["id"] for g in new["games"] if g["status"] not in ("Fully Playable", "Mostly Playable", "Early Development")]
if bad:
    errors.append(f"unknown status on {bad[:5]}")
for key in ("games", "otherProjects"):
    o = {x["id"]: x for x in old[key]}
    n = {x["id"]: x for x in new[key]}
    missing = set(o) - set(n)
    if missing:
        errors.append(f"{key}: removed {sorted(missing)[:5]}")
    for i in set(o) & set(n):
        for f in ("legacyId", "type", "console", "title"):
            if o[i].get(f) != n[i].get(f):
                errors.append(f"{i}: {f} changed")
        if o[i].get("status") != n[i].get("status") or o[i].get("ownerRated") != n[i].get("ownerRated"):
            if o[i].get("ownerRated") and i not in a.owner_change:
                errors.append(f"{i}: owner-rated entry changed")
            if o[i].get("status") != n[i].get("status") and not any(
                    h.get("field") == "status" and h.get("new") == n[i].get("status") for h in n[i].get("history", [])):
                errors.append(f"{i}: status changed without a history entry")
print("OK" if not errors else "\n".join(errors[:20]))
sys.exit(1 if errors else 0)
