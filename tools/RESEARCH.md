# Daily research run

How the daily RECOMP research task updates `catalogue.json`. Run from the repo root.

## Policy
1. **Apply automatically** only factual updates: a newer version tag (release field + `filesUrl`), each with a `history[]` entry (date, field, old, new, source link). Set `verified` to the run date on changed entries.
2. **Propose, don't apply**: new games, rating changes, moving entries between `games` and `otherProjects`, anything excluded, unclear version labels, unreachable repos. Write these to `proposals/YYYY-MM-DD.md`.
3. Never delete entries. Never change `id` or `legacyId`.
4. On a run that changes something: bump `catalogueVersion` (`YYYY.MM.DD-1`) and `updated`, recompute `counts` (the apply tool does this), run the verify tool before committing.
5. Never fill in a version or date from memory. If it can't be confirmed, leave it and say so.

## Which games each day
- Every day: all Fully Playable games, plus all Original Xbox, Xbox 360, PlayStation 2 and PlayStation 3 games.
- Plus by weekday (America/Toronto): Mon Nintendo 64 · Tue PlayStation 1 · Wed PSP, GameCube · Thu Wii, Dreamcast · Fri Nintendo 64 · Sat PlayStation 1 · Sun PSP, GameCube, Wii, Dreamcast.

## Steps
```
python3 -I tools/check_tags.py catalogue.json /tmp/a.json --status "Fully Playable"
python3 -I tools/check_tags.py catalogue.json /tmp/b.json --console "Original Xbox,Xbox 360,PlayStation 2,PlayStation 3"
python3 -I tools/check_tags.py catalogue.json /tmp/c.json --console "<today's rotation>"
python3 -I tools/classify.py catalogue.json /tmp/a.json /tmp/b.json /tmp/c.json /tmp/classified.json
cp catalogue.json /tmp/catalogue.before.json
python3 -I tools/apply_updates.py catalogue.json /tmp/classified.json YYYY-MM-DD
python3 -I tools/verify_catalogue.py catalogue.json /tmp/catalogue.before.json
```
(Overlapping games are fine: classify keeps each result; apply skips entries already current.)

Kinds from `classify.py`: `update` and `vague-fill` are applied; `needs-look` and `unreachable` go to proposals; `same` and `no-tags` need nothing. `tools/ignore_tags.json` lists entries whose tags must never be applied (e.g. tags inherited from another project).

Before applying, glance over the `update` list for anything implausible (a huge jump, a 2025 date, a label like `windows-latest`). Move doubtful ones to proposals instead.

## Finding new projects
- Read https://recomp.fyi (its terms allow reading, including by an assistant; do **not** copy the table or large parts of it). Use it only to spot candidates.
- Also: web search for new static recompilation releases; allrecomps.com, recompedia.com, recomp.gg as tip sources.
- For each candidate: check it is not already in `catalogue.json` (match `projectUrl` and title, in both `games` and `otherProjects`), then confirm it exists with `git ls-remote --tags <url>`. Only confirmed candidates go to proposals, with link and newest version label.
- Consoles not yet in the catalogue (Switch, Switch 2, DS, 3DS, etc.) are not proposed until the owner decides whether to cover them.

## Proposals file
Only list what is new since earlier `proposals/*.md` files; say how many earlier items are still open rather than repeating them. Plain language, links for everything.
