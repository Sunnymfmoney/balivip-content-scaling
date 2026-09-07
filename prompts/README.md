# Prompt library

Copy a prompt, fill the inputs, paste it into Claude with this repo open.

Every prompt assumes Claude has already read `CLAUDE.md`, which it does automatically
in this folder. That is where the brand rules live, so the prompts stay short.

| Prompt | Use |
|---|---|
| `carousel.md` | Any carousel from a brief |
| `carousel-from-folder.md` | Ten carousels from one wedding folder |
| `reel.md` | A single reel |
| `reel-from-folder.md` | Ten reels from one wedding folder |
| `story.md` | A story set |
| `caption.md` | A caption for an existing post |
| `cta.md` | Fix or write an ask |
| `testimonial.md` | Turn a Google review into a slide |
| `article-feature.md` | One press feature into six posts |
| `venue.md` | Venue and destination content |
| `lead-magnet.md` | Conversion content |
| `repurpose.md` | Old assets into new posts |
| `content-from-transcript.md` | Calls and notes into content |
| `content-from-screenshots.md` | Screenshots, links and folders into content |
| `week-plan.md` | A full week from one wedding |

## Two rules for every prompt

1. **Give Claude the real inputs.** A link to the folder, the actual review text, the
   real transcript. Vague inputs produce generic content, every time.
2. **Ask it to run the gate.** End with "then run make check". If it fails, it will
   fix it. That loop is the whole quality system.
