---
layout: section
chapter: '8 · What it all adds up to'
---

# Chapter 8

## What it all adds up to

<div v-click class="thesis" style="margin-top:0.8em">Two ideas do the work &#8212; attention and the feed-forward network. Everything else helps them learn.</div>

<!--
Four slides of synthesis and one of credits.

Transition: "Start with where the numbers actually are."
-->

---
chapter: '8 · What it all adds up to'
clicks: 3
---

# Where the 63 million numbers live

<span class="eyebrow math">The base model, counted from its weight shapes</span>

<div v-click="1" class="params">
  <div v-for="k in ['ffn', 'embeddings', 'attention', 'layernorm']" :key="k" class="pr">
    <span class="pk">{{ { ffn: 'feed-forward', embeddings: 'embeddings (shared)', attention: 'attention (all three kinds)', layernorm: 'LayerNorm' }[k] }}</span>
    <span class="pbar"><span :class="k" :style="{ width: Math.max(100 * N.base.params[k] / N.base.params.total, 0.6) + '%' }"></span></span>
    <span class="pv">{{ (N.base.params[k] / 1e6).toFixed(N.base.params[k] < 1e6 ? 2 : 1) }}M &#183; {{ (100 * N.base.params[k] / N.base.params.total).toFixed(0) }}%</span>
  </div>
  <div class="tot">total {{ N.base.params.total.toLocaleString('en-US') }} &#8212; the paper reports &#8220;65M&#8221; for base</div>
</div>

<div v-click="2" class="obs">
  <div><b>The feed-forward layers are the biggest single block</b> &#8212; inside the towers they hold twice what attention holds. Attention is the idea; the FFN is much of the capacity.</div>
</div>

<div v-click="3" class="obs">
  <div>And the numbers are only half the story: the same architecture trained on better, larger data is a better model. <b>Data quality is part of the system.</b></div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.params { display: flex; flex-direction: column; gap: 0.35em; margin: 0.5em 0; }
.pr { display: grid; grid-template-columns: 13em 1fr 9em; align-items: center; gap: 1em; }
.pk { font-size: 0.85rem; color: var(--ann-ink); text-align: right; }
.pbar { height: 1.3em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); border-radius: 0.3em; overflow: hidden; }
.pbar span { display: block; height: 100%; }
.pbar .ffn { background: var(--ann-circuit); }
.pbar .embeddings { background: var(--ann-indigo); }
.pbar .attention { background: var(--qkv-query); }
.pbar .layernorm { background: var(--ann-ember); }
.pv { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--ann-indigo); font-variant-numeric: tabular-nums; }
.tot { font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--ann-muted); text-align: right; }
.obs { margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Counted in scripts/verify-attention.py section 12 from the weight shapes
(including biases; embeddings shared between source, target and output, as in
the paper). Our count is 63.1M; the paper says 65M - the difference is in
counting conventions, and the script asserts we're in that neighbourhood.

[click] Read the bars: FFN about 40%, embeddings and attention about 30%
each, LayerNorm a rounding error.
[click] Stanford CME 295 makes the same point: the two components that
matter most are attention and the FFN, and the FFN carries a large share of
the parameters.
[click] Data. The architecture is necessary, not sufficient.

Transition: "One function, two jobs."
-->

---
chapter: '8 · What it all adds up to'
clicks: 3
---

# The same softmax, doing two different jobs

<span class="eyebrow structure">A common confusion</span>

<div class="two">
  <div v-click="1" class="tc"><div class="th">Inside attention</div><div class="tq">&#8220;How much should this word listen to each other word?&#8221;</div><div class="td">Over the <b>keys</b>: one row of the n &#215; n (or 8 &#215; 7) grid. Runs in every head of every layer.</div></div>
  <div v-click="2" class="tc"><div class="th">At the very top</div><div class="tq">&#8220;Which token comes next?&#8221;</div><div class="td">Over the <b>vocabulary</b>: 37,000 entries. Runs once per generated token.</div></div>
</div>

<div v-click="3" class="obs">Same formula, e<sup>x</sup> divided by the sum, both producing numbers that add to 1. One is a set of <b>mixing weights</b>; the other is a <b>prediction</b>.</div>

<style>
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1em; margin: 0.5em 0; }
.tc { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.6em 0.9em; background: var(--ann-paper-raised); }
.tc:first-child { border-left: 4px solid var(--qkv-query); }
.tc:last-child { border-left: 4px solid var(--ann-ember); }
.th { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--ann-indigo); }
.tq { font-family: 'Space Grotesk', sans-serif; font-size: 1.05rem; margin: 0.3em 0; }
.td { font-size: 0.82rem; color: var(--ann-ink-soft); }
.td b { color: var(--ann-indigo); }
.obs { margin-top: 0.5em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Part I made this point in one line on its logits slide; here it gets a slide
because it is one of the most common confusions when reading the paper.

Transition: "Three ways to use the two towers."
-->

---
chapter: '8 · What it all adds up to'
clicks: 4
---

# Keep one tower, or both

<span class="eyebrow structure">Three families, one architecture</span>

<div class="fam">
  <div v-click="1" class="fc"><div class="fh">Encoder only</div><div class="fe">BERT (2018)</div><div class="fd">Bidirectional reading, no generation. Classification, search, tagging &#8212; understanding tasks.</div></div>
  <div v-click="2" class="fc"><div class="fh">Encoder&#8211;decoder</div><div class="fe">2017 original, T5</div><div class="fd">Read a source, write a target. Translation, summarisation.</div></div>
  <div v-click="3" class="fc lit"><div class="fh">Decoder only</div><div class="fe">GPT, and nearly every chat model</div><div class="fd">Prompt and answer are one stream; next-token prediction does everything. <b>Part I&#8217;s machine.</b></div></div>
</div>

<div v-click="4" class="transition-line">Decoder-only won for general models because one objective &#8212; predict the next token &#8212; scales on any text. <span class="arrow">Scale it, then teach it to use tools and take steps, and you have today&#8217;s agents.</span></div>

<style>
.fam { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.9em; margin: 0.5em 0; }
.fc { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.6em 0.9em; background: var(--ann-paper-raised); }
.fc.lit { border: 2px solid var(--ann-circuit); background: var(--ann-circuit-soft); }
.fh { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--ann-indigo); font-size: 1.05rem; }
.fe { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--ann-ember); margin: 0.2em 0; }
.fd { font-size: 0.8rem; color: var(--ann-ink-soft); line-height: 1.4; }
.fd b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.6em; padding-top: 0.45em; }
</style>

<!--
[click] Encoder-only: BERT. Masked-word prediction, read in both directions.
[click] Encoder-decoder: today's subject.
[click] Decoder-only: GPT. Part I.
[click] Why decoder-only took over for general-purpose models, and the road
the Stanford course follows next: training, scaling, and agents.

Transition: "The whole argument on one page."
-->

---
chapter: '8 · What it all adds up to'
clicks: 1
zoom: 0.9
---

# Every fix, and the problem it fixed

<span class="eyebrow structure">The argument of both decks, on one page</span>

| Problem | Earlier answer | Why it fell short | The fix |
|---|---|---|---|
| Text is not numbers | raw text | networks need numbers | **tokenization** |
| Words: huge vocabulary, unknown words | word tokens | OOV, bear &#8800; bears | **subwords (BPE)** |
| Meaning, not just identity | one-hot | every pair equally different | **embeddings** (Word2Vec &#8594; learned) |
| Meaning depends on context | static vectors | one vector per word | **contextual models** |
| Long-range context | RNN | vanishing gradients, bottleneck | LSTM, then **attention** |
| Slow, sequential | RNN / LSTM | cannot parallelise | **self-attention only** |
| Word order lost | bag of vectors | attention sees a set | **positional encoding** |
| One relation at a time | single head | one weighting per word | **multi-head + W<sub>O</sub>** |
| Deep stacks won&#8217;t train | plain stacking | signal and scale drift | **residual + LayerNorm** |
| Decoder could cheat | full attention | sees the answer | **causal mask** |
| Reading the source while writing | one vector | bottleneck | **cross-attention** |

<div v-click="1" class="foot">Each row&#8217;s fix creates the next row&#8217;s problem. That is the whole story from text to Transformer.</div>

<style>
.slidev-layout table { font-size: 0.74rem; }
.slidev-layout table td { padding: 0.22em 0.6em; }
.slidev-layout table th { padding: 0.3em 0.6em; }
.foot { margin-top: 0.5em; font-size: 0.85rem; color: var(--ann-indigo); font-family: 'Space Grotesk', sans-serif; font-weight: 600; }
</style>

<!--
A reference slide - students photograph it. Do not read it out; pick two
rows (RNN to attention, and the mask) and let the rest stand.

[click] The one-sentence version of both decks.

Transition: "Credits and where to go next."
-->

---
layout: default
chapter: ''
---

# Credits &amp; where to go next

<span class="eyebrow structure">Read these next</span>

<div class="creds">
  <div><b>Stanford CME 295, Transformers &amp; LLMs</b> &#8212; lecture 1 on YouTube covers this whole path in one sitting; later lectures go on to training, scaling and agents. The teddy-bear sentence and the clock analogy are borrowed from it.</div>
  <div><b>Vaswani et al., &#8220;Attention Is All You Need&#8221; (2017)</b> &#8212; short and readable once you have seen this deck. Every dimension in chapter 6 is from its Table 3, &#8220;base&#8221; row.</div>
  <div><b>Bahdanau, Cho &amp; Bengio (2014)</b> &#8212; attention, born inside an RNN translator.</div>
  <div><b>The Annotated Transformer</b> (Harvard NLP) &#8212; the paper, line by line, as runnable code.</div>
  <div><b>The Illustrated Transformer</b> (Jay Alammar) &#8212; the encoder&#8211;decoder diagrams most people learned from.</div>
</div>

<div class="note">
Every diagram here was drawn for this deck. Every number &#8212; the heads, the cross-attention, the shapes, the parameter count, the smoothing targets &#8212; is generated and checked by
<code>scripts/verify-attention.py</code>, cross-checked against PyTorch. <b>If a slide disagrees with that script, the slide is wrong.</b>
</div>

<style>
.creds { display: flex; flex-direction: column; gap: 0.35em; margin: 0.5em 0; font-size: 0.85rem; color: var(--ann-ink-soft); }
.creds b { color: var(--ann-indigo); }
.note { margin-top: 0.8em; padding-top: 0.5em; border-top: 1px dashed var(--ann-line); font-size: 0.78rem; color: var(--ann-ink-soft); }
.note code { font-family: 'JetBrains Mono', monospace; font-size: 0.95em; }
.note b { color: var(--ann-ember); }
</style>

<!--
Leave this up during questions. The study aids in docs/study/ (cheat sheet,
flashcards, quiz, and an interactive page) cover both decks.
-->
