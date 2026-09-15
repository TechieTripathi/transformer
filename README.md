# Transformers

A standalone Slidev deck: **73 slides, ~120 minutes**, written for a single
large class (~500 students) with the full ability range in the room. It
assumes **no prior knowledge** — tokenization, embeddings, attention,
decoding, the block, and training are all built from nothing.

```bash
npm install
npm run verify     # re-derive every number on every slide
npm run dev        # http://localhost:3030
npm run build      # static site, with a downloadable PDF
npm run export     # PDF only
```

## The numbers

[`scripts/verify-attention.py`](scripts/verify-attention.py) is the authoritative
source for every figure in the deck.

> **If a slide disagrees with that script, the slide is wrong.**

It re-derives the worked attention example, the decoding distributions at every
temperature, the top-k and top-p cuts, the softmax-saturation demonstration,
the loss table, and the tokenizations — and `--torch` cross-checks the attention
output against PyTorch's `F.scaled_dot_product_attention` in float64.

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
node scripts/check-overflow.mjs http://localhost:3030 73       # content colliding with the chapter footer
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
the entry file's folder. **`transformers.md` must stay at the repo
root** — moving it into a subfolder would break that.

```
transformers.md                entry: headmatter + 9 src includes
pages/                         one file per chapter, 00–08
components/                    Callout, PipelineMap, ProbBars, AttentionHeat,
                               AttentionTrace, TokenStrip, SpotlightSentence,
                               VectorMap, MaskGrid
composables/useDeckNumbers.ts  GENERATED — do not edit by hand
styles/index.css               palette, utilities, Q/K/V colours
global-bottom.vue              chapter + page footer
scripts/                       verify-attention.py, check-clicks, screenshot
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
