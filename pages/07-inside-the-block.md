---
layout: section
chapter: '7 · Inside the block'
---

# Chapter 7

## Inside the block, and how it learned

<div v-click class="thesis" style="margin-top:0.8em">Attention decides <i>what to look at</i>. Something else has to decide <i>what to do with it</i> &#8212; and all of it had to be learned from nothing.</div>

<!--
Twenty seconds. Two jobs in this chapter: finish the architecture, then
answer the question that has been hanging since chapter 2 - where did all
those numbers come from?

Transition: "Attention was only half of the block."
-->

---
chapter: '7 · Inside the block'
clicks: 5
---

# Look, then think

<span class="eyebrow structure">The transformer block</span>

<div class="blockdia">
  <div v-click="1" class="bstep att">
    <div class="bn">Attention</div>
    <div class="bq">&#8220;Which words matter to me?&#8221;</div>
    <div class="bd">Words <b>talk to each other</b>. Information moves sideways.</div>
  </div>
  <div v-click="2" class="barrow">&#8595;</div>
  <div v-click="2" class="bstep ffn">
    <div class="bn">Feed-forward</div>
    <div class="bq">&#8220;What do I make of that?&#8221;</div>
    <div class="bd">Each word <b>thinks on its own</b>. No looking sideways at all.</div>
  </div>
</div>

<div v-click="3" class="obs">
  <div>Attention is <b>communication</b>. Feed-forward is <b>computation</b>. The block alternates between the two, over and over.</div>
  <div>The feed-forward part processes every position <b>separately and identically</b> &#8212; it has no idea the other words exist.</div>
</div>

<div v-click="4" class="statement-box">Surprise: <b>two thirds</b> of a large model&#8217;s numbers live in the feed-forward parts. Attention gets all the attention, and about a third of the parameters.</div>

<div v-click="5" class="transition-line">There is good evidence this is where <b>facts</b> end up stored. <span class="arrow">Attention fetches; feed-forward remembers.</span></div>

<style>
.blockdia { display: flex; flex-direction: column; align-items: center; gap: 0.15em; margin: 0.3em 0; }
.bstep { width: 30em; border-radius: 0.5em; padding: 0.45em 1em; border: 1px solid var(--ann-line); }
.bstep.att { background: var(--ann-ember-soft); border-left: 4px solid var(--ann-ember); }
.bstep.ffn { background: var(--ann-circuit-soft); border-left: 4px solid var(--ann-circuit); }
.bn { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; }
.bstep.att .bn { color: var(--ann-ember); }
.bstep.ffn .bn { color: var(--ann-circuit); }
.bq { font-family: 'Space Grotesk', sans-serif; font-size: 0.95rem; margin: 0.05em 0 0.1em; }
.bd { font-size: 0.78rem; color: var(--ann-ink-soft); }
.barrow { color: var(--ann-muted); font-size: 1.2rem; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.88rem; margin-top: 0.4em; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] Attention, reframed in one word: communication. Words talking to each
other.
[click] Feed-forward: computation. Each word alone with its thoughts. Stress
that it genuinely cannot see the other words - it is applied to each position
independently, with the same weights.

[click] The alternation. Gather, then digest. Gather, then digest. Ninety-six
times.

[click] The parameter split, and lead with how counter-intuitive it is:
everyone talks about attention, and attention is about a third of the model.
The boring-sounding part is two thirds.

[click] The facts point. Research on where factual knowledge lives in these
models keeps landing on the feed-forward layers - you can find and even edit
specific facts there. Keep it to one sentence; it is a teaser, not a topic.

Likely student question: "What does the feed-forward layer actually do?"
Honest answer: "Multiply by a big matrix, zero out the negatives, multiply by
another big matrix. That's it. Why that stores facts is genuinely an active
research question."

Transition: "One more piece, and it's the reason you can stack ninety-six of
these."
-->

---
chapter: '7 · Inside the block'
clicks: 5
---

# The road that runs through everything

<span class="eyebrow structure">Residual connections</span>

<div v-click="1" class="key-message">Each block does not <b>replace</b> the vector. It computes a small change and <b>adds</b> it.</div>

<div v-click="2" class="resid">
  <span class="rv">what came in</span>
  <span class="rop">+</span>
  <span class="rv rc">what this block figured out</span>
  <span class="rop">=</span>
  <span class="rv rr">what goes out</span>
</div>

<div v-click="3" class="obs">
  <div>So there is a <b>straight road</b> from the input all the way to the output, and each block is a <b>detour</b> that rejoins it.</div>
  <div>A block that has nothing useful to add can contribute almost nothing and do no harm. Early in training, they all do exactly that &#8212; and then they <b>come online one by one</b>.</div>
</div>

<div v-click="4" class="obs">
  <div>This is what makes <b>depth</b> possible. Ninety-six layers that each <b>rewrote</b> the vector from scratch would be the telephone game &#8212; by the end, nonsense. Ninety-six that each <b>nudge</b> it are not.</div>
</div>

<div v-click="5" class="transition-line">A vector that starts out meaning <b>king</b> gets nudged, block after block, <span class="arrow">until it means something like &#8220;a Scottish king who murdered his predecessor, described in Shakespearean English&#8221;.</span></div>

<style>
.resid { display: flex; align-items: center; justify-content: center; gap: 0.7em; margin: 0.5em 0; flex-wrap: wrap; }
.rv { font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; padding: 0.3em 0.8em; border-radius: 0.4em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.rv.rc { background: var(--ann-circuit-soft); border-color: var(--ann-circuit); color: var(--ann-circuit); }
.rv.rr { background: var(--ann-indigo-soft); border-color: var(--ann-indigo); color: var(--ann-indigo); font-weight: 600; }
.rop { color: var(--ann-muted); font-size: 1.2rem; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
[click] Add, don't replace. Simple, and it is the single most important
structural idea after attention itself.

[click] The three boxes. Point at the plus.

[click] The road-and-detour picture. Then the "come online over time" fact,
which is lovely and true: residual blocks are usually initialised to
contribute almost nothing, and the network switches them on as it finds uses
for them.

[click] Why depth works at all. Without this, deep networks degrade - the
signal gets mangled by repeated transformation. With it, depth is cheap.

[click] The king example. Do NOT say the name. Let them get there. Somebody
always shouts "Macbeth", and the moment they do, the idea of "a vector
accumulating context as it travels" has landed better than any diagram could
manage.

For anyone who has met calculus: addition sends gradients through unchanged,
so this also gives training a clear path back to the early layers. One
sentence, and only if the room is with you.

Transition: "Now the question I've been dodging since chapter four."
-->

---
chapter: '7 · Inside the block'
clicks: 6
---

# &#8220;Isn&#8217;t that cheating?&#8221;

<span class="eyebrow why">The obvious objection</span>

<div v-click="1" class="obj">
  If every word can look at every word &#8212; and we are training it to predict the <b>next</b> word &#8212;
  then it can just <b>look at the answer</b>.
</div>

<div v-click="2" class="obs">That is a completely correct objection. And the fix is one of the most elegant things in the design.</div>

<div v-click="3" class="attempt bad">
  <div class="ah">Attempt 1: set the future scores to <b>zero</b></div>
  <div class="ab">Fails. After softmax, a score of 0 still gets a <b>positive</b> share &#8212; because e<sup>0</sup> = 1. The future leaks in, and the row no longer means what we said it means.</div>
</div>

<div v-click="4" class="attempt good">
  <div class="ah">Attempt 2: set them to <b>&#8722;&#8734;</b>, <i>before</i> softmax</div>
  <div class="ab">Works. e<sup>&#8722;&#8734;</sup> = 0 exactly. The future gets a <b>true</b> zero, the surviving words rescale among themselves, and the row still adds to <b>1</b>.</div>
</div>

<div v-click="5" class="statement-box">Not &#8220;it reads left to right&#8221;. It sees <b>everything</b> &#8212; and we <b>blindfold</b> it.</div>

<div v-click="6" class="transition-line">A deliberate choice, made in one line of arithmetic. <span class="arrow">Here is what it looks like.</span></div>

<style>
.obj { font-family: 'Space Grotesk', sans-serif; font-size: 1.12rem; color: var(--ann-ink); margin: 0.3em 0 0.35em; max-width: 40em; }
.obj b { color: var(--ann-ember); }
.obs { font-size: 0.85rem; color: var(--ann-ink-soft); margin-bottom: 0.35em; }
.attempt { border-radius: 0.45em; padding: 0.4em 0.9em; margin-bottom: 0.3em; border: 1px solid var(--ann-line); }
.attempt.bad { background: var(--ann-ember-soft); border-left: 4px solid var(--ann-ember); }
.attempt.good { background: var(--ann-circuit-soft); border-left: 4px solid var(--ann-circuit); }
.ah { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.92rem; }
.attempt.bad .ah { color: var(--ann-ember); }
.attempt.good .ah { color: var(--ann-circuit); }
.ab { font-size: 0.78rem; color: var(--ann-ink-soft); margin-top: 0.1em; }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.95rem; margin-top: 0.35em; }
.slidev-layout .transition-line { margin-top: 0.35em; padding-top: 0.3em; }
</style>

<!--
Ask the objection AS A QUESTION before you reveal it. "We're training it to
predict the next word, and I've just told you every word can see every other
word. Is anyone bothered by that?" Someone will be. Let them say it.

[click] The objection, stated properly. Validate it - it is exactly right.

[click] Tell them the fix is elegant. Then do not give it immediately.

[click] THE FAILED ATTEMPT FIRST. This is the pedagogical payload of the
slide and it is why the -infinity feels inevitable rather than arbitrary.
Zero seems like the obvious fix and it does not work, because exp(0) is 1,
not 0. Work that through out loud.

[click] The real fix, and why it works: exp of minus infinity is exactly
zero, and the remaining words renormalise among themselves.

[click] Kill the "reads left to right" mental model explicitly. It sees the
whole sequence in one go; we choose to blindfold part of it. That framing
also explains why the SAME model can be used without the mask for tasks where
you do want to see everything.

[click] Transition.

Transition: "It's easier to see than to say."
-->

---
chapter: '7 · Inside the block'
clicks: 3
---

# The causal mask

<span class="eyebrow math">Mechanism</span>

<div v-click="1">

<MaskGrid :words="['The','cat','is','sleeping','on','the','warm','mat']" compact />

</div>

<div v-click="2" class="obs">
  <div>Row <b>sleeping</b> may look at <i>The, cat, is, sleeping</i> &#8212; and nothing after. Row <b>The</b> may look only at itself.</div>
  <div>No learned numbers here at all. This is a <b>rule</b>, written once, applied every time.</div>
</div>

<div v-click="3" class="transition-line">Every training sentence now teaches the model <b>as many lessons as it has words</b> &#8212; one prediction per position, all computed at once. <span class="arrow">That is why this design trains so fast.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.35em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The staircase. Trace one row with your finger, out loud, using the
real words - that is why the axes carry words rather than indices.

[click] Two observations. The second is worth stressing: unlike almost
everything else in this lecture, there is nothing learned here. It is a fixed
rule. Students find that reassuring after chapter 4.

[click] The efficiency payoff, and it is the real reason this design won:
because every position predicts simultaneously under the mask, one sentence
of ten words is ten training examples, computed in a single pass. The old
designs got one lesson per sentence per step. That is the difference between
trainable and not.

Transition: "One more trick, and it's the reason a chatbot can reply at
all."
-->

---
chapter: '7 · Inside the block'
clicks: 4
---

# Not redoing the whole thing every time

<span class="eyebrow practice">The KV cache</span>

<div v-click="1" class="kv">
  <div class="kvr"><span class="kn">Token 1</span><span class="kb">compute keys &amp; values for 1</span></div>
  <div class="kvr"><span class="kn">Token 2</span><span class="kb">reuse 1 &#183; compute only <b>2</b></span></div>
  <div class="kvr"><span class="kn">Token 3</span><span class="kb">reuse 1, 2 &#183; compute only <b>3</b></span></div>
  <div class="kvr dim"><span class="kn">Token 500</span><span class="kb">reuse 499 &#183; compute only <b>500</b></span></div>
</div>

<div v-click="2" class="obs">
  <div>A word&#8217;s <span class="k">key</span> and <span class="v">value</span> never change once computed &#8212; nothing later can affect them, <b>because of the mask</b>. So keep them.</div>
  <div>You do not reread a story from the start every time you write one more word. Neither does it.</div>
</div>

<div v-click="3" class="obs">
  <div>The cost: that cache has to live in memory, and it grows with every token. On a long conversation it can end up <b>larger than the model</b>.</div>
</div>

<div v-click="4" class="transition-line">A direct consequence of the blindfold. <span class="arrow">Now: where did every number in this machine actually come from?</span></div>

<style>
.kv { display: flex; flex-direction: column; gap: 0.15em; margin: 0.4em 0; }
.kvr { display: grid; grid-template-columns: 8em 1fr; align-items: baseline; gap: 1em; font-size: 0.86rem; }
.kn { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--ann-indigo); font-weight: 600; }
.kb { color: var(--ann-ink-soft); }
.kb b { color: var(--ann-ember); }
.kvr.dim { opacity: 0.6; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The ladder. The pattern is obvious by row three.

[click] The reason it is SAFE, which is the interesting part and follows from
the previous slide: because of the mask, nothing later can change an earlier
token's key or value. If the model could see the future, this trick would be
wrong. The blindfold buys the speed-up.

Then the story analogy, which everyone gets instantly.

[click] The cost. Worth saying because it is the dominant memory cost in
serving these things, and it explains why long conversations get expensive
rather than just slow.

[click] Transition into training. This is the last structural piece; the rest
of the chapter answers the question they have been carrying since chapter 2.

Transition: "Every number I've shown you today was learned. Here's how."
-->

---
chapter: '7 · Inside the block'
clicks: 5
---

# Millions of knobs, all turned by trial and error

<span class="eyebrow structure">Training</span>

<div v-click="1" class="recall">
  <div class="rl">You already met one. Chapter 4, the matrix that made <span class="q">queries</span>:</div>
  <div class="mx">
    <span>1</span><span class="hot">&#8722;1</span>
    <span>0</span><span>0</span>
    <span>1</span><span>0</span>
    <span>&#8722;1</span><span>1</span>
  </div>
  <div class="rl">That <span class="hot-t">&#8722;1</span> is a <b>knob</b>. It began as a random number. Training turned it, a hair at a time, until <b>it</b> asked a question that <b>glass</b> happened to answer.</div>
  <div class="rl big">GPT&#8209;3 has <b>175,000,000,000</b> of them.</div>
</div>

<div class="loop">
  <div v-click="2"><span class="ln">1</span>Show it real text with the next word hidden: <i>&#8220;The cat is ___&#8221;</i></div>
  <div v-click="3"><span class="ln">2</span>It predicts <b>running</b>. The truth was <b>sleeping</b>.</div>
  <div v-click="4"><span class="ln">3</span>Measure how wrong. Nudge <b>every knob</b> slightly in the direction that would have been less wrong.</div>
  <div v-click="5"><span class="ln">4</span>Repeat. Trillions of times.</div>
</div>

<style>
.recall { display: flex; flex-direction: column; gap: 0.3em; margin: 0.2em 0 0.1em; }
.rl { font-size: 0.85rem; color: var(--ann-ink-soft); }
.rl b { color: var(--ann-indigo); }
.rl.big { font-size: 0.95rem; }
.rl.big b { color: var(--ann-ember); font-family: 'JetBrains Mono', monospace; }
.hot-t { color: var(--ann-ember); font-family: 'JetBrains Mono', monospace; font-weight: 700; }
.mx {
  display: grid; grid-template-columns: 2.4em 2.4em; gap: 2px;
  width: max-content; margin: 0.1em 0;
}
.mx span {
  font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums;
  font-size: 0.92rem; text-align: center; padding: 0.12em 0;
  background: var(--ann-paper-raised); border: 1px solid var(--ann-line); border-radius: 3px;
}
.mx span.hot {
  background: var(--ann-ember-soft); border-color: var(--ann-ember);
  color: var(--ann-ember); font-weight: 700;
}
.loop { display: flex; flex-direction: column; gap: 0.32em; margin-top: 0.6em; }
.loop > div { display: flex; align-items: baseline; gap: 0.8em; font-size: 0.93rem; }
.ln {
  flex-shrink: 0; width: 1.6em; height: 1.6em; border-radius: 999px;
  background: var(--ann-indigo-soft); color: var(--ann-indigo);
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.78rem;
  display: inline-flex; align-items: center; justify-content: center;
}
.loop b { color: var(--ann-ember); }
</style>

<!--
[click] Go back to chapter 4 explicitly - put the matrix up and say "you have
seen this before, we multiplied by it to get the query for every word." Then
point at the highlighted minus one.

The whole purpose of this slide is to make "parameter" stop being an abstract
word. A student who has computed with that matrix by hand now learns that the
numbers in it were not chosen by anyone - they were found, by being wrong
about the next word an enormous number of times. That is a much more concrete
idea than a picture of dials, and they have the arithmetic to anchor it.

Then the count. Say the number slowly - a hundred and seventy-five billion
knobs, every one of them found the same way.

[click] Step 1: the task. Note it is the SAME task as chapter 5 - predict the
next token. Training and using are the same operation; only what happens
afterwards differs.

[click] Step 2: it is wrong. Early on it is wrong essentially always, and its
output is noise.

[click] Step 3 is the one that matters, and it is worth being precise: not
"it notices its mistake", but "we measure the error and compute, for each
knob, which way to turn it". Nothing notices anything.

[click] Step 4. The scale is the thing. Trillions of words, months of
compute, thousands of processors.

MUST SAY, because it is the honest frame for the whole lecture: "Nobody wrote
a grammar. Nobody told it what a pronoun is. Nobody programmed 'it refers to
glass'. That 0.85 from chapter four is the residue of an enormous amount of
being wrong about the next word and adjusting slightly."

Transition: "Two pieces of that need naming."
-->

---
chapter: '7 · Inside the block'
clicks: 5
---

# How wrong, and which way

<span class="eyebrow math">Loss and backpropagation</span>

<div v-click="1" class="half">
  <div class="hh">Loss &#8212; <i>how wrong were we?</i></div>
  <div class="hb">Look at the probability the model gave to the <b>correct</b> word. High probability, small loss. Low probability, big loss.</div>
</div>

<div v-click="2" class="losstab">
  <div class="lr hd"><span>probability on the right answer</span><span>loss</span></div>
  <div class="lr"><span>0.90</span><span class="lg">0.11</span></div>
  <div class="lr"><span>0.50</span><span class="lg">0.69</span></div>
  <div class="lr"><span>0.10</span><span class="lb">2.30</span></div>
  <div class="lr"><span>0.01</span><span class="lb">4.61</span></div>
</div>

<div v-click="3" class="obs">Notice it is not a straight line. Being <b>confidently wrong</b> is punished far harder than being unsure &#8212; and as the probability approaches zero, the loss heads for <b>infinity</b>. That asymmetry is deliberate.</div>

<div v-click="4" class="half">
  <div class="hh">Backpropagation &#8212; <i>which way should each knob go?</i></div>
  <div class="hb">Work backwards through the network, computing for every single weight how much it contributed to the error, and therefore which way to nudge it.</div>
</div>

<div v-click="5">

<Callout>
  <template #misconception>The network notices its mistake and corrects itself.</template>
  <template #clarification>It is <b>calculus, not awareness</b>. Backpropagation computes exactly how much each weight contributed to the error and nudges it slightly in the direction that reduces it. Nothing is noticed. Nothing is understood. It is arithmetic, all the way down.</template>
</Callout>

</div>

<style>
.half { margin-top: 0.25em; }
.hh { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--ann-indigo); }
.hb { font-size: 0.8rem; color: var(--ann-ink-soft); }
.hb b { color: var(--ann-ink); }
.losstab { margin: 0.35em 0; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; max-width: 24em; }
.lr { display: grid; grid-template-columns: 1fr 5em; padding: 0.02em 0; }
.lr span:last-child { text-align: right; font-variant-numeric: tabular-nums; }
.lr.hd { font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ann-muted); border-bottom: 1px solid var(--ann-line); padding-bottom: 0.15em; margin-bottom: 0.1em; }
.lg { color: var(--ann-circuit); }
.lb { color: var(--ann-ember); font-weight: 600; }
.obs { font-size: 0.79rem; color: var(--ann-ink-soft); margin-top: 0.25em; }
.obs b { color: var(--ann-ember); }
.slidev-layout .callout { font-size: 0.72rem; }
.slidev-layout .callout-row { padding: 0.3em 0.9em; }
</style>

<!--
Two named things, fast. Neither gets derived - this is a lecture about
transformers, not about optimisation, and the room has had ninety minutes.

[click] Loss in one sentence.

[click] The table. Read the shape: from 0.9 to 0.5 the loss roughly sextuples;
from 0.1 to 0.01 it doubles again and keeps going.

[click] The asymmetry, and why it is wanted: you want a classifier that is
terrified of being confidently wrong. Connect it to chapter 5 - the model's
"confidence" is the number this loss is computed from.

[click] Backpropagation, named, not derived.

[click] The callout. This is the misconception that matters most for how they
think about AI in general, and it is the note the chapter should end on.

If the room is tired, this is the slide to compress - the callout is the part
that must survive.

Transition: "That's the machine. All of it. Chapter eight is about what it
still gets wrong."
-->

---
chapter: '7 · Inside the block'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 7 &#183; takeaway</span>

<div v-click="1" class="recap big">
  <div>A block = <b>attention</b> (words talk) then <b>feed-forward</b> (each word thinks), <b>added</b> onto a running total.</div>
  <div>The <b>mask</b> blindfolds the future, which is also what makes the <b>KV cache</b> safe.</div>
  <div>Every number was found by being wrong about the next word, trillions of times.</div>
</div>

<div v-click="2" class="transition-line">You now know the whole machine. <span class="arrow">So let&#8217;s be honest about what it cannot do.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.6em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
The map, fully lit, for the first time since chapter 5's example. Say it:
"Every box. You know what happens in every one of them."

[click] Three lines.
[click] Hand off to chapter 8 - and set the tone: this is not a debunking
chapter, it is a calibration chapter.

Transition: "Chapter eight."
-->
