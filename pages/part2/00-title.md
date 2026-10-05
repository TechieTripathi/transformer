---
layout: cover
class: title-cover
---

# Transformers II

### The original machine: an encoder that reads, a decoder that writes, and the tricks that make it learn

<div class="p2-sub">Part II &#183; assumes Part I &#183; every number checked by <code>scripts/verify-attention.py</code></div>

<style>
.p2-sub { margin-top: 1.6em; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--ann-muted); }
.p2-sub code { font-family: inherit; }
</style>

<!--
Part I ended with the whole decoder-only machine: tokens, embeddings,
attention, feed-forward, the mask, next-token prediction. That is the shape of
every chatbot.

But it is not the shape the 2017 paper drew. The original Transformer was a
translator with two halves, and several pieces Part I skipped or waved at
are needed to read that paper - or any lecture that follows it, such as
Stanford CME 295.

Transition: "Here is the half we never drew."
-->

---
chapter: ''
clicks: 3
---

# Part I drew half the machine

<span class="eyebrow structure">Where we are</span>

<div class="split">
  <div>

<EncDecMap :highlight="$clicks >= 1 ? ['dec-embed','dec-mask','dec-ffn','linear','softmax'] : []" :pending="$clicks >= 2 ? 'cross' : ''" compact />

  </div>
  <div class="side">
    <div v-click="1" class="pt"><b>The lit column is Part I.</b> A decoder: masked self-attention, feed-forward, a vocabulary softmax. GPT is this, and nothing else.</div>
    <div v-click="2" class="pt"><b>The 2017 translator had a second tower</b> &#8212; an encoder that reads the whole source sentence first &#8212; and a bridge, <b>cross-attention</b>, through which the decoder consults it.</div>
    <div v-click="3" class="pt"><b>Today:</b> why the old recurrent design had to go, positions done properly, many heads with real shapes, both towers, one sentence end to end, and the training tricks.</div>
  </div>
</div>

<style>
.split { display: grid; grid-template-columns: 1.35fr 1fr; gap: 1.2em; align-items: center; }
.side { display: flex; flex-direction: column; gap: 0.6em; }
.pt { font-size: 0.84rem; color: var(--ann-ink-soft); line-height: 1.4; }
.pt b { color: var(--ann-indigo); }
</style>

<!--
This picture is the map for the whole of Part II. It comes back at the end of
every chapter with a different box lit, exactly like the pipeline map in
Part I.

[click] Light the decoder. "This is everything from Part I. Notice what is
missing from it." Let them spot the dark box in the middle and the whole left
tower.

[click] The pending box: cross-attention. The left tower is the encoder. In
translation it reads the English sentence; the decoder writes the French one,
asking the encoder questions as it goes.

[click] The plan for the session.

Likely question: "Why did chatbots drop the encoder?" Short answer for now:
"Because for open-ended generation there is no separate source sentence -
the prompt and the answer are one stream. Chapter 8 comes back to this."

Transition: "First, the thing the 2017 paper was replacing."
-->

---
chapter: ''
clicks: 4
zoom: 0.94
---

# The plan

<span class="eyebrow structure">Eight chapters, one argument</span>

<div class="roadmap">
  <div><span class="rn">1</span><div><b>Before attention</b><span>Recurrent translators, the one-vector bottleneck, vanishing gradients, LSTMs &#8212; and the 2014 fix.</span></div></div>
  <div><span class="rn">2</span><div><b>Position, properly</b><span>Learned tables vs sine waves: clock hands, nearby-means-similar, and the length limit.</span></div></div>
  <div v-click="1"><span class="rn">3</span><div><b>Many heads, with shapes</b><span>Two heads on the Part I example, d<sub>k</sub> = d<sub>model</sub>/h, concatenate, W<sub>O</sub>.</span></div></div>
  <div v-click="1"><span class="rn">4</span><div><b>The encoder</b><span>Self-attention with no mask, Add &amp; Norm, a feed-forward that widens 4&#215;, stacked six times.</span></div></div>
  <div v-click="2"><span class="rn">5</span><div><b>The decoder</b><span>&lt;BOS&gt;, masked self-attention, <b>cross-attention</b>, the vocabulary softmax, &lt;EOS&gt;.</span></div></div>
  <div v-click="2"><span class="rn">6</span><div><b>One sentence, end to end</b><span>Every tensor in the base model, with its shape &#8212; measured, not remembered.</span></div></div>
  <div v-click="3"><span class="rn">7</span><div><b>Tricks that make it train</b><span>Residuals, LayerNorm, dropout, label smoothing.</span></div></div>
  <div v-click="3"><span class="rn">8</span><div><b>What it all adds up to</b><span>Where the 63 million numbers live, three families of model, and the road to LLMs and agents.</span></div></div>
</div>

<div v-click="4" class="transition-line">Same rule as Part I: <span class="arrow">every number on screen is re-derived by a script, and if a slide disagrees with it, the slide is wrong.</span></div>

<style>
.roadmap { display: flex; flex-direction: column; gap: 0.1em; margin-top: 0.3em; }
.roadmap > div { display: flex; align-items: flex-start; gap: 0.7em; }
.rn { flex-shrink: 0; width: 1.55em; height: 1.55em; border-radius: 999px; background: var(--ann-indigo-soft); color: var(--ann-indigo); font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.78rem; display: flex; align-items: center; justify-content: center; }
.roadmap b { font-family: 'Space Grotesk', sans-serif; font-size: 0.85rem; display: block; line-height: 1.2; }
.roadmap span:last-child { font-size: 0.72rem; color: var(--ann-ink-soft); line-height: 1.25; }
.slidev-layout .transition-line { margin-top: 0.6em; padding-top: 0.45em; }
</style>

<!--
Ninety seconds. Chapters 1-2 are context and repair work; 3-6 are the
architecture; 7 is training; 8 pulls it together.

If time is short, chapter 1 can be compressed to its first and last slides -
Part I already has a one-slide version of the RNN story.

Transition: "Chapter one."
-->
