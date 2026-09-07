# Prompt: Carousel

## Inputs needed
- The one idea the deck argues
- Which segment: Indian, international, Chinese, western, or all
- Which pillar and which type: aesthetic, authority, or conversion
- The ask, and where it goes
- Which review to use at slide 2, if any
- Roughly how many slides

## The prompt

```
Build a carousel for BaliVIP.

Idea:      [the single argument, one sentence]
Segment:   [Indian / international / Chinese / western / all]
Type:      [aesthetic / authority / conversion]
Ask:       [the one CTA]
Goes to:   [comment keyword / DM / link in bio / WhatsApp / nothing]
Review:    [name from reference/reviews.md, or "none"]
Length:    [8-12] slides

Structure: cover, review at slide 2, one idea per body slide, one CTA.

Before you write, read strategy/03-cta-and-conversion-rules.md and
playbooks/carousels.md.

Write it to content/carousels/<slug>/deck.json, then run:
  make <slug>
  python3 scripts/fit.py build/<slug>

Fix anything either one reports. Then give me the caption, ask first.
```

## Output format
`deck.json`, rendered PNGs in `build/<slug>/`, and a caption.

## Quality standard
- Every headline stands alone if screenshotted
- One idea per slide, nothing repeated
- No photograph twice
- Every line fits on one rendered line
- The ask answers what the deck taught

## Brand rules
No invented numbers. No venue or vendor counts. No em dashes. No venue named without
clearance. Reviews verbatim. American spelling.

## CTA rules
Exactly one. Names the deliverable and the timing. No urgency, no begging, no
exclamation mark.
