# recomp-catalogue

Static recompilation catalogue for **RECOMP Library**.

This repository is the single source of truth for the game catalogue. The daily research updates it, and the RECOMP Library app reads it.

## What's here

| File | What it is |
|---|---|
| `catalogue.json` | The catalogue. `games` holds the rated games shown in the app (Fully Playable / Mostly Playable / Early Development). `otherProjects` holds the alternate implementations, review leads and excluded/reference projects that are tracked but not rated. |
| `archive/Static_Recompilation_Master_2026-10-18_Merged_601.xlsx` | The original master workbook this catalogue was converted from, kept unchanged for reference. |
| `archive/workbook-notes-2026-10-18.json` | The workbook's section, audit and scope notes, preserved word for word. |
| `proposals/` | Dated lists of things that need the owner's yes or no. |
| `tools/` | The research scripts. `tools/RESEARCH.md` describes the daily run. |

## How entries work

- Every entry has a permanent `id` (for example `xbox360-sonic-unleashed`) that never changes, even if the title is corrected.
- `legacyId` is the entry's old workbook position (for example `Xbox 360:7`). The app uses it to carry over favourites and edits. Entries added after the conversion have `legacyId: null`.
- `status` is the rating, written on the entry itself.
- `ownerRated: true` means the owner checked the game personally and set its rating. Research never changes those ratings.
- `history` records each change the research makes: the date, what changed, why, and the source link.

## Rating rules

- **Fully Playable:** strong documented evidence the game is playable start to finish (or completion confirmed by the owner). Maintainer claims count, but are labelled as such.
- **Mostly Playable:** meaningful gameplay or progression is documented, but full playability isn't established.
- **Early Development:** limited, unstable, incomplete or insufficiently evidenced gameplay.
- A game is never promoted just because a repository exists, a build launches, or a release is published.
- One primary implementation per game; significant alternatives go in `otherProjects` as `alternate`.
- **Who rates (decided 2026-11-18):** the research rates new games and keeps ratings up to date from each project's own evidence, recording the reason in `history`. Games the owner has checked personally carry `ownerRated: true`; the owner's rating always wins and research never changes it.

## History

- 2026-11-18: first research run (104 version updates); 4 new games and 2 alternates added and rated; owner-rated protection added.
- 2026-11-18: converted from the 2026-10-18 master workbook (601 rated games: 55 / 297 / 249; 222 other tracked projects). All 601 entries were verified field-for-field against the data in RECOMP Library Preview 04A.
