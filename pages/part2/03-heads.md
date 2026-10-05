---
layout: section
chapter: '3 · Many heads, with shapes'
---

# Chapter 3

## Many heads, with shapes

<div v-click class="thesis" style="margin-top:0.8em">One head asks one kind of question. Real sentences need several asked at once &#8212; and it costs no more than asking one.</div>

<!--
Part I's multi-head slide was qualitative. This chapter runs two heads on
the same three words from Part I's worked example, then scales the shapes up
to the 2017 base model.

Transition: "Same sentence, two heads."
-->

---
chapter: '3 · Many heads, with shapes'
clicks: 3
zoom: 0.95
---

# Same three words, two different questions

<span class="eyebrow attention">h = 2 on the Part I worked example</span>

<div class="heads2">
  <div v-click="1" class="hcol">
    <div class="hh">head 1 &#183; <span class="dim">the Part I head</span></div>

<AttentionHeat stage="softmax" :highlight-row="2" compact note="it → glass 0.85: 'which noun am I?'" />

  </div>
  <div v-click="2" class="hcol">
    <div class="hh">head 2 &#183; <span class="dim">different W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub></span></div>

<AttentionHeat stage="softmax" :matrix="N.multihead.head2.weights" compact note="everyone → dropped: 'what happened?'" />

  </div>
</div>

<div v-click="3" class="obs">
  <div><b>Same input X, same arithmetic</b>, different learned matrices &#8212; and a completely different pattern. Head 1 resolves the pronoun; head 2 sends every word to the verb.</div>
  <div>Neither head was told what to look for. Training found both because both reduce the loss.</div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.heads2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2em; }
.hh { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: var(--qkv-query); text-align: center; }
.hh .dim { color: var(--ann-muted); font-weight: 400; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.3em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Numbers: scripts/verify-attention.py section 8, cross-checked against
torch.nn.MultiheadAttention.

[click] Head 1 is exactly the Part I chapter 4 result: "it" puts 0.85 on
"glass".
[click] Head 2 uses different matrices (in the script as W_Q2, W_K2, W_V2).
Every row puts most of its weight on "dropped" - 0.80 for glass and it, 0.62
for dropped itself.

[click] The point: heads specialise because the matrices differ, and the
matrices differ because training pushed them apart. These two patterns are
hand-designed so they are easy to read; real heads are usually murkier, as
Part I warned.

Transition: "How do two heads fit in the same vector?"
-->

---
chapter: '3 · Many heads, with shapes'
clicks: 4
---

# Slice the vector, don't copy it

<span class="eyebrow math">d<sub>k</sub> = d<sub>model</sub> &#247; h</span>

<div v-click="1" class="key-message">Each head projects into a <b>smaller</b> space. Split d<sub>model</sub> between the heads and the total work stays the same as one big head.</div>

<div class="slices">
  <div v-click="2" class="sl"><span class="sn">worked example</span><span class="sv">d<sub>model</sub> 4 &#247; h 2 = <b>d<sub>k</sub> 2</b></span><span class="sd">each head&#8217;s W<sub>Q</sub> is 4&#215;2</span></div>
  <div v-click="3" class="sl"><span class="sn">2017 base model</span><span class="sv">512 &#247; 8 = <b>64</b></span><span class="sd">each head&#8217;s Q, K, V: n &#215; 64</span></div>
  <div v-click="3" class="sl"><span class="sn">GPT-3</span><span class="sv">12,288 &#247; 96 = <b>128</b></span><span class="sd">96 heads in each of 96 layers</span></div>
</div>

<div v-click="4" class="obs">
  <div>So &#8220;more heads&#8221; does not mean &#8220;more parameters&#8221;: W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub> are still d<sub>model</sub> &#215; d<sub>model</sub> in total, just cut into h slices.</div>
  <div>The √d<sub>k</sub> in the formula is the <b>per-head</b> width: √64 = 8 in the base model.</div>
</div>

<style>
.slices { display: flex; flex-direction: column; gap: 0.3em; margin: 0.5em 0; }
.sl { display: grid; grid-template-columns: 10em 13em 1fr; align-items: baseline; gap: 1em; padding: 0.35em 0.9em; border-radius: 0.45em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.sn { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--ann-muted); text-transform: uppercase; letter-spacing: 0.05em; }
.sv { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; }
.sv b { color: var(--qkv-query); }
.sd { font-size: 0.8rem; color: var(--ann-ink-soft); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
[click] The design choice that makes multi-head free.
[click] The worked example: 4 split into two heads of 2.
[click] The base model: 8 heads of 64. GPT-3: 96 of 128.
[click] Two consequences. Parameter count unchanged; and d_k in the scaling
factor is per head, which is easy to get wrong when reading code.

Transition: "Two heads, two answers. Now merge them."
-->

---
chapter: '3 · Many heads, with shapes'
clicks: 4
---

# Lay the answers side by side, then mix

<span class="eyebrow math">Concatenate, then W<sub>O</sub></span>

<div class="mhflow">
  <div v-click="1" class="mstep"><span class="ml">head 1 output</span><span class="mv">3 &#215; 2</span></div>
  <div v-click="1" class="mstep"><span class="ml">head 2 output</span><span class="mv">3 &#215; 2</span></div>
  <div v-click="2" class="mop">&#8594; concatenate &#8594;</div>
  <div v-click="2" class="mstep wide"><span class="ml">[ head 1 | head 2 ]</span><span class="mv">3 &#215; 4</span></div>
  <div v-click="3" class="mop">&#8594; &#215; W<sub>O</sub> (4&#215;4) &#8594;</div>
  <div v-click="3" class="mstep out"><span class="ml">multi-head output</span><span class="mv">3 &#215; 4</span></div>
</div>

<div v-click="3" class="calc-strip mrow">
  <span class="calc-chip"><span class="lbl">row &#8220;it&#8221; after concat</span>[ {{ N.multihead.concat[2].map(v => v.toFixed(2)).join(', ') }} ]</span>
  <span class="calc-op">&#8594;</span>
  <span class="calc-chip fwd"><span class="lbl">after W<sub>O</sub></span>[ {{ N.multihead.output[2].map(v => v.toFixed(2)).join(', ') }} ]</span>
</div>

<div v-click="4" class="obs">
  <div><b>W<sub>O</sub></b> is learned like everything else. It decides how the heads&#8217; findings combine, and it brings the result back to d<sub>model</sub> so the next layer gets the shape it expects.</div>
  <div>Like an image model running many filters over a picture and combining their maps: each head is a filter for one kind of relationship.</div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.mhflow { display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 0.5em; margin: 0.5em 0; }
.mstep { display: flex; flex-direction: column; align-items: center; padding: 0.4em 0.8em; border-radius: 0.45em; background: var(--qkv-query-soft); border: 1px solid var(--qkv-query); }
.mstep.wide { background: var(--ann-indigo-soft); border-color: var(--ann-indigo); }
.mstep.out { background: var(--ann-circuit-soft); border-color: var(--ann-circuit); }
.ml { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--ann-ink-soft); }
.mv { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; font-weight: 700; color: var(--ann-indigo); }
.mop { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--ann-muted); }
.mrow { justify-content: center; font-size: 0.85rem; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Numbers: scripts/verify-attention.py section 8; the multi-head output matches
torch.nn.MultiheadAttention to 1e-16.

[click] Two head outputs, each 3 x 2: one 2-number vector per word, per head.
[click] Concatenate along the feature axis: 3 x 4. The first two numbers in
each row are head 1's answer, the last two head 2's.
[click] Multiply by W_O. Read out the "it" row before and after. W_O mixes
the two heads' findings into every output dimension.

[click] Why W_O exists, and the CNN analogy for those who know it (Stanford
CME 295 makes the same comparison).

Formula, for the notes:
MultiHead(Q,K,V) = Concat(head_1, ..., head_h) W_O
where head_i = softmax(Q_i K_i^T / sqrt(d_k)) V_i.

Transition: "Where we are."
-->

---
chapter: '3 · Many heads, with shapes'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 3 &#183; takeaway</span>

<EncDecMap :highlight="['enc-attn','dec-mask','cross']" compact />

<div v-click="1" class="recap">
  <div><b>MultiHead = Concat(head<sub>1</sub>, &#8230;, head<sub>h</sub>) W<sub>O</sub></b>, each head running the Part I formula in its own d<sub>k</sub> = d<sub>model</sub>/h slice.</div>
  <div>Every attention box in both towers is multi-head: 8 heads of 64 in the base model.</div>
</div>

<div v-click="2" class="transition-line">We have every part. <span class="arrow">Chapter 4 assembles the left tower.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
All three attention boxes lit: self-attention in the encoder, masked
self-attention and cross-attention in the decoder. All three are multi-head.

Transition: "Chapter four: the encoder."
-->
