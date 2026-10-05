---
layout: section
chapter: '7 · Tricks that make it train'
---

# Chapter 7

## Tricks that make it train

<div v-click class="thesis" style="margin-top:0.8em">Attention and feed-forward are the engine. Four unglamorous details are why the engine starts.</div>

<!--
Stanford CME 295 lists these as the "computational tricks" of the original
paper. None of them is the core idea; all of them matter in practice.

Transition: "The first two you have met."
-->

---
chapter: '7 · Tricks that make it train'
clicks: 4
---

# Add &amp; Norm, revisited

<span class="eyebrow structure">Residual connection + layer normalisation</span>

<div class="an">
  <div v-click="1" class="anc"><div class="ah">Add &#8212; the residual</div><div class="af">x + Sublayer(x)</div><div class="ad">The sub-layer learns a <b>change</b>, not a replacement. The gradient has a straight road back through the &#8220;+ x&#8221;, multiplied by 1 &#8212; the cure for chapter 1&#8217;s vanishing signal.</div></div>
  <div v-click="2" class="anc"><div class="ah">Norm &#8212; LayerNorm</div><div class="af">[ 20, 40, 40, 100 ] &#8594; [ &#8722;1.00, &#8722;0.33, &#8722;0.33, 1.67 ]</div><div class="ad">Re-centre each vector at 0 with spread 1, then a learned scale and shift. Keeps magnitudes sane through many layers.</div></div>
</div>

<div v-click="3" class="obs">
  <div>2017 order (<b>post-norm</b>): LayerNorm(x + Sublayer(x)). Modern order (<b>pre-norm</b>): x + Sublayer(LayerNorm(x)) &#8212; more stable for very deep stacks.</div>
</div>

<div v-click="4" class="transition-line">Both exist for the same reason: <span class="arrow">fast, stable convergence when you stack many layers.</span></div>

<style>
.an { display: grid; grid-template-columns: 1fr 1fr; gap: 1em; margin: 0.4em 0; }
.anc { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.6em 0.9em; background: var(--ann-paper-raised); }
.anc:first-child { border-left: 4px solid var(--ann-circuit); }
.anc:last-child { border-left: 4px solid var(--ann-indigo); }
.ah { font-family: 'Space Grotesk', sans-serif; font-weight: 700; color: var(--ann-indigo); }
.af { font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; margin: 0.3em 0; color: var(--ann-ink); }
.ad { font-size: 0.8rem; color: var(--ann-ink-soft); line-height: 1.4; }
.ad b { color: var(--ann-indigo); }
.obs { margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.6em; padding-top: 0.4em; }
</style>

<!--
LayerNorm numbers: scripts/verify-attention.py section 10 (checked against
torch's layer_norm). Same example as Part I chapter 7.

[click] Residual. Tie back to chapter 1's vanishing gradients: an addition
passes the gradient through with factor 1.
[click] LayerNorm.
[click] Post-norm vs pre-norm, one sentence.
[click] Their shared purpose.

Transition: "Third trick: break the network on purpose."
-->

---
chapter: '7 · Tricks that make it train'
clicks: 3
---

# Dropout: train with random parts missing

<span class="eyebrow structure">Regularisation</span>

<div v-click="1" class="key-message">During training, each number coming out of a sub-layer is set to zero with probability <b>p = 0.1</b> &#8212; a different random 10% every step.</div>

<div v-click="2" class="drop">
  <span v-for="i in 20" :key="i" class="dc" :class="{ off: [3, 11].includes(i) }">{{ [3, 11].includes(i) ? '0' : '•' }}</span>
  <span class="dcap">one vector, one training step: 2 of 20 dropped</span>
</div>

<div v-click="3" class="obs">
  <div>No unit can rely on any particular other unit being there, so the network spreads what it knows across many of them. Less memorising of the training set; better on new sentences.</div>
  <div>At inference nothing is dropped. The 2017 base model applied it after every sub-layer and to the embeddings + positions, with p = 0.1.</div>
</div>

<style>
.drop { display: flex; flex-wrap: wrap; align-items: center; gap: 0.3em; margin: 0.6em 0; }
.dc { width: 1.9em; height: 1.9em; display: inline-flex; align-items: center; justify-content: center; border-radius: 0.3em; background: var(--ann-circuit-soft); color: var(--ann-circuit); font-family: 'JetBrains Mono', monospace; font-weight: 700; }
.dc.off { background: var(--ann-ember-soft); color: var(--ann-ember); border: 2px dashed var(--ann-ember); }
.dcap { flex-basis: 100%; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--ann-muted); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
</style>

<!--
[click] The rule. Surviving values are scaled up by 1/(1-p) during training
so the expected total is unchanged - mention only if asked.
[click] The picture: which units drop is random each step.
[click] Why it works, and where the paper used it.

Likely question: "Do LLMs still use dropout?" Answer: "Many very large
models use little or none - with trillions of training tokens, overfitting
is less of a worry than underfitting. It matters more for smaller data."

Transition: "The last trick is the most interesting: lying to the model,
slightly, about the right answer."
-->

---
chapter: '7 · Tricks that make it train'
clicks: 3
zoom: 0.95
---

# Label smoothing: never demand 100%

<span class="eyebrow math">&#949; = 0.1</span>

<div class="ls">
  <div v-click="1">

<ProbBars :tokens="[...N.smoothing.tokens]" :probs="[...N.smoothing.hard]" caption="hard target: blue = 100%, everything else 0" compact />

  </div>
  <div v-click="2">

<ProbBars :tokens="[...N.smoothing.tokens]" :probs="[...N.smoothing.paper]" caption="smoothed target: blue = 90%, the other 10% shared out" compact />

  </div>
</div>

<div v-click="3" class="obs">
  <div>The model is trained towards the <b>right-hand</b> target. Being 100% sure is now <b>penalised</b>, not rewarded.</div>
  <div>On the Part I distribution (blue 0.80): loss against the hard target <b>{{ N.smoothing.lossHard.toFixed(3) }}</b>, against the smoothed one <b>{{ N.smoothing.lossSmoothed.toFixed(3) }}</b> &#8212; and that one can never reach 0.</div>
</div>

<script setup>
import { N } from '../../composables/useDeckNumbers'
</script>

<style>
.ls { display: grid; grid-template-columns: 1fr 1fr; gap: 1.2em; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.3em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Numbers: scripts/verify-attention.py section 11. The slide shows the paper's
variant (eps spread over the K-1 wrong tokens: 0.9 / 0.025 each); PyTorch's
label_smoothing spreads eps over all K tokens (0.92 / 0.02). The script
cross-checks the PyTorch version exactly and prints both.

[click] The usual one-hot target.
[click] The smoothed one.
[click] What changes: the target itself is uncertain, so the optimum is
uncertain too.

Transition: "Why would you want that?"
-->

---
chapter: '7 · Tricks that make it train'
clicks: 3
---

# Why smoothing helps

<span class="eyebrow honesty">Language has more than one right answer</span>

<div v-click="1" class="key-message"><i>A cute teddy bear is reading</i> &#8594; <i>Un ours en peluche mignon lit</i>, or <i>Un mignon ours en peluche lit</i>, or <i>&#8230; est en train de lire</i>. All fine. The training data shows <b>one</b>.</div>

<div v-click="2" class="obs">
  <div>A hard target says the one in the data is right and every alternative is <b>infinitely</b> wrong. Pushing towards 100% makes the model over-confident about one phrasing.</div>
  <div>Smoothing keeps a little probability on the alternatives &#8212; a model that is <b>less sure</b> and, measured by translation quality, <b>better</b>.</div>
</div>

<div v-click="3" class="statement-box">The 2017 paper reports exactly that trade: label smoothing made perplexity worse (the model is less certain) but improved BLEU, the translation-quality score.</div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; font-size: 1rem; }
.slidev-layout .statement-box { margin-top: 0.6em; font-size: 0.88rem; padding: 0.45em 1em; }
</style>

<!--
[click] Multiple valid translations of the running example.
[click] The argument.
[click] The result from the paper. BLEU compares a translation with
reference translations by overlapping word sequences; higher is better.

Transition: "Where we are."
-->

---
chapter: '7 · Tricks that make it train'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 7 &#183; takeaway</span>

<EncDecMap highlight="addnorm" compact />

<div v-click="1" class="recap">
  <div><b>Residual + LayerNorm</b> (every Add &amp; Norm bar) make depth trainable. <b>Dropout</b> (p = 0.1) fights memorising.</div>
  <div><b>Label smoothing</b> (&#949; = 0.1) stops the model demanding certainty that language does not have. The <b>mask</b> keeps the decoder honest.</div>
</div>

<div v-click="2" class="transition-line">Engine, plumbing, training. <span class="arrow">Chapter 8: what it all adds up to.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Every Add & Norm bar lit.

Transition: "Chapter eight."
-->
