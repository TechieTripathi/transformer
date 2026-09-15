<!--
  TokenStrip - text partitioned into tokens.

  The deck's opening figure, and the static fallback for tiktokenizer if the
  hall has no network.

  THE ONE RULE: chunks butt together with ZERO gap, zero padding, zero border
  radius. The point of the picture is that the text is PARTITIONED - every
  character belongs to exactly one chunk and nothing is left over. Any gap
  invents whitespace that is not in the string, which is precisely the thing
  students then misunderstand about leading spaces.

  Whitespace is shown with glyph substitution, opt-in, because " the" being
  one token INCLUDING its leading space is the single most surprising fact on
  the slide:  space -> U+22C5 dot operator,  tab -> arrow,  newline -> \n.

  19 hues cycled by chunk index so adjacent chunks never collide. The colours
  carry NO meaning - they are a partition marker, nothing else - which is why
  they are pale and the text stays ink-black on top. Font size is 22px
  minimum: this is a panel the back row has to READ, not merely see.

  CLICK CONTRACT: none.
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  tokens: string[]
  ids?: number[]
  showWhitespace?: boolean
  showIds?: boolean
  caption?: string
  size?: number
}>(), { showWhitespace: true, showIds: false, size: 22 })

// tiktokenizer's palette: 19 Tailwind -200 steps, chosen so that no two
// adjacent chunks land on similar hues.
const HUES = [
  '#bae6fd', '#fde68a', '#bfdbfe', '#bbf7d0', '#fed7aa', '#a5f3fc', '#e5e7eb',
  '#e9d5ff', '#c7d2fe', '#d9f99d', '#fecdd3', '#ddd6fe', '#fef08a', '#a7f3d0',
  '#e4e4e7', '#fecaca', '#f5d0fe', '#fbcfe8', '#99f6e4',
]

const shown = computed(() => props.tokens.map((t, i) => ({
  raw: t,
  text: props.showWhitespace
    ? t.replace(/ /g, '⋅').replace(/\t/g, '→').replace(/\n/g, '\\n')
    : t,
  hue: HUES[i % HUES.length],
  id: props.ids?.[i],
})))
</script>

<template>
  <div class="tokwrap">
    <div class="tokpanel" :style="{ fontSize: size + 'px' }">
      <span v-for="(t, i) in shown" :key="i" class="tok" :style="{ background: t.hue }">{{ t.text }}</span>
    </div>

    <div class="meta">
      <span class="count"><b>{{ tokens.length }}</b> tokens</span>
      <span class="count"><b>{{ tokens.join('').length }}</b> characters</span>
    </div>

    <div v-if="showIds && ids" class="ids">{{ ids.join(', ') }}</div>
    <div v-if="caption" class="cap">{{ caption }}</div>
  </div>
</template>

<style scoped>
.tokwrap { margin: 0.4em 0; }

/* Pinned light in BOTH themes. The -200 pastels carry dark text and simply
   fail on a dark ground; a panel that changes legibility with the theme is
   worse than one that is consistently light. */
.tokpanel {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace;
  line-height: 1.65;
  white-space: pre-wrap;
  word-break: break-word;
  color: #111827;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 14px 16px;
}

/* No padding, no radius, no margin, no gap. Deliberate. */
.tok { border-radius: 0; }

.meta {
  display: flex;
  gap: 1.2em;
  margin-top: 0.45em;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.78rem;
  color: var(--ann-muted);
}
.meta b { color: var(--ann-indigo); }

.ids {
  margin-top: 0.4em;
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 0.76rem;
  color: var(--ann-ink-soft);
  word-break: break-all;
}

.cap { margin-top: 0.5em; font-size: 0.8rem; color: var(--ann-ink-soft); }
</style>
