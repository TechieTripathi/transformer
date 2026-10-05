<!--
  Timeline - "how we got here", from one-model-per-task to agents.

  Used twice: the opening of Part I (so the audience knows why this one
  architecture deserves two hours) and the opening of Part II (to place the
  2017 encoder-decoder, which Part I never drew, on the same line).

  The story it tells is the one Stanford CME 295 opens with: a decade of
  task-specific recurrent models, one architecture in 2017 that scaled, a
  product moment in 2022, and systems that act rather than chat.

  CLICK CONTRACT: none. `upTo` reveals events progressively if the slide
  wants to drive it from $clicks; `highlight` lights one event.

  BEWARE `opacity` AS AN ATTRIBUTE (UnoCSS attributify reads opacity="1" as
  1%). Every opacity here is set through :style.

  PROPS
    events     override the default list ({ when, label, sub })
    highlight  index of the event to light (teal ring)
    upTo       show events 0..upTo, dim the rest. Default: all.
    compact    shorter
-->

<script setup lang="ts">
import { computed } from 'vue'

type Ev = { when: string, label: string, sub: string }

const props = withDefaults(defineProps<{
  events?: Ev[]
  highlight?: number
  upTo?: number
  compact?: boolean
}>(), { compact: false })

const DEFAULT: Ev[] = [
  { when: '2010s',   label: 'One model per job',   sub: 'RNNs: a translator, a sentiment model, a tagger…' },
  { when: '2014',    label: 'Attention added', sub: 'RNN translators learn to look back at the source' },
  { when: '2017',    label: 'The Transformer',      sub: '“Attention Is All You Need” — drop the recurrence' },
  { when: '2018–20', label: 'Scale it up',          sub: 'BERT, GPT-2, GPT-3: same idea, more data and compute' },
  { when: '2022',    label: 'ChatGPT',              sub: 'one general model you simply talk to' },
  { when: 'now',     label: 'Agents',               sub: 'models that plan, call tools and act' },
]

const evs = computed(() => props.events ?? DEFAULT)
const last = computed(() => props.upTo ?? evs.value.length - 1)

const W = 920
const H = computed(() => (props.compact ? 150 : 178))
const Y = 56
const PAD = 84
const xOf = (i: number) => PAD + i * ((W - 2 * PAD) / Math.max(evs.value.length - 1, 1))
const shown = (i: number) => i <= last.value
</script>

<template>
  <div class="timeline" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">
      <line :x1="PAD - 30" :y1="Y" :x2="W - PAD + 30" :y2="Y"
            stroke="var(--ann-line)" stroke-width="3" stroke-linecap="round" />

      <g v-for="(e, i) in evs" :key="e.when + e.label" :style="{ opacity: shown(i) ? 1 : 0.18 }">
        <circle :cx="xOf(i)" :cy="Y" :r="highlight === i ? 13 : 9"
                :fill="highlight === i ? 'var(--ann-circuit)' : 'var(--ann-paper-raised)'"
                :stroke="highlight === i ? 'var(--ann-circuit)' : 'var(--ann-indigo)'"
                stroke-width="3" />
        <text :x="xOf(i)" :y="Y - 22" class="when" :class="{ lit: highlight === i }">{{ e.when }}</text>
        <text :x="xOf(i)" :y="Y + 36" class="lbl" :class="{ lit: highlight === i }">{{ e.label }}</text>
        <foreignObject :x="xOf(i) - 72" :y="Y + 46" width="144" height="80">
          <div xmlns="http://www.w3.org/1999/xhtml" class="sub">{{ e.sub }}</div>
        </foreignObject>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.timeline svg { width: 100%; max-height: 34vh; display: block; }
.timeline.is-compact svg { max-height: 28vh; }
text { text-anchor: middle; }
.when {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 15px; font-weight: 600; fill: var(--ann-indigo);
}
.lbl {
  font-family: 'Space Grotesk', ui-sans-serif, sans-serif;
  font-size: 15px; font-weight: 700; fill: var(--ann-ink);
}
.lit { fill: var(--ann-circuit); }
.sub {
  font-family: 'Inter', ui-sans-serif, sans-serif;
  font-size: 12px; line-height: 1.3; text-align: center; color: var(--ann-ink-soft);
}
</style>
