---
layout: section
chapter: '2 · Position, properly'
---

# Chapter 2

## Position, properly

<div v-click class="thesis" style="margin-top:0.8em">Attention sees a bag of words. <i>The dog bit the man</i> and <i>the man bit the dog</i> look identical to it &#8212; until we write position into the vectors.</div>

<!--
Part I chapter 2 covered "just add the position in" in one slide. This
chapter answers the follow-up questions: add WHAT, and what happens past
the longest sentence seen in training?

Transition: "Option one: learn it."
-->

---
chapter: '2 · Position, properly'
clicks: 4
---

# Option 1: learn a vector for every position

<span class="eyebrow structure">Learned positional embeddings</span>

<div v-click="1" class="key-message">Exactly like the word embedding table, but indexed by <b>slot</b> instead of by token: row 0, row 1, row 2 &#8230; each learned during training.</div>

<div v-click="2" class="ptab">
  <div class="pr"><span class="pk">position 0</span><span class="pv">[ learned ]</span></div>
  <div class="pr"><span class="pk">position 1</span><span class="pv">[ learned ]</span></div>
  <div class="pr dots"><span class="pk">&#8942;</span><span class="pv"></span></div>
  <div class="pr"><span class="pk">position 511</span><span class="pv">[ learned ]</span></div>
  <div class="pr miss"><span class="pk">position 512</span><span class="pv">no row &#8212; never trained</span></div>
</div>

<div v-click="3" class="obs">
  <div><b>Simple, flexible, works well</b> &#8212; BERT and GPT-2 used it.</div>
  <div>But the table has a <b>last row</b>. A sequence longer than anything seen in training has positions the model has never learned anything about.</div>
</div>

<div v-click="4" class="transition-line">The 2017 paper tried both and found them about equally good. <span class="arrow">It chose the one with no last row.</span></div>

<style>
.ptab { display: flex; flex-direction: column; gap: 0.15em; margin: 0.5em 0; max-width: 28em; }
.pr { display: grid; grid-template-columns: 9em 1fr; gap: 1em; font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; padding: 0.2em 0.7em; border-radius: 0.3em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.pr.dots { background: none; border: none; color: var(--ann-muted); }
.pr.miss { border: 2px dashed var(--ann-ember); color: var(--ann-ember); background: var(--ann-ember-soft); }
.pk { color: var(--ann-indigo); }
.pr.miss .pk { color: var(--ann-ember); }
.pv { color: var(--ann-ink-soft); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
[click] The idea: a second embedding table, one row per slot, added to the
token embedding.
[click] The table. 512 rows is typical of the era; GPT-2 had 1,024.
[click] The trade-off. Flexible - the model learns whatever position signal
helps - but bounded.
[click] Vaswani et al. report the two options giving nearly identical results
and pick sinusoids for their potential to extrapolate.

Transition: "So what is a position vector that needs no table?"
-->

---
chapter: '2 · Position, properly'
clicks: 4
---

# Option 2: a clock with many hands

<span class="eyebrow intuition">Sinusoidal positional encoding</span>

<div v-click="1" class="key-message">A clock tells the time with hands that turn at different speeds. Read all the hands together and you know exactly when it is. Do the same for position.</div>

<div class="clock">
  <div v-click="2" class="hand"><span class="hn">fast hand</span><span class="hd">turns every ~6 positions &#8212; tells neighbours apart</span></div>
  <div v-click="2" class="hand"><span class="hn">medium hands</span><span class="hd">turn every 20, 60, 200 &#8230; positions</span></div>
  <div v-click="2" class="hand"><span class="hn">slow hands</span><span class="hd">barely move in a sentence &#8212; tell the beginning of a book from the end</span></div>
</div>

<div v-click="3" class="formula">
  PE<sub>(pos, 2i)</sub> = sin( pos / 10000<sup>2i/d</sup> ) &nbsp;&nbsp;&nbsp; PE<sub>(pos, 2i+1)</sub> = cos( pos / 10000<sup>2i/d</sup> )
</div>

<div v-click="4" class="obs">
  <div>Each <b>sin/cos pair</b> is one hand: its angle is where the hand points. Pair <i>i</i> turns more slowly as <i>i</i> grows.</div>
  <div><b>Nothing is learned and nothing runs out</b> &#8212; the formula gives a vector for position 10,000 as happily as for position 3.</div>
</div>

<style>
.clock { display: flex; flex-direction: column; gap: 0.25em; margin: 0.4em 0; }
.hand { display: grid; grid-template-columns: 9em 1fr; gap: 1em; align-items: baseline; padding: 0.3em 0.8em; border-left: 3px solid var(--ann-indigo); background: var(--ann-paper-raised); border-radius: 0 0.4em 0.4em 0; }
.hn { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; font-weight: 700; color: var(--ann-indigo); }
.hd { font-size: 0.85rem; color: var(--ann-ink-soft); }
.formula { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; text-align: center; margin: 0.6em 0 0.3em; color: var(--ann-ink); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
The clock analogy is the one Stanford CME 295 uses; it is the best intuition
for this formula there is.

[click] Hours, minutes, seconds. One hand alone is ambiguous - the seconds
hand is in the same place every minute - but together they pin down a moment.
[click] Map to dimensions. The fast hand changes a lot between neighbours;
the slow hands distinguish distant positions.
[click] The formula. 10000^(2i/d) is the "gear ratio" for pair i. Do not
derive; just point at where i appears.
[click] Two properties to take away.

Likely question: "Why both sin and cos?" Answer: "A hand needs two numbers to
say where it points - sin and cos are its x and y. That pairing is also what
makes 'shift by k' the same rotation for every position, which the verify
script tests."

Transition: "Here are the hands, drawn."
-->

---
chapter: '2 · Position, properly'
clicks: 2
zoom: 0.95
---

# What the encoding actually looks like

<span class="eyebrow math">d = 16, positions 0&#8211;15</span>

<div class="pegrid">
  <div>

<PosEncStrip mode="strip" :rows="16" :highlight-row="$clicks >= 1 ? 5 : undefined" />

  </div>
  <div class="side">
    <div class="pt">Each <b>row</b> is the vector added to the token at that position. Teal is positive, ember negative; square size is magnitude.</div>
    <div v-click="1" class="pt">Read across <b>row 5</b>: the left columns are mid-swing; the right columns have barely moved from where row 0 started. Every row is a different combination &#8212; a unique fingerprint.</div>
    <div v-click="2" class="pt">The numbers under the columns are each hand&#8217;s period: the fastest turns once every <b>6.3</b> positions, the slowest once every <b>19,869</b>.</div>
  </div>
</div>

<style>
.pegrid { display: grid; grid-template-columns: 1.3fr 1fr; gap: 1.2em; align-items: center; }
.side { display: flex; flex-direction: column; gap: 0.6em; }
.pt { font-size: 0.85rem; color: var(--ann-ink-soft); line-height: 1.4; }
.pt b { color: var(--ann-indigo); }
</style>

<!--
Numbers: scripts/verify-attention.py section 7 (16 dimensions so the columns
are legible; the base model uses 512).

Let them look first. The left columns flicker; the right columns are nearly
solid. That visual IS the clock.

[click] Row 5 highlighted.
[click] The periods. Point out the geometric progression - each pair turns
about 3.16x more slowly than the last (10000^(2/16)).

Transition: "Does it really make nearby positions similar?"
-->

---
chapter: '2 · Position, properly'
clicks: 3
---

# Nearby positions look alike

<span class="eyebrow math">d = 512, the real base model</span>

<PosEncStrip mode="curve" compact />

<div class="obs">
  <div v-click="1">Compare position 20 with every position from 0 to 40. Itself: <b>1.00</b>. One away: <b>0.97</b>. Five away: <b>0.74</b>. Twenty away: <b>0.62</b>.</div>
  <div v-click="2">So the model gets <b>distance</b> almost for free: the dot product of two position vectors already says roughly how far apart they are &#8212; and attention is made of dot products.</div>
  <div v-click="3">Modern models go one step further and <b>rotate</b> the queries and keys by their position (RoPE), so attention scores depend directly on relative distance. Same clock, used differently.</div>
</div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.3em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Numbers: scripts/verify-attention.py section 7, similarity normalised so
identical = 1.

[click] Read four values off the curve.
[click] Why it matters: attention compares vectors with dot products, so a
position signal whose dot products encode distance is exactly the right
shape.
[click] RoPE, one sentence. Llama, Mistral, Qwen and most open models use
it. The extrapolation story is honest: sinusoids and RoPE both produce
vectors past the training length, but models still degrade there unless the
encoding is stretched - an active research area.

Transition: "Where we are."
-->

---
chapter: '2 · Position, properly'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 2 &#183; takeaway</span>

<EncDecMap :highlight="['enc-embed','dec-embed']" compact />

<div v-click="1" class="recap">
  <div>Input to each tower = <b>token embedding + position encoding</b>, both of width d<sub>model</sub>.</div>
  <div><b>Learned</b> tables are flexible but end at their last row; <b>sinusoids</b> are a clock with many hands, need no training, and give nearby positions similar vectors.</div>
</div>

<div v-click="2" class="transition-line">Now the vectors know what and where. <span class="arrow">Chapter 3: many attention heads at once, with real shapes.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Both embedding boxes lit: the encoder and decoder use the same recipe.

Transition: "Chapter three."
-->
