<!--
  VectorMap - words as points in space, and the arithmetic you can do on them.

  The cluster picture: similar words land near each other.

  A WARNING WORTH KNOWING. Schluter (NAACL 2018) showed that a 2-D projection
  of this kind can be made to look convincing almost regardless of whether the
  relation really holds - if the two groups cluster at all, the projection will
  hand you the picture you wanted. So this is used for INTUITION only, and the
  deck says so out loud: chapter 8 comes back and shows that the famous
  king - man + woman demo depends on the search being forbidden to return its
  own inputs.

  CLICK CONTRACT: none.
-->

<script setup lang="ts">
type Pt = { label: string, x: number, y: number, group?: string }

const props = withDefaults(defineProps<{
  points?: Pt[]
  axes?: [string, string]
  compact?: boolean
}>(), {
  axes: () => ['vehicles → animals', 'small → large'],
  points: () => ([
    { label: 'cat',    x: 0.74, y: 0.30, group: 'animal' },
    { label: 'dog',    x: 0.82, y: 0.42, group: 'animal' },
    { label: 'horse',  x: 0.88, y: 0.72, group: 'animal' },
    { label: 'mouse',  x: 0.68, y: 0.14, group: 'animal' },
    { label: 'bike',   x: 0.16, y: 0.22, group: 'vehicle' },
    { label: 'car',    x: 0.24, y: 0.48, group: 'vehicle' },
    { label: 'bus',    x: 0.30, y: 0.76, group: 'vehicle' },
    { label: 'truck',  x: 0.20, y: 0.84, group: 'vehicle' },
  ]),
  compact: false,
})

const W = 620
const H = 340
const PAD = 46
const px = (x: number) => PAD + x * (W - 2 * PAD)
const py = (y: number) => H - PAD - y * (H - 2 * PAD)

const colourOf = (g?: string) =>
  g === 'animal' ? 'var(--ann-ember)'
  : g === 'vehicle' ? 'var(--ann-circuit)'
  : 'var(--ann-indigo)'
</script>

<template>
  <div class="vmap" :class="{ 'is-compact': compact }">
    <svg :viewBox="`0 0 ${W} ${H}`" xmlns="http://www.w3.org/2000/svg">

      <line :x1="PAD - 12" :y1="H - PAD" :x2="W - PAD + 12" :y2="H - PAD"
            stroke="var(--ann-line)" stroke-width="1.5" />
      <line :x1="PAD - 12" :y1="H - PAD" :x2="PAD - 12" :y2="PAD - 12"
            stroke="var(--ann-line)" stroke-width="1.5" />
      <text :x="W / 2" :y="H - 12" class="axis">{{ axes[0] }}</text>
      <text :x="16" :y="H / 2" class="axis" :transform="`rotate(-90 16 ${H / 2})`">{{ axes[1] }}</text>

      <g v-for="p in points" :key="p.label">
        <circle :cx="px(p.x)" :cy="py(p.y)" r="7" :fill="colourOf(p.group)" />
        <text :x="px(p.x) + 12" :y="py(p.y) + 5" class="lbl" :fill="colourOf(p.group)">{{ p.label }}</text>
      </g>
    </svg>
  </div>
</template>

<style scoped>
.vmap svg { width: 100%; max-height: 42vh; display: block; margin: 0 auto; }
.vmap.is-compact svg { max-height: 32vh; }

.lbl {
  font-family: 'Space Grotesk', ui-sans-serif, sans-serif;
  font-size: 16px;
  font-weight: 600;
}
.axis {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-size: 11px;
  letter-spacing: 0.07em;
  fill: var(--ann-muted);
  text-anchor: middle;
}
</style>
