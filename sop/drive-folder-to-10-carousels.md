# SOP: One Drive folder to 10 carousels

**Time** About 2 hours for 10, mostly writing.

## 1. Pull and register the photos

Download the folder into `photos/`. Then add each usable photograph to
`photos/manifest.tsv` with a short code:

```
INI16	Indian photos/Wedding_M&V_Day2-4743.jpg
```

Codes by prefix: `INI` Indian, `INT` international, `WES` international/mixed,
`LOC` local and detail, `VEN` venue, `PRF` review photographs.

**Register once, use forever.** Every deck references the code, so replacing a
photograph updates every carousel that used it.

## 2. Check placement

Add an entry to `brand/placement.json` saying where the copy should sit:

```json
"INI16": { "pos": "bottom" }
```

`bottom` if the top of the photograph is busy, `top` if the bottom is. Copy must land
on the quiet part of the frame and never on a face.

## 3. The ten shapes

| # | Deck | Pillar |
|---|---|---|
| 1 | How NOT to [thing] | Education |
| 2 | What a [culture] wedding actually needs | Cultural |
| 3 | Our process, in order | Authority |
| 4 | [N] questions to ask before you book | Education |
| 5 | What this venue type requires | Venue |
| 6 | The review, told properly | Proof |
| 7 | What it took, behind the scenes | Recap |
| 8 | Two things people confuse | Education |
| 9 | The lead magnet | Conversion |
| 10 | The aesthetic set, minimal copy | Aesthetic |

## 4. Write the decks

Use `prompts/carousel-from-folder.md`. One deck at a time. Claude writes the JSON
directly into `content/carousels/<name>/deck.json`.

## 5. Build and check

```bash
make <name>
python3 scripts/fit.py build/<name>
```

`fit.py` catches any line that wrapped. Shorten it or move the `<br>`.

## 6. The two checks no script does

- **The standalone test.** Screenshot each headline. Does it work alone?
- **No repeats.** No photograph twice inside a set publishing together.
