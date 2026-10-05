# Transformers

Two Slidev decks and a study kit.

- **Part I** — `transformers.md`: **84 slides, ~135 minutes**, written for a single
  large class (~500 students) with the full ability range in the room. It
  assumes **no prior knowledge** — tokenization, embeddings, attention,
  decoding, the block, and training are all built from nothing.
- **Part II** — `transformers-2.md`: **51 slides, ~75 minutes**. The original 2017
  encoder–decoder: why recurrence had to go, positions done properly, multi-head
  attention with real shapes, the encoder, the decoder and cross-attention, one
  sentence traced through the base model, and the training tricks. Assumes Part I.
- **Study kit** — `docs/study/`: cheat sheet, flashcards and quiz in Markdown,
  plus `transformers-study.html`, a self-contained interactive page (open it
  locally; no network needed).

Both decks were extended using Stanford CME 295, lecture 1
([video](https://www.youtube.com/watch?v=114i2Kz-LZA);
[organized notes](docs/Stanford_CME295_Transformers_LLMs_Organized_Notes.md)) as a
reference for coverage. All slide text, diagrams and numbers are original to these decks.

```bash
npm install
npm run verify     # re-derive every number on every slide (both decks)
npm run dev        # Part I  - http://localhost:3030
npm run dev:2      # Part II
npm run build      # Part I static site, with a downloadable PDF
npm run build:2    # Part II
npm run export     # PDF only (export:2 for Part II)
npm run study      # rebuild docs/study/transformers-study.html from the Markdown
```

Running short on time in Part I? Slides 3 (*How we got here*) and 19 (*Word2Vec*)
can be given `hide: true` in their frontmatter without breaking anything later.

## The numbers

[`scripts/verify-attention.py`](scripts/verify-attention.py) is the authoritative
source for every figure in the deck.

> **If a slide disagrees with that script, the slide is wrong.**

It re-derives the worked attention example, the decoding distributions at every
temperature, the top-k and top-p cuts, the softmax-saturation demonstration,
the loss table, the tokenizations and vocabulary sizes, a BPE merge trace,
sinusoidal positional encodings (with a rotation property test), a two-head
attention, a cross-attention example, LayerNorm, label smoothing, and the shapes
and parameter count of the 2017 base model — measured by a real forward pass.
`--torch` cross-checks attention, multi-head (`nn.MultiheadAttention`),
cross-attention, LayerNorm and the label-smoothed loss against PyTorch in float64.

`composables/useDeckNumbers.ts` is **generated** from it (`npm run numbers`) and
imported by every component, so the deck has exactly one source of truth.

```
npm run verify:torch     # + PyTorch cross-check
npm run numbers          # regenerate useDeckNumbers.ts
```

The tokenizations are frozen in the script and **asserted** against `tiktoken`
when it is installed, so the deck renders without that dependency but drift is
still caught.

## The worked example

Chapter 4 computes attention by hand on three words from
*"The boy dropped the glass because **it** was slippery"*, with `d_model = 4`
and `d_k = 2` so every dot product is a two-term sum a student can check in
their head. It answers the question the lecture opens with:

```
q_it · k_glass = (3)(1) + (−1)(−1) = 4   →   ÷√2 = 2.83   →   softmax   →   0.85
```

and then shows the output vector for *it* arriving at `[0.90, 1.10]`, which is
very nearly `v_glass = [1, 1]`. The pronoun has been resolved by a weighted
average.

## Checks

These exist because all three failure modes are invisible while authoring and
obvious from the back of a lecture hall.

```bash
npm run dev -- --port 3030

node scripts/check-clicks.mjs                          # declared clicks vs v-click indices used
node scripts/check-overflow.mjs http://localhost:3030 84       # content colliding with the chapter footer
                                                               # (Part II: npx slidev transformers-2.md, then 51)
node scripts/screenshot.mjs http://localhost:3030 out/ # capture every slide, then view at 25%
```

`check-clicks` catches the silent one: a slide whose `clicks:` is lower than its
highest `v-click="n"` swallows the reveals past that point with no error.

## Legibility floor

The back row is 25–30 m out, and a projector in a lit hall delivers maybe 15:1
contrast against a laptop's 1000:1 — so contrast fails before size does. The
deck holds itself to:

- nothing smaller than ~2% of image height
- mask grids ≤ 8×8, charts ≤ 15 bars, monospace token panels ≥ 22px
- magnitude encoded **twice** — circle area *and* colour, never colour alone
- no grey or olive in any categorical palette

The Q/K/V palette (`--qkv-query`, `--qkv-key`, `--qkv-value`) was checked with a
colourblindness validator rather than by eye: worst-adjacent CVD ΔE 22.1,
normal-vision 27.8, all three ≥ 3:1 against the paper ground. The hue assignment
(query purple, key orange, value blue) matches the de-facto convention in the
published explainers, so a student who goes looking afterwards finds the same
colours meaning the same things.

## Layout

`styles/index.css`, `components/`, `composables/` and `global-bottom.vue` are
picked up by Slidev for any entry file in this directory, because `userRoot` is
the entry file's folder. **`transformers.md` and `transformers-2.md` must stay at
the repo root** — moving either into a subfolder would break that.

```
transformers.md                Part I entry: headmatter + 9 src includes
transformers-2.md              Part II entry
pages/                         Part I, one file per chapter, 00–08
pages/part2/                   Part II, one file per chapter, 00–08
components/                    Callout, PipelineMap, ProbBars, AttentionHeat,
                               AttentionTrace, TokenStrip, SpotlightSentence,
                               VectorMap, MaskGrid, Timeline, BpeTrace,
                               RnnUnroll, PosEncStrip, ShapeTrace, EncDecMap
composables/useDeckNumbers.ts  GENERATED — do not edit by hand
styles/index.css               palette, utilities, Q/K/V colours
global-bottom.vue              chapter + page footer
scripts/                       verify-attention.py, check-clicks, screenshot,
                               build-study.mjs
docs/study/                    cheatsheet.md, flashcards.md, quiz.md (sources),
                               _template.html, transformers-study.html (generated)
```

Presenter notes are the real script: nearly every slide carries longer notes
than visible content, including suggested phrasing, per-click timing, the likely
student question with its answer, and the transition into the next slide.

## Credits

Every diagram was drawn for this deck. Where a teaching device was borrowed —
the smoothie correction to the library analogy, the "three roles" framing of
Q/K/V, the token-strip visual, the failed `set-it-to-zero` attempt before the
mask — the sources are listed on the deck's final slide. No third-party figures
are embedded.
