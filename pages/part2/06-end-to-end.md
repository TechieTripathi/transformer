---
layout: section
chapter: '6 · One sentence, end to end'
---

# Chapter 6

## One sentence, end to end

<div v-click class="thesis" style="margin-top:0.8em">Seven English tokens in, French out. Every tensor along the way, with its real shape &#8212; measured by running the model, not copied from a diagram.</div>

<!--
This is the chapter to point people at when they say "I understand the
pieces but not how they fit". Every shape on the next three slides came from
an actual numpy forward pass at the paper's base dimensions, in
scripts/verify-attention.py section 12 (random weights - the shapes do not
depend on what was learned).

Transition: "The sentence and the settings."
-->

---
chapter: '6 · One sentence, end to end'
clicks: 3
---

# The sentence, and the machine&#8217;s settings

<span class="eyebrow structure">The 2017 &#8220;base&#8221; Transformer</span>

<div v-click="1" class="pair">
  <div class="lang"><span class="ll">source &#183; 7 tokens</span><span class="toks"><span v-for="t in N.base.src" :key="t" class="tk">{{ t }}</span></span></div>
  <div class="lang"><span class="ll">target &#183; 7 tokens + &lt;BOS&gt;</span><span class="toks"><span class="tk sp">&lt;BOS&gt;</span><span v-for="t in N.base.tgt" :key="t" class="tk">{{ t }}</span></span></div>
</div>

<div v-click="2" class="dims">
  <div class="dm"><span>d<sub>model</sub></span><b>{{ N.base.dims.d_model }}</b><i>width of every token vector</i></div>
  <div class="dm"><span>h</span><b>{{ N.base.dims.h }}</b><i>attention heads</i></div>
  <div class="dm"><span>d<sub>k</sub></span><b>{{ N.base.dims.d_k }}</b><i>per-head width = 512 / 8</i></div>
  <div class="dm"><span>d<sub>ff</sub></span><b>{{ N.base.dims.d_ff.toLocaleString('en-US') }}</b><i>feed-forward hidden width</i></div>
  <div class="dm"><span>N</span><b>{{ N.base.dims.N }}</b><i>blocks per tower</i></div>
  <div class="dm"><span>vocab</span><b>{{ N.base.dims.vocab.toLocaleString('en-US') }}</b><i>shared BPE tokens</i></div>
</div>

<div v-click="3" class="obs">The token split is simplified for readability (a real BPE would cut <i>peluche</i> and <i>mignon</i> differently). The shapes would change only in the token count.</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.pair { display: flex; flex-direction: column; gap: 0.4em; margin: 0.4em 0 0.6em; }
.lang { display: grid; grid-template-columns: 12em 1fr; align-items: center; gap: 1em; }
.ll { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--ann-muted); text-transform: uppercase; }
.toks { display: flex; flex-wrap: wrap; gap: 0.3em; }
.tk { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; padding: 0.1em 0.45em; border-radius: 0.3em; background: var(--ann-indigo-soft); color: var(--ann-indigo); font-variant-ligatures: none; }
.tk.sp { background: var(--ann-ember-soft); color: var(--ann-ember); }
.dims { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.4em 1em; }
.dm { display: grid; grid-template-columns: 4em 5em 1fr; align-items: baseline; padding: 0.3em 0.7em; border-radius: 0.4em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.dm span { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: var(--ann-ink-soft); }
.dm b { font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; color: var(--ann-indigo); }
.dm i { font-style: normal; font-size: 0.72rem; color: var(--ann-muted); }
.obs { margin-top: 0.6em; font-size: 0.8rem; color: var(--ann-ink-soft); }
</style>

<!--
The sentence pair is Stanford CME 295's running example - deliberately, so
anyone who watches that lecture recognises it.

[click] Source and target. The target is fed in shifted by one, behind <BOS>
(teacher forcing, chapter 5) - so 8 decoder positions.
[click] The six numbers that define the base model. Everything on the next
three slides follows from these and the two token counts.
[click] Honesty about the toy tokenization.

Transition: "Left tower first."
-->

---
chapter: '6 · One sentence, end to end'
clicks: 3
---

# Through the encoder

<span class="eyebrow structure">Every shape measured by a real forward pass</span>

<ShapeTrace :stages="['encoder']" :up-to="[1, 3, 6, 99][$clicks]" />

<div v-click="3" class="obs">Seven rows in, seven rows out, at every level. Only two things are ever not 7 &#215; 512: the per-head score grid (8 heads &#215; 7 &#215; 7) and the feed-forward&#8217;s wide middle (7 &#215; 2,048).</div>

<style>
.obs { margin-top: 0.5em; font-size: 0.86rem; color: var(--ann-ink-soft); }
</style>

<!--
Walk it top to bottom.

Before clicking: token ids (7) and embedding + position (7 x 512).
[click] Q and K for one head: 7 x 64.
[click] Scores: 8 x 7 x 7 - one square grid per head, and concat back to
7 x 512.
[click] FFN hidden 7 x 2048, then the encoder output after 6 layers: 7 x 512.

The observation is the takeaway: the residual stream keeps its shape, which
is what lets you stack, add, and normalise without thinking about it.

Transition: "Right tower."
-->

---
chapter: '6 · One sentence, end to end'
clicks: 3
---

# Through the decoder, and across

<span class="eyebrow structure">The two attention sub-layers have different shapes</span>

<ShapeTrace :stages="['decoder', 'cross']" :up-to="[0, 4, 8, 99][$clicks]" :highlight="$clicks >= 2 ? 7 : undefined" />

<div v-click="3" class="obs">Masked self-attention is <b>8 &#215; 8</b> per head: target against target. Cross-attention is <b>8 &#215; 7</b>: every target position against every source token. That rectangle is the bridge.</div>

<style>
.obs { margin-top: 0.5em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
[click] Masked self-attention: Q and K both 8 x 64, scores 8 x 8 x 8.
[click] Cross-attention: Q is 8 x 64 (from the decoder), K is 7 x 64 (from
the encoder). Highlighted: scores 8 x 8 x 7.
[click] Decoder output 8 x 512.

Have the room predict the cross-attention score shape before you reveal it.
If they get "8 by 7", the chapter has landed.

Transition: "And out the top."
-->

---
chapter: '6 · One sentence, end to end'
clicks: 3
---

# Out the top, one token at a time

<span class="eyebrow generation">Logits, probabilities, and the loop</span>

<ShapeTrace :stages="['output']" />

<div class="gen">
  <div v-click="1" class="gl"><b>Training</b> uses all 8 rows at once: each position predicts the next target token, and the loss is averaged over all of them &#8212; 8 lessons per sentence pair, in one pass.</div>
  <div v-click="2" class="gl"><b>Inference</b> uses only the <b>last</b> row: pick a token, append it, run the decoder again. The encoder ran <b>once</b>; its 7 &#215; 512 output is reused at every step.</div>
  <div v-click="3" class="seq">
    <span class="tk sp">&lt;BOS&gt;</span><span class="ar">&#8594;</span>
    <span v-for="t in N.base.tgt" :key="t" class="tk">{{ t }}</span><span class="ar">&#8594;</span>
    <span class="tk sp">&lt;EOS&gt;</span>
  </div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.gen { display: flex; flex-direction: column; gap: 0.45em; margin-top: 0.6em; }
.gl { font-size: 0.86rem; color: var(--ann-ink-soft); }
.gl b { color: var(--ann-indigo); }
.seq { display: flex; flex-wrap: wrap; align-items: center; gap: 0.3em; justify-content: center; margin-top: 0.3em; }
.tk { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; padding: 0.1em 0.45em; border-radius: 0.3em; background: var(--ann-indigo-soft); color: var(--ann-indigo); font-variant-ligatures: none; }
.tk.sp { background: var(--ann-ember-soft); color: var(--ann-ember); }
.ar { color: var(--ann-muted); }
</style>

<!--
[click] Training: teacher forcing plus the mask means every position is a
training example. This is the parallelism that made the design win.
[click] Inference: one row matters, and the encoder is not re-run. (With a KV
cache, the decoder's past keys and values aren't recomputed either.)
[click] The output sequence, ending in <EOS>.

Transition: "Where we are."
-->

---
chapter: '6 · One sentence, end to end'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 6 &#183; takeaway</span>

<EncDecMap :dim-others="false" compact />

<div v-click="1" class="recap">
  <div>Encoder: <b>7 &#215; 512</b> at every level. Decoder: <b>8 &#215; 512</b>. Self-attention grids are square; the cross-attention grid is <b>8 &#215; 7</b>.</div>
  <div>Logits are <b>8 &#215; 37,000</b>; at inference only the last row is used, and the encoder runs once.</div>
</div>

<div v-click="2" class="transition-line">That is the forward pass. <span class="arrow">Chapter 7: the details that make it actually train.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Transition: "Chapter seven."
-->
