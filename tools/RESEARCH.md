# Daily research run

How the daily RECOMP research task updates `catalogue.json`. Run from the repo root.

## Policy (updated 2026-11-18: the owner asked Claude to decide ratings)
1. **Apply automatically:**
   - newer version tags (release + `filesUrl`);
   - **new games**, once confirmed with git: add to `games` with a rating, `legacyId: null`, and `history` entries for the addition and the rating; extra implementations of a game already listed go to `otherProjects` as `alternate`;
   - **rating changes** (Early Development / Mostly Playable / Fully Playable), judged from the project's own README, release notes or docs using the rating rules in the main README. Only re-rate when there is a clear new statement (e.g. a new release says the game can now be finished). Record a `history` entry with `field: "status"`, old, new, source link and a one-line reason.
   Every change gets a `history` entry and `verified` set to the run date.
2. **Never change the rating of an entry with `ownerRated: true`.** The owner checked those games personally. If evidence seems to disagree, mention it in the proposals file instead.
3. **Never replace a primary project automatically.** When a new project for an already-listed game appears, add it as an `alternate`. If it looks stronger, propose a swap and compare both directions in plain words (what the new one does better *and* where it is behind, e.g. fewer updates, missing features, platforms, release downloads). Developer claims are accepted at face value for ratings until proven otherwise (owner decision 2026-11-18).
4. **Propose, don't apply:** unclear version labels, unreachable repos, moving existing entries between `games` and `otherProjects`, anything excluded, consoles not yet covered, and anything doubtful.
5. Never delete entries. Never change `id` or `legacyId`.
6. On a run that changes something: bump `catalogueVersion` (`YYYY.MM.DD-1`) and `updated`, recompute `counts`, and run the verify tool before committing.
7. Never fill in a version or date from memory. If it can't be confirmed, leave it and say so.

## When the owner rates a game
When the owner says they checked a game and gives its rating: set `status`, set `ownerRated: true`, add a `history` entry (`field: "status"`, note "Rated by the owner"), and run verify with `--owner-change <id>` for that entry only.

## Consoles covered
Nintendo 64, PlayStation 1, PlayStation 2, PlayStation 3, PSP, Original Xbox, Xbox 360, GameCube, Wii, Dreamcast, PC (Windows and DOS; console name `PC`), PlayStation 4, Nintendo Switch. Id prefixes: `pc-`, `ps4-`, `switch-`. Not covered (skip): Switch 2, PS5, Xbox Series, NES, SNES, Genesis, GB/GBC/GBA, DS/3DS, Saturn, Wii U, 3DO, FM Towns, arcade, Mac-only. Note: recomp.fyi does not list Switch projects (consoles still on sale), so find Switch projects through web search and allrecomps.com / recomp.gg.

## Unavailable projects
If a project's repository can't be reached (`git ls-remote` asks for a username), set `unavailable: true` and `unavailableSince`, add a history entry, and list it in proposals. If an `unavailable` project is reachable again, remove the flag with a history entry.

## Which games each day
- Every day: all Fully Playable games, plus all Original Xbox, Xbox 360, PlayStation 2 and PlayStation 3 games.
- Plus by weekday (America/Toronto): Mon Nintendo 64, PC · Tue PlayStation 1, PlayStation 4 · Wed PSP, GameCube, Nintendo Switch · Thu Wii, Dreamcast, PC · Fri Nintendo 64, PlayStation 4 · Sat PlayStation 1, Nintendo Switch · Sun PSP, GameCube, Wii, Dreamcast.

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
- Read https://recomp.fyi/feed.xml: its newest additions (about two days' worth, dozens of projects a day). The main recomp.fyi page only shows its first 50 rows, and the rest loads by script; don't try to pull the full table. Its terms allow reading, including by an assistant; do **not** copy the table or large parts of it. Use it only to spot candidates, and write every entry from the project's own repo.
- Skip decompilations and source ports (RECOMP covers recompilations). Skip Android-only projects (owner decision 2026-11-18: not included).
- Also: web search for new static recompilation releases; allrecomps.com, recompedia.com, recomp.gg as tip sources.
- For each candidate: check it is not already in `catalogue.json` (match `projectUrl` and title, in both `games` and `otherProjects`), then confirm it exists with `git ls-remote --tags <url>` and read its README (a `--depth 1 --filter=blob:none --no-checkout` clone, then `git show HEAD:README.md`). Confirmed candidates are added and rated (policy 1); for the newest version use `tools/check_tags.py` (sorted by date, not name).
- Consoles not covered (see above) are skipped.

## Proposals file
Only list what is new since earlier `proposals/*.md` files; say how many earlier items are still open rather than repeating them. Plain language, links for everything.
