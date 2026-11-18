"""Read the newest version tags for catalogue games straight from GitHub (git ls-remote + a
tiny tag-only fetch for dates). Works without the GitHub API.

Usage:
  python3 -I tools/check_tags.py catalogue.json OUT.json [--status "Fully Playable"] [--console "Xbox 360,PlayStation 2"]
Both filters are optional; when both are given a game must match both.
"""
import argparse, json, re, subprocess, tempfile, time

ap = argparse.ArgumentParser()
ap.add_argument("catalogue"); ap.add_argument("out")
ap.add_argument("--status"); ap.add_argument("--console")
a = ap.parse_args()
consoles = set(a.console.split(",")) if a.console else None
games = [g for g in json.load(open(a.catalogue))["games"]
         if (not a.status or g["status"] == a.status) and (not consoles or g["console"] in consoles)]

def run(args, cwd=None, timeout=120):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=timeout)

def norm(s):
    return s.lower().lstrip("v")

results = []
for g in games:
    url = (g.get("projectUrl") or "").rstrip("/")
    m = re.match(r"https://github\.com/([^/]+)/([^/#?]+)", url)
    r = {"id": g["id"], "title": g["title"], "console": g["console"],
         "catalogueRelease": g["release"], "url": url}
    if not m:
        r["error"] = "no GitHub project URL"; results.append(r); continue
    repo = f"https://github.com/{m.group(1)}/{m.group(2)}"
    try:
        ls = run(["git", "ls-remote", "--tags", repo], timeout=60)
        if ls.returncode != 0:
            r["error"] = "ls-remote failed: " + ls.stderr.strip()[-200:]
            results.append(r); continue
        tags = sorted({l.split("refs/tags/")[1].removesuffix("^{}")
                       for l in ls.stdout.splitlines() if "refs/tags/" in l})
        r["tagCount"] = len(tags)
        if not tags:
            results.append(r); continue
        with tempfile.TemporaryDirectory() as d:
            run(["git", "init", "-q", "--bare", d])
            f = run(["git", "fetch", "-q", "--depth", "1", "--filter=tree:0", repo,
                     "+refs/tags/*:refs/tags/*"], cwd=d, timeout=240)
            if f.returncode != 0:
                r["fetchWarning"] = f.stderr.strip()[-200:]
            fe = run(["git", "for-each-ref", "refs/tags", "--sort=-creatordate",
                      "--format=%(refname:short)\t%(creatordate:short)\t%(*committerdate:short)"], cwd=d)
        rows = []
        for line in fe.stdout.splitlines():
            name, d1, d2 = (line.split("\t") + ["", ""])[:3]
            rows.append({"tag": name, "date": d2 or d1})
        rows.sort(key=lambda x: x["date"], reverse=True)
        r["newest"] = rows[:3]
        if rows:
            top = rows[0]["tag"]
            r["catalogueMentionsNewest"] = norm(top) in norm(g["release"]) or \
                norm(top) in (g.get("filesUrl") or "").lower()
    except subprocess.TimeoutExpired:
        r["error"] = "timed out"
    results.append(r)
    time.sleep(1)

json.dump(results, open(a.out, "w"), indent=1)
print(f"checked {len(results)}")
