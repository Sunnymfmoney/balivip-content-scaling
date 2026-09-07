# Prompt: Ten carousels from one folder

## Inputs needed
- The folder path
- The wedding type
- Any review from this couple

## The prompt

```
Build ten carousels from this wedding folder.

Folder: [path]
Type:   [Indian / international / Chinese / western / mixed]
Review: [paste, or "none"]

Step 1. List the usable photographs and propose a manifest code for each. Tell me
which ones are not good enough and why.

Step 2. Add them to photos/manifest.tsv and brand/placement.json. For placement,
"bottom" if the top of the frame is busy, "top" if the bottom is. Copy must land on
the quiet part and never on a face.

Step 3. Propose ten decks against the ten shapes in
sop/drive-folder-to-10-carousels.md. One line each. Wait for me to approve.

Step 4. Build the ones I approve, one at a time. After each:
  make <slug>
  python3 scripts/fit.py build/<slug>

Fix anything reported. Then give me the caption.

No photograph may appear in more than one deck.
```

## Output format
The photo audit, ten one-liners, then the built decks.

## Quality standard
Every headline standalone. Every line fits. No repeated photographs.

## Brand rules
All standard rules. Consent confirmed before any couple appears.

## CTA rules
Of ten decks, roughly two carry a hard ask. The rest are aesthetic or authority.
