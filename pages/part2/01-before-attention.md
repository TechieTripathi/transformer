---
layout: section
chapter: '1 · Before attention'
---

# Chapter 1

## Before attention

<div v-click class="thesis" style="margin-top:0.8em">The 2017 paper did not invent a better translator from scratch. It deleted the part of the old one that could not scale.</div>

<!--
Twenty seconds. Part I gave this one slide; here it gets five, because the
2017 design only makes sense as a list of repairs to this one.

Transition: "Here is how translation worked in 2014."
-->

---
chapter: '1 · Before attention'
clicks: 4
---

# Translation, 2014: squeeze the sentence into one vector

<span class="eyebrow why">Sequence to sequence</span>

<div class="s2s">
  <div v-click="1" class="tower enc">
    <span class="w">A</span><span class="w">cute</span><span class="w">teddy</span><span class="w">bear</span><span class="w">is</span><span class="w">reading</span>
    <div class="cap">encoder RNN reads, one word at a time</div>
  </div>
  <div v-click="2" class="neck"><div class="vec">one vector</div><div class="cap">everything it understood</div></div>
  <div v-click="3" class="tower dec">
    <span class="w">Un</span><span class="w">ours</span><span class="w">en</span><span class="w">peluche</span><span class="w">mignon</span><span class="w">lit</span>
    <div class="cap">decoder RNN writes, one word at a time</div>
  </div>
</div>

<div v-click="4" class="obs">
  <div>A 6-word sentence and a 60-word paragraph both have to fit through the <b>same fixed-size vector</b>. Long inputs lose detail &#8212; and translation quality fell off a cliff as sentences got longer.</div>
  <div>And both halves still queue: word 6 cannot be read until word 5 has been.</div>
</div>

<style>
.s2s { display: grid; grid-template-columns: 1fr auto 1fr; gap: 1em; align-items: center; margin: 0.6em 0; }
.tower { display: flex; flex-wrap: wrap; gap: 0.3em; padding: 0.6em; border-radius: 0.5em; border: 1px solid var(--ann-line); background: var(--ann-paper-raised); }
.tower.enc { border-left: 4px solid var(--ann-circuit); }
.tower.dec { border-left: 4px solid var(--qkv-query); }
.w { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; padding: 0.1em 0.45em; border-radius: 0.3em; background: var(--ann-indigo-soft); color: var(--ann-indigo); }
.cap { flex-basis: 100%; font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; color: var(--ann-muted); margin-top: 0.3em; }
.neck { text-align: center; }
.vec { font-family: 'Space Grotesk', sans-serif; font-weight: 700; padding: 0.5em 0.9em; border-radius: 999px; background: var(--ann-ember-soft); border: 2px solid var(--ann-ember); color: var(--ann-ember); }
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
The sentence pair is the one Stanford CME 295 uses for its walkthrough; we
will trace it through the full Transformer in chapter 6.

[click] The encoder: a recurrent network, as in Part I chapter 3, reading
left to right.
[click] Its final hidden state - one vector - is all that crosses over.
[click] The decoder unrolls that vector into French, one word at a time.

[click] The bottleneck. Ask the room: "Would you translate a long paragraph
by reading it once, closing the book, and writing from memory?" That is what
this design does. Sutskever et al. (2014) made it work surprisingly well on
short sentences; it degraded on long ones.

Transition: "There is a second problem, and it is about training."
-->

---
chapter: '1 · Before attention'
clicks: 4
---

# Why far-away words are hard to learn

<span class="eyebrow math">Vanishing (and exploding) gradients</span>

<div v-click="1" class="key-message">To learn that word 1 mattered for word 11, the training signal has to travel back through <b>ten</b> steps &#8212; and it is multiplied by roughly the same factor at every step.</div>

<div class="vg">
  <div v-click="2" class="vr">
    <span class="vl">factor 0.5</span>
    <span v-for="(v, i) in N.vanishing.shrink.values" :key="i" class="vc shrink" :style="{ opacity: 0.25 + 0.75 * v }">{{ v < 0.01 ? v.toFixed(4) : v.toFixed(2) }}</span>
  </div>
  <div v-click="3" class="vr">
    <span class="vl">factor 1.5</span>
    <span v-for="(v, i) in N.vanishing.grow.values" :key="i" class="vc grow">{{ v < 10 ? v.toFixed(1) : v.toFixed(0) }}</span>
  </div>
  <div class="vr axis"><span class="vl">steps back</span><span v-for="i in N.vanishing.steps + 1" :key="i" class="vc ax">{{ i - 1 }}</span></div>
</div>

<div v-click="4" class="obs">
  <div>Below 1: after ten steps the signal is <b>a thousandth</b> of what it was &#8212; distant words effectively stop teaching anything. Above 1: it <b>explodes</b> and training blows up.</div>
  <div>Attention side-steps this completely: every word is <b>one step</b> from every other word, so there is nothing to compound.</div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.vg { display: flex; flex-direction: column; gap: 0.25em; margin: 0.4em 0; }
.vr { display: grid; grid-template-columns: 7em repeat(11, 1fr); gap: 0.25em; align-items: center; }
.vl { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--ann-muted); text-align: right; padding-right: 0.4em; }
.vc { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; text-align: center; padding: 0.3em 0; border-radius: 0.3em; font-variant-numeric: tabular-nums; }
.vc.shrink { background: var(--ann-circuit-soft); color: var(--ann-circuit); font-weight: 600; }
.vc.grow { background: var(--ann-ember-soft); color: var(--ann-ember); font-weight: 600; }
.vc.ax { font-size: 0.68rem; color: var(--ann-muted); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.45em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; font-size: 1rem; }
</style>

<!--
Numbers: scripts/verify-attention.py, "vanishing" - it is just powers, but
the deck's rule is that every figure has a source.

[click] The setup. Training adjusts weights by sending an error signal
backwards (Part I chapter 7). Through a recurrent chain, the path back to an
early word passes through every step in between.

[click] Factor 0.5: halve it ten times and you have about 0.001. Fade the
row with your hand as you read it.
[click] Factor 1.5: ten steps gives about 58. The model's updates for early
words are either negligible or huge and destabilising.

[click] The consequence, and the punchline that motivates everything after:
attention puts every pair of words one step apart, so the product has one
term, not ten.

Likely question: "Can't you just keep the factor at exactly 1?" Answer:
"That's precisely the idea behind the LSTM's cell state and, later, residual
connections - give the signal a path where it is multiplied by about 1."

Transition: "Which is the next slide."
-->

---
chapter: '1 · Before attention'
clicks: 3
---

# The LSTM patch: a protected memory lane

<span class="eyebrow structure">Long short-term memory, 1997</span>

<div class="lstm">
  <div v-click="1" class="lane cell"><span class="ln">cell state</span><span class="lt">a lane that information can ride along <b>unchanged</b>, step after step</span></div>
  <div v-click="2" class="gates">
    <div class="g"><b>forget</b> gate<span>what to erase from the lane</span></div>
    <div class="g"><b>input</b> gate<span>what new information to write onto it</span></div>
    <div class="g"><b>output</b> gate<span>what to reveal as this step&#8217;s hidden state</span></div>
  </div>
  <div v-click="1" class="lane hid"><span class="ln">hidden state</span><span class="lt">the working memory a plain RNN has, as before</span></div>
</div>

<div v-click="3" class="obs">
  <div>Each gate is a learned dial between 0 and 1. When the forget gate sits near 1, the lane multiplies the old memory by about 1 &#8212; the vanishing problem, <b>mostly</b> fixed.</div>
  <div>But it still reads <b>one word at a time</b>, and it still has to carry everything in a fixed-size memory. Better plumbing, same queue.</div>
</div>

<style>
.lstm { display: flex; flex-direction: column; gap: 0.35em; margin: 0.5em 0; }
.lane { display: grid; grid-template-columns: 9em 1fr; align-items: center; gap: 1em; padding: 0.45em 0.9em; border-radius: 0.45em; }
.lane.cell { background: var(--ann-circuit-soft); border-left: 4px solid var(--ann-circuit); }
.lane.hid { background: var(--ann-indigo-soft); border-left: 4px solid var(--ann-indigo); }
.ln { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: var(--ann-indigo); }
.lt { font-size: 0.85rem; color: var(--ann-ink-soft); }
.lt b { color: var(--ann-circuit); }
.gates { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.6em; padding: 0 0.5em; }
.g { font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; padding: 0.35em 0.6em; border: 1px dashed var(--ann-line); border-radius: 0.4em; background: var(--ann-paper-raised); }
.g b { color: var(--ann-ember); }
.g span { display: block; font-family: 'Inter', sans-serif; font-size: 0.74rem; color: var(--ann-ink-soft); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Keep it qualitative. The equations are not needed to follow the rest of the
deck, and the gate names are the part people remember.

[click] Two lanes. The hidden state is what a plain RNN has. The cell state is
new: it is updated by addition, and that matters - adding is how you keep a
signal from shrinking (the same idea as residual connections in chapter 7).

[click] Three gates, each a small learned layer squashed to 0-1. Forget,
write, reveal.

[click] What it fixed and what it did not. It made long-range learning
practical enough that LSTMs dominated translation, speech and text from about
2014 to 2017. It did not fix the queue or the bottleneck.

Transition: "The bottleneck was fixed first - in 2014 - and the fix is the
seed of everything."
-->

---
chapter: '1 · Before attention'
clicks: 3
---

# The 2014 fix: let the decoder look back

<span class="eyebrow attention">Attention is born, bolted onto an RNN</span>

<div v-click="1">

<RnnUnroll mode="attention" :words="['A','cute','teddy','bear','is','reading','→ ours']" :focus="3" compact />

</div>

<div v-click="2" class="obs">
  <div>Instead of one vector, the decoder keeps <b>every</b> encoder hidden state, and when writing each French word it computes a weighted blend of them &#8212; weights learned, different for every word it writes.</div>
  <div>Writing <i>ours</i>, it leans on <i>bear</i>. No bottleneck: the whole source sentence stays available.</div>
</div>

<div v-click="3" class="transition-line">Translation quality stopped falling off with sentence length. <span class="arrow">Three years later, someone asked: if attention does the real work, why keep the RNN at all?</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.3em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.4em; }
</style>

<!--
Bahdanau, Cho and Bengio, 2014. Same picture as Part I's "fix" slide, now in
its original setting: translation.

[click] The last box is the decoder writing "ours" (bear). It reaches back to
every encoder position directly; the strongest arc goes to "bear".

[click] This IS attention - the weighted average from Part I chapter 4 -
with the decoder's state asking the question and the encoder's states
answering. In chapter 5 the same move reappears as cross-attention.

[click] The 2017 question, verbatim in spirit: "Attention Is All You Need".
Delete the recurrence; keep only the direct connections; get parallelism and
one-step paths for free.

Transition: "Where we are."
-->

---
chapter: '1 · Before attention'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 1 &#183; takeaway</span>

<EncDecMap :highlight="['cross']" compact />

<div v-click="1" class="recap">
  <div>RNN translators squeezed a sentence into <b>one vector</b>, read it <b>one word at a time</b>, and struggled to learn across distance.</div>
  <div>LSTMs protected the memory; 2014 attention removed the bottleneck. The <b>2017 Transformer</b> removed the RNN.</div>
</div>

<div v-click="2" class="transition-line">Removing the RNN removed the only thing that knew word order. <span class="arrow">Chapter 2 puts it back.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
The lit box is cross-attention: the direct descendant of the 2014 fix, and
the one part of the 2017 design that is recognisably the old idea.

[click] Two lines.
[click] The hand-off: with no recurrence, nothing in the model knows which
word came first.

Transition: "Chapter two."
-->
