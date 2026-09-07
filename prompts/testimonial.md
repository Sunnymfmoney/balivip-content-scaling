# Prompt: Testimonial

## Inputs needed
- The review, pasted verbatim from Google
- The reviewer's name as it appears on Google
- The photo code for that couple's own wedding
- Which deck it goes into

## The prompt

```
Turn this review into a BaliVIP slide.

Review (verbatim):
"[paste the whole thing, do not shorten it]"

Name:   [exactly as on Google]
Photo:  [the code for THAT couple's wedding, from photos/manifest.tsv]
Deck:   [which carousel, or "standalone"]

Rules:
- Reproduce the review word for word. Never trim it to fit. The card steps the type
  size down automatically
- If the original contains an ellipsis, keep it and set "elision_is_in_source": true
- The photograph must be that reviewer's own wedding

Add it to reference/reviews.md if it is not there, then build the slide and run
make check.
```

## Output format
The slide JSON, the rendered card, and an updated `reference/reviews.md`.

## Quality standard
Character for character against Google. Name spelled exactly. Correct couple's photo.

## Brand rules
Never trim. Never a stock photo behind a real review. Ask the couple before it goes
on a paid ad.

## CTA rules
A review slide usually carries no ask. It buys permission for the ask later.
