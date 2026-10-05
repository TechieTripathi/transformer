<!--
  EncDecMap - the original 2017 Transformer: an encoder and a decoder.

  Part II's equivalent of PipelineMap, with the same contract, so a student
  re-orients by recognising one fixed picture with a moving highlight:

    highlight   key or array of keys to light. [] = all at full strength.
    pending     key drawn as NOT BUILT YET (dashed ember, "next").
    dimOthers   false = everything at full strength.
    compact     shorter.

  Keys:  src  enc-embed  enc-attn  enc-ffn  enc-out
         tgt  dec-embed  dec-mask  cross    dec-ffn  linear  softmax
         addnorm (lights every Add & Norm bar at once)

  Part I's deck is decoder-only - the right-hand column minus its middle
  box. That is the single sentence this picture exists to make visible.

  CLICK CONTRACT: none.  Opacity only via :style (UnoCSS attributify trap).
-->

<script setup lang="ts">
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  highlight?: string | string[]
  pending?: string
  dimOthers?: boolean
  compact?: boolean
}>(), { highlight: () => [], pending: '', dimOthers: true, compact: false })

type Chip = { key: string, label: string, x: number, y: number, w: number, h: number, thin?: boolean }

const EX = 90, DX = 430, CW = 230, CH = 32, AN = 14

const CHIPS: Chip[] = [
  // encoder
  { key: 'enc-embed', label: 'embedding + position', x: EX, y: 338, w: CW, h: 30 },
  { key: 'enc-attn',  label: 'Self-attention',        x: EX, y: 274, w: CW, h: CH },
  { key: 'addnorm',   label: 'Add & Norm',            x: EX, y: 252, w: CW, h: AN, thin: true },
  { key: 'enc-ffn',   label: 'Feed-forward',          x: EX, y: 212, w: CW, h: CH },
  { key: 'addnorm',   label: 'Add & Norm',            x: EX, y: 190, w: CW, h: AN, thin: true },
  { key: 'enc-out',   label: 'encoder output',        x: EX, y: 128, w: CW, h: 30 },
  // decoder
  { key: 'dec-embed', label: 'embedding + position',  x: DX, y: 338, w: CW, h: 30 },
  { key: 'dec-mask',  label: 'Masked self-attention', x: DX, y: 274, w: CW, h: CH },
  { key: 'addnorm',   label: 'Add & Norm',            x: DX, y: 252, w: CW, h: AN, thin: true },
  { key: 'cross',     label: 'Cross-attention',       x: DX, y: 212, w: CW, h: CH },
  { key: 'addnorm',   label: 'Add & Norm',            x: DX, y: 190, w: CW, h: AN, thin: true },
  { key: 'dec-ffn',   label: 'Feed-forward',          x: DX, y: 150, w: CW, h: CH },
  { key: 'addnorm',   label: 'Add & Norm',            x: DX, y: 128, w: CW, h: AN, thin: true },
  { key: 'linear',    label: 'Linear → vocabulary',   x: DX, y: 72,  w: CW, h: 30 },
  { key: 'softmax',   label: 'Softmax → next token',  x: DX, y: 30,  w: CW, h: 30 },
]

const W = 760
const H = 410

const active = computed(() => {
  const h = props.highlight
  return new Set(Array.isArray(h) ? h : h ? [h] : [])
})
const isOn = (k: string) =>
  !props.dimOthers || active.value.size === 0 || active.value.has(k) || k === props.pending
  || (k === 'src' && active.value.has('enc-embed')) || (k === 'tgt' && active.value.has('dec-embed'))
const isLit = (k: string) => active.value.has(k)
const isPending = (k: string) => k === props.pending
</script>

<template>
  <div class="encdec" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <marker id="ed-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L7,3 L0,6 z" fill="var(--ann-muted)" />
        </marker>
        <marker id="ed-arrow-k" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto" markerUnits="strokeWidth">
          <path d="M0,0 L7,3 L0,6 z" fill="var(--qkv-key)" />
        </marker>
      </defs>

      <!-- block boxes -->
      <rect :x="EX - 12" y="180" :width="CW + 24" height="136" rx="10" fill="none"
            stroke="var(--ann-indigo)" stroke-width="1.5" stroke-dasharray="5 4" :style="{ opacity: 0.6 }" />
      <text :x="EX - 22" y="252" class="rep end">× N</text>
      <rect :x="DX - 12" y="118" :width="CW + 24" height="198" rx="10" fill="none"
            stroke="var(--ann-indigo)" stroke-width="1.5" stroke-dasharray="5 4" :style="{ opacity: 0.6 }" />
      <text :x="DX + CW + 22" y="300" class="rep start">× N</text>

      <text :x="EX + CW / 2" y="16" class="colhdr">ENCODER &#183; reads the source</text>
      <text :x="DX + CW / 2" y="16" class="colhdr">DECODER &#183; writes the target</text>

      <!-- spines -->
      <line :x1="EX + CW / 2" y1="336" :x2="EX + CW / 2" y2="161" stroke="var(--ann-muted)" stroke-width="1.5"
            marker-end="url(#ed-arrow)" :style="{ opacity: 0.6 }" />
      <line :x1="DX + CW / 2" y1="336" :x2="DX + CW / 2" y2="63" stroke="var(--ann-muted)" stroke-width="1.5"
            marker-end="url(#ed-arrow)" :style="{ opacity: 0.6 }" />

      <!-- the bridge: encoder output feeds K and V of every cross-attention -->
      <path :d="`M ${EX + CW} 143 L ${(EX + CW + DX) / 2} 143 L ${(EX + CW + DX) / 2} 228 L ${DX - 3} 228`"
            fill="none" stroke="var(--qkv-key)" stroke-width="2.5" marker-end="url(#ed-arrow-k)"
            :style="{ opacity: isOn('cross') || isOn('enc-out') ? 1 : 0.35 }" />
      <text :x="(EX + CW + DX) / 2 + 6" y="190" class="bridge start"
            :style="{ opacity: isOn('cross') || isOn('enc-out') ? 1 : 0.35 }">K, V</text>

      <g v-for="(c, i) in CHIPS" :key="i">
        <rect :x="c.x" :y="c.y" :width="c.w" :height="c.h" :rx="c.thin ? 4 : 7"
              :fill="isLit(c.key) ? 'var(--ann-circuit-soft)' : c.thin ? 'var(--ann-indigo-soft)' : 'var(--ann-paper-raised)'"
              :stroke="isLit(c.key) ? 'var(--ann-circuit)' : isPending(c.key) ? 'var(--ann-ember)' : 'var(--ann-line)'"
              :stroke-width="isLit(c.key) || isPending(c.key) ? 2.5 : 1"
              :stroke-dasharray="isPending(c.key) ? '6 4' : undefined"
              :style="{ opacity: isOn(c.key) ? 1 : 0.4 }" />
        <text :x="c.x + c.w / 2" :y="c.y + c.h / 2 + (c.thin ? 4 : 5)" class="lbl"
              :class="{ thin: c.thin, lit: isLit(c.key), pending: isPending(c.key) }"
              :style="{ opacity: isOn(c.key) ? 1 : 0.4 }">{{ c.label }}</text>
        <text v-if="isPending(c.key) && !c.thin" :x="c.x + c.w + 8" :y="c.y + c.h / 2 + 4" class="nextlbl start">&#8592; next</text>
      </g>

      <text :x="EX + CW / 2" y="392" class="tok" :style="{ opacity: isOn('src') ? 1 : 0.4 }">source tokens: A cute teddy bear …</text>
      <text :x="DX + CW / 2" y="392" class="tok" :style="{ opacity: isOn('tgt') ? 1 : 0.4 }">&lt;BOS&gt; + target so far: Un ours …</text>
    </svg>
  </div>
</template>

<style scoped>
.encdec svg { width: 100%; max-height: 58vh; display: block; margin: 0 auto; }
.encdec.is-compact svg { max-height: 35vh; }
text { text-anchor: middle; }
.start { text-anchor: start; }
.end { text-anchor: end; }
.lbl { font-family: 'Space Grotesk', ui-sans-serif, sans-serif; font-size: 15px; font-weight: 600; fill: var(--ann-ink); }
.lbl.thin { font-family: 'JetBrains Mono', monospace; font-size: 10px; font-weight: 500; fill: var(--ann-indigo); }
.lbl.lit { fill: var(--ann-circuit); }
.lbl.pending { fill: var(--ann-ember); }
.colhdr { font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 0.08em; font-weight: 600; fill: var(--ann-indigo); }
.rep { font-family: 'JetBrains Mono', monospace; font-size: 15px; font-weight: 700; fill: var(--ann-indigo); }
.bridge { font-family: 'JetBrains Mono', monospace; font-size: 13px; font-weight: 700; fill: var(--qkv-key); }
.tok { font-family: 'JetBrains Mono', monospace; font-size: 12px; fill: var(--ann-ink-soft); }
.nextlbl { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; fill: var(--ann-ember); }
</style>
