# SOP: Reels with HyperFrames

Two ways to make video in this repo. Use the simpler one when it is enough.

| | `make video` | HyperFrames (`video/`) |
|---|---|---|
| Input | Rendered slides | HTML composition |
| Motion | Cross fades only | Full animation, video, audio, captions |
| Use for | Story sets, simple sequences | Real reels, footage, anything animated |
| Time | Seconds | A few minutes |

## The simple route

```bash
make new NAME=venue-myths KIND=reel
make venue-myths
make video NAME=venue-myths SECONDS=3
```

## The HyperFrames route

The `video/` folder is a working project, already on brand: BaliVIP fonts, the ink
and gold palette, Instagram-safe copy zones, a slow push on each photograph.

```bash
cd video
cp /path/to/footage.mp4 assets/
# edit index.html
npx hyperframes check      # lint, runtime, layout, motion, contrast
npx hyperframes render     # writes renders/*.mp4
```

`check` must pass before you render. It catches missing assets, broken paths and
contrast failures that are invisible until the video is on a phone.

### Editing the composition

Each scene is a `.clip` div with `data-start` and `data-duration`. To change the
words, edit `.headline` and `.sub`. To change the photograph, drop a file in
`assets/` and update the `src`.

Rules the framework enforces:

- Every timed element needs `data-start` and a duration
- Timelines must be paused and registered on `window.__timelines`
- No `Math.random()`, no `Date.now()`, no network calls. Renders must be deterministic
- Assets are root-relative: `assets/x.jpg`, never `../brand/x.jpg`

Ask Claude in this repo. The HyperFrames skills are bundled in `.claude/skills/` and
it knows the contract.

## Reel structure

| Beat | Time |
|---|---|
| Hook | 0 to 1.5s, motion in frame one |
| Turn | 1.5 to 3s |
| Body | 3 to 15s, one idea |
| Ask | last 3s |

## Subtitles

- On by default. Most people watch on mute.
- Jost Medium, bottom third, above the safe zone.
- Two lines maximum, never over a face.
- Match the spoken words exactly. Do not paraphrase your own voiceover.

## Pacing

Slow. A 4 second hold on a beautiful frame is correct for this brand. Cutting every
half second is a different, cheaper brand.
