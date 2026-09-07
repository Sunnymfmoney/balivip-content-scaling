# SOP: One Drive folder to 10 reels

**Time** About 90 minutes for 10, once you have done it twice.

## 1. Pull the folder

Download the wedding folder from the shared Drive to `photos/` or `video/assets/`.
Keep the original folder name so you can trace it later.

## 2. Sort ruthlessly, once

Make four piles. Do this before you think about content, not during.

| Pile | What goes in it |
|---|---|
| **Motion** | Anything with movement: entrances, dancing, confetti, fireworks, walking |
| **Detail** | Rings, flowers, stationery, food, the small things done properly |
| **Room** | Wide shots of spaces, before and after, setup |
| **People** | Reactions, guests, family, the couple's faces |

Anything that is not a 9 out of 10 gets deleted now. A weak clip in a reel drags the
whole thing down and no edit saves it.

## 3. Assign the ten

The same folder yields the same ten shapes, every time:

| # | Shape | Pile | Job |
|---|---|---|---|
| 1 | The 20 second recap | all | Aesthetic |
| 2 | Setup to finished, one cut | Room | Authority |
| 3 | The entrance, full energy | Motion | Aesthetic |
| 4 | One detail, told properly | Detail | Authority |
| 5 | A "do not" lesson from this wedding | Room + Motion | Authority |
| 6 | What this culture's events needed | all | Authority |
| 7 | The thing that went wrong and was fixed | Room | Authority |
| 8 | Guest reactions | People | Aesthetic |
| 9 | The review, over footage | all | Conversion |
| 10 | Blue hour, held long, no words | Room | Aesthetic |

Seven aesthetic or authority, one conversion, two flexible. That is the correct mix.

## 4. Write before you edit

Open Claude in this repo and use `prompts/reel-from-folder.md`. Give it the wedding
type, what stood out, and any review from that couple. Get all ten hooks and captions
first. Editing without the words written is how a day disappears.

## 5. Build

- Simple slide-based reels: `make new NAME=x KIND=reel` then `make x`, then
  `make video NAME=x SECONDS=3`.
- Anything with real footage, motion or captions: use the `video/` HyperFrames
  project. See `sop/hyperframes-reels.md`.

## 6. Gate and schedule

`make check`, then `qa/pre-publish-checklist.md`, then schedule.

## Do not

- Do not use the same clip in two reels going out the same week.
- Do not post a couple before consent is confirmed in writing.
- Do not name the venue without clearance.
