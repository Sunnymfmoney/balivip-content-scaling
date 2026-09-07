# Prompt: Story set

## Inputs needed
- The idea
- The assets
- Whether you want an interactive sticker
- The ask

## The prompt

```
Build a story set for BaliVIP.

Idea:        [one sentence]
Assets:      [folder or photo codes]
Frames:      [3-5]
Interactive: [question box / poll / quiz / slider / none]
Ask:         [story reply / link sticker / none]

Structure: stop, teach or show, ask.

Read playbooks/stories.md first.

Write it to content/stories/<slug>/deck.json and run make <slug>.
```

## Output format
`deck.json`, rendered 1080x1920 frames, plus the sticker wording if interactive.

## Quality standard
- Copy clears the top and bottom 250px. The build handles this
- Five frames maximum
- If it asks a question, someone has to answer the replies

## Brand rules
Stories can be rougher than the feed. That is correct, not sloppy. Everything else
applies: no invented numbers, no unnamed-clearance venues, no em dashes.

## CTA rules
Interactive stickers beat links. Two or three interactive frames a week produce more
enquiries than any single post.
