---
layout: section
chapter: '6 · The knobs you actually turn'
---

# Chapter 6

## The knobs you actually turn

<div v-click class="thesis" style="margin-top:0.8em">None of these change the model. Every one of them changes how we <i>pick</i> from what the model already said.</div>

<!--
Twenty seconds, but sell this chapter: "This is the chapter you can use on
Monday. If you've ever seen a slider called temperature in some AI tool and
wondered what it does, the next fifteen minutes are for you."

State the thesis and promise to prove it - you will, with one line of real
library code.

Transition: "The model has handed us a list of odds. Somebody has to pick."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
---

# Always take the best one?

<span class="eyebrow generation">Greedy vs sampling</span>

<div class="two">
  <div v-click="1" class="cw">
    <div class="ch">Greedy</div>
    <div class="cs">Always take the highest number.</div>
    <div class="cb"><b>blue</b>, every time. Same prompt, same answer, forever.</div>
    <div class="cc good">Predictable. Safe.</div>
    <div class="cc bad">Repetitive, and often oddly flat.</div>
  </div>
  <div v-click="2" class="cw">
    <div class="ch">Sampling</div>
    <div class="cs">Roll a weighted die.</div>
    <div class="cb"><b>blue</b> 80 times in 100, <b>clear</b> 10, <b>dark</b> 5 &#8230;</div>
    <div class="cc good">Varied. Feels alive.</div>
    <div class="cc bad">Sometimes picks something silly.</div>
  </div>
</div>

<div v-click="3" class="obs">This is why the same question can give you a different answer twice. <b>Not a bug</b> &#8212; a die roll.</div>

<div v-click="4" class="obs">And here is the surprise: <b>always taking the most likely word produces bad writing.</b> Real human text is not the most probable text &#8212; it is full of choices that were only fairly likely. Greedy output reads flat and loops.</div>

<div v-click="5" class="transition-line">So we sample. <span class="arrow">And now we need a way to control <i>how adventurous</i> the die is.</span></div>

<style>
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1em; margin: 0.4em 0; }
.cw { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.55em 0.9em; background: var(--ann-paper-raised); }
.ch { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.05rem; color: var(--ann-indigo); }
.cs { font-size: 0.85rem; color: var(--ann-ink); margin: 0.15em 0 0.3em; }
.cb { font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: var(--ann-ink-soft); margin-bottom: 0.35em; }
.cb b { color: var(--ann-circuit); }
.cc { font-size: 0.75rem; padding-left: 1.1em; position: relative; }
.cc::before { position: absolute; left: 0; }
.cc.good::before { content: '\2713'; color: var(--ann-circuit); }
.cc.bad::before { content: '\2715'; color: var(--ann-ember); }
.obs { margin-top: 0.4em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
[click] Greedy. Deterministic, which sounds ideal.
[click] Sampling. A weighted die - and stress the weighting: it is not random
between the options, it is random IN PROPORTION.

[click] Answer the question every user has: why did it say something
different the second time? Because somebody rolled a die. It is a design
choice, not a malfunction.

[click] The counter-intuitive research result, and it is worth dwelling on:
always picking the most likely next word produces noticeably worse text. It
gets repetitive and it loops. Human writing is full of moderately-likely
choices; text made only of maximally-likely ones reads like a form letter.
Students find this genuinely surprising and it is a nice demonstration that
"best" is not a well-defined goal here.

[click] Motivate the knob.

Likely student question: "Then why does anything use greedy?" Answer: "When
you want the same input to give the same output every time - code generation,
extraction, anything you'll test. And for maths, where you want the single
most likely answer, not an interesting one."

Transition: "Temperature."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 4
---

# Temperature: how sharp the odds are

<span class="eyebrow generation">Temperature</span>

<div v-click="1">

<ProbBars :compare="[0.5, 1.0, 1.5]" compact />

</div>

<div v-click="2" class="obs">
  <div>Same model. Same prompt. Same logits. <b>Only the division changed.</b></div>
  <div><b>Low</b> temperature sharpens: the leader takes almost everything. <b>High</b> temperature flattens: the others get a real chance.</div>
</div>

<div v-click="3" class="ends">
  <div><span class="et">T &#8594; 0</span>the sharpest possible &#8212; this <b>is</b> greedy</div>
  <div><span class="et">T = 1</span>the model&#8217;s own odds, untouched</div>
  <div><span class="et">T &#8594; &#8734;</span>everything flattens towards pure random</div>
</div>

<div v-click="4" class="transition-line">Same knob, three behaviours. <span class="arrow">And greedy turns out to be one end of it, not a separate thing.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.45em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.ends { display: flex; flex-direction: column; gap: 0.18em; margin-top: 0.45em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.ends > div { display: flex; align-items: baseline; gap: 0.9em; }
.et { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--ann-indigo); font-weight: 600; flex: 0 0 5em; }
.ends b { color: var(--ann-ember); }
</style>

<!--
[click] Three panels, SHARED SCALE. Say that out loud - "the x-axis is the
same on all three, so you're seeing a real comparison." If the scales
differed, the comparison would be meaningless, and plenty of published
versions of this picture get it wrong.

[click] The crucial fact, stated as bluntly as possible: same model, same
prompt, same logits. The only thing that changed is a division. Nothing about
the network moved.

[click] The three regimes. The T to 0 case is the nice one: greedy decoding
is not a separate algorithm, it is the limit of this one. Two things they
learned separately turn out to be one thing.

[click] Transition.

If you have network and a projector that can take it, THIS is the moment for
a live demo - the Transformer Explainer site from Georgia Tech runs GPT-2 in
the browser with a temperature slider, and dragging it from 0.3 to 10 while
the bars visibly flatten is the best sixty seconds available. Have the static
version as a fallback; halls have no wifi surprisingly often.

Transition: "The maths, for anyone who wants it - and it is one division."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
---

# Temperature does not change the model

<span class="eyebrow math">Proof, more or less</span>

<div v-click="1" class="plain">Divide every logit by T, then softmax as usual.</div>

<div v-click="2" class="formula">

$$P_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$$

</div>

<div v-click="3" class="codebox">
  <div class="cl">the actual implementation, from a real library</div>

```python
scores = scores / self.temperature
```

</div>

<div v-click="4" class="obs">
  <div>That is the whole thing. It happens <b>after</b> the network has finished, on its way out.</div>
  <div>It does not touch the <b>weights</b>, the <b>training</b>, the <b>knowledge</b>, or the <b>architecture</b>. The model is <b>frozen</b>.</div>
</div>

<div v-click="5">

<Callout>
  <template #misconception>Turning up the temperature makes the model more creative.</template>
  <template #clarification>It makes the output <b>less determined by the training data</b>, which is not the same thing. Controlled studies find higher temperature is weakly linked to novelty and <b>more strongly linked to incoherence</b> &#8212; and that changing it across the normal range makes <b>no significant difference to problem-solving</b> at all. It is a <b>variety</b> knob, not a quality knob.</template>
</Callout>

</div>

<style>
.plain { font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 500; color: var(--ann-indigo); text-align: center; margin: 0.3em 0; }
.formula { text-align: center; margin: 0.1em 0 0.35em; }
.formula :deep(.katex-display) { margin: 0.15em 0; font-size: 0.95em; }
.codebox { margin: 0.3em 0; }
.cl { font-family: 'JetBrains Mono', monospace; font-size: 0.66rem; letter-spacing: 0.08em; text-transform: uppercase; color: var(--ann-muted); margin-bottom: 0.15em; }
.codebox :deep(pre) { font-size: 0.9rem !important; }
.obs { display: flex; flex-direction: column; gap: 0.25em; margin-top: 0.3em; font-size: 0.8rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .callout { font-size: 0.73rem; }
.slidev-layout .callout-row { padding: 0.32em 0.9em; }
</style>

<!--
[click] The sentence.
[click] The formula - note it is LITERALLY the softmax from chapter 4 with a
division inserted. Point at the /T and say "that is the only new thing on
this slide."

[click] The line of real code. This is the most convincing thing you can put
in front of a sceptic: one division, in the library everybody uses, applied
after the model has finished. Let it sit there for a second.

[click] Spell out the four things it does NOT touch. Students genuinely
believe temperature makes the model "think differently" - kill it here.

[click] The callout. The clarification is backed by actual studies and it is
worth naming them as studies rather than as opinion: one found temperature
weakly correlated with novelty and more strongly with incoherence; another
tested nine models across the 0 to 1 range and found no statistically
significant effect on problem-solving.

MUST SAY: "So if someone tells you to turn the temperature up to make the
model smarter, they've misunderstood what it does."

Likely student question: "What should I set it to?" Honest answer: "Low -
0 to 0.3 - for anything with a right answer. Around 1 for conversation. Above
1 mostly when you want surprise more than sense. And most of the time the
default is fine, which is a boring but true answer."

Transition: "Temperature reshapes the odds. The other two knobs do something
different - they delete options."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
---

# Top-K: keep the best few

<span class="eyebrow generation">Top-K</span>

<div class="key-message" style="margin-top:-0.4em">Throw away everything except the <b>K</b> most likely tokens. Then sample from what is left.</div>

<div v-click="1">

<ProbBars :top-k="3" compact />

</div>

<div v-click="2" class="obs">
  <div>With <b>K = 3</b>, <code>green</code> and <code>red</code> are removed <b>entirely</b> &#8212; not made unlikely, <b>deleted</b>. Their probability becomes exactly zero.</div>
  <div>The survivors are rescaled so they add to 1 again: <span class="num">0.80</span> becomes <span class="num">0.85</span>.</div>
</div>

<div v-click="3" class="obs">
  <div><b>Why bother?</b> Because that long tail of 50,000 tokens holds a lot of probability between them. Generate 500 words and you <i>will</i> eventually roll one of them &#8212; and one absurd word derails everything after it.</div>
</div>

<div v-click="4" class="statement-box">Temperature changes the <b>shape</b> of the distribution. Top-K changes <b>which options exist at all</b>.</div>

<div v-click="5" class="transition-line">Useful. But <b>K</b> is a fixed number, and distributions are not all the same shape. <span class="arrow">That is the problem Top-P solves.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-family: 'JetBrains Mono', monospace; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); padding: 0 0.25em; border-radius: 3px; }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.92rem; margin-top: 0.4em; }
.slidev-layout .key-message { margin: 0.3em 0 0.35em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The chart with the cut drawn. The struck-through, greyed rows make
"deleted" visible.

[click] Stress DELETED, not discouraged. This is the structural difference
from temperature and the thing to get right: temperature can make a token
almost impossible but never impossible. Top-K makes it impossible.

[click] The motivation. Do the arithmetic out loud, because it is
persuasive: fifty thousand tokens each holding a tiny probability still add
up to a few per cent, and a few per cent over hundreds of draws is a
near-certainty. One genuinely absurd token, and everything after it is
conditioned on the absurdity.

[click] The one-line contrast: shape versus support. This is the sentence
that makes the two knobs distinct in their heads.

[click] Set up the weakness: K is fixed, distributions are not.

Transition: "Same idea, smarter rule."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
---

# Top-P: keep enough to cover the odds

<span class="eyebrow generation">Top-P &#183; nucleus sampling</span>

<div class="key-message" style="margin-top:-0.4em">Take the best tokens until their probabilities add up to <b>P</b>. Keep those. Bin the rest.</div>

<div v-click="1">

<ProbBars :top-p="0.9" compact />

</div>

<div v-click="2" class="cum">
  <span>blue <b>0.80</b></span><span class="arr">&#8594;</span>
  <span>+ clear = <b>0.90</b></span><span class="arr">&#8594;</span>
  <span class="stop">that&#8217;s 90%. Stop.</span>
</div>

<div v-click="3" class="obs">
  <div>On <b>this</b> distribution, P = 0.9 keeps just <b>two</b> tokens &#8212; because the model was already confident, and two words were enough to cover nine tenths of the odds.</div>
</div>

<div v-click="4" class="obs">
  <div>On a <b>flat</b> distribution &#8212; &#8220;write a funny story about a cat&#8221;, where thousands of continuations are reasonable &#8212; the same P = 0.9 keeps <b>six of eight</b>, or hundreds of tokens.</div>
</div>

<div v-click="5" class="transition-line">Same setting, different behaviour, depending on how sure the model is. <span class="arrow">That is the whole point: it <b>adapts</b>. Top-K cannot.</span></div>

<style>
.cum { display: flex; align-items: baseline; gap: 0.6em; margin: 0.45em 0 0.2em; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; flex-wrap: wrap; }
.cum b { color: var(--ann-indigo); }
.arr { color: var(--ann-muted); }
.stop { color: var(--ann-ember); font-weight: 600; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.3em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.35em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The chart, showing two kept and three cut.

[click] Walk the running total out loud: eighty, plus ten is ninety, stop.
Very concrete, and it makes "cumulative" mean something without the word.

[click] The result on a confident distribution: two tokens.

[click] The result on an uncertain one: many. THIS is the idea. The same
number behaves differently depending on the model's confidence, which is
exactly what you want - be strict when it knows, permissive when it doesn't.

[click] Name the property: it adapts. And say plainly that Top-K cannot,
because K is a count and counts don't know anything about confidence.

Likely student question: "Can you use both?" Answer: "Yes, and people do -
top-k first as a hard ceiling, then top-p. Belt and braces."

Transition: "Put them on the same distribution and the difference is
obvious."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 4
---

# The same five words, two rules

<span class="eyebrow generation">Top-K vs Top-P</span>

<div class="vs">
  <div v-click="1" class="vc">
    <div class="vh">Top-K = 3</div>
    <ProbBars :top-k="3" compact />
    <div class="vn">&#8220;Give me the best <b>three</b>.&#8221;<br>Always three, whatever the odds look like.</div>
  </div>
  <div v-click="2" class="vc">
    <div class="vh">Top-P = 0.9</div>
    <ProbBars :top-p="0.9" compact />
    <div class="vn">&#8220;Give me enough to cover <b>90%</b>.&#8221;<br>Here that is two. Elsewhere it might be two hundred.</div>
  </div>
</div>

<div v-click="3" class="obs">Identical model, identical prompt, identical distribution &#8212; and the two rules keep <b>different sets of words</b>. Neither is wrong. They answer different questions.</div>

<div v-click="4" class="transition-line">Top-K asks <b>&#8220;how many?&#8221;</b>. Top-P asks <b>&#8220;how much?&#8221;</b>. <span class="arrow">Temperature asks neither &#8212; it asks &#8220;how sharp?&#8221;</span></div>

<style>
.vs { display: grid; grid-template-columns: 1fr 1fr; gap: 1.3em; margin: 0.3em 0; }
.vh { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; color: var(--ann-indigo); margin-bottom: 0.2em; }
.vn { margin-top: 0.3em; font-size: 0.78rem; color: var(--ann-ink-soft); line-height: 1.4; }
.vn b { color: var(--ann-ember); }
.obs { margin-top: 0.4em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
The slide that makes the distinction stick, because it is the SAME numbers
on both sides. Most explanations use a different example for each and the
contrast evaporates.

[click] Top-K keeps three.
[click] Top-P keeps two. Point at the difference: dark survives on the left
and dies on the right, from identical input.

[click] Neither is wrong - they are answering different questions. Say that,
because students want one of them to be the correct one.

[click] The three-way summary in six words. Have them write it down:
how many, how much, how sharp.

Transition: "All three at once, and where they sit."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
---

# Two completely different kinds of number

<span class="eyebrow structure">The distinction that matters</span>

<div class="split">
  <div v-click="1" class="sc learned">
    <div class="sh">Learned parameters</div>
    <div class="ss">The model found these, over months, from data.</div>
    <div class="sl">
      <span>embedding table</span><span>W<sub>Q</sub>, W<sub>K</sub>, W<sub>V</sub> &#215; every head</span>
      <span>feed-forward weights</span><span>biases</span>
    </div>
    <div class="sn"><b>175,000,000,000</b> of them, for GPT-3.<br>You cannot change these. They <i>are</i> the model.</div>
  </div>
  <div v-click="2" class="sc chosen">
    <div class="sh">Generation settings</div>
    <div class="ss">You choose these, per request, in a fraction of a second.</div>
    <div class="sl">
      <span>temperature</span><span>top_k</span>
      <span>top_p</span><span>max_tokens</span>
      <span>stop</span><span>seed</span>
    </div>
    <div class="sn"><b>Six</b> of them, give or take.<br>They change <i>how we pick</i>, never <i>what it knows</i>.</div>
  </div>
</div>

<div v-click="3" class="analogy">
  <b>A student sitting an exam.</b> The learned parameters are everything they know.
  The generation settings are the instruction on the paper: &#8220;answer briefly&#8221;, &#8220;give several possibilities&#8221;, &#8220;be imaginative&#8221;.
</div>

<div v-click="4" class="obs">The instruction changes the answer. <b>It does not change the student.</b></div>

<div v-click="5" class="transition-line">Confusing these two is the commonest mistake people make about AI settings. <span class="arrow">One last limit, and then what is inside the box.</span></div>

<style>
.split { display: grid; grid-template-columns: 1fr 1fr; gap: 1.1em; margin: 0.35em 0; }
.sc { border: 1px solid var(--ann-line); border-radius: 0.5em; padding: 0.5em 0.85em; background: var(--ann-paper-raised); }
.sc.learned { border-left: 4px solid var(--ann-circuit); }
.sc.chosen { border-left: 4px solid var(--ann-ember); }
.sh { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.98rem; color: var(--ann-indigo); }
.ss { font-size: 0.76rem; color: var(--ann-ink-soft); margin: 0.1em 0 0.3em; }
.sl { display: grid; grid-template-columns: 1fr 1fr; gap: 0.05em 0.6em; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: var(--ann-ink); }
.sn { margin-top: 0.35em; padding-top: 0.3em; border-top: 1px dashed var(--ann-line); font-size: 0.74rem; color: var(--ann-ink-soft); }
.sn b { color: var(--ann-indigo); }
.analogy { margin-top: 0.45em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.analogy b { color: var(--ann-indigo); }
.obs { margin-top: 0.25em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-ember); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
The word "parameters" gets used for both of these, constantly, and it causes
real confusion - people talk about "tuning the parameters" meaning a slider,
and about "a 70-billion-parameter model" meaning weights, in the same
sentence.

[click] Learned. Enormous, fixed, produced by training.
[click] Chosen. Six-ish, per request, produced by you.

[click] The exam analogy. It's a good one because it separates knowledge from
delivery cleanly, and every student in the room has lived it.

[click] The punchline sentence.

[click] Transition.

Likely student question: "What's seed?" Answer: "The die roll. Same seed,
same rolls, same output - it's how you make sampling reproducible without
going all the way to greedy. Handy when you're testing something."

And max_tokens and stop are worth ten seconds each: max_tokens is just "stop
after this many", and stop is "stop when you produce this text". Both are
about ending, not about choosing - which is why nobody finds them confusing.

Transition: "One more limit, and it's the one people hit."
-->

---
chapter: '6 · The knobs you actually turn'
clicks: 5
zoom: 0.95
---

# The context window

<span class="eyebrow generation">The limit you will meet</span>

<div class="key-message" style="margin-top:-0.4em">There is a hard cap on how many tokens the model can look at <b>at once</b>.</div>

<div v-click="1" class="ctx">
  <div class="cbox">
    <div class="cbh">CONTEXT WINDOW</div>
    <div class="crow">the system instructions</div>
    <div class="crow">everything said earlier in the conversation</div>
    <div class="crow">any documents you pasted</div>
    <div class="crow">your actual question</div>
    <div class="crow out">&#8230; and the answer has to fit in here too</div>
  </div>
</div>

<div v-click="2" class="obs">
  <div>Roughly: <span class="big-mono">input + output &#8804; the limit</span>. Fill it with a document and there is no room left to reply.</div>
  <div>Go past it and something has to be <b>dropped</b> &#8212; usually the oldest part of the conversation. Which is why a long chat can seem to <b>forget</b> the beginning.</div>
</div>

<div v-click="3" class="obs">
  <div>Remember chapter 4: every token attends to every token. Double the context and you <b>quadruple</b> the comparisons. That is why this limit exists and why it is expensive to raise.</div>
</div>

<div v-click="4" class="obs">
  <div>And remember chapter 1: the limit is counted in <b>tokens</b>, not words &#8212; so the same conversation costs a Korean speaker three times more of it.</div>
</div>

<div v-click="5" class="transition-line">Two chapters of machinery, cashed in as one practical limit. <span class="arrow">Now &#8212; what else is in the box, and where did all those numbers come from?</span></div>

<style>
.ctx { margin: 0.4em 0; }
.cbox { border: 2px solid var(--ann-indigo); border-radius: 0.5em; padding: 0.45em 0.9em; background: var(--ann-indigo-soft); max-width: 34em; }
.cbh { font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; letter-spacing: 0.12em; color: var(--ann-indigo); margin-bottom: 0.25em; }
.crow { font-size: 0.83rem; color: var(--ann-ink); padding: 0.05em 0; }
.crow.out { color: var(--ann-ember); font-style: italic; margin-top: 0.2em; padding-top: 0.25em; border-top: 1px dashed var(--ann-indigo); }
.obs { display: flex; flex-direction: column; gap: 0.25em; margin-top: 0.35em; font-size: 0.81rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.3em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.35em; padding-top: 0.3em; }
</style>

<!--
[click] The box, with everything that competes for space inside it. Students
are usually surprised that the system prompt and the whole conversation are
in there - they think of the window as "how long a question I can ask".

[click] The budget, and the forgetting. This explains a behaviour every one
of them has experienced.

[click] The quadratic cost, and this is a genuine payoff from chapter 4 - if
every token attends to every token, the work grows as the square. Say it as a
consequence they could have predicted, because they could have.

[click] The callback to chapter 1. Two chapters converging on one practical
fact is worth pointing out explicitly; it shows the lecture was built rather
than listed.

[click] Transition into chapter 7.

Likely student question: "Modern models have million-token contexts though?"
Answer: "They do, and getting there took real engineering to dodge that
square - and there's good evidence models get less reliable at using the
middle of a very long context even when it technically fits. Big window is
not the same as good use of it."

Transition: "We've been treating the middle of the machine as a box. Let's
open it."
-->
