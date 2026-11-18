# recomp-catalogue

Static recompilation catalogue for **RECOMP Library**.

This repository is the single source of truth for the game catalogue. The daily research updates it, and the RECOMP Library app reads it.

## What's here

| File | What it is |
|---|---|
| `catalogue.json` | The catalogue. `games` holds the 601 rated games shown in the app (Fully Playable / Mostly Playable / Early Development). `otherProjects` holds the alternate implementations, review leads and excluded/reference projects that are tracked but not rated. |
| `archive/Static_Recompilation_Master_2026-10-18_Merged_601.xlsx` | The original master workbook this catalogue was converted from, kept unchanged for reference. |
| `archive/workbook-notes-2026-10-18.json` | The workbook's section, audit and scope notes, preserved word for word. |

## How entries work

- Every entry has a permanent `id` (for example `xbox360-sonic-unleashed`) that never changes, even if the title is corrected.
- `legacyId` is the entry's old workbook position (for example `Xbox 360:7`). The app uses it to carry over favourites and edits.
- `status` is the rating, written on the entry itself.
- `history` records each change the research makes: the date, what changed, why, and the source link.

## Rating rules

- **Fully Playable:** strong documented evidence the game is playable start to finish (or completion confirmed by the owner). Maintainer claims count, but are labelled as such.
- **Mostly Playable:** meaningful gameplay or progression is documented, but full playability isn't established.
- **Early Development:** limited, unstable, incomplete or insufficiently evidenced gameplay.
- A game is never promoted just because a repository exists, a build launches, or a release is published.
- One primary implementation per game; significant alternatives go in `otherProjects` as `alternate`.

## History

- 2026-11-18: converted from the 2026-10-18 master workbook (601 rated games: 55 / 297 / 249; 222 other tracked projects). All 601 entries were verified field-for-field against the data in RECOMP Library Preview 04A.
