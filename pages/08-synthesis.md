---
layout: section
chapter: '8 · What it still gets wrong'
---

# Chapter 8

## What it still gets wrong

<div v-click class="thesis" style="margin-top:0.8em">Everything in this chapter follows from one fact you already know: it was trained to guess what is <i>likely</i>, and nobody ever taught it what is <i>true</i>.</div>

<!--
Twenty seconds. Set the tone before you start, because this chapter can be
misread as debunking:

"This is not the bit where I tell you it's rubbish. It clearly isn't. This is
the bit where we work out what it's actually doing, so you can predict when
it'll be brilliant and when it'll let you down. That's a more useful skill
than either hype or cynicism."

Transition: "First, credit where it's due."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 5
---

# Why this design took over

<span class="eyebrow structure">Credit where it is due</span>

<div class="why">
  <div v-click="1"><span class="wn">1</span><div><b>It finds relationships at any distance.</b> The first word and the thousandth are one dot product apart. Older designs had to pass information along a chain, and it faded.</div></div>
  <div v-click="2"><span class="wn">2</span><div><b>It trains in parallel.</b> Every position, every prediction, in one pass &#8212; which is what made it possible to use the amount of text and compute that turned out to be necessary.</div></div>
  <div v-click="3"><span class="wn">3</span><div><b>It keeps getting better with scale.</b> More data, more parameters, more compute &#8212; and it kept improving, for far longer than anyone expected.</div></div>
  <div v-click="4"><span class="wn">4</span><div><b>It is not about language.</b> The same machinery now runs on images, audio, video, protein structures and code. Nothing in chapter 4 mentioned words.</div></div>
</div>

<div v-click="5" class="transition-line">Point 4 is the one to sit with. <span class="arrow">We built a general-purpose way of letting parts of a thing consult other parts of the same thing. Language was just the first thing we pointed it at.</span></div>

<style>
.why { display: flex; flex-direction: column; gap: 0.3em; margin: 0.4em 0; }
.why > div { display: flex; align-items: flex-start; gap: 0.75em; }
.wn {
  flex-shrink: 0; width: 1.6em; height: 1.6em; border-radius: 999px;
  background: var(--ann-circuit-soft); color: var(--ann-circuit);
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.8rem;
  display: flex; align-items: center; justify-content: center;
}
.why b { color: var(--ann-indigo); }
.why div div { font-size: 0.86rem; color: var(--ann-ink-soft); }
</style>

<!--
[click] Distance. Connect to chapter 4 - a dot product does not care how far
apart two words are. That is genuinely new; the previous generation of models
had to carry information along a chain and it decayed.

[click] Parallelism, which is the mask payoff from chapter 7.

[click] Scaling. Be careful and honest: it kept improving longer than
expected, and there is real debate about how much further that goes.

[click] Generality, and this is the one worth the time. Go back to chapter 4
in their heads: nothing in the dot product, the softmax or the weighted sum
mentioned language. Feed it patches of an image and it works. That is why
this one architecture ate the whole field.

[click] The closing framing.

Transition: "Now the part that matters for using it sensibly."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 5
---

# Probable is not the same as true

<span class="eyebrow honesty">The big one</span>

<div v-click="1" class="two-q">
  <div class="qa asks"><span class="ql">It asks</span>&#8220;What word is <b>likely</b> to come next?&#8221;</div>
  <div class="qa never"><span class="ql">It never asks</span>&#8220;Is what I am about to say <b>true</b>?&#8221;</div>
</div>

<div v-click="2" class="obs">There is <b>no step</b> anywhere in this lecture where truth was checked. Go back through the map: tokens, vectors, attention, feed-forward, logits, softmax, sample. No step checks anything against the world.</div>

<div v-click="3" class="statement-box">A confident wrong answer and a confident right answer are produced by <b>exactly the same process</b>. From the inside, they are identical.</div>

<div v-click="4" class="obs">This is what &#8220;hallucination&#8221; means, and the word is misleading &#8212; it suggests a malfunction. <b>Nothing is malfunctioning.</b> The machine is doing exactly what it always does; it is just that this time the likely words were not the true ones.</div>

<div v-click="5" class="transition-line">Which gives you the single most useful habit: <span class="arrow">the model&#8217;s confidence tells you about its <b>training data</b>, not about reality.</span></div>

<style>
.two-q { display: flex; flex-direction: column; gap: 0.35em; margin: 0.4em 0; }
.qa { display: flex; align-items: baseline; gap: 0.9em; padding: 0.4em 0.9em; border-radius: 0.45em; font-family: 'Space Grotesk', sans-serif; font-size: 1.08rem; }
.qa.asks { background: var(--ann-circuit-soft); border-left: 4px solid var(--ann-circuit); }
.qa.never { background: var(--ann-ember-soft); border-left: 4px solid var(--ann-ember); }
.ql { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.07em; color: var(--ann-muted); flex: 0 0 7em; }
.obs { font-size: 0.84rem; color: var(--ann-ink-soft); margin-top: 0.4em; }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.4em 1em; font-size: 0.95rem; margin-top: 0.4em; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
The most important slide in the second half. Do not rush it.

[click] The two questions, side by side.

[click] The audit. Actually walk the map backwards out loud - tokens, no
truth check; attention, no truth check; softmax, no truth check. It is a
complete argument and it takes fifteen seconds.

[click] The identity claim, which is the sharp version: right and wrong
answers come out of the same machinery, with the same confidence, by the same
route. There is no internal flag.

[click] Defuse the word "hallucination". It implies a fault, and framing it
as a fault leads people to expect it to be fixed like a bug. It is not a bug;
it is the cost of the mechanism.

[click] The practical habit. This is the sentence a sixteen-year-old should
leave with: confidence is a statement about the training data.

Likely student question: "So how do you know when to trust it?" Honest
answer: "Broadly - trust it more where the internet had lots of consistent
text and the cost of being wrong is low. Trust it least on specifics that
sound checkable: numbers, dates, citations, quotes, names. Those are exactly
the shapes it can produce plausibly without having them."

Transition: "Let me show you how easy it is to fool yourself about this
stuff - including me, and including the researchers."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 5
---

# The famous demo that is partly a trick

<span class="eyebrow honesty">Cashing a promise from chapter 2</span>

<div v-click="1" class="famous"><span class="big-mono">king &#8722; man + woman &#8776; queen</span></div>

<div v-click="2" class="obs">It does work. But the standard software is <b>forbidden from answering with any of the three input words</b> &#8212; because a classical analogy expects four different terms. So it <b>cannot</b> reply &#8220;king&#8221;.</div>

<div v-click="3" class="obs">Lift that ban, and the nearest answer is very often just <b>one of the inputs handed back</b>. On one standard test, a well-known model&#8217;s score fell from about <b>72%</b> to about <b>19%</b>.</div>

<div v-click="4" class="obs">The relationships in the embedding space are <b>real</b>. The famous demo was <b>measuring them badly</b> &#8212; and the same flaw made the model look more biased in some ways and less in others.</div>

<div v-click="5" class="statement-box">Real effect. Bad thermometer. <b>Both things are true</b>, and telling them apart is most of what science is.</div>

<style>
.famous { text-align: center; margin: 0.5em 0 0.6em; }
.famous .big-mono { font-size: 1.6rem; color: var(--ann-indigo); }
.obs { font-size: 0.85rem; color: var(--ann-ink-soft); margin-top: 0.4em; }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.45em 1em; font-size: 1rem; margin-top: 0.55em; }
</style>

<!--
CASH THE CHAPTER 2 DEBT HERE, and say you are doing it: "In chapter two I put
this up, said it was partly a trick, and promised to come back. Here we are."

[click] The famous claim.

[click] The exclusion. This is the mechanism, and it is worth stating
precisely because it sounds like a technicality and is not: the search is
explicitly prevented from returning any of the three inputs.

[click] The numbers. Concrete, published, and dramatic.

[click] The balanced conclusion. BOTH halves matter. Students who hear only
"it's fake" become cynics; students who hear only "it works" become
credulous. The embedding structure is genuinely there. The test was a bad way
to measure it.

[click] The one-liner, and it is the transferable skill from this whole
lecture: "real effect, bad thermometer" is a distinction they will need for
the rest of their lives, in and out of AI.

Likely student question: "Why did nobody notice for years?" Answer: "People
did - the criticisms go back to 2016. But the picture was so tidy and so
quotable that it outran the caveats. That happens a lot, and it's worth
noticing when a result is popular because it's true versus because it makes a
good diagram."

Transition: "One more, and it's about a picture I showed you."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 5
---

# The attention picture is not an explanation

<span class="eyebrow honesty">About my own slides</span>

<div v-click="1" class="obs">In chapter 4 I showed you that <b>it</b> put <b>0.85</b> on <b>glass</b>, and we all felt we understood why the model did what it did. Careful.</div>

<div v-click="2" class="statement-box">The attention weights show what the model <b>looked at</b>. They do not show what it <b>used</b>.</div>

<div v-click="3" class="obs">
  Three reasons researchers argue about this:
  <div class="rz">
    <div><b>&#183;</b> You can often find a <i>completely different</i> set of weights that produces the <i>same</i> answer.</div>
    <div><b>&#183;</b> A word can get a big weight and still contribute almost nothing, because its <span class="v">value</span> vector is tiny.</div>
    <div><b>&#183;</b> After a few layers everything is mixed into everything, so a late-layer picture tells you little about the input.</div>
  </div>
</div>

<div v-click="4" class="obs">And the strangest finding: in many real models, the <b>most-attended token is the first one in the sequence</b> &#8212; a marker with no meaning. Softmax <b>must</b> hand out a full 100%, so the model learns somewhere to dump the leftovers.</div>

<div v-click="5" class="transition-line">Attention maps are a <b>hypothesis generator</b>, not evidence. <span class="arrow">Pretty is not the same as true &#8212; which is the same lesson as the last slide, about a nicer-looking picture.</span></div>

<style>
.obs { font-size: 0.83rem; color: var(--ann-ink-soft); margin-top: 0.35em; }
.obs b { color: var(--ann-indigo); }
.rz { display: flex; flex-direction: column; gap: 0.15em; margin-top: 0.25em; padding-left: 0.4em; }
.rz > div { font-size: 0.79rem; }
.rz b { color: var(--ann-ember); }
.slidev-layout .statement-box { padding: 0.4em 1em; font-size: 0.95rem; margin-top: 0.4em; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
This slide takes back some of the authority of the best slide in the lecture,
on purpose. That is a good thing to model in front of 500 students: showing
them how to hold a result you like at arm's length.

[click] Name the temptation - and own it, because I created it two chapters
ago with a very persuasive picture.

[click] The distinction: looked at, versus used. Six words, and it is the
whole slide.

[click] The three reasons. Keep them brisk. The first is the strongest - if
several different attention patterns give the same output, no single one of
them can be THE explanation.

[click] The attention-sink finding, which students find delightfully weird:
the most-attended token is frequently the first one, regardless of meaning.
The reason follows directly from chapter 4 - the weights must sum to one, so
when a word has nothing it particularly needs, the surplus has to go
somewhere, and models learn to park it on a fixed spot.

That is also a lovely closing demonstration that "attention = importance" is
simply false.

[click] The verdict. Hypothesis generator, not evidence.

Transition: "Two definitions, and then we're done."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 4
---

# Transformer, or LLM?

<span class="eyebrow structure">Two words people mix up</span>

<div class="defs">
  <div v-click="1" class="def">
    <div class="dh">Transformer</div>
    <div class="db">The <b>design</b>. Attention, feed-forward, residuals, stacked. Everything in chapters 3, 4 and 7. It is a shape, and it is not large or small or clever on its own.</div>
  </div>
  <div v-click="2" class="def">
    <div class="dh">Large language model</div>
    <div class="db">What you get when you build that shape at enormous size and train it on an enormous amount of text.</div>
  </div>
</div>

<div v-click="3" class="eq">
  <span>Transformer</span><span class="op">+</span><span>a very large amount of text</span><span class="op">+</span><span>months of compute</span><span class="op">=</span><span class="res">an LLM</span>
</div>

<div v-click="4" class="transition-line">The architecture is not the achievement. <span class="arrow">The architecture is what made the achievement <b>affordable</b>.</span></div>

<style>
.defs { display: flex; flex-direction: column; gap: 0.4em; margin: 0.5em 0; }
.def { border: 1px solid var(--ann-line); border-left: 4px solid var(--ann-indigo); border-radius: 0.45em; padding: 0.45em 0.9em; background: var(--ann-paper-raised); }
.dh { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1rem; color: var(--ann-indigo); }
.db { font-size: 0.83rem; color: var(--ann-ink-soft); margin-top: 0.1em; }
.db b { color: var(--ann-ink); }
.eq { display: flex; align-items: center; justify-content: center; gap: 0.7em; flex-wrap: wrap; margin: 0.7em 0 0.3em; font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; }
.eq .op { color: var(--ann-muted); font-size: 1.1rem; }
.eq .res { color: var(--ann-ember); font-weight: 700; font-size: 1rem; }
</style>

<!--
Quick, but it fixes a genuine confusion - students use the two words
interchangeably and then cannot follow anything they read.

[click] Transformer: a shape. Emphasise that a transformer can be tiny - you
can train one on a laptop in minutes.
[click] LLM: that shape, at scale, trained on a lot.

[click] The equation.

[click] The closing line, which is the honest historical claim: the ideas
were not all new, and the transformer's real contribution was making training
at this scale practical. Parallelism, not magic.

Transition: "Right. If you remember nothing else."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 7
---

# If you remember only this

<span class="eyebrow structure">Seven things</span>

<div class="seven">
  <div v-click="1"><span class="sn">1</span><b>Tokens.</b> It reads chunks, not letters &#8212; which is why it cannot spell.</div>
  <div v-click="2"><span class="sn">2</span><b>Embeddings.</b> Every chunk becomes a list of numbers, and nearby means &#8220;used alike&#8221;.</div>
  <div v-click="3"><span class="sn">3</span><b>Attention.</b> Every word asks a question, every word answers, and the answers get <b>blended</b> &#8212; never picked.</div>
  <div v-click="4"><span class="sn">4</span><b>Softmax.</b> Turns scores into shares that add to 1, and never gives anything a zero.</div>
  <div v-click="5"><span class="sn">5</span><b>It predicts the next token.</b> Everything else is a side effect of doing that very well.</div>
  <div v-click="6"><span class="sn">6</span><b>Temperature, top-k, top-p.</b> These change <i>how we pick</i>, never <i>what it knows</i>.</div>
  <div v-click="7"><span class="sn">7</span><b>Likely is not true.</b> Nothing in the machine ever checks.</div>
</div>

<style>
.seven { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; }
.seven > div { display: flex; align-items: baseline; gap: 0.8em; font-size: 0.93rem; color: var(--ann-ink-soft); }
.sn {
  flex-shrink: 0; width: 1.65em; height: 1.65em; border-radius: 999px;
  background: var(--ann-indigo-soft); color: var(--ann-indigo);
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.8rem;
  display: inline-flex; align-items: center; justify-content: center;
}
.seven b { color: var(--ann-indigo); }
</style>

<!--
Seven is the ceiling of what anyone holds in working memory, and that is
deliberate - do not add an eighth.

Reveal one at a time and say each one out loud, properly. Do not read them
fast. This is the list that survives the walk home.

If you are running short of time, this slide is the one that must not be cut.
Everything else in chapter 8 is optional; this is the exam-revision slide,
the corridor-conversation slide, and the thing a parent gets told over dinner.

Consider pausing after seven and asking: "Which of those seven surprised you
most?" In a room this size you will not take many answers, but the question
makes them rank the list, which is worth more than hearing it again.

Transition: "One picture, and then questions."
-->

---
chapter: '8 · What it still gets wrong'
clicks: 2
---

# The whole thing

<span class="eyebrow structure">Two hours, one picture</span>

<PipelineMap :dim-others="false" />

<div v-click="1" class="story">
  Text becomes <b>chunks</b>. Chunks become <b>vectors</b>. Position gets <b>added in</b>.
  Then, ninety-six times over: every word <b>asks</b> every other word a question, the answers are <b>blended</b> in proportion, and each word <b>thinks</b> about what it got.
  The final vector is scored against <b>every word it knows</b>, softmax turns the scores into <b>odds</b>, and one word is <b>drawn</b>.
  Then the whole thing runs again.
</div>

<div v-click="2" class="transition-line">That is it. That is the machine. <span class="arrow">There is no other part.</span></div>

<style>
.story { margin-top: 0.7em; font-size: 0.95rem; line-height: 1.6; color: var(--ann-ink-soft); max-width: 46em; }
.story b { color: var(--ann-indigo); }
</style>

<!--
[click] Read the paragraph out loud, slowly, pointing at the map as you go.
It is written to be spoken and to map box-for-box onto the picture.

[click] "There is no other part." Mean it - a lot of students assume there
must be some additional cleverness they were not shown. There isn't. That is
simultaneously the most impressive and the most sobering thing about the
subject, and it is a good note to land on.

Transition: nothing. Advance.
-->

---
layout: quote
chapter: '8 · What it still gets wrong'
---

<div class="eyebrow structure" style="justify-content:center">The one sentence</div>

# &#8220;A transformer is a machine for <span style="color:var(--ann-ember)">finding relationships between words</span>, which it uses to <span style="color:var(--ann-circuit)">predict how a sentence is likely to continue</span> &#8212; and everything you can control happens <span style="color:var(--ann-indigo)">after it has finished thinking.</span>&#8221;

<style>
h1 { font-size: 1.6rem; line-height: 1.5; }
</style>

<!--
The closer. Read it once, slowly, and then stop talking.

The three coloured phrases map to the three parts of the lecture, and say so
if you have the time: ember is chapters 3 and 4, the relationships. Teal is
chapter 5, the prediction. Indigo is chapter 6, the knobs - and the deliberate
point that the knobs come last, after the model's work is over, because that
is the thing people most often get backwards.

Then pause. Let it sit. Then go to questions.
-->

---
layout: end
chapter: ''
---

# Questions?

<div class="transition-line" style="text-align:center; margin-top:1em;">
The slides are downloadable from this link &#8212; including the presenter notes,<br>
and the script that recomputes every number on them.
</div>

<!--
Take questions.

The four that come up most, with short answers ready:

"Is it conscious / does it understand?" - Point back at chapter 7: it is
arithmetic on numbers found by trial and error. Nothing in that process
resembles understanding. But also be honest that "what would count as
understanding" is a genuinely hard question and you are not going to settle
it in a Q&A.

"Will it take my job?" - Out of scope, and say so kindly, but the useful
version of the answer comes from this lecture: it is very good at producing
likely continuations of text, and very bad at knowing whether they are true.
Work that is mostly the first thing is exposed; work that needs the second is
less so.

"How do I make it better at X?" - Give them more context, because chapter 6:
the model only sees what is in the window. And ask for reasoning steps,
because chapter 5: it can only use its own output as scratch paper.

"What should I learn next?" - The tokenizer tools are the best hour they can
spend, because they can play with them immediately. After that, anything that
makes them implement one small transformer from scratch.

Last thing: point at the credits slide and tell them the good free resources
are all listed there, so nobody has to write them down now.
-->

---
layout: default
chapter: ''
---

# Credits &amp; where to go next

<span class="eyebrow structure">All of these are free</span>

<div class="creds">
  <div><b>Transformer Explainer</b> &#8212; Polo Club, Georgia Tech. A live GPT-2 in your browser with a temperature slider. Start here.</div>
  <div><b>Tokenizer playgrounds</b> &#8212; tiktokenizer and similar. Paste anything and watch it get chopped up. Chapter 1, hands-on.</div>
  <div><b>&#8220;Let&#8217;s build GPT from scratch&#8221;</b> &#8212; Andrej Karpathy. Builds a working transformer in two hours of video and 225 lines of code.</div>
  <div><b>3Blue1Brown, chapters 5&#8211;7</b> &#8212; the best visual treatment of attention and embeddings that exists.</div>
  <div><b>The Illustrated Transformer</b> &#8212; Jay Alammar. The diagrams that taught most of the field.</div>
  <div><b>Dive into Deep Learning</b> (d2l.ai) and <b>The Annotated Transformer</b> &#8212; if you want the code and the maths in full.</div>
</div>

<div class="note">
Every diagram in this deck was drawn for it. Every number was generated and checked by
<code>scripts/verify-attention.py</code>, which cross-checks against PyTorch &#8212;
<b>if a slide disagrees with that script, the slide is wrong.</b>
</div>

<style>
.creds { display: flex; flex-direction: column; gap: 0.28em; margin: 0.5em 0; font-size: 0.85rem; color: var(--ann-ink-soft); }
.creds b { color: var(--ann-indigo); }
.note {
  margin-top: 0.8em; padding-top: 0.5em; border-top: 1px dashed var(--ann-line);
  font-size: 0.78rem; color: var(--ann-ink-soft);
}
.note code { font-family: 'JetBrains Mono', monospace; font-size: 0.95em; }
.note b { color: var(--ann-ember); }
</style>

<!--
Leave this up during questions - it is the slide people photograph.

Say one sentence about why it is here: the good free material on this subject
is genuinely excellent and mostly better than anything you could buy, and
they should go and use it.

The bottom note is not decoration. It is the standard the deck holds itself
to, and saying it out loud invites the room to check you - which is the right
relationship for a student to have with a lecturer.
-->
