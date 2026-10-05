---
layout: section
chapter: '5 · The decoder'
---

# Chapter 5

## The decoder

<div v-click class="thesis" style="margin-top:0.8em">Write one word at a time, never peek ahead &#8212; and before every word, go back and consult the source.</div>

<!--
The decoder is Part I's whole machine plus one box. Most of this chapter is
recognition; the new idea is cross-attention.

Transition: "It has to start somewhere."
-->

---
chapter: '5 · The decoder'
clicks: 3
---

# Start from &lt;BOS&gt;

<span class="eyebrow generation">The first input is a signal, not a word</span>

<div v-click="1" class="key-message">Before a single French word exists, the decoder still needs an input. It gets the special token <code>&lt;BOS&gt;</code> &#8212; &#8220;a sequence begins here&#8221; &#8212; with its embedding and position 0.</div>

<div v-click="2" class="steps">
  <div class="st"><span class="si">step 1 input</span><span class="sv">&lt;BOS&gt;</span><span class="so">&#8594; Un</span></div>
  <div class="st"><span class="si">step 2 input</span><span class="sv">&lt;BOS&gt; Un</span><span class="so">&#8594; ours</span></div>
  <div class="st"><span class="si">step 3 input</span><span class="sv">&lt;BOS&gt; Un ours</span><span class="so">&#8594; en</span></div>
  <div class="st dots"><span class="si">&#8942;</span></div>
</div>

<div v-click="3" class="obs">
  <div>Exactly Part I&#8217;s generation loop. The decoder&#8217;s input is <b>everything it has written so far</b>, beginning with <code>&lt;BOS&gt;</code>.</div>
</div>

<style>
.steps { display: flex; flex-direction: column; gap: 0.25em; margin: 0.4em 0; max-width: 32em; }
.st { display: grid; grid-template-columns: 7.5em 1fr 6em; align-items: baseline; gap: 1em; }
.si { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--ann-muted); text-transform: uppercase; }
.sv { font-family: 'JetBrains Mono', monospace; font-size: 1.1rem; color: var(--ann-indigo); font-variant-ligatures: none; }
.so { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--ann-ember); font-size: 1.1rem; }
.st.dots .si { color: var(--ann-muted); }
.obs { margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code, .key-message code { font-variant-ligatures: none; }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
[click] <BOS>, from Part I chapter 1's special-tokens slide, finally doing
its job.
[click] The loop. Each step's output is appended to the next step's input.
[click] Callback to Part I chapter 5.

Transition: "First sub-layer: attention over what has been written."
-->

---
chapter: '5 · The decoder'
clicks: 3
---

# Masked self-attention: look back, never ahead

<span class="eyebrow attention">Sub-layer 1</span>

<div class="mgrid">
  <div v-click="1">

<AttentionHeat stage="causal" compact />

  </div>
  <div class="side">
    <div v-click="1" class="pt">Same mechanism as the encoder, with the <b>causal mask</b>: scores for later positions set to &#8722;&#8734; before softmax, so they get exactly 0.</div>
    <div v-click="2" class="pt">Why it matters in <b>training</b>: the whole French sentence is fed in at once (&#8220;teacher forcing&#8221;), and without the mask position 2 could simply read the answer at position 3.</div>
    <div v-click="3" class="pt">Why it is harmless at <b>inference</b>: later positions do not exist yet anyway. The mask makes training match the way the model will be used.</div>
  </div>
</div>

<style>
.mgrid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.3em; align-items: center; }
.side { display: flex; flex-direction: column; gap: 0.6em; }
.pt { font-size: 0.86rem; color: var(--ann-ink-soft); line-height: 1.4; }
.pt b { color: var(--ann-indigo); }
</style>

<!--
[click] Part I chapter 7's mask, with the worked-example numbers.
[click] Teacher forcing: during training the decoder sees the true target,
shifted right by one (that is what <BOS> is for), and predicts every next
token in parallel. The mask is what makes that parallel training honest.
[click] At inference, the mask changes nothing - and that equivalence is also
what makes the KV cache safe (Part I).

Transition: "Second sub-layer - the new one."
-->

---
chapter: '5 · The decoder'
clicks: 4
---

# Cross-attention: ask the encoder

<span class="eyebrow attention">Sub-layer 2 &#183; the bridge between the towers</span>

<div class="xsplit">
  <div>

<EncDecMap :highlight="['cross','enc-out']" compact />

  </div>
  <div class="side">
    <div v-click="1" class="role q"><b>Queries</b> from the <b>decoder</b>: &#8220;given what I have written, what do I need from the source?&#8221;</div>
    <div v-click="2" class="role k"><b>Keys</b> from the <b>encoder</b> output: what each source word offers.</div>
    <div v-click="2" class="role v"><b>Values</b> from the <b>encoder</b> output: what each source word passes on.</div>
    <div v-click="3" class="pt">Same formula as self-attention. Only the <b>source</b> of Q versus K, V changes &#8212; so the score matrix is <b>decoder length &#215; encoder length</b>, not square.</div>
    <div v-click="4" class="pt">This is the 2014 idea from chapter 1, rebuilt out of Transformer parts.</div>
  </div>
</div>

<style>
.xsplit { display: grid; grid-template-columns: 1.3fr 1fr; gap: 1.1em; align-items: center; }
.side { display: flex; flex-direction: column; gap: 0.45em; }
.role { font-size: 0.82rem; padding: 0.35em 0.7em; border-radius: 0.4em; color: var(--ann-ink-soft); }
.role.q { background: var(--qkv-query-soft); border-left: 4px solid var(--qkv-query); }
.role.k { background: var(--qkv-key-soft); border-left: 4px solid var(--qkv-key); }
.role.v { background: var(--qkv-value-soft); border-left: 4px solid var(--qkv-value); }
.role.q b { color: var(--qkv-query); }
.role.k b { color: var(--qkv-key); }
.role.v b { color: var(--qkv-value); }
.pt { font-size: 0.82rem; color: var(--ann-ink-soft); line-height: 1.4; }
.pt b { color: var(--ann-indigo); }
</style>

<!--
The single most important new idea in Part II.

[click] Queries: from the decoder's current representations.
[click] Keys and values: from the final encoder output - the same 7 vectors,
reused by all six decoder layers.
[click] Shape consequence. In the base-model walkthrough: 8 decoder positions
x 7 source tokens per head.
[click] Lineage: Bahdanau attention, now multi-head and with no RNN.

Likely question: "Why not just concatenate source and target and use
self-attention?" Answer: "You can - that's roughly what decoder-only models
do with a prompt. The encoder-decoder split lets the source be read
bidirectionally and encoded once."

Transition: "Let's compute one."
-->

---
chapter: '5 · The decoder'
clicks: 3
---

# Cross-attention, by hand

<span class="eyebrow math">Decoder has written &#8220;&lt;BOS&gt; le&#8221; &#183; encoder read &#8220;the cat sleeps&#8221;</span>

<div class="xhand">
  <div v-click="1">

<AttentionHeat stage="raw" :matrix="N.crossattn.scores" :row-labels="[...N.crossattn.decTokens]" :col-labels="[...N.crossattn.encTokens]" compact note="raw scores q · k   (2 decoder rows × 3 encoder columns)" />

  </div>
  <div v-click="2">

<AttentionHeat stage="softmax" :matrix="N.crossattn.weights" :row-labels="[...N.crossattn.decTokens]" :col-labels="[...N.crossattn.encTokens]" :highlight-row="1" compact note="after ÷√2 and softmax — every row sums to 1" />

  </div>
</div>

<div v-click="3" class="obs">
  <div>Having written <i>le</i>, the decoder puts <b>{{ Math.round(N.crossattn.weights[1][1] * 100) }}%</b> of its attention on <i>cat</i> &#8212; exactly the word it must translate next (<i>chat</i>). At <code>&lt;BOS&gt;</code> it looked mostly at <i>the</i>.</div>
  <div>A rectangle, not a square: 2 things written so far, 3 source words available.</div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.xhand { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2em; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.2em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-variant-ligatures: none; }
</style>

<!--
Numbers: scripts/verify-attention.py section 9, cross-checked against
torch's scaled_dot_product_attention. The vectors are already projected
(d_k = 2) and small enough to check: q_le = [0, 2], k_cat = [0, 2], so
q_le · k_cat = 4.

[click] Raw scores. The "le" row: 0 for the, 4 for cat, 2 for sleeps.
[click] Divide by sqrt(2), softmax: 0.05 / 0.77 / 0.19.
[click] The payoff: the decoder knows where to look in the source for the
next word. A real model learns these queries and keys from data.

Transition: "After the FFN, how does a vector become a French word?"
-->

---
chapter: '5 · The decoder'
clicks: 4
---

# From vector to word, until &lt;EOS&gt;

<span class="eyebrow generation">Linear &#8594; softmax &#8594; pick &#8594; append</span>

<div class="pipe">
  <div v-click="1" class="pp"><span class="pl">decoder output, last position</span><span class="pv">1 &#215; 512</span></div>
  <div v-click="1" class="pa">&#215; W<sub>vocab</sub> (512 &#215; 37,000)</div>
  <div v-click="2" class="pp"><span class="pl">logits: one score per vocabulary entry</span><span class="pv">1 &#215; 37,000</span></div>
  <div v-click="2" class="pa">softmax</div>
  <div v-click="3" class="pp out"><span class="pl">probabilities &#8594; pick one (greedy, or sample)</span><span class="pv">&#8220;ours&#8221;</span></div>
</div>

<div v-click="4" class="obs">
  <div>Append it, run the decoder again. Stop when the picked token is <code>&lt;EOS&gt;</code>. Everything from Part I chapters 5 and 6 &#8212; temperature, top-k, top-p &#8212; applies here unchanged.</div>
  <div>In the 2017 paper the output matrix is <b>the same numbers</b> as the input embedding table (weights are shared), which is why the parameter count in chapter 8 counts the embeddings once.</div>
</div>

<style>
.pipe { display: flex; flex-direction: column; align-items: center; gap: 0.15em; margin: 0.4em 0; }
.pp { display: flex; justify-content: space-between; gap: 2em; width: 32em; padding: 0.35em 0.9em; border-radius: 0.45em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.pp.out { background: var(--ann-ember-soft); border-color: var(--ann-ember); }
.pl { font-size: 0.82rem; color: var(--ann-ink-soft); }
.pv { font-family: 'JetBrains Mono', monospace; font-weight: 700; color: var(--ann-indigo); }
.pp.out .pv { color: var(--ann-ember); }
.pa { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--ann-muted); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-variant-ligatures: none; }
</style>

<!--
[click] The last decoder vector times the vocabulary matrix. 37,000 is the
shared English-German BPE vocabulary size in the 2017 paper.
[click] Logits, then softmax - the SECOND use of softmax (chapter 8 contrasts
the two).
[click] Pick a token. The lecture's simple version is "take the most likely";
Part I chapter 6 is the full story.
[click] The loop and the stop condition, plus weight tying.

Transition: "Where we are."
-->

---
chapter: '5 · The decoder'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 5 &#183; takeaway</span>

<EncDecMap :dim-others="false" compact />

<div v-click="1" class="recap">
  <div>Decoder block = <b>masked</b> self-attention &#8594; <b>cross-attention</b> (Q from here, K and V from the encoder) &#8594; FFN, each with Add &amp; Norm, &#215;6.</div>
  <div>Then a linear layer to the vocabulary and a softmax. Start at <code>&lt;BOS&gt;</code>, loop until <code>&lt;EOS&gt;</code>.</div>
</div>

<div v-click="2" class="transition-line">Every box is lit. <span class="arrow">Chapter 6: push one real sentence through all of them and watch the shapes.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
.recap code { font-variant-ligatures: none; }
</style>

<!--
The map, fully lit, for the first time.

Transition: "Chapter six."
-->
