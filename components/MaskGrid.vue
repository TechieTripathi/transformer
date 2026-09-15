<!--
  MaskGrid - the causal mask, drawn as a picture of a RULE.

  This is the figure that answers the question every student asks: "if it can
  see the whole sentence at once, how is predicting the next word not
  cheating?" It is worth more than any learned-attention heatmap precisely
  because there is nothing to hand-wave - no training, no weights, no
  interpretation. Row i may look at columns 0..i. That is the whole picture.

  THREE DELIBERATE DEPARTURES from the figure everyone copies (the Annotated
  Transformer's 20x20 viridis imshow):

  1. 8 rows, not 20. At 20x20 each cell is under 2% of image height and the
     back row sees grey mush.
  2. TWO DISCRETE COLOURS, not a continuous colormap. The mask is BOOLEAN.
     A gradient implies degrees of maskedness, which do not exist.
  3. Real words on both axes, not integers. "sleeping may look at The, cat,
     is, sleeping" is a sentence a student can read off the picture;
     "row 3, columns 0-3" is not.

  CLICK CONTRACT: none.

  BEWARE `opacity` AS AN ATTRIBUTE.
  Slidev runs UnoCSS with the attributify preset, which reads bare HTML
  attributes as utility classes. `opacity="1"` is therefore parsed as the
  utility `opacity-1`, and on the Tailwind scale that means ONE PER CENT - so
  a fully opaque element renders invisible, and only when the value is exactly
  1. Every opacity here is set through `:style` for that reason. Do not
  "simplify" it back to an attribute.
 `revealRows` draws only the first N rows so a slide
  can build the staircase across its own v-clicks, or across v-switch.
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  words?: string[]
  compact?: boolean
}>(), {
  words: () => ['The', 'cat', 'is', 'sleeping', 'on', 'the', 'warm', 'mat'],
  compact: false,
})

const n = computed(() => props.words.length)

const CELL = 46
const LEFT = 118
const TOP = 78
const W = computed(() => LEFT + n.value * CELL + 20)
const H = computed(() => TOP + n.value * CELL + 30)
</script>

<template>
  <div class="mask" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">
      <text :x="LEFT + (n * CELL) / 2" :y="20" class="axis">
        &#8230; is allowed to look at these words
      </text>

      <g v-for="(w, c) in words" :key="'h' + c">
        <text :x="LEFT + c * CELL + CELL / 2" :y="TOP - 12" class="word"
              :transform="`rotate(-42 ${LEFT + c * CELL + CELL / 2} ${TOP - 12})`">{{ w }}</text>
      </g>

      <text :x="20" :y="TOP + (n * CELL) / 2" class="axis"
            :transform="`rotate(-90 20 ${TOP + (n * CELL) / 2})`">when predicting this word &#8230;</text>

      <g v-for="(w, r) in words" :key="'r' + r">
        <template>
          <text :x="LEFT - 12" :y="TOP + r * CELL + CELL / 2 + 5" class="word end">{{ w }}</text>
          <g v-for="(_, c) in words" :key="'c' + c">
            <rect :x="LEFT + c * CELL" :y="TOP + r * CELL" :width="CELL - 2" :height="CELL - 2"
                  rx="3"
                  :fill="c <= r ? 'var(--ann-circuit)' : 'var(--ann-ember-soft)'"
                  :style="{ opacity: c <= r ? 0.85 : 1 }"
                  :stroke="c <= r ? 'var(--ann-circuit)' : 'var(--ann-ember)'"
                  stroke-width="1.5" />
            <text :x="LEFT + c * CELL + (CELL - 2) / 2" :y="TOP + r * CELL + (CELL - 2) / 2 + 6"
                  class="glyph" :class="c <= r ? 'yes' : 'no'">{{ c <= r ? '✓' : '✕' }}</text>
          </g>
        </template>
      </g>

      <text :x="W / 2" :y="H - 8" class="note">
        It can look backward. It cannot look forward &#8212; because forward is the answer.
      </text>
    </svg>
  </div>
</template>

<style scoped>
.mask svg { width: 100%; max-height: 50vh; display: block; margin: 0 auto; }
.mask.is-compact svg { max-height: 38vh; }

text { text-anchor: middle; }

.word {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 14px;
  fill: var(--ann-ink);
}
.word.end { text-anchor: end; }

.axis {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11.5px;
  letter-spacing: 0.07em;
  fill: var(--ann-muted);
}

.glyph { font-size: 20px; font-weight: 700; }
.glyph.yes { fill: var(--ann-paper); }
.glyph.no { fill: var(--ann-ember); }

.note {
  font-family: 'Space Grotesk', ui-sans-serif, sans-serif;
  font-size: 13px;
  fill: var(--ann-ink-soft);
}
</style>
