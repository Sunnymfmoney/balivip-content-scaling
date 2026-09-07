# BaliVIP Content Scaling

Make carousels, story sequences and videos that already look like BaliVIP, without
rebuilding anything in Canva.

You write the words in a small text file. This repo turns them into finished slides
at the right size, in the right fonts, with the right colours, every time.

---

## One time setup

You need Python 3, Google Chrome, and ffmpeg.

```bash
git clone <this repo>
cd balivip-content-scaling

pip3 install playwright pillow
python3 -m playwright install chrome

brew install ffmpeg        # only needed for video
```

**Then add the photographs.** They are not in this repo because they are too large
for git. Download the BaliVIP photo library from the shared Google Drive and put the
folders inside `photos/`, so it looks like this:

```
photos/
  Indian photos/
  International photos/
  Local photos/
  Venue photos/
  manifest.tsv
```

Check it worked:

```bash
make check
```

---

## Making a post

**1. Start a new one**

```bash
make new NAME=venue-myths KIND=carousel
```

`KIND` is `carousel`, `story` or `reel`.

**2. Write the words**

Open `content/carousels/venue-myths/deck.json`. It is a list of slides. Change the
words. You do not need to know how to code.

```json
{
  "kind": "content",
  "photo": "INI10",
  "lead": "An Indian wedding needs<br>four or five separate spaces.",
  "body": "Across two or three days.<br>Count your events, not your guests."
}
```

`<br>` starts a new line. `photo` is a short code from `photos/manifest.tsv`.

**3. Build it**

```bash
make venue-myths
```

Finished PNGs land in `build/venue-myths/`. Upload them in number order.

**4. Make it a video, if you want one**

```bash
make video NAME=venue-myths SECONDS=3
```

---

## Working with Claude

This repo is built to be handed to Claude. Open the folder in Claude Code and say
what you want:

> Make a five slide carousel about what a Chinese wedding actually needs. Use the
> voice rules and the review from Mega Septiandara.

Claude reads `CLAUDE.md` and already knows the brand voice, the banned claims, the
deck structure and the review rules. It will write the JSON and run the build.

**It will refuse to publish some things, on purpose.** If it says a claim is banned
or a review cannot be trimmed, that is the point. Those rules exist because those
exact claims went out before and had to be pulled down.

---

## The safety net

```bash
make check
```

Checks every deck for banned claims, em dashes, trimmed reviews and wrong image
sizes. If it says **DO NOT POST**, do not post. Fix it and run it again.

---

## Commands

| Command | What it does |
|---|---|
| `make new NAME=x KIND=carousel` | Start a new deck |
| `make x` | Build, render and check the deck named x |
| `make check` | Check every deck |
| `make video NAME=x SECONDS=3` | Turn rendered slides into an MP4 |
| `make list` | Show every deck in the repo |
| `make clean` | Delete everything in build/ |

---

## What lives where

```
CLAUDE.md          the rules. Read this first, it is short
content/           your posts, one folder each
photos/            the photo library (not in git) and manifest.tsv
brand/             fonts, CSS and photo placement. Do not edit casually
scripts/           the build engine
reference/         voice notes, approved reviews, banned claims
build/             finished slides and videos (not in git)
```

---

## If something breaks

**"PHOTO NOT FOUND"** The code is not in `photos/manifest.tsv`, or the file is not
where the manifest says. Run `make list-photos` to see valid codes.

**Slides look like the wrong font.** Chrome could not load the fonts and quietly used
a default. Check `brand/fonts/` still has all seven `.ttf` files, then rebuild.

**A line wrapped and looks broken.** Run `python3 scripts/fit.py build/<name>`. It
names the line. Shorten it or move the `<br>`.

**Video command fails.** Install ffmpeg: `brew install ffmpeg`.

---

## The operating system

The build engine above is half of this repo. The other half is how to decide what to
make, and how to make it convert without cheapening the brand.

| Folder | What is in it |
|---|---|
| `strategy/` | Positioning, audience, pillars, CTA rules, what never to do |
| `playbooks/` | One per format: reels, carousels, stories, pinned, press, testimonials, education, venues, recaps, cultural, lead magnets |
| `sop/` | Step by step: a Drive folder into 10 reels, one wedding into a week, an article into six posts, scheduling |
| `automations/` | ManyChat, keywords, the post-to-destination map, troubleshooting |
| `prompts/` | 15 reusable Claude prompts with inputs, output format and brand rules |
| `qa/` | Pre-publish checklist and the luxury standard |
| `analytics/` | Post scorecard and the log to fill in |
| `templates/` | Content calendar |
| `reference/` | Approved reviews, voice notes, banned claims |
| `video/` | HyperFrames project for real reels, already on brand |

### Start here, in this order

1. `strategy/01-positioning.md`, who is reading and what they are afraid of
2. `strategy/04-do-not-ruin-the-brand.md`, twenty rules, each one already cost something
3. `strategy/02-content-pillars.md`, the three types and the mix
4. `sop/one-wedding-to-one-week.md`, the highest leverage workflow in the repo

That is about twenty minutes and it is enough to start.

### A first week, realistically

```bash
# Monday: plan
# open templates/content-calendar.csv, fill seven rows
# use prompts/week-plan.md with Claude and one wedding folder

# Tuesday and Wednesday: build
make new NAME=count-your-events KIND=carousel
make count-your-events

# Thursday: check and schedule
make check
# then qa/pre-publish-checklist.md, then Meta Business Suite

# Friday: log last week in analytics/post-log.csv
```

### Video

Two routes. `make video NAME=x` cross-fades rendered slides, which is enough for
story sets. For real reels with footage, motion and captions, use the `video/`
HyperFrames project: it is already set up with BaliVIP fonts, palette and safe zones.
See `sop/hyperframes-reels.md`.
