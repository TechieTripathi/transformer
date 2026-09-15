<!--
  ProbBars - every probability distribution in the deck.

  WHY THIS EXISTS
  The source draft hand-drew bar charts out of block characters on NINE
  separate slides (the sky-is-blue distribution, low/high temperature, the
  three-way temperature comparison, top-k, top-p, greedy, sampling, Paris).
  Block characters do not survive a projector. This is one chart, driven by
  data that comes from scripts/verify-attention.py.

    IF A NUMBER HERE DISAGREES WITH THAT SCRIPT, THIS FILE IS WRONG.

  CHART RULES (these are not preferences)
  - Probability is MAGNITUDE, so: one hue, bars from a common baseline, a
    rounded data-end, a 2px gap between bars. Not a rainbow, not one colour
    per token - colour here carries no identity, only "this is a bar".
  - Value labels wear TEXT colour, never the bar colour.
  - `compare` renders small multiples on a SHARED x-scale. If the scales
    differed the comparison would be a lie, which is exactly the lie the
    draft's ASCII version told.

  CLICK CONTRACT
  NONE. This component deliberately declares no clicks of its own, so a slide
  using it never needs a `clicks:` bump on its account. A slide that wants the
  chart to arrive in stages wraps it, or wraps each `compare` panel, in its
  own `v-click` div. Keeping clicks out of the component is the whole point:
  v-click directives inside a child cannot be auto-counted by Slidev, and a
  slide that forgets the resulting `clicks: N` silently swallows reveals with
  no error. Fewer components with clicks, fewer ways to get that wrong.
-->

<script setup lang="ts">
import { computed } from 'vue'
import { N } from '../composables/useDeckNumbers'

const props = withDefaults(defineProps<{
  tokens?: string[]
  logits?: number[]
  probs?: number[]
  temperature?: number
  compare?: number[]
  topK?: number
  topP?: number
  caption?: string
  compact?: boolean
}>(), {
  temperature: 1,
  compact: false,
})

const tokens = computed(() => props.tokens ?? [...N.decode.tokens])
const logits = computed(() => props.logits ?? [...N.decode.logits])

function softmax(z: number[], T = 1): number[] {
  const s = z.map(v => v / T)
  const m = Math.max(...s)
  const e = s.map(v => Math.exp(v - m))
  const sum = e.reduce((a, b) => a + b, 0)
  return e.map(v => v / sum)
}

const series = computed(() => {
  if (props.compare?.length)
    return props.compare.map(T => ({ label: `T = ${T}`, probs: softmax(logits.value, T) }))
  const probs = props.probs ?? softmax(logits.value, props.temperature)
  const label = props.probs || props.temperature === 1 ? '' : `T = ${props.temperature}`
  return [{ label, probs }]
})

// One scale across every panel. This is the whole point of small multiples:
// if the panels were scaled independently the comparison would be a lie.
const scaleMax = computed(() =>
  Math.max(...series.value.flatMap(s => s.probs), 1e-6))

// Which rows survive the cut, by rank. Computed on the FIRST panel only -
// a cut is a decoding decision, taken once.
const kept = computed<Set<number>>(() => {
  const probs = series.value[0].probs
  const order = [...probs.keys()].sort((a, b) => probs[b] - probs[a])
  if (props.topK != null) return new Set(order.slice(0, props.topK))
  if (props.topP != null) {
    const out = new Set<number>()
    let cum = 0
    for (const i of order) { out.add(i); cum += probs[i]; if (cum >= props.topP) break }
    return out
  }
  return new Set(order)
})

const hasCut = computed(() => props.topK != null || props.topP != null)
const survives = (i: number) => !hasCut.value || kept.value.has(i)
const pct = (p: number) => `${(p / scaleMax.value) * 100}%`
</script>

<template>
  <div class="probbars" :class="{ 'is-compact': compact, 'is-compare': series.length > 1 }">
    <div v-for="(s, si) in series" :key="si" class="panel">
      <div v-if="s.label" class="panel-label">{{ s.label }}</div>

      <div v-for="(tok, i) in tokens" :key="tok" class="row"
           :class="{ cut: !survives(i) }">
        <span class="tok">{{ tok }}</span>
        <span class="track">
          <span class="fill" :style="{ width: pct(s.probs[i]) }" />
        </span>
        <span class="val">{{ s.probs[i].toFixed(s.probs[i] < 0.001 ? 4 : 2) }}</span>
      </div>

      <div v-if="hasCut && si === 0" class="cutnote">
        <template v-if="topK != null">
          kept: the best <b>{{ topK }}</b> &#183; everything below is discarded before sampling
        </template>
        <template v-else>
          kept: enough to cover <b>{{ topP }}</b> of the probability
          &#8212; here that is <b>{{ kept.size }}</b> token<span v-if="kept.size !== 1">s</span>
        </template>
      </div>
    </div>

    <div v-if="caption" class="cap">{{ caption }}</div>
  </div>
</template>

<style scoped>
.probbars { margin: 0.3em 0; }
.is-compare { display: grid; grid-template-columns: repeat(auto-fit, minmax(0, 1fr)); gap: 1.4em; }

.panel-label {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--ann-indigo);
  letter-spacing: 0.06em;
  margin-bottom: 0.35em;
}

.row {
  display: flex;
  align-items: center;
  gap: 0.6em;
  margin-bottom: 2px;          /* the 2px surface gap between fills */
  transition: opacity 0.25s;
}

.tok {
  flex: 0 0 5.2em;
  text-align: right;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.86rem;
  color: var(--ann-ink);
}

.track {
  flex: 1 1 auto;
  height: 15px;
  background: var(--ann-paper-raised);
  border: 1px solid var(--ann-line);
  border-radius: 3px;
  overflow: hidden;
}

/* One hue. Magnitude, not identity - so every bar is the same colour, and
   the rounded end is on the data end only. */
.fill {
  display: block;
  height: 100%;
  background: var(--ann-indigo);
  border-radius: 0 4px 4px 0;
  transition: width 0.3s ease;
}

/* Values are TEXT. They never wear the series colour. */
.val {
  flex: 0 0 3.2em;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 0.82rem;
  color: var(--ann-ink-soft);
}

.row.cut { opacity: 0.32; }
.row.cut .fill { background: var(--ann-muted); }
.row.cut .tok { text-decoration: line-through; }

.cutnote {
  margin-top: 0.5em;
  padding-top: 0.4em;
  border-top: 1px dashed var(--ann-ember);
  font-size: 0.76rem;
  color: var(--ann-ink-soft);
}

.cap {
  margin-top: 0.5em;
  font-size: 0.76rem;
  color: var(--ann-muted);
}

.is-compact .track { height: 11px; }
.is-compact .tok, .is-compact .val { font-size: 0.74rem; }
</style>
