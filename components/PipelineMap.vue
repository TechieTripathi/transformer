<!--
  PipelineMap - the one canonical "where are we" map for the whole deck.

  WHY THIS EXISTS
  The source draft drew the same pipeline SIX times, in ASCII, with slightly
  different wording each time ("The Transformer Sees Numbers", "The Pipeline",
  "The Full Transformer Idea", "The Mathematics Map", "The Entire Story",
  "The Transformer in One Picture"). Those are not six diagrams, they are one
  diagram shown six times - so this is one component shown six times with a
  different stage lit.

  That is also the single best accommodation available for a 500-seat hall.
  A student who lost the thread two minutes ago re-orients by RECOGNISING a
  picture in a fixed position, rather than by RECALLING where we are. Same
  map, same place on the slide, every time; only the highlight moves.

  CLICK CONTRACT

  BEWARE `opacity` AS AN ATTRIBUTE.
  Slidev runs UnoCSS with the attributify preset, which reads bare HTML
  attributes as utility classes. `opacity="1"` is therefore parsed as the
  utility `opacity-1`, and on the Tailwind scale that means ONE PER CENT - so
  a fully opaque element renders invisible, and only when the value is exactly
  1. Every opacity here is set through `:style` for that reason. Do not
  "simplify" it back to an attribute.

  This component declares NO clicks of its own - it is a static map whose
  state is driven entirely by the `highlight` prop. Slides using it therefore
  do NOT need a `clicks:` bump on its account.

  PROPS
    highlight   stage key, or array of keys, to light. [] = all dim (the
                "here is the whole machine" view at the end).
    pending     stage key drawn as NOT BUILT YET - dashed ember outline,
                labelled "next". This exists because a map that lights a box
                the audience has not been taught yet quietly lies to them:
                chapter 3 ends by saying "we have no idea how to compute
                this", and lighting the attention box there contradicts the
                sentence underneath it.
    dimOthers   false renders every stage at full strength (Chapter 8's
                final recap, where nothing is "current" any more).
    compact     shorter, for slides that carry a map plus other content.
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  highlight?: string | string[]
  pending?: string
  dimOthers?: boolean
  compact?: boolean
}>(), { highlight: () => [], pending: '', dimOthers: true, compact: false })

type Stage = { key: string, label: string, sub?: string }

// The spine of the entire lecture, in the order the deck teaches it.
const STAGES: Stage[] = [
  { key: 'text',     label: 'Text',           sub: 'what you type' },
  { key: 'tokens',   label: 'Tokens',         sub: 'chunks' },
  { key: 'embed',    label: 'Embeddings',     sub: 'vectors' },
  { key: 'position', label: '+ Position',     sub: 'where' },
  { key: 'attention',label: 'Attention',      sub: 'which words' },
  { key: 'ffn',      label: 'Feed-Forward',   sub: 'think' },
  { key: 'logits',   label: 'Logits',         sub: 'raw scores' },
  { key: 'probs',    label: 'Probabilities',  sub: 'softmax' },
  { key: 'next',     label: 'Next token',     sub: 'choose' },
]

const W = 920
const H = 154
const CHIP_W = 92
const CHIP_H = 44
const GAP = 11
const Y = 44

const startX = (W - (STAGES.length * CHIP_W + (STAGES.length - 1) * GAP)) / 2
const xOf = (i: number) => startX + i * (CHIP_W + GAP)

const active = computed(() => {
  const h = props.highlight
  return new Set(Array.isArray(h) ? h : h ? [h] : [])
})

const isOn = (k: string) =>
  !props.dimOthers || active.value.size === 0 || active.value.has(k) || k === props.pending
const isLit = (k: string) => active.value.has(k)
const isPending = (k: string) => k === props.pending

// The repeat bracket spans attention + feed-forward: those two ARE the block.
const blockFrom = STAGES.findIndex(s => s.key === 'attention')
const blockTo = STAGES.findIndex(s => s.key === 'ffn')
const blockX = xOf(blockFrom) - 5
const blockW = xOf(blockTo) + CHIP_W - xOf(blockFrom) + 10
</script>

<template>
  <div class="pipemap" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="pm-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3"
                orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L7,3 L0,6 z" fill="var(--ann-muted)" />
        </marker>
      </defs>

      <!-- the repeated block, named so "repeat" is never mysterious -->
      <g class="blockbox">
        <rect :x="blockX" :y="Y - 13" :width="blockW" :height="CHIP_H + 26"
              rx="8" fill="none" stroke="var(--ann-indigo)"
              stroke-width="1.5" stroke-dasharray="5 4" opacity="0.55" />
        <text :x="blockX + blockW / 2" :y="Y - 19" class="blocklbl">
          one transformer block &#183; repeated many times
        </text>
      </g>

      <g v-for="(s, i) in STAGES" :key="s.key">
        <line v-if="i > 0"
              :x1="xOf(i - 1) + CHIP_W" :y1="Y + CHIP_H / 2"
              :x2="xOf(i) - 3" :y2="Y + CHIP_H / 2"
              stroke="var(--ann-muted)" stroke-width="1.5"
              marker-end="url(#pm-arrow)"
              :style="{ opacity: isOn(s.key) ? 0.75 : 0.42 }" />

        <rect :x="xOf(i)" :y="Y" :width="CHIP_W" :height="CHIP_H" rx="7"
              :fill="isLit(s.key) ? 'var(--ann-circuit-soft)' : 'var(--ann-paper-raised)'"
              :stroke="isLit(s.key) ? 'var(--ann-circuit)'
                     : isPending(s.key) ? 'var(--ann-ember)' : 'var(--ann-line)'"
              :stroke-width="isLit(s.key) || isPending(s.key) ? 2.5 : 1"
              :stroke-dasharray="isPending(s.key) ? '6 4' : undefined"
              :style="{ opacity: isOn(s.key) ? 1 : 0.45 }" />

        <text v-if="isPending(s.key)" :x="xOf(i) + CHIP_W / 2" :y="Y - 6" class="nextlbl">
          next &#8595;
        </text>

        <text :x="xOf(i) + CHIP_W / 2" :y="Y + 19" class="lbl"
              :class="{ lit: isLit(s.key), pending: isPending(s.key) }"
              :style="{ opacity: isOn(s.key) ? 1 : 0.45 }">{{ s.label }}</text>
        <text :x="xOf(i) + CHIP_W / 2" :y="Y + 34" class="sub"
              :style="{ opacity: isOn(s.key) ? 1 : 0.45 }">{{ s.sub }}</text>
      </g>

      <!-- the generation loop: the output token becomes part of the next input -->
      <path
        :d="`M ${xOf(STAGES.length - 1) + CHIP_W / 2} ${Y + CHIP_H + 4}
             C ${xOf(STAGES.length - 1)} ${Y + CHIP_H + 40},
               ${xOf(1) + CHIP_W} ${Y + CHIP_H + 40},
               ${xOf(1) + CHIP_W / 2} ${Y + CHIP_H + 4}`"
        fill="none" stroke="var(--ann-ember)" stroke-width="1.8"
        stroke-dasharray="6 4" marker-end="url(#pm-arrow)" opacity="0.8" />
      <text :x="W / 2" :y="Y + CHIP_H + 56" class="looplbl">
        then do the whole thing again, one token at a time
      </text>
    </svg>
  </div>
</template>

<style scoped>
.pipemap svg { width: 100%; max-height: 30vh; display: block; }
.pipemap.is-compact svg { max-height: 25vh; }

text { text-anchor: middle; }

.lbl {
  font-family: 'Space Grotesk', ui-sans-serif, sans-serif;
  font-size: 13px;
  font-weight: 600;
  fill: var(--ann-ink);
}
.lbl.lit { fill: var(--ann-circuit); }
.lbl.pending { fill: var(--ann-ember); }

.nextlbl {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  fill: var(--ann-ember);
}

.sub {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 9.5px;
  fill: var(--ann-muted);
}

.blocklbl, .looplbl {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 10px;
  letter-spacing: 0.06em;
}
.blocklbl { fill: var(--ann-indigo); }
.looplbl { fill: var(--ann-ember); }
</style>
