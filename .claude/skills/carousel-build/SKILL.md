---
name: carousel-build
description: Build and ship Instagram carousels, pinned posts and story sets where copy sits over photographs. Use for any photo-plus-words slide set for Sunny or a client, and when a set is criticised for covering faces, looking flat or black, reading as a template, repeating itself, or shipping a claim nobody can source. Covers the whole run: type placement, the review card, the standalone test, one-ask CTAs, the claims discipline, the QA gate that blocks a bad build, and how to publish without destroying the client's files.
---

# Building a photo carousel that survives the client

Built from the BALIVIP pinned-post set, 2 September 2026. Nine rounds of rejection over one
day, from a first build the client called "still black" to a signed-off final. Every rule
here is a scar. Read `reference/composition.md` for the build contract and the CSS.

## The five things that got it rejected

Fix these before anything else, because they are what a client actually sees.

**1. Type on the subject.** The obvious heuristic is "put words on the darkest band". It is
wrong. The emptiest part of a wedding photograph is usually a bright sky, so darkness-first
scoring sends copy straight onto people's faces. Score on **detail**, not darkness, and let
the scrim handle brightness. `scripts/place.py` does this.

**2. A text card with dead ground.** A card bottom-anchored like a photo slide leaves an
empty third at the top. Beside nine full-bleed photographs it reads as broken, not minimal.
A card fills its frame or it carries a photograph.

**3. The same photograph doing duty across slides.** Three genuinely different reviews on
one repeated image read as one repeated slide. Vary the photograph before you vary anything
else, and match it to that slide's subject.

**4. Slides that only work in sequence.** See the standalone test below.

**5. A number nobody can source.** See the claims discipline below.

## The standalone test

**Every slide must survive being screenshotted alone and sent to one person.**

Nobody reads a carousel in order. They screenshot slide 6 and send it to their partner. So
each slide carries a complete claim, and:

- **No label headlines.** "The venue." "The vendors." "On the day." Those only mean something
 in sequence. Promote the fact out of the body: *"We shortlist venues against your events,
 not the photographs."* If a slide only sets up the next slide, it is not a slide.
- **No orphan references.** "...across all three" when only two things are named on the slide.
 Every pronoun and count needs its antecedent on the same slide.

Heuristic the gate uses: a headline of three words or fewer containing no *we / you / your*
is almost always a label. CTAs are exempt, because an imperative is the point.

## One ask per carousel

The last slide gets **one** action, and no two carousels in a set get the same one.

Three failures to check for, all of which shipped once:

- Two asks on one slide, "send us your dates **or** comment BALI"
- The same CTA copy word-for-word on two different carousels
- The button contradicting the headline: "Comment VIP" above a WhatsApp button

Map the asks to funnel position so they differ by design: top of funnel earns a comment
trigger, middle asks for the specifics, bottom asks for the booking. Explain what they get
and when. Keep comment keywords to four or five letters.

## The claims discipline

**A number that traces only to a meeting does not go on a slide.**

"600 weddings" shipped three times because a client said it twice on a call and I flagged it
each time instead of stopping it. It had no source anywhere; the company's own published
copy said "hundreds of weddings". Flagging while shipping is not flagging.

Before a number ships, find it in the client's own published material or a system of record.
If it is not there, use what is: *"Planning Bali weddings since 2003"* beats an unsourced
round number, and reads more premium.

Watch for the second-order version: a claim that promises a **deliverable** that does not
exist. "You get all sixteen venues with real curfew and capacity" was undeliverable at
sixteen and impossible at fifty. When a count changes, re-read every promise attached to it.

## The QA gate

`scripts/qa_gate.py` blocks the build. Run it before every publish.

 python3 qa_gate.py build.py renders/ banned.json 29

`banned.json` is `{"regex": "why"}` and it is the project's memory. **Every time something is
retracted, add it.** That file is what stops the same mistake shipping twice. The gate also
catches label headlines, missing or wrong-sized renders, visible divider rules, and faint
slide numbers.

Beyond the gate, by eye: caption against photograph (is the ritual named the ritual shown),
every cover at the real mobile grid tile, and a diff against the previous version, **if the
wording is unchanged, the work is not changed.**

## Publishing

**Use `copy`, never `sync`.** The client drops files into these folders. `sync` deletes
anything not present locally, and it will destroy their uploads. A `check` afterwards
reporting "differences" for their files is the correct result, not an error.

**Verify from the destination, never from your own copy.** Download the files back out,
hash them against local, then render one and look at it. A local file matching your intent
proves nothing about what the client opens. A whole version got reviewed from the wrong
folder because of this.

**One folder, updated in place.** Spawning v5, v6, v7 is how a client ends up reviewing a
stale build and telling you nothing changed. If a new version folder is genuinely needed,
rename every older one to `OLD vN - superseded, use vX` the same minute.

## Working rules

- Never quietly change a client's offer or a claim they instructed. Fix the factual errors,
 surface the rest, and let them decide.
- Reproducing a named reviewer's words is a different act from quoting a star rating. Public
 on a review site is not the same as asked. Raise it before it pins.
- When a client says a slide is wrong, look at the pixels before defending the code. "It's
 still black" meant the slide was literally still black, twice, while the reply explained
 the layout.
