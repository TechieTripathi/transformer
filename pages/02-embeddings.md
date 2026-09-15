---
layout: section
chapter: '2 · Turning words into numbers'
---

# Chapter 2

## Turning words into numbers

<div v-click class="thesis" style="margin-top:0.8em">A token id is a seat number. It tells you nothing about who is sitting there. We need numbers that carry <i>meaning</i>.</div>

<!--
Twenty seconds.

The hinge: "We ended chapter one with six numbers. But those numbers are
arbitrary labels - 8415 is not bigger or better or furrier than 279, it is
just the slot the chunk happened to land in. If we feed arbitrary labels into
arithmetic, we get arbitrary answers out. So the next job is to replace the
label with something that actually means something."

Transition: "Here's the problem, precisely."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 4
---

# A label is not a meaning

<span class="eyebrow why">The problem</span>

<div class="cmp">
  <div v-click="1" class="col bad">
    <div class="ch">Token ids</div>
    <div class="rows">
      <div><code>cat</code><span class="num">8415</span></div>
      <div><code>dog</code><span class="num">5679</span></div>
      <div><code>car</code><span class="num">1841</span></div>
    </div>
    <div class="cmt">Is a <code>dog</code> closer to a <code>cat</code> or to a <code>car</code>?<br>The numbers say <b>car</b>. The numbers are wrong.</div>
  </div>
  <div v-click="2" class="col good">
    <div class="ch">Vectors</div>
    <div class="rows">
      <div><code>cat</code><span class="num">[0.8, 0.2, 0.9, 0.1]</span></div>
      <div><code>dog</code><span class="num">[0.7, 0.3, 0.9, 0.2]</span></div>
      <div><code>car</code><span class="num">[0.1, 0.9, 0.0, 0.8]</span></div>
    </div>
    <div class="cmt">Now <code>cat</code> and <code>dog</code> agree almost everywhere,<br>and <code>car</code> disagrees almost everywhere.</div>
  </div>
</div>

<div v-click="3" class="key-message">We give every token a <b>list of numbers</b> instead of one number. That list is called an <b>embedding</b>.</div>

<div v-click="4" class="transition-line">Nobody writes these lists. <span class="arrow">They start out random, and training moves them until words used in similar ways end up with similar lists.</span></div>

<style>
.cmp { display: grid; grid-template-columns: 1fr 1.25fr; gap: 1.2em; margin: 0.4em 0; }
.col { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.6em 0.9em; background: var(--ann-paper-raised); }
.col.bad { border-left: 4px solid var(--ann-ember); }
.col.good { border-left: 4px solid var(--ann-circuit); }
.ch { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; letter-spacing: 0.1em; text-transform: uppercase; color: var(--ann-muted); margin-bottom: 0.4em; }
.rows > div { display: flex; justify-content: space-between; gap: 1em; font-size: 0.9rem; padding: 0.1em 0; }
.rows code { font-family: 'JetBrains Mono', monospace; }
.cmt { margin-top: 0.5em; padding-top: 0.4em; border-top: 1px dashed var(--ann-line); font-size: 0.76rem; color: var(--ann-ink-soft); line-height: 1.4; }
.cmt b { color: var(--ann-ember); }
.slidev-layout .key-message { margin: 0.5em 0 0.4em; }
</style>

<!--
[click] The ids. Ask the question out loud and let them answer: "dog - closer
to cat, or closer to car?" Everyone says cat. Then point at the numbers: 5679
is much nearer 8415 than 1841 is... no wait, work it through on the board of
their heads - the ids give you an ordering that has nothing to do with
meaning. Whatever answer the ids give, it is an accident.

[click] The vectors. Now compare them column by column. cat and dog agree in
three of four places. car agrees in none.

Be honest that these particular numbers are invented for the slide. Real ones
have hundreds or thousands of entries and no human-readable meaning per slot.
Say that explicitly - students who go looking will otherwise expect slot one
to be labelled "furriness".

[click] Name it: embedding. Write it down.

[click] The crucial point, and it is the same point as every other "where did
the numbers come from" moment in this lecture: nobody wrote them. This is the
first place to plant that idea, because chapter 7 pays it off.

Likely student question: "How many numbers per word?" Answer: "Depends on the
model. Hundreds to tens of thousands. GPT-3 used 12,288 per token. And the
table has one row per token in the vocabulary - about 50,000 rows - so that
one table alone is over 600 million numbers."

Transition: "If a word is a list of numbers, we can draw it."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 4
zoom: 0.97
---

# Words become places

<span class="eyebrow intuition">Intuition</span>

<div v-click="1" class="key-message">A list of numbers is a <b>position</b>. Similar words end up in similar places.</div>

<div v-click="2">

<VectorMap compact />

</div>

<div v-click="3" class="obs">
  <div>Two numbers gives you a flat map like this. Three gives you a room. Real models use <b>thousands</b> &#8212; which nobody can picture, and you do not need to.</div>
  <div>All that matters is the idea: <b>close together means used in similar ways</b>.</div>
</div>

<div v-click="4" class="transition-line">Careful with the word &#8220;meaning&#8221;. <span class="arrow">The model never learned what a cat <i>is</i>. It learned which words turn up in the same kinds of sentences.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.3em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.45em; }
</style>

<!--
[click] The key message.

[click] The map. Give them a moment. Then narrate: "Animals over here,
vehicles over there. Big things up, small things down. Nobody drew this - it
is what falls out of reading a very large amount of text and noticing which
words behave alike."

[click] The dimension point. The honest framing matters: do not pretend you
can visualise 12,288 dimensions, and do not let them think they are failing
to. Tell them the picture is a two-dimensional shadow of something much
bigger, and that the shadow is enough for today.

[click] The caveat, and say it slowly, because it is the first appearance of
the deck's running honesty theme: distributional meaning is not meaning. The
model knows cat and dog keep similar company. That is genuinely useful and
genuinely not understanding.

Likely student question: "Who decides the axes?" Answer: "Nobody. I picked
these two directions to draw a readable picture. In the real space the
directions are not labelled and mostly do not correspond to anything you
could name - which will matter in chapter 8."

Transition: "Here is the thing that made people sit up when this was
discovered."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 5
---

# Directions mean things

<span class="eyebrow intuition">Intuition</span>

<div v-click="1" class="statement-box" style="margin-top:-0.3em">

<span class="big-mono">sushi &#8722; Japan + Germany &#8776; bratwurst</span>

</div>

<div v-click="2" class="obs">
  <div>Subtracting <code>Japan</code> from <code>sushi</code> leaves something like &#8220;national dish of&#8221;. Add <code>Germany</code> and you land near the German one.</div>
  <div>The <b>direction</b> between two words carries a relationship. That relationship then works on <i>other</i> words.</div>
</div>

<div v-click="3" class="famous">
  You have probably met the famous version: <span class="big-mono">king &#8722; man + woman &#8776; queen</span>
</div>

<div v-click="4">

<Callout>
  <template #misconception>That one is the clean proof that embeddings capture meaning.</template>
  <template #clarification>It is <b>partly a trick</b>. The usual software is <b>forbidden from returning any of the three input words</b> &#8212; so it <i>cannot</i> answer &#8220;king&#8221;. Lift that ban and the top answer is very often just one of the inputs handed back. The relationships are real; that particular demo is doing less work than it appears to. <b>We come back to this properly in chapter 8.</b></template>
</Callout>

</div>

<div v-click="5" class="transition-line">Good enough to build on, not good enough to be smug about. <span class="arrow">Now &#8212; a problem this picture cannot solve.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.45em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-family: 'JetBrains Mono', monospace; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); padding: 0 0.25em; border-radius: 3px; }
.famous { margin: 0.5em 0 0.4em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.slidev-layout .statement-box { padding: 0.35em 1.1em; }
.slidev-layout .callout { font-size: 0.75rem; }
.slidev-layout .callout-row { padding: 0.36em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.4em; }
</style>

<!--
[click] Lead with the sushi one, not the king one. It is memorable, it is
funny, it carries zero classroom risk, and unlike the famous example it
actually survives scrutiny.

[click] Unpack the arithmetic in words: subtract the country, you are left
with the role; add a different country, you get that country's version.

[click] NOW bring up king/man/woman, because most of the room has heard it.

[click] The callout, and this is the slide's real content. The demo is
constrained: the standard implementation excludes the input words from the
candidate answers, because the classical definition of an analogy expects
four different terms. That exclusion is doing a lot of the work. Researchers
(Nissim and colleagues, 2020) showed that when you remove the ban, the top
answer is usually just the third input word again.

Be careful to land BOTH halves: the embedding relationships are real and
useful, AND the famous demo oversells them. Students who only hear half of
this become either credulous or cynical, and both are worse than accurate.

MAKE THE PROMISE: chapter 8, properly, with what the field concluded. Then
actually pay it.

[click] Transition.

Likely student question: "So is the bias stuff in word embeddings fake too?"
Excellent question, and the answer is no: "The bias is real and well
documented. What the researchers showed is that the analogy TEST is a bad
instrument for measuring it - it can manufacture results in either direction.
Real problem, bad thermometer."

Transition: "Now here's something no amount of clever embedding can fix."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 4
---

# The bag-of-words problem

<span class="eyebrow why">The problem</span>

<div class="sents">
  <div v-click="1" class="s"><span class="lbl">A</span>Dog bites man.</div>
  <div v-click="2" class="s"><span class="lbl">B</span>Man bites dog.</div>
</div>

<div v-click="3" class="obs">
  <div><b>Identical</b> words. <b>Identical</b> embeddings. Completely different meaning &#8212; and only one of them is news.</div>
  <div>So far, everything we have built would treat these as the same input. Our machine has a <b>set</b> of words, not a sentence.</div>
</div>

<div v-click="4" class="key-message">We have to tell it <b>where</b> each word sits.</div>

<style>
.sents { display: flex; flex-direction: column; gap: 0.5em; margin: 0.8em 0 0.6em; }
.s {
  font-family: 'Space Grotesk', sans-serif; font-size: 1.7rem; font-weight: 600;
  display: flex; align-items: center; gap: 0.7em;
}
.lbl {
  font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;
  width: 1.7em; height: 1.7em; border-radius: 999px;
  background: var(--ann-indigo-soft); color: var(--ann-indigo);
  display: inline-flex; align-items: center; justify-content: center;
}
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.6em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
A deliberately short, deliberately big slide. It is a hinge, and it should
feel like one.

[click] Read A out loud.
[click] Read B out loud. Wait for the laugh.

[click] Make the point precisely - and this is a genuinely important property
that surprises people: the attention machinery we are about to build is, on
its own, completely blind to order. Feed it the words in any sequence and it
produces the same answers, just shuffled. It sees a SET.

That is not a flaw someone failed to fix; it is a direct consequence of how
the arithmetic works, as they will see in chapter 4.

[click] The fix, stated as a requirement.

Likely student question: "Couldn't you just feed the words in order?" Answer:
"That's what the previous generation of models did - one word at a time, in
order. It works, and it's slow, because you can't do step five until you've
done step four. The whole speed advantage of this design comes from doing
every position at once. So we keep the parallelism and pay for it by writing
the position into the numbers."

Transition: "And the fix is almost comically blunt."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 5
---

# Just add the position in

<span class="eyebrow math">Mechanism</span>

<div class="posmath">
  <div v-click="1" class="pr">
    <span class="pl">what the word is</span>
    <span class="pv">[ 0.8, 0.2, 0.9, 0.1 ]</span>
  </div>
  <div v-click="2" class="pr plus"><span class="pl"></span><span class="pv">+</span></div>
  <div v-click="2" class="pr">
    <span class="pl">where it sits (position 3)</span>
    <span class="pv">[ 0.1, &#8722;0.3, 0.2, 0.4 ]</span>
  </div>
  <div v-click="3" class="pr eq">
    <span class="pl">what goes into the machine</span>
    <span class="pv res">[ 0.9, &#8722;0.1, 1.1, 0.5 ]</span>
  </div>
</div>

<div v-click="4" class="obs">
  <div>One vector now carries <b>both</b> facts at once. The same word in a different slot becomes a genuinely different input.</div>
  <div>It looks like it should destroy the meaning. It does not &#8212; there is an enormous amount of room in a few thousand dimensions, and training learns to read the two parts apart.</div>
</div>

<div v-click="5" class="transition-line">Modern models do this by <b>rotating</b> the vectors by an angle that depends on position, rather than adding &#8212; but the job is the same. <span class="arrow">Tell the machine where the words are.</span></div>

<style>
.posmath { display: flex; flex-direction: column; gap: 0.12em; margin: 0.5em 0; }
.pr { display: grid; grid-template-columns: 15em 1fr; align-items: baseline; gap: 1.2em; }
.pl { font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--ann-muted); text-align: right; }
.pv { font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-variant-numeric: tabular-nums; }
.pr.plus .pv { color: var(--ann-muted); }
.pr.eq { margin-top: 0.3em; padding-top: 0.4em; border-top: 2px solid var(--ann-ink); }
.pv.res { color: var(--ann-indigo); font-weight: 700; }
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.7em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
[click] The word vector.
[click] A second vector that depends only on the SLOT, not the word. Position
three always contributes the same thing, whatever word is in it.
[click] Add them. Component by component. That's it. That is the whole fix.

Expect scepticism here, and welcome it - somebody will say "but you've just
corrupted the meaning". That is the right instinct, so answer it properly:

[click] In four dimensions, yes, it would be a mess. In twelve thousand there
is room for both signals to coexist, and because the position part is the
same every time, the rest of the machine can learn to separate them. It is
less elegant than it sounds and it works better than it deserves to.

[click] The modern footnote, worth one sentence and no more: almost every
current open model - Llama, Qwen, Mistral, Gemma - uses rotation instead of
addition, which makes what the machine sees depend on the DISTANCE between
two words rather than their absolute slots. Same job, better behaved. Do not
derive it; just make sure nobody leaves thinking the sine-wave picture they
will find online is the current state of the art.

Likely student question: "What if the sentence is longer than any position it
was trained on?" Answer: "Then it degrades, sometimes badly. Extending that
limit is an active research area, and it's why models advertise a context
length - we'll meet that in chapter 6."

Transition: "Now every word is a vector that knows what it is and where it
is. Which finally lets us ask the interesting question."
-->

---
chapter: '2 · Turning words into numbers'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 2 &#183; takeaway</span>

<PipelineMap :highlight="['tokens','embed','position']" />

<div v-click="1" class="recap">
  <div><b>Tokens</b> became <b>vectors</b> &#8212; lists of numbers where nearby means &#8220;used alike&#8221;.</div>
  <div><b>Position</b> was folded in, so word order survives.</div>
  <div>Every one of those numbers was <b>learned</b>, not written.</div>
</div>

<div v-click="2" class="transition-line">But every word is still sitting on its own. <span class="arrow">And the meaning of a word depends on the <i>other</i> words. That is chapter 3.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.6em; font-size: 0.9rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Thirty seconds. Point at the three lit boxes.

[click] The three-line recap. Say the third line with emphasis - it is the
one that keeps coming back, and by chapter 7 they should be expecting it.

[click] The hand-off, and make the problem vivid before you leave: "Right
now, the vector for 'bank' is the same whether I'm talking about a river or a
mortgage. Every word is frozen at its dictionary meaning, sitting alone. That
is obviously not how language works."

Transition: "So let's look at what a word's neighbours do to it."
-->
