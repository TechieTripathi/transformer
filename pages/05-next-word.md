---
layout: section
chapter: '5 · From numbers to the next word'
---

# Chapter 5

## From numbers to the next word

<div v-click class="thesis" style="margin-top:0.8em">The machine never chooses an answer. It produces a <i>probability for every word it knows</i>, and then something else does the choosing.</div>

<!--
Twenty seconds. But flag the thesis as the most misunderstood idea about
these systems: "If you take one idea from the second half of this lecture,
take this one. The model does not answer your question. It reports odds."

Transition: "Here's what actually comes out of the machine."
-->

---
chapter: '5 · From numbers to the next word'
clicks: 5
---

# One score for every word it knows

<span class="eyebrow generation">Logits</span>

<div class="key-message" style="margin-top:-0.4em">After the last layer, the final vector is compared against <b>every token in the vocabulary</b>. About 50,000 of them.</div>

<div v-click="1" class="logits">
  <div class="lh">&#8220;The sky is &#8230;&#8221;</div>
  <div class="lr"><span class="lt">blue</span><span class="lv">3.9</span></div>
  <div class="lr"><span class="lt">clear</span><span class="lv">1.8</span></div>
  <div class="lr"><span class="lt">dark</span><span class="lv">1.1</span></div>
  <div class="lr"><span class="lt">green</span><span class="lv">0.6</span></div>
  <div class="lr"><span class="lt">red</span><span class="lv">0.2</span></div>
  <div class="lr dim"><span class="lt">&#8230; and 50,000 more</span><span class="lv">&#8230;</span></div>
</div>

<div v-click="2" class="obs">
  <div>These raw scores have a name: <b>logits</b>. They are not probabilities &#8212; they do not add up to anything and they can be negative.</div>
  <div>Every token gets one. Including <code>zebra</code>, <code>&#8901;the</code>, and <code>GoldMagikarp</code>.</div>
</div>

<div v-click="3" class="statement-box">Sound familiar? It is the <b>same dot product</b> as chapter 4 &#8212; the final vector against each word&#8217;s entry in the embedding table.</div>

<div v-click="4" class="obs">
  <div>And the same fix applies: to turn scores into shares, use <b>softmax</b>.</div>
</div>

<div v-click="5" class="transition-line">One operation, used twice, for two completely different jobs. <span class="arrow">That is most of what a transformer is.</span></div>

<style>
.logits { margin: 0.4em 0; font-family: 'JetBrains Mono', monospace; }
.lh { font-size: 0.95rem; color: var(--ann-ink-soft); margin-bottom: 0.3em; }
.lr { display: grid; grid-template-columns: 12em 5em; font-size: 1rem; padding: 0.02em 0; }
.lv { text-align: right; font-variant-numeric: tabular-nums; color: var(--ann-indigo); font-weight: 600; }
.lr.dim { color: var(--ann-muted); }
.lr.dim .lv { color: var(--ann-muted); font-weight: 400; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-family: 'JetBrains Mono', monospace; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); padding: 0 0.25em; border-radius: 3px; }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.88rem; margin-top: 0.4em; }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The five logits. Be clear these are the top five of fifty thousand -
students imagine a shortlist, and there is no shortlist.

[click] Name them. Logits. Flag what they are NOT: not probabilities, no
constraint to sum to anything, can be negative.

[click] The connection back to chapter 4. This is worth a beat, because it is
genuinely elegant and it makes the machine feel smaller and more
comprehensible: the same "compare two vectors with a dot product" operation
does BOTH jobs - deciding which words to look at, and deciding which word to
say. One idea, reused.

[click] So the same softmax applies.

[click] The observation that a transformer is a small number of ideas used
over and over. Students who feel overwhelmed find this genuinely reassuring,
and it is true.

Likely student question: "Does it really score all 50,000 every single time?"
Answer: "Yes, every token generated. That's a 50,000-way dot product per word
- and one reason these things are expensive to run."

Transition: "Softmax turns those into odds."
-->

---
chapter: '5 · From numbers to the next word'
clicks: 4
---

# It does not know the answer. It has odds.

<span class="eyebrow generation">The distribution</span>

<div v-click="1">

<ProbBars caption="The same five words, after softmax. Now they are shares of 1." />

</div>

<div v-click="2" class="obs">
  <div>The machine is not saying &#8220;blue&#8221;. It is saying <b>blue is 80% likely, clear is 10%, dark is 5%</b> &#8212; and something for all 50,000 others.</div>
</div>

<div v-click="3">

<Callout>
  <template #misconception>The model works out the answer and then tells you.</template>
  <template #clarification>There is <b>no answer inside it</b>. There is a distribution &#8212; a number for every word it knows. What you experience as &#8220;the model said blue&#8221; is a <b>separate step</b> that picks one word out of that distribution. We will spend all of chapter 6 on that step, because it is the part you can control.</template>
</Callout>

</div>

<div v-click="4" class="transition-line">This is the single most useful idea for understanding how these things behave. <span class="arrow">&#8220;Knowing&#8221; is a high number, not a fact.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .callout { font-size: 0.77rem; }
.slidev-layout .callout-row { padding: 0.4em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
[click] The bars. Let them look. Point out that this is the SAME information
as the logits slide, just normalised.

[click] Say the distribution out loud as odds, not as an answer.

[click] The callout - and this is the chapter's thesis, so read both halves
slowly. The clarification does two things: it removes the idea of an answer,
and it makes a promise about chapter 6.

[click] The closing line is the one to have them write down. "Knowing is a
high number, not a fact" is the sentence that makes hallucination, confident
wrongness, and temperature all make sense later.

Likely student question: "But if I ask it what 2+2 is, it's certain, right?"
Answer: "It'll put a very high number on '4' - maybe 0.9999. That's not
certainty, it's a high number. And the interesting cases are exactly the ones
where it puts 0.9 on something false, which happens, and looks identical from
the outside."

Transition: "So it picks blue. Then what?"
-->

---
chapter: '5 · From numbers to the next word'
clicks: 5
---

# One word at a time, and then again

<span class="eyebrow generation">Generation</span>

<div class="gen">
  <div v-click="1" class="gr"><span class="gi">in</span><span class="gt">The sky is</span><span class="ga">&#8594;</span><span class="go">blue</span></div>
  <div v-click="2" class="gr"><span class="gi">in</span><span class="gt">The sky is <b>blue</b></span><span class="ga">&#8594;</span><span class="go">today</span></div>
  <div v-click="3" class="gr"><span class="gi">in</span><span class="gt">The sky is <b>blue today</b></span><span class="ga">&#8594;</span><span class="go">.</span></div>
</div>

<div v-click="4" class="obs">
  <div>Each output word is <b>glued onto the input</b> and the whole thing runs again. Fifty thousand scores, softmax, pick one. Every single word.</div>
  <div>The typing effect you see in a chatbot is <b>not an animation</b>. That is the actual speed of the actual machine.</div>
</div>

<div v-click="5" class="statement-box">

It reads like you scan a page &#8212; all at once. It writes like you text &#8212; one piece at a time, <b>and it cannot go back</b>.

</div>

<style>
.gen { display: flex; flex-direction: column; gap: 0.35em; margin: 0.5em 0; }
.gr { display: grid; grid-template-columns: 2.5em 20em 2em 1fr; align-items: baseline; gap: 0.6em; }
.gi { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; text-transform: uppercase; color: var(--ann-muted); }
.gt { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; }
.gt b { color: var(--ann-circuit); }
.ga { color: var(--ann-muted); font-size: 1.1rem; }
.go { font-family: 'Space Grotesk', sans-serif; font-size: 1.2rem; font-weight: 700; color: var(--ann-ember); }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.45em 1em; font-size: 1rem; margin-top: 0.5em; }
</style>

<!--
[click][click][click] Three steps, and narrate the growth: the output becomes
part of the input. Emphasise that the ENTIRE machine runs again from scratch
for each word - all the attention, all the layers.

[click] Two observations. The second one always gets a reaction: the
streaming text in ChatGPT is not a designed effect to look futuristic, it is
the machine working. Worth saying because it makes the whole thing concrete.

[click] The read/write asymmetry. This is the one that fixes the commonest
confusion in the room - "does it read the whole thing at once or not?" Both,
depending on which half you mean.

The "cannot go back" clause is worth dwelling on for ten seconds: once a word
is out, it is part of the input forever. A model that starts an answer badly
is now conditioned on its own bad start. That explains a LOT of observed
behaviour, including why asking it to "think step by step" helps - you are
giving it more input to condition on before it has to commit.

Likely student question: "Could it plan ahead?" Answer: "Not in this design -
each step only produces the next token. Though there's a subtlety: because it
predicts from everything so far, it can be trained to produce text that
happens to set itself up well. That's roughly what the 'reasoning' models are
doing - using their own output as scratch paper."

Transition: "The formal version of what we just did, in one line."
-->

---
chapter: '5 · From numbers to the next word'
clicks: 4
---

# The whole job, in one line

<span class="eyebrow math">Next-token prediction</span>

<div v-click="1" class="plain">

Given everything so far, how likely is each possible next token?

</div>

<div v-click="2" class="formula">

$$P(\text{next token} \mid \text{everything before it})$$

</div>

<div v-click="3" class="obs">
  <div>That is the <b>entire</b> training objective. Not &#8220;be helpful&#8221;, not &#8220;be correct&#8221;, not &#8220;understand the question&#8221;. Just: <b>what comes next?</b></div>
  <div>Everything else &#8212; answering questions, writing code, translating, summarising &#8212; is a <b>side effect</b> of getting extremely good at that one task on a very large amount of text.</div>
</div>

<div v-click="4" class="transition-line">Which is either underwhelming or astonishing, depending on how long you look at it. <span class="arrow">It is worth looking at it for a while.</span></div>

<style>
.plain { font-family: 'Space Grotesk', sans-serif; font-size: 1.3rem; font-weight: 500; color: var(--ann-indigo); text-align: center; margin: 0.6em 0; }
.formula { text-align: center; margin: 0.3em 0 0.5em; }
.formula :deep(.katex-display) { margin: 0.2em 0; }
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.5em; font-size: 0.88rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
Plain English first. Again. Always.

[click] The sentence.
[click] The same sentence in symbols. Say "that vertical bar just means
'given'." Three seconds, and a chunk of the room stops being frightened of
the notation.

[click] The two observations. The second is the big one and deserves a real
pause: nobody programmed question-answering. Nobody wrote a translation
module. All of it fell out of predicting the next chunk of text, at
enormous scale.

Resist the temptation to over-claim here. The honest position is that this is
surprising and not fully understood, and saying so is better than either
"it's just autocomplete" or "it understands".

[click] Give them the ambivalence deliberately. A sixteen-year-old who leaves
thinking "that's suspiciously simple and also somehow it works" has the same
view as most researchers.

Transition: "Let's watch it do one properly."
-->

---
chapter: '5 · From numbers to the next word'
clicks: 4
---

# One complete example

<span class="eyebrow generation">End to end</span>

<div class="q">&#8220;What is the capital of France?&#8221;</div>

<div v-click="1">

<PipelineMap :dim-others="false" compact />

</div>

<div v-click="2">

<ProbBars
  :tokens="['Paris','London','Berlin','Rome','other']"
  :probs="[0.95,0.01,0.01,0.01,0.02]"
  compact />

</div>

<div v-click="3" class="obs">Every box on that map ran. Tokens, vectors, position, ninety-six layers of attention and feed-forward, fifty thousand scores, softmax. <b>To produce this list.</b></div>

<div v-click="4" class="transition-line">And then a separate step picks <b>Paris</b>. <span class="arrow">Which brings us to the part you can actually control.</span></div>

<style>
.q { font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--ann-indigo); margin: -0.2em 0 0.3em; }
.obs { margin-top: 0.4em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
The consolidation slide for the first half of the lecture.

[click] The whole map, undimmed for the first time. "All of it. Every box."

[click] The result: a distribution, overwhelmingly on Paris.

[click] Make the disproportion vivid - hundreds of billions of multiplications
to produce a five-line list of odds. That is genuinely what happens.

[click] And the hand-off to chapter 6: the model's job ended at the list.
Choosing from it is somebody else's job, and that somebody is configurable.

Worth noting out loud: 0.95 on Paris is a very confident distribution, and it
is confident because the training data agreed. Ask something the internet
disagrees about and the distribution is flat - and a flat distribution is the
model telling you it does not know. Nobody ever shows the user that number,
which is a genuine shame and a good thing to notice.

Transition: "Chapter six. The knobs."
-->

---
chapter: '5 · From numbers to the next word'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 5 &#183; takeaway</span>

<PipelineMap :highlight="['logits','probs','next']" />

<div v-click="1" class="recap">
  <div>The last vector is scored against <b>every token</b> &#8212; those scores are <b>logits</b>.</div>
  <div>Softmax turns them into a <b>probability distribution</b> over the whole vocabulary.</div>
  <div>One token is chosen, appended, and the whole machine runs again.</div>
</div>

<div v-click="2" class="transition-line">The model&#8217;s job ends at the distribution. <span class="arrow">Everything you can actually tune happens after it.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.6em; font-size: 0.9rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Thirty seconds.

[click] Three lines.
[click] The hand-off, and it is the cleanest chapter boundary in the deck:
everything up to here is the model, everything after is the sampling. Two
genuinely separate things that students routinely merge.

Transition: "So. Who picks?"
-->
