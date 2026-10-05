---
layout: section
chapter: '4 · The encoder'
---

# Chapter 4

## The encoder

<div v-click class="thesis" style="margin-top:0.8em">Read the whole source sentence at once, let every word look at every other word, and do it six times.</div>

<!--
The encoder is the simpler tower: no mask, no cross-attention. If Part I
made sense, this chapter is mostly assembly.

Transition: "One block."
-->

---
chapter: '4 · The encoder'
clicks: 4
---

# One encoder block

<span class="eyebrow structure">Self-attention &#8594; Add &amp; Norm &#8594; Feed-forward &#8594; Add &amp; Norm</span>

<div class="encsplit">
  <div>

<EncDecMap :highlight="$clicks >= 3 ? ['enc-attn','enc-ffn','addnorm'] : $clicks >= 2 ? ['enc-ffn'] : $clicks >= 1 ? ['enc-attn'] : []" compact />

  </div>
  <div class="side">
    <div v-click="1" class="pt"><b>Multi-head self-attention.</b> Every source word gathers information from every other source word. Communication.</div>
    <div v-click="2" class="pt"><b>Feed-forward.</b> Each word, alone, through two matrices with a ReLU between. Computation.</div>
    <div v-click="3" class="pt"><b>Add &amp; Norm</b> after each: add the sub-layer&#8217;s input back (residual), then LayerNorm. The two pieces of plumbing from Part I chapter 7.</div>
    <div v-click="4" class="pt formula">out = LayerNorm( x + Sublayer(x) )</div>
  </div>
</div>

<style>
.encsplit { display: grid; grid-template-columns: 1.35fr 1fr; gap: 1.2em; align-items: center; }
.side { display: flex; flex-direction: column; gap: 0.6em; }
.pt { font-size: 0.85rem; color: var(--ann-ink-soft); line-height: 1.4; }
.pt b { color: var(--ann-indigo); }
.pt.formula { font-family: 'JetBrains Mono', monospace; font-size: 1rem; color: var(--ann-ink); text-align: center; padding: 0.4em; border: 1px solid var(--ann-line); border-radius: 0.4em; background: var(--ann-paper-raised); }
</style>

<!--
[click] Self-attention, multi-head, unmasked (next slide is about why no
mask).
[click] Feed-forward, per position.
[click] Add & Norm: this is exactly "residual then layer norm". The 2017 paper
puts the norm AFTER the addition ("post-norm"); modern models normalise
BEFORE each sub-layer instead ("pre-norm"), which trains more stably when
very deep. Mention once.
[click] The formula the paper writes for every sub-layer.

Transition: "Notice what is NOT here: a mask."
-->

---
chapter: '4 · The encoder'
clicks: 3
---

# No mask: the encoder reads in both directions

<span class="eyebrow attention">Bidirectional self-attention</span>

<div class="nomask">
  <div v-click="1">

<AttentionHeat stage="softmax" compact note="encoder: every cell filled — later words inform earlier ones" />

  </div>
  <div v-click="2">

<AttentionHeat stage="causal" compact />

  </div>
</div>

<div v-click="3" class="obs">
  <div>The encoder is not generating anything &#8212; the whole source sentence is given. There is no future to hide, so <b>every word may look at every word</b>, before and after it.</div>
  <div>That is why encoder representations are so good for understanding tasks: <i>bank</i> can be read in the light of <i>river</i> even when <i>river</i> comes later.</div>
</div>

<style>
.nomask { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2em; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.2em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Same worked example, two treatments.

[click] Left: full attention - what the encoder does.
[click] Right: the causal version - what the decoder (and every GPT) does.
Glass, being first, can only see itself.

[click] The reason. Masking exists to stop a model cheating at
next-token prediction. The encoder is not predicting the source; it is
reading it. BERT is an encoder-only model trained this way.

Transition: "Now the feed-forward, with its real size."
-->

---
chapter: '4 · The encoder'
clicks: 3
---

# The feed-forward widens 4&#215;, then shrinks back

<span class="eyebrow math">d<sub>model</sub> 512 &#8594; d<sub>ff</sub> 2048 &#8594; 512</span>

<ShapeTrace :stages="['encoder']" :highlight="$clicks >= 1 ? 6 : undefined" :up-to="$clicks >= 2 ? 99 : 6" />

<div v-click="3" class="obs">
  <div><b>FFN(x) = max(0, x W<sub>1</sub> + b<sub>1</sub>) W<sub>2</sub> + b<sub>2</sub></b>: widen to 2,048, zero the negatives, project back to 512. Applied to each of the 7 tokens separately, with the same weights.</div>
  <div>The wide middle is where capacity lives: per layer, the FFN holds <b>twice</b> as many numbers as the attention.</div>
</div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Every shape in this table was MEASURED by running a forward pass at the
paper's dimensions (scripts/verify-attention.py section 12), with the
7-token source "A cute teddy bear is reading .".

[click] The FFN hidden row: 7 x 2048. Four times wider.
[click] The rest of the encoder: everything else stays 7 x 512 - one row per
source token, all the way up.

[click] The formula and the parameter fact. Per layer: attention ~1.05M
numbers, FFN ~2.10M. That is Part I's "two thirds in the feed-forward".

Transition: "Stack it."
-->

---
chapter: '4 · The encoder'
clicks: 3
---

# Six times, then hand over

<span class="eyebrow structure">N = 6</span>

<div v-click="1" class="key-message">The encoder block is repeated <b>six</b> times, each with its own weights. Same shapes in, same shapes out: 7 &#215; 512 at every level.</div>

<div v-click="2" class="stack">
  <div class="lvl" v-for="i in 6" :key="i"><span>encoder block {{ 7 - i }}</span><span class="sh">7 &#215; 512</span></div>
</div>

<div v-click="3" class="obs">
  <div>The output is one vector per source token, each now <b>context-aware</b>: <i>bear</i> knows it is cute, teddy, and reading.</div>
  <div>The encoder&#8217;s job is done. These 7 vectors are handed to <b>every</b> decoder layer as the keys and values of cross-attention.</div>
</div>

<style>
.stack { display: flex; flex-direction: column; gap: 0.15em; margin: 0.4em auto; max-width: 22em; }
.lvl { display: flex; justify-content: space-between; padding: 0.2em 0.9em; border-radius: 0.35em; background: var(--ann-circuit-soft); border: 1px solid var(--ann-circuit); font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--ann-indigo); }
.lvl .sh { font-weight: 700; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
[click] N = 6 in the base model; 96 layers in GPT-3 for comparison.
[click] The stack. The shape never changes, which is what makes stacking
trivial - and what residuals rely on.
[click] The hand-off. Stress "every decoder layer": the same encoder output is
reused six times on the other side.

Transition: "Where we are."
-->

---
chapter: '4 · The encoder'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 4 &#183; takeaway</span>

<EncDecMap :highlight="['enc-embed','enc-attn','enc-ffn','enc-out']" compact />

<div v-click="1" class="recap">
  <div>Encoder block = <b>unmasked</b> multi-head self-attention + FFN (512&#8594;2048&#8594;512), each wrapped in <b>Add &amp; Norm</b>, &#215;6.</div>
  <div>Output: one context-aware 512-vector per source token &#8212; the <b>memory</b> the decoder will consult.</div>
</div>

<div v-click="2" class="transition-line">The left tower is complete. <span class="arrow">Chapter 5: the tower that writes.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Transition: "Chapter five: the decoder."
-->
