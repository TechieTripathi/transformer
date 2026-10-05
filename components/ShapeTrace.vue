<!--
  ShapeTrace - every tensor in the original base Transformer, with its shape.

  Numbers come from composables/useDeckNumbers.ts (N.base.trace). Those
  shapes were MEASURED by scripts/verify-attention.py section 12, which runs
  a real forward pass at d_model = 512, h = 8, d_ff = 2048, N = 6 on a
  7-token source and 8-position target. IF A SHAPE HERE DISAGREES, THIS FILE
  IS WRONG.

  CLICK CONTRACT: none.
    stages     only rows whose stage contains one of these strings
               (e.g. ['encoder'] or ['cross']). Default: all.
    upTo       rows after this index are drawn faint (for progressive build)
    highlight  index (within the filtered rows) to ring in ember
-->

<script setup lang="ts">
import { computed } from 'vue'
import { N } from '../composables/useDeckNumbers'

const props = withDefaults(defineProps<{
  stages?: string[]
  upTo?: number
  highlight?: number
  compact?: boolean
}>(), { compact: false })

type Row = { stage: string, tensor: string, shape: number[], note: string }
const all = N.base.trace as unknown as Row[]

const rows = computed(() => all.filter(r => !props.stages || props.stages.some(s => r.stage.includes(s))))
const fmt = (shape: number[]) => shape.map(s => s.toLocaleString('en-US')).join(' × ')
const tone = (stage: string) =>
  stage.includes('cross') ? 'cross' : stage.includes('decoder') ? 'dec' : stage.includes('output') ? 'out' : 'enc'
</script>

<template>
  <table class="shapes" :class="{ 'is-compact': compact }">
    <thead><tr><th>where</th><th>tensor</th><th>shape</th><th>read it as</th></tr></thead>
    <tbody>
      <tr v-for="(r, i) in rows" :key="r.stage + r.tensor"
          :class="[tone(r.stage), { lit: highlight === i }]"
          :style="{ opacity: upTo === undefined || i <= upTo ? 1 : 0.22 }">
        <td class="st">{{ r.stage }}</td>
        <td>{{ r.tensor }}</td>
        <td class="sh">{{ fmt(r.shape) }}</td>
        <td class="nt">{{ r.note }}</td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.slidev-layout table.shapes { font-size: 0.8rem; }
.slidev-layout table.shapes.is-compact { font-size: 0.72rem; }
.slidev-layout table.shapes td { padding: 0.22em 0.6em; }
.slidev-layout table.shapes th { padding: 0.3em 0.6em; }
.st { font-family: 'JetBrains Mono', monospace; font-size: 0.85em; color: var(--ann-muted); white-space: nowrap; }
.sh { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--ann-indigo); white-space: nowrap; font-variant-numeric: tabular-nums; }
.nt { color: var(--ann-ink-soft); font-size: 0.9em; }
tr.enc td:first-child { border-left: 4px solid var(--ann-circuit); }
tr.dec td:first-child { border-left: 4px solid var(--qkv-query); }
tr.cross td:first-child { border-left: 4px solid var(--qkv-key); }
tr.out td:first-child { border-left: 4px solid var(--ann-ember); }
tr.lit td { background: var(--ann-ember-soft); }
</style>
