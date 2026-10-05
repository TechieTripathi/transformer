<!--
  RnnUnroll - the pre-2017 answer to "which words matter?": read left to
  right and carry everything in one running memory (the hidden state).

  Three modes, one picture, so the comparison is fair:
    'rnn'        cells in a chain; each passes its memory h to the next.
                 The step numbers make the second flaw visible: step 7
                 cannot start until step 6 has finished - no parallelism.
    'fade'       the first flaw: what is left of "glass" by the time the
                 chain reaches "it". Dot AREA shrinks by a constant factor
                 per step - an illustration of the vanishing signal, not a
                 measured quantity, and labelled as such.
    'attention'  the fix: "it" connects to every earlier word DIRECTLY, one
                 step away regardless of distance.

  CLICK CONTRACT: none - drive `mode` from the slide.
  Opacity only via :style (UnoCSS attributify trap; see AttentionHeat).
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  mode?: 'rnn' | 'fade' | 'attention'
  words?: string[]
  focus?: number      // index of the word whose signal we follow
  query?: number      // index of the word doing the looking
  compact?: boolean
}>(), { mode: 'rnn', compact: false })

const ws = computed(() => props.words ?? ['The', 'boy', 'dropped', 'the', 'glass', 'because', 'it'])
const n = computed(() => ws.value.length)
const focusI = computed(() => props.focus ?? 4)
const queryI = computed(() => props.query ?? n.value - 1)

const W = 920
const H = 230
const CW = 92, CH = 56, Y = 92
const gap = computed(() => (W - 60 - n.value * CW) / Math.max(n.value - 1, 1))
const xOf = (i: number) => 30 + i * (CW + gap.value)

// Illustrative decay: area x0.45 per step after the focus word.
const DECAY = 0.45
const dotR = (i: number) => {
  const k = i - focusI.value
  if (k < 0) return 0
  return 16 * Math.sqrt(Math.pow(DECAY, k))
}
</script>

<template>
  <div class="rnn" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="rnn-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L7,3 L0,6 z" fill="var(--ann-indigo)" />
        </marker>
        <marker id="rnn-arrow-e" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L7,3 L0,6 z" fill="var(--ann-ember)" />
        </marker>
      </defs>

      <g v-for="(w, i) in ws" :key="i">
        <!-- word -->
        <text :x="xOf(i) + CW / 2" :y="Y + CH + 46" class="word"
              :class="{ focus: mode !== 'rnn' && i === focusI, query: mode === 'attention' && i === queryI }">{{ w }}</text>
        <line :x1="xOf(i) + CW / 2" :y1="Y + CH + 26" :x2="xOf(i) + CW / 2" :y2="Y + CH + 4"
              stroke="var(--ann-muted)" stroke-width="1.5" marker-end="url(#rnn-arrow)"
              :style="{ opacity: mode === 'attention' ? 0.35 : 0.8 }" />

        <!-- cell -->
        <rect :x="xOf(i)" :y="Y" :width="CW" :height="CH" rx="8"
              :fill="mode === 'attention' ? 'var(--ann-paper-raised)' : 'var(--ann-indigo-soft)'"
              stroke="var(--ann-indigo)" stroke-width="1.5"
              :style="{ opacity: mode === 'attention' ? 0.45 : 1 }" />
        <text v-if="mode !== 'fade'" :x="xOf(i) + CW / 2" :y="Y + CH / 2 + 6" class="h"
              :style="{ opacity: mode === 'attention' ? 0.45 : 1 }">h<tspan class="sub" dy="4">{{ i + 1 }}</tspan></text>
        <circle v-if="mode === 'fade' && dotR(i) > 0" :cx="xOf(i) + CW / 2" :cy="Y + CH / 2" :r="dotR(i)"
                fill="var(--ann-ember)" :style="{ opacity: 0.25 + 0.75 * (dotR(i) / 16) }" />
        <text v-if="mode === 'rnn'" :x="xOf(i) + CW / 2" :y="Y - 12" class="stepno">step {{ i + 1 }}</text>

        <!-- memory hand-off -->
        <line v-if="i < n - 1" :x1="xOf(i) + CW" :y1="Y + CH / 2" :x2="xOf(i + 1) - 3" :y2="Y + CH / 2"
              stroke="var(--ann-indigo)" stroke-width="2.2" marker-end="url(#rnn-arrow)"
              :style="{ opacity: mode === 'attention' ? 0.3 : 1 }" />
      </g>

      <!-- direct connections -->
      <template v-if="mode === 'attention'">
        <path v-for="j in queryI" :key="'a' + j"
              :d="`M ${xOf(queryI) + CW / 2} ${Y - 4} Q ${(xOf(queryI) + xOf(j - 1)) / 2 + CW / 2} ${Y - 30 - (queryI - j + 1) * 9} ${xOf(j - 1) + CW / 2} ${Y - 4}`"
              fill="none" :stroke="j - 1 === focusI ? 'var(--ann-ember)' : 'var(--ann-muted)'"
              :stroke-width="j - 1 === focusI ? 4 : 1.5"
              :marker-end="j - 1 === focusI ? 'url(#rnn-arrow-e)' : 'url(#rnn-arrow)'"
              :style="{ opacity: j - 1 === focusI ? 1 : 0.55 }" />
      </template>

      <text :x="W / 2" :y="H - 6" class="note">
        <template v-if="mode === 'rnn'">one running memory h, handed along &#183; each step must wait for the one before</template>
        <template v-else-if="mode === 'fade'">what is left of &#8220;{{ ws[focusI] }}&#8221; by the time we reach &#8220;{{ ws[queryI] }}&#8221; (illustration)</template>
        <template v-else>&#8220;{{ ws[queryI] }}&#8221; reaches every earlier word in ONE step &#8212; distance no longer matters</template>
      </text>
    </svg>
  </div>
</template>

<style scoped>
.rnn svg { width: 100%; max-height: 36vh; display: block; }
.rnn.is-compact svg { max-height: 28vh; }
text { text-anchor: middle; }
.word { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 19px; fill: var(--ann-ink); }
.word.focus { fill: var(--ann-ember); font-weight: 700; }
.word.query { fill: var(--qkv-query); font-weight: 700; }
.h { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 20px; font-weight: 600; fill: var(--ann-indigo); }
.h .sub { font-size: 13px; }
.stepno { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 12px; fill: var(--ann-muted); }
.note { font-family: 'JetBrains Mono', ui-monospace, monospace; font-size: 13px; fill: var(--ann-ink-soft); }
</style>
