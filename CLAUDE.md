# CLAUDE.md

You are helping the BaliVIP Wedding social media team make content at scale.

Read this file before you write a single line of copy or touch a deck.

---

## What this repo is

A content factory. You describe a post in JSON, the repo renders it as finished
1080x1350 carousel slides, 1080x1920 story frames, or an MP4. Every output carries
BaliVIP's real fonts, colours and layout, so nothing has to be rebuilt in Canva.

Three formats, one engine:

| Format | Size | Use |
|---|---|---|
| `carousel` | 1080x1350 | Feed posts and pinned posts |
| `story` | 1080x1920 | Stories, safe zones already handled |
| `reel` | 1080x1920 | Slide sequences exported to MP4 |

## The loop

```bash
make new NAME=venue-myths KIND=carousel   # scaffold a deck
# edit content/carousels/venue-myths/deck.json
make venue-myths                          # build, render, and gate in one step
```

`make <name>` refuses to finish if the quality gate fails. That is deliberate.


---

## Where everything is

Read the file for the job in front of you. Do not read all of them.

| Doing | Read |
|---|---|
| Anything at all, first time | `strategy/01-positioning.md`, `strategy/04-do-not-ruin-the-brand.md` |
| Deciding what to post | `strategy/02-content-pillars.md` |
| Writing an ask | `strategy/03-cta-and-conversion-rules.md` |
| A specific format | `playbooks/<format>.md` |
| Turning assets into posts | `sop/` |
| Keywords, ManyChat, destinations | `automations/` |
| A reusable prompt | `prompts/` |
| Before publishing | `qa/pre-publish-checklist.md` |
| Judging what worked | `analytics/scorecard.md` |
| The exact words of a review | `reference/reviews.md` |

**Never invent a review, a number, or a claim that is not in `reference/`.**

## The three types

Every post is exactly one. Decide before writing.

- **Aesthetic** stops the scroll and proves taste. Usually no ask.
- **Authority** proves competence. Soft ask.
- **Conversion** produces an enquiry. One hard ask.

Target mix is roughly 40 / 40 / 20. Conversion only works because the other 80
percent earned it.

---

## Hard rules. These are not style preferences.

**1. No em dashes. Ever.** Not in slides, not in captions, not in your replies in
this repo. Use a comma, a full stop, or rewrite the sentence. The gate fails on one.

**2. Never invent a number.** Not a venue count, not a wedding count, not a price,
not a years-in-business figure. If you cannot point at where a number came from,
leave it out. Write `[NEEDS CHECKING]` and ask a human. A number that has to be
walked back costs more than the post ever earned.

**3. Counts of venues and vendors are banned outright.** Not reduced. Banned. Every
version of that claim that shipped was wrong, and every promise attached to a count
had to be retracted. `reference/banned-claims.json` holds the list and the gate
enforces it. Do not reword your way around it.

**4. A review is quoted word for word or not at all.** Never trim a review to make it
fit the card. The type size steps down automatically for longer quotes, so length is
never a reason to edit someone's words. If the original review genuinely contains an
ellipsis, keep it and set `"elision_is_in_source": true` on that slide. A couple who
sees their own review misquoted on your feed is a problem you cannot apologise your
way out of.

**5. Never name a venue in copy** unless a human has explicitly cleared that specific
post. Venue relationships are commercial and they change.

**6. Real people are in these photographs.** Never put a couple's photograph on a
slide that makes a claim about a different couple. If a review is on the slide, the
photograph must be that reviewer's own wedding.

---

## The voice

BaliVIP's buyers are not shopping for a beautiful wedding. They are shopping for a
way to stop being afraid. Most of them are wiring a large sum to strangers in a
country they have never visited, for a day that cannot be rescheduled.

**Write to that.** Calm, specific, and operational. The brand is the most capable
option in Bali, not the one asking for the booking.

**Do**
- Short sentences. Common words. Roughly a third grade reading level.
- Name the actual thing. "A baraat needs a driveway and room to turn around" beats
  "we handle cultural requirements."
- Lead with what the reader gets, then earn it underneath.
- Imperative CTAs. "WhatsApp us now", not "Message us your date."
- Prove competence through mechanism: what you plan for, what you ask, what the
  couple never sees.

**Do not**
- Do not beg. No "no pressure", no soft hedges, no asking permission.
- Do not use trade jargon. If the internal team has to ask what a line means, it
  does not publish. That has happened twice and both lines are now banned.
- Do not open on a founder portrait or a static shot. A hook has to stop a scroll.
- Do not write a headline that only makes sense on the previous slide. Every
  headline has to stand alone if someone screenshots it and sends it to one person.

**British or American spelling:** American. "Center", "color", "makeup" as one word.

---

## Deck structure that works

Cover, proof, then the argument, then one ask.

1. **Cover.** The hook. One idea. This is the only slide most people see.
2. **Review.** A real Google review with that couple's photograph behind it.
   Proof arrives before the pitch, not after.
3. **The body.** One idea per slide. No slide repeats another.
4. **CTA.** One ask. Name what they get and when they get it.

**The last slide asks for exactly one thing.** Not two. If a deck asks for a comment
and a WhatsApp and a link tap, it gets none of them.

---

## Slide kinds

Every slide is an object in `deck.json` with a `kind`.

```jsonc
{ "kind": "cover",  "photo": "INT07", "title": "Line one<br>Line two", "hook": "One sentence." }
{ "kind": "cover",  "trio": ["INI14","INT03","WES10"], "title": "...", "hook": "..." }
{ "kind": "review", "photo": "PRF2", "who": "Naresh Ahuja", "quote": "Word for word." }
{ "kind": "content","photo": "INI10", "lead": "The point.", "body": "The detail." }
{ "kind": "checklist","photo":"INT28","lead":"Do these five<br>things instead.","items":["...","..."] }
{ "kind": "cta",    "photo": "INI12", "lead": "The ask.", "body": "What they get.", "action": "Comment VIP below" }
```

- `<br>` forces a line break. Use it to control where lines land.
- `pos`: `"top"` or `"bottom"` moves the copy block. Defaults come from
  `brand/placement.json`, which knows where each photograph has empty space.
- `crop`: `"50% 18%"` shifts the CTA photograph's focal point.

**Line length matters.** Type steps down as copy gets longer, but a line that wraps
looks broken. Run `python3 scripts/fit.py build/<name>` to catch any line that
wrapped, and shorten it.

---

## Photographs

`photos/` is not in git. It is large and it is BaliVIP's own library. Pull it from
the shared Drive and drop it in, then keep `photos/manifest.tsv` in sync:

```
INT07	International photos/220526_CherieJames_1192.jpg
```

Slides reference the short key, never a filename. Change a photo in one place and
every deck that uses it updates.

**No photograph should appear twice** across a set of decks that publish together.
The build does not enforce this. You have to check.

---

## Before anything is posted

Run the gate. Then check these by eye, because no script can:

- [ ] Does every headline stand alone?
- [ ] Does the last slide ask for exactly one thing?
- [ ] Is every number on a slide traceable to a source?
- [ ] Is every review word for word against the actual Google review?
- [ ] Does the review photograph show that reviewer's own wedding?
- [ ] No photograph repeated across decks going out together?
- [ ] Does any copy sit on a face, or on the bright part of a photograph?

## When you are not sure

Ask. Do not guess and do not fill a gap with a plausible number. "I need a real
figure for this, where does it come from" is always the right move, and it takes a
minute. Publishing a wrong claim takes weeks to undo.
