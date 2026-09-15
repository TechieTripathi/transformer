<!--
  SpotlightSentence - one sentence, with how much each word is attended to.

  THE REPAIR IS BUILT INTO THE COMPONENT.
  The source draft leans on "attention is like a spotlight". A spotlight is
  SELECTIVE: it lights one thing and leaves the rest of the stage dark. Real
  attention does the opposite - softmax output is never zero, so every single
  word keeps a share. That is the most damaging misconception in the subject,
  and a component that dimmed the low-weight words to nothing would teach it
  on every slide it appeared on.

  So: no word is ever drawn at zero. Every word keeps a visible bar and
  readable text, and the weakest still shows its number. The query word is
  ember (it is the one asking); every other word is teal at an opacity
  floored well above zero (they are the ones being read).

  CLICK CONTRACT: none.
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  words: string[]
  weights?: number[]
  query?: number
  note?: string
}>(), {})

const maxW = computed(() => Math.max(...(props.weights ?? [1]), 1e-9))

const cells = computed(() => props.words.map((w, i) => {
  const val = props.weights?.[i] ?? 0
  return {
    word: w,
    val,
    isQuery: props.query === i,
    // floored at 0.22: never invisible, because nothing is ever zero
    strength: 0.22 + (val / maxW.value) * 0.78,
    pct: (val / maxW.value) * 100,
  }
}))
</script>

<template>
  <div class="spot">
    <div class="line">
      <div v-for="(c, i) in cells" :key="i" class="cell" :class="{ q: c.isQuery }">
        <span class="w" :style="c.isQuery ? undefined : { opacity: c.strength }">{{ c.word }}</span>
        <template v-if="!c.isQuery">
          <span class="bar"><span class="fill" :style="{ width: c.pct + '%' }" /></span>
          <span class="n">{{ c.val.toFixed(2) }}</span>
        </template>
        <span v-else class="asking">asking</span>
      </div>
    </div>
    <div v-if="note" class="note">{{ note }}</div>
  </div>
</template>

<style scoped>
.spot { margin: 0.5em 0; }

.line {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-end;
  gap: 0.5em;
}

.cell {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  min-width: 3.4em;
}

.w {
  font-family: 'Space Grotesk', ui-sans-serif, sans-serif;
  font-size: 1.32rem;
  font-weight: 600;
  color: var(--ann-circuit);
  line-height: 1.2;
}

.cell.q .w {
  color: var(--ann-ember);
  border-bottom: 3px solid var(--ann-ember);
  padding-bottom: 1px;
}

.bar {
  display: block;
  width: 100%;
  height: 9px;
  background: var(--ann-paper-raised);
  border: 1px solid var(--ann-line);
  border-radius: 2px;
  overflow: hidden;
}
.fill {
  display: block;
  height: 100%;
  background: var(--ann-circuit);
  border-radius: 0 3px 3px 0;
}
.cell.q .fill { background: var(--ann-ember); }

.n {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
  font-size: 0.72rem;
  color: var(--ann-ink-soft);
}

.asking {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: var(--ann-ember);
  padding-top: 11px;
}

.note {
  margin-top: 0.7em;
  font-size: 0.84rem;
  color: var(--ann-ink-soft);
}
</style>
