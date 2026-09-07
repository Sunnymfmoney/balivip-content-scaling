# SOP: Turning testimonials into pinned content

## 1. Get the review verbatim

Open the actual Google review. Copy it character for character into
`reference/reviews.md` with the name and the source. Do not retype from memory and do
not shorten it.

## 2. Find that couple's photographs

The photograph on a review slide **must be that reviewer's own wedding**. Ask the
team for the folder if you do not have it. If you cannot find their wedding, you
cannot use their review on a photograph. Use it as text on a plain frame instead.

## 3. Register the photograph

```
PRF4	International photos/<their file>.jpg
```

Use a `PRF` code so it is obvious it is reserved for a review slide.

## 4. Match the review to the deck

The review at slide 2 must argue what the deck argues. See the table in
`playbooks/testimonials.md`. A staffing review on a pricing deck is a wasted slide.

## 5. Build it

```json
{ "kind": "review", "photo": "PRF4", "who": "Full Name",
  "quote": "The review, verbatim." }
```

If the original review genuinely contains an ellipsis, keep it and add
`"elision_is_in_source": true`. The gate blocks any other ellipsis, on purpose.

## 6. Consent

Before it goes on a paid ad, ask the couple. Public on Google is not the same as
agreeing to appear in advertising. One message.

## 7. Check

`make <deck>` then read the card at full size. Every word must match Google exactly.
