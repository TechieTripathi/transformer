---
layout: section
chapter: '4 · Attention, mechanically'
---

# Chapter 4

## Attention, mechanically

<div v-click class="thesis" style="margin-top:0.8em">Three questions, one dot product, and a row of numbers that adds up to one. We will do the whole thing by hand.</div>

<!--
Set the tone. This is the centre of the lecture.

"For the next twenty-five minutes we are going to build the machinery, and
then we are going to run it on three real words with numbers small enough
that you can check every step. If my arithmetic is wrong, shout."

Transition: "It starts with the machine asking itself three questions."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# Every word plays three roles

<span class="eyebrow attention">The key idea</span>

<div class="roles">
  <div v-click="1" class="role q">
    <div class="rn">Query</div>
    <div class="rq">&#8220;What am I looking for?&#8221;</div>
    <div class="rd">The question this word is asking of the sentence.</div>
  </div>
  <div v-click="2" class="role k">
    <div class="rn">Key</div>
    <div class="rq">&#8220;What have I got?&#8221;</div>
    <div class="rd">The advertisement this word puts out, so others can find it.</div>
  </div>
  <div v-click="3" class="role v">
    <div class="rn">Value</div>
    <div class="rq">&#8220;What will I pass on?&#8221;</div>
    <div class="rd">What this word actually contributes, if someone attends to it.</div>
  </div>
</div>

<div v-click="4" class="key-message">For <b>it</b>, the query is roughly &#8220;I am a pronoun &#8212; what noun am I standing in for?&#8221; and <b>glass</b>&#8217;s key is roughly &#8220;I am a noun, and I just got dropped.&#8221;</div>

<div v-click="5" class="transition-line">Keys and values are <b>different on purpose</b>. <span class="arrow">How easy you are to find, and what you are worth once found, are not the same thing.</span></div>

<style>
.roles { display: flex; flex-direction: column; gap: 0.3em; margin: 0.4em 0; }
.role { display: grid; grid-template-columns: 6.5em 16em 1fr; align-items: baseline; gap: 1em; padding: 0.35em 0.8em; border-radius: 0.45em; }
.role.q { background: var(--qkv-query-soft); border-left: 4px solid var(--qkv-query); }
.role.k { background: var(--qkv-key-soft); border-left: 4px solid var(--qkv-key); }
.role.v { background: var(--qkv-value-soft); border-left: 4px solid var(--qkv-value); }
.rn { font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 1.05rem; }
.role.q .rn { color: var(--qkv-query); }
.role.k .rn { color: var(--qkv-key); }
.role.v .rn { color: var(--qkv-value); }
.rq { font-family: 'Space Grotesk', sans-serif; font-size: 0.98rem; font-weight: 500; }
.rd { font-size: 0.78rem; color: var(--ann-ink-soft); }
.slidev-layout .key-message { margin: 0.5em 0 0.35em; font-size: 1rem; }
</style>

<!--
The three roles are the single most important vocabulary in the lecture, and
this framing - roles a word PLAYS, rather than things a word HAS - is the one
that avoids the commonest confusion. Take it slowly.

[click] Query. The question. Emphasise that the word is ASKING.
[click] Key. The advert. "What have I got that someone might be looking for?"
[click] Value. The goods. "Here is what you get if you pick me."

[click] Make it concrete on our sentence, because abstract Q/K/V is where
people glaze over. Do not claim these are literally what the vectors encode -
nobody knows what they encode - say "roughly", and mean it.

[click] The key-vs-value distinction, which almost every explanation fudges.
Use a human example if it helps: a job advert is not the job. A book's title
is not the book. How findable you are and what you deliver are separate
things, and the model learns them separately.

Colour is doing work from here on: purple is always query, orange always key,
blue always value, on every slide and inside every formula. Point that out
once, now - it means a student who cannot yet follow the symbols can still
follow the colours.

Transition: "There's an analogy everyone uses for this. I'm going to give it
to you and then break it."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# The library &#8212; and the smoothie

<span class="eyebrow attention">Careful</span>

<div v-click="1" class="lib">
  <div><span class="ln q">Query</span>You walk into a library and ask: &#8220;I want a book about space.&#8221;</div>
  <div><span class="ln k">Key</span>Every book has a title on its spine. You compare your question to the titles.</div>
  <div><span class="ln v">Value</span>You pull down the good one and read what is inside.</div>
</div>

<div v-click="2" class="brk">And here is where the analogy lies to you.</div>

<div v-click="3">

<Callout>
  <template #misconception>You find the best-matching book and read that one.</template>
  <template #clarification>You do not take one book. You put <b>every book in the library</b> in a blender &#8212; <b>85%</b> of the space book, <b>10%</b> of the cookbook, <b>5%</b> of the phone directory &#8212; and drink the result. The good match dominates the flavour. But nothing is left out, and what you get is a <b>smoothie</b>, not a book.</template>
</Callout>

</div>

<div v-click="4" class="obs">Keep the library for <b>query</b>, <b>key</b> and <b>value</b> &#8212; it is genuinely good for those three. Throw away the part where you pick one.</div>

<div v-click="5" class="transition-line">So: how does a machine compare a question with an advertisement? <span class="arrow">Both of them are just lists of numbers.</span></div>

<style>
.lib { display: flex; flex-direction: column; gap: 0.3em; margin: 0.3em 0; font-size: 0.92rem; }
.lib > div { display: flex; align-items: baseline; gap: 0.9em; }
.ln {
  flex: 0 0 5.2em; font-family: 'Space Grotesk', sans-serif; font-weight: 700;
  font-size: 0.85rem; padding: 0.1em 0.5em; border-radius: 0.3em; text-align: center;
}
.ln.q { background: var(--qkv-query-soft); color: var(--qkv-query); }
.ln.k { background: var(--qkv-key-soft); color: var(--qkv-key); }
.ln.v { background: var(--qkv-value-soft); color: var(--qkv-value); }
.brk { margin: 0.55em 0 0.4em; font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 1.02rem; color: var(--ann-ember); }
.obs { margin-top: 0.45em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .callout { font-size: 0.76rem; }
.slidev-layout .callout-row { padding: 0.38em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
[click] Give them the library straight, with no hedging. It is a good
analogy for the three roles and they should have it.

[click] Then turn on it. The one-line break gets a beat of silence.

[click] The callout. The smoothie is deliberately silly because silly is
memorable, and the percentages are the ones they will meet for real in eight
slides' time - so this is a plant, not a throwaway.

[click] Be explicit about which half to keep and which to discard. Students
handle "this analogy is 70% right" perfectly well if you tell them WHICH 70%.

[click] Transition into the arithmetic.

Likely student question: "Then why does everyone use the library analogy?"
Honest answer: "Because the names came from databases - query, key and value
are literally borrowed from lookup tables, and a lookup table DOES return one
thing. The names are a historical accident, and they've been misleading
people ever since. A fair number of researchers think 'attention' was a badly
chosen word too."

Transition: "Two lists of numbers. How do you measure whether they match?"
-->

---
chapter: '4 · Attention, mechanically'
clicks: 6
---

# Measuring a match: the dot product

<span class="eyebrow math">Mechanism</span>

<div v-click="1" class="key-message">Multiply the matching slots together, then add it all up. One number: <b>how well do these two agree?</b></div>

<div v-click="2" class="dp">
  <div class="dpr"><span class="dl">A</span><span class="dv">[ 2, 3 ]</span></div>
  <div class="dpr"><span class="dl">B</span><span class="dv">[ 4, 1 ]</span></div>
  <div v-click="3" class="dpr calc"><span class="dl">A &#183; B</span><span class="dv">(2&#215;4) + (3&#215;1) = 8 + 3 = <b>11</b></span></div>
</div>

<div v-click="4" class="obs">
  <div><b>Big</b> when the two lists are large in the <i>same</i> places. <b>Small</b> when they are large in different places. It can be <b>negative</b> when they actively disagree.</div>
  <div>That is the whole comparison. No lookup, no search, no matching of text &#8212; just multiply and add.</div>
</div>

<div v-click="5" class="statement-box">

Score for &#8220;how much should <span class="q">this word</span> attend to <span class="k">that word</span>?&#8221; &nbsp;=&nbsp; <span class="q">query</span> &#183; <span class="k">key</span>

</div>

<div v-click="6" class="transition-line">Every attention score in every AI system you have ever used <span class="arrow">is one of these.</span></div>

<style>
.dp { display: flex; flex-direction: column; gap: 0.15em; margin: 0.5em 0; }
.dpr { display: grid; grid-template-columns: 5em 1fr; align-items: baseline; gap: 1.2em; }
.dl { font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: var(--ann-muted); text-align: right; }
.dv { font-family: 'JetBrains Mono', monospace; font-size: 1.3rem; font-variant-numeric: tabular-nums; }
.dpr.calc { margin-top: 0.3em; padding-top: 0.35em; border-top: 2px solid var(--ann-ink); }
.dpr.calc .dv b { color: var(--ann-indigo); font-size: 1.5rem; }
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.4em 1em; font-size: 0.95rem; margin-top: 0.4em; }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.4em; }
</style>

<!--
Plain English first, symbols second - and here the "symbols" are two-digit
arithmetic, so nobody gets left behind.

[click] The plain-English definition.

[click] Two tiny vectors.

[click] Work it out ON THE SLIDE, out loud, slowly. Two fours are eight, three
ones are three, eleven. In a mixed-ability room this is the moment where the
weaker half realises they can actually follow the maths, so do not skip it or
speed through it apologetically.

[click] The interpretation - and the negative case matters, because scores
genuinely do go negative and they will see one in three slides.

[click] The connection: this is what we use for the score. Note the colours
in the box match the colours from two slides ago.

[click] The scale line. Worth saying with a bit of weight: the headline
mechanism of every large language model is multiply-and-add.

Likely student question: "Why multiply rather than, say, subtract and see how
close they are?" Good question: "Distance would also work, and some systems
use it. The dot product has two advantages: it's extremely fast on the
hardware we have - it's just a matrix multiply, which GPUs are built for -
and it lets the model express 'these actively disagree' with a negative
number, which distance can't."

Transition: "Right. Let's do it for real, on our sentence."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 4
zoom: 0.96
---

# The worked example

<span class="eyebrow math">Worked by hand &#183; 1 of 6</span>

<div class="key-message" style="margin-top:-0.4em">Three words from our sentence. Four numbers each. Small enough to check in your head.</div>

<div v-click="1">

<AttentionTrace stage="setup" compact />

</div>

<div v-click="2" class="obs">
  <div>These are the vectors from chapter 2 &#8212; meaning <b>plus</b> position, already added together.</div>
  <div>Real ones have thousands of entries and are decimals. These are whole numbers <b>so that you can check me</b>.</div>
</div>

<div v-click="3" class="statement-box">Our question: how much should <span class="q">it</span> attend to <span class="k">glass</span>?</div>

<div v-click="4" class="transition-line">Everything from here is arithmetic you could do on paper. <span class="arrow">Follow it &#8212; that is the point of the next five slides.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.45em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.95rem; margin-top: 0.4em; }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
Set the contract for the next six slides explicitly: "Everything you are
about to see is real arithmetic on these numbers. I have not rounded anything
to make it prettier. There is a script in the repository that recomputes all
of it and checks it against PyTorch, and if a slide disagrees with the script
then the slide is wrong."

Say that out loud. It is the difference between a lecture they believe and a
lecture they take on faith, and the second kind does not survive contact with
a sceptical sixteen-year-old.

[click] The three vectors. Note we are using three words from the sentence,
not all nine - glass, dropped, and it. Say so, so nobody thinks the other six
vanished.

[click] Two caveats. The second is the important one: these are small whole
numbers PRECISELY so the room can audit the arithmetic.

[click] State the question we are answering. It is the same question from
chapter 3, which they were promised would get a number.

[click] Transition.

Transition: "First job: turn each word into its three roles."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 4
zoom: 0.98
---

# Three roles, three multiplications

<span class="eyebrow math">Worked by hand &#183; 2 of 6</span>

<div v-click="1">

<AttentionTrace stage="qkv" compact />

</div>

<div v-click="2" class="obs">
  <div>Each word&#8217;s vector is multiplied by <b>three different learned matrices</b>. <b>Same input, three outputs</b> &#8212; Q, K and V are not three things the word <i>has</i>, they are three <i>views</i> of the one thing it is.</div>
</div>

<div v-click="3">

<Callout>
  <template #misconception>Query, key and value are three separate pieces of information stored with each word.</template>
  <template #clarification>There is only ever <b>one vector per word</b>. The three matrices are the <b>only</b> things that differ &#8212; and those matrices are the <b>learned parameters</b>. They are the same for every word in the sentence, and they are what training actually changes.</template>
</Callout>

</div>

<div v-click="4" class="transition-line">Now we have a question, an advert and a payload for each word. <span class="arrow">Time to compare them.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.4em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.trace :deep(svg) { max-height: 26vh !important; }
.slidev-layout .callout { font-size: 0.74rem; }
.slidev-layout .callout-row { padding: 0.34em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.38em; }
</style>

<!--
[click] The picture. Walk one row: "Take 'it'. Multiply by the query matrix,
get 3 and -1. Multiply the SAME vector by the key matrix, get -1 and -3.
Multiply by the value matrix, get 1 and 3. One input, three outputs."

[click] The two observations. The second is the misconception-killer in
advance of the callout.

[click] The callout. TEACH THIS EXPLICITLY - it is the most common
misunderstanding after the spotlight one. Three lines of code make it
unarguable, and if the room has coders, write them:
    q = x @ W_Q
    k = x @ W_K
    v = x @ W_V
Same x. Three matrices. That's the entire thing.

Also flag which things here are LEARNED: the three W matrices. Not the
vectors, not the scores - the matrices. Everything else on the next four
slides is just arithmetic on top of them. This is the second appearance of
"where did the numbers come from", and chapter 7 answers it.

[click] Transition.

Likely student question: "Why not just compare the word vectors directly?
Why bother with the matrices at all?" Really good question: "Because then
every word would only ever be able to ask one question - 'who is like me?'.
The matrices let 'it' ask 'who is a noun I could be standing in for?', which
is a completely different question from 'who resembles the word it?'. The
projections buy you the freedom to look for something other than yourself."

Transition: "Nine comparisons: every word's question against every word's
advert."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# Every question against every advert

<span class="eyebrow math">Worked by hand &#183; 3 of 6</span>

<div v-click="1">

<AttentionHeat stage="raw" :highlight-row="2" compact />

</div>

<div v-click="2" class="calc-strip" style="justify-content:center">
  <div class="calc-chip q"><span class="lbl">query of &#8220;it&#8221;</span>[ 3, &#8722;1 ]</div>
  <div class="calc-op">&#183;</div>
  <div class="calc-chip k"><span class="lbl">key of &#8220;glass&#8221;</span>[ 1, &#8722;1 ]</div>
  <div class="calc-op">=</div>
  <div v-click="3" class="calc-chip upd"><span class="lbl">(3&#215;1) + (&#8722;1&#215;&#8722;1)</span>3 + 1 = <b>4</b></div>
</div>

<div v-click="4" class="obs">
  <div>Nine numbers, because every word compares itself against every word &#8212; <b>including itself</b>.</div>
  <div>In the row for <b>it</b>: <span class="num">4</span> against glass, <span class="num">1</span> against dropped, <span class="num">0</span> against itself. <b>Glass wins.</b></div>
  <div>Notice the top row is all negative. Negative scores are normal and they mean &#8220;actively unlike&#8221;.</div>
</div>

<div v-click="5" class="transition-line">These are raw scores. They are not yet weights &#8212; they do not add up to anything. <span class="arrow">Two steps to fix that.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.8rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
.calc-chip b { font-size: 1.1rem; color: var(--ann-indigo); }
</style>

<!--
[click] The matrix. Nine circles. Explain the reading convention once: the
row is the word DOING the looking, the column is the word being looked AT.
Row "it", column "glass" is "how much does it care about glass".

Point out the circles: bigger circle AND darker colour both mean bigger
number. Two channels for the same fact, on purpose, because from row 30 of
this hall colour alone does not survive.

[click] The arithmetic strip for the headline cell.
[click] Do the sum out loud: three times one is three; minus one times minus
one is plus one; three plus one is four. Ask them to check the sign on the
second term - it is the one people get wrong, and having the room catch it
is better than you announcing it.

[click] Three observations. "Including itself" matters - it answers the
question they may have had in chapter 3.

[click] The set-up for softmax: these are scores, not weights. A four and a
one and a zero are not shares of anything.

Likely student question: "Why does 'it' score 0 against itself? Shouldn't a
word match itself perfectly?" Lovely question: "It would if we compared the
word to itself. But we're comparing its QUESTION to its OWN ADVERT, and those
went through two different matrices. 'It' is asking 'what noun am I standing
in for?' and advertising 'I am a pronoun'. Those genuinely don't match - and
that's the projections earning their keep."

Transition: "Step one of two: a division that looks like a detail and isn't."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# Why we divide first

<span class="eyebrow math">Worked by hand &#183; 4 of 6</span>

<div class="key-message" style="margin-top:-0.4em">Big scores make the next step too greedy. So we shrink them, by &#8730;(length of the vectors).</div>

<div v-click="1" class="sat">
  <div class="sr"><span class="sl">gentle scores</span><span class="sv">softmax([0.1, &#8722;0.2, 0.3, &#8722;0.2, 0.5])</span></div>
  <div class="sr"><span class="sl"></span><span class="sv res">= [0.19, 0.14, 0.24, 0.14, 0.29]</span><span class="sc good">every word still contributes</span></div>
  <div v-click="2" class="sr"><span class="sl">same, &#215;8</span><span class="sv">softmax([0.8, &#8722;1.6, 2.4, &#8722;1.6, 4.0])</span></div>
  <div v-click="2" class="sr"><span class="sl"></span><span class="sv res">= [0.03, 0.00, 0.16, 0.00, <b>0.80</b>]</span><span class="sc bad">one word takes almost everything</span></div>
</div>

<div v-click="3" class="obs">
  <div>Same <i>shape</i> of scores. Just bigger. And the result collapses onto a single winner.</div>
  <div>That is exactly the &#8220;spotlight&#8221; behaviour we said it should not have &#8212; and a machine that has already made up its mind has nothing left to learn from.</div>
</div>

<div v-click="4" class="statement-box">Our vectors have length 2, so we divide every score by &#8730;2 &#8776; <span class="num">1.41</span>. The <span class="num">4</span> becomes <span class="num">2.83</span>.</div>

<div v-click="5" class="transition-line">A one-line fix for a real problem. <span class="arrow">Now the step that finally makes them weights.</span></div>

<style>
.sat { display: flex; flex-direction: column; gap: 0.08em; margin: 0.4em 0; }
.sr { display: grid; grid-template-columns: 8.5em 21em 1fr; align-items: baseline; gap: 0.9em; }
.sl { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--ann-muted); text-align: right; }
.sv { font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; font-variant-numeric: tabular-nums; }
.sv.res { color: var(--ann-indigo); }
.sv.res b { color: var(--ann-ember); font-size: 1.05rem; }
.sc { font-size: 0.72rem; font-style: italic; }
.sc.good { color: var(--ann-circuit); }
.sc.bad { color: var(--ann-ember); }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.45em; font-size: 0.81rem; color: var(--ann-ink-soft); }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.9rem; margin-top: 0.4em; }
.slidev-layout .key-message { margin: 0.3em 0 0.4em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
This is the one step in the pipeline that usually gets waved away as "a
technical detail". It takes ninety seconds to justify properly and it is
worth it, because it is a place where a student can see WHY a design decision
exists rather than being told it does.

[click] Gentle scores through softmax: a spread. Everyone contributes.
[click] The SAME numbers multiplied by eight: one token takes 80%. Say the
word that matters - it SATURATES.

[click] Draw the link back to chapter 3 explicitly: this is the spotlight
failure mode, arriving through the back door. And add the training argument -
a saturated attention row has almost no gradient, so the model stops being
able to learn anything from it. (You do not need them to know what a gradient
is yet; "it gets stuck and can't improve" is enough, and chapter 7 pays it.)

[click] Our concrete case: length 2, divide by root 2. Show the 4 becoming
2.83 so the number they have been tracking survives into the next slide.

[click] Transition.

Likely student question: "Why the square root specifically?" Answer for the
keen ones, skip it live if you are behind: "If you add up a lot of random
products, the spread of the total grows like the square root of how many
terms there were. Dividing by that exactly cancels it, so the scores stay in
a sensible range no matter how long the vectors are. It's in the original
paper, and it's one line of statistics."

Transition: "And now, softmax."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
zoom: 0.96
---

# Softmax: turning scores into shares

<span class="eyebrow math">Worked by hand &#183; 5 of 6</span>

<div class="key-message" style="margin-top:-0.4em">Make every score positive, then divide by the total. Now they add up to <b>1</b>.</div>

<div v-click="1">

<AttentionHeat stage="softmax" :highlight-row="2" compact />

</div>

<div v-click="2" class="obs">
  <div>Each row now adds to exactly <b>1</b>. Each row is a full set of shares.</div>
  <div>&#8220;Make it positive&#8221; is done with <b>e<sup>x</sup></b>, which is never zero &#8212; so <b>no weight is ever zero</b>. That is the promise from chapter 3, kept.</div>
</div>

<div v-click="3" class="formula">

$$P_i = \frac{e^{z_i}}{\sum_j e^{z_j}}$$

</div>

<div v-click="4" class="obs">
  <div>If the formula means nothing to you, the sentence above it is enough. <b>It says exactly the same thing.</b></div>
</div>

<div v-click="5" class="transition-line">Look at the row for <b>it</b>. <span class="arrow">We promised you a number in chapter 3.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.81rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.formula { text-align: center; margin: 0.3em 0; }
.formula :deep(.katex-display) { margin: 0.2em 0; font-size: 0.95em; }
.slidev-layout .key-message { margin: 0.3em 0 0.35em; font-size: 1rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
Note the ORDER here, and keep it on every maths slide in this deck: plain
English first, picture second, symbols LAST. The weaker half of the room gets
a complete, correct understanding from the first two and never needs the
third. The stronger half gets the third and is satisfied. Nobody is bored and
nobody is lost.

[click] The matrix, now as weights. Point at a row and say "these three add
to one".

[click] The two facts. The second is a promise being paid - chapter 3 claimed
no weight is ever zero, and here is the reason: e to the power of anything is
positive, always. A student can verify that claim themselves.

[click] The formula. Introduce it as a translation, not as new content: "this
is the sentence at the top, written in symbols."

[click] Say this out loud and mean it: if the formula is noise to you, you
have lost nothing. That single sentence keeps a third of the room in the
lecture, and it costs you five seconds.

[click] Point at the row for "it" and pause before advancing. The next slide
is the payoff.

Transition: nothing - just advance.
-->

---
layout: fact
chapter: '4 · Attention, mechanically'
clicks: 3
---

# 0.85

<div class="payoff">of <b>it</b>&#8217;s attention goes to <b>glass</b></div>

<div v-click="1" class="rest">the rest: <span class="num">0.10</span> to <i>dropped</i> &#183; <span class="num">0.05</span> to itself</div>

<div v-click="2" class="asked">You answered this in chapter 3 without thinking about it.<br>That is the number.</div>

<div v-click="3" class="check">q<sub>it</sub> &#183; k<sub>glass</sub> = 4 &#8594; &#247;&#8730;2 = 2.83 &#8594; softmax &#8594; <b>0.8482</b></div>

<style>
h1 { font-size: 6rem; color: var(--ann-ember); line-height: 1; margin-bottom: 0.1em; }
.payoff { font-family: 'Space Grotesk', sans-serif; font-size: 1.5rem; font-weight: 500; color: var(--ann-ink); }
.payoff b { color: var(--ann-indigo); }
.rest { margin-top: 1em; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; color: var(--ann-ink-soft); }
.asked { margin-top: 1.4em; font-size: 1.05rem; color: var(--ann-ink-soft); line-height: 1.5; }
.check {
  margin-top: 1.2em; font-family: 'JetBrains Mono', monospace; font-size: 0.85rem;
  color: var(--ann-muted); font-variant-numeric: tabular-nums;
}
.check b { color: var(--ann-ember); }
</style>

<!--
THE PEAK OF THE LECTURE. Let it breathe. Do not talk over the reveal.

Put it up. Say nothing for three seconds.

Then: "In chapter three I asked you what 'it' referred to, and you all knew.
I said I'd put a number on it. That's the number. Eighty-five per cent of
what 'it' becomes is made of 'glass'."

[click] The remainder - and point out that dropped and itself are still
there. Not zero. Never zero.

[click] The callback to chapter 3. This is the moment the deck's promise is
paid, so pay it explicitly and let them enjoy it.

[click] The whole chain on one line, for anyone who wants to check it. Read
it out: dot product four, divide by root two, softmax, nought point eight
five. Four steps. That's the mechanism that runs every chatbot on earth.

If you do one thing well in this lecture, do this slide well.

Transition: "But a number isn't the output. What does the machine DO with
it?"
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
zoom: 0.95
---

# What the weights are for

<span class="eyebrow math">Worked by hand &#183; 6 of 6</span>

<div v-click="1">

<AttentionTrace stage="blend" :row="2" compact />

</div>

<div v-click="2" class="obs">
  <div>The <span class="v">value</span> vectors are drawn at the strength of their weight &#8212; <b>glass</b> nearly solid, <b>dropped</b> a ghost. Faint, but <b>there</b>.</div>
  <div>Multiply each value by its weight, add them all up. That sum is the new vector for <b>it</b>.</div>
</div>

<div v-click="3" class="punch">
  <span class="pv">new &#8220;it&#8221; = [0.90, 1.10]</span>
  <span class="parr">&#8776;</span>
  <span class="pv g">value of &#8220;glass&#8221; = [1, 1]</span>
</div>

<div v-click="4" class="statement-box">The word <b>it</b> has become, almost entirely, the word <b>glass</b>.</div>

<div v-click="5" class="transition-line">That is what attention is <i>for</i>. <span class="arrow">Not to score words &#8212; to move meaning from where it is to where it is needed.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.4em; font-size: 0.81rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.punch { display: flex; align-items: center; justify-content: center; gap: 1.1em; margin: 0.5em 0 0.35em; }
.pv { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; font-variant-numeric: tabular-nums; color: var(--ann-indigo); font-weight: 600; }
.pv.g { color: var(--qkv-value); }
.parr { font-size: 1.3rem; color: var(--ann-muted); }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.98rem; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
This is the slide most explanations skip, and it is the one that makes the
whole thing make sense. Attention is not a scoring system - the scores are
just the means. THIS is the output.

[click] The picture. Draw their eye to the fading: "the value vectors are
drawn at their own weight. Glass is nearly solid. Dropped is a ghost. Look
carefully - the ghost is still visible. Nothing is ever zero."

[click] The operation, in words: weight times value, all added up.

[click] The two vectors side by side. Let them compare digit by digit.

[click] The punchline, and it is genuinely lovely: the vector that entered
this layer meaning "it" leaves it meaning, near enough, "glass". The pronoun
has been resolved - not by a rule, not by a grammar module, but by a weighted
average.

[click] Then the generalisation, which is the sentence to remember from this
chapter: attention MOVES MEANING. Every layer, every word's vector gets
updated by the words around it, and after enough layers "it" carries
everything the sentence knows about that glass.

Likely student question: "Does that happen for every word at once?" Yes -
say so: "Every word does this simultaneously, in one matrix multiplication.
That's the trick that makes it fast, and it's why it needed to be told about
position."

Transition: "One more misconception to head off, and then what happens when
you stack this up."
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# It is a weighted average &#8212; that is all

<span class="eyebrow attention">Careful</span>

<div class="extremes">
  <div v-click="1" class="ex">
    <div class="exh">If one weight were 1 and the rest 0</div>
    <div class="exb">You would have a <b>lookup table</b>. Ask for &#8220;glass&#8221;, get glass.</div>
  </div>
  <div v-click="2" class="ex">
    <div class="exh">If every weight were the same</div>
    <div class="exb">You would have a <b>plain average</b>. Every word contributes equally, which is to say uselessly.</div>
  </div>
  <div v-click="3" class="ex mid">
    <div class="exh">Attention</div>
    <div class="exb">Lives <b>in between</b>, and the model <b>learns where</b> &#8212; separately for every word, in every sentence.</div>
  </div>
</div>

<div v-click="4" class="obs">This is why &#8220;it looks the answer up&#8221; is wrong, and why &#8220;it just averages everything&#8221; is also wrong. Those are the two <b>ends</b> of a dial. Attention is the dial.</div>

<div v-click="5" class="transition-line">The whole mechanism in one sentence: <span class="arrow">a weighted average, where the model computes its own weights.</span></div>

<style>
.extremes { display: flex; flex-direction: column; gap: 0.35em; margin: 0.5em 0; }
.ex { display: grid; grid-template-columns: 17em 1fr; gap: 1.2em; align-items: baseline; padding: 0.4em 0.9em; border-radius: 0.45em; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); }
.ex.mid { border-left: 4px solid var(--ann-circuit); background: var(--ann-circuit-soft); }
.exh { font-family: 'Space Grotesk', sans-serif; font-weight: 600; font-size: 0.92rem; color: var(--ann-indigo); }
.exb { font-size: 0.84rem; color: var(--ann-ink-soft); }
.exb b { color: var(--ann-ink); }
.obs { margin-top: 0.5em; font-size: 0.83rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
</style>

<!--
The cleanest cure for "there's a database inside" that exists, and it costs
one slide.

[click] One extreme: a hard lookup. Note this is a PERFECTLY GOOD thing to
be - it's what a dictionary does. It just isn't what this is.
[click] The other extreme: a flat average. Also a real thing, also not this.
[click] Attention sits between, and crucially the POSITION on that dial is
learned and changes word by word and sentence by sentence.

[click] Name both misconceptions at once and dispose of both. Students
usually hold one or the other; showing them as two ends of one dial fixes
both in a single move.

[click] The one-sentence version. Have them write it down. If a student
remembers exactly one sentence from this chapter, this is the one - it is
accurate, it is complete, and it is short enough to keep.

For the keen: this is not a new invention. It is a statistical technique
called kernel smoothing, which dates to 1964. Worth saying - it takes some of
the mystique off, in a good way, and it is true.

Transition: "One question I've been dodging: the model computes ONE set of
weights. Is one enough?"
-->

---
chapter: '4 · Attention, mechanically'
clicks: 5
---

# One set of weights is not enough

<span class="eyebrow math">Multi-head attention</span>

<div v-click="1" class="key-message">Different questions need different answers. So run the whole thing <b>many times in parallel</b>, with different matrices.</div>

<div class="heads">
  <div v-click="2" class="hd"><span class="hn">head 1</span>which noun does this pronoun mean?</div>
  <div v-click="2" class="hd"><span class="hn">head 2</span>what is the verb of this subject?</div>
  <div v-click="2" class="hd"><span class="hn">head 3</span>which adjective describes this thing?</div>
  <div v-click="2" class="hd"><span class="hn">head 4</span>&#8230; something nobody has a name for</div>
</div>

<div v-click="3" class="obs">
  <div>Each head gets its <b>own</b> <span class="q">W<sub>Q</sub></span>, <span class="k">W<sub>K</sub></span> and <span class="v">W<sub>V</sub></span>, so each learns to ask a different kind of question. Their answers get joined back together.</div>
  <div>GPT-3 ran <b>96</b> heads in each of <b>96</b> layers.</div>
</div>

<div v-click="4">

<Callout>
  <template #misconception>Each head has a job, and researchers know what each one does.</template>
  <template #clarification>A <b>few</b> heads do something you can name &#8212; there are famous ones that track the previous word, or match verbs to subjects. <b>Most do not.</b> And you can delete a surprising number with almost no effect: one study pruned <b>38 of 48</b> heads and lost almost nothing. But you still need them <b>all while it is learning</b>.</template>
</Callout>

</div>

<div v-click="5" class="transition-line">Many questions, asked at once, about every word. <span class="arrow">And then it all has to become an actual word.</span></div>

<style>
.heads { display: grid; grid-template-columns: 1fr 1fr; gap: 0.25em 1.2em; margin: 0.45em 0; }
.hd { display: flex; align-items: baseline; gap: 0.7em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.hn { font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.06em; color: var(--qkv-query); flex: 0 0 4.6em; }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.35em; font-size: 0.81rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.35em; font-size: 0.98rem; }
.slidev-layout .callout { font-size: 0.73rem; }
.slidev-layout .callout-row { padding: 0.32em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.35em; }
</style>

<!--
[click] The motivation first: one weighting can only express one kind of
relationship, and a sentence has many at once.

[click] Four example questions. The fourth is deliberate and important - be
honest that most heads are not interpretable. Do not present a tidy picture
you are about to demolish.

[click] The mechanism (own matrices, results joined) and the scale. Let the
96 x 96 land.

[click] The callout. This is a correction to something students will read
everywhere online, because the original paper said heads "may" be
interpretable and every summary since dropped the hedge. Give the real
picture: a few named heads, mostly not, heavily prunable AFTER training but
necessary DURING it.

The last clause is the interesting bit and worth a sentence: you cannot just
train a small model with four heads and get the same result. You need the
many heads to find the good solution, and then most of them turn out to be
scaffolding. That is a genuinely strange fact about how these things learn.

[click] Transition.

Transition: "We've now got vectors that have been enriched by their
neighbours, ninety-six ways, ninety-six times over. How does that become a
word?"
-->

---
chapter: '4 · Attention, mechanically'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 4 &#183; takeaway</span>

<PipelineMap highlight="attention" />

<div v-click="1" class="recap">
  <div>Every word produces a <span class="q">query</span>, a <span class="k">key</span> and a <span class="v">value</span> &#8212; three views of one vector, through three <b>learned</b> matrices.</div>
  <div><span class="q">Query</span> &#183; <span class="k">key</span> gives a score. Divide by &#8730;d. Softmax turns scores into shares that add to <b>1</b>.</div>
  <div>The output is those shares applied to the <span class="v">values</span> &#8212; a <b>blend</b>. Meaning moves from where it is to where it is needed.</div>
</div>

<div v-click="2" class="transition-line">Everything after this is <b>consequences</b>. <span class="arrow">Starting with: how does a pile of vectors become a word?</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.32em; margin-top: 0.6em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
The most important recap in the deck. Take a full minute; do not rush into
chapter 5.

[click] Three lines, and they should be able to reconstruct the whole
mechanism from them. Read each one slowly. If you have time, ask the room to
tell you what comes after "query dot key gives a score" before you say it.

[click] Then reframe the rest of the lecture: the hard part is done. Say that
explicitly - it gives people who struggled through chapter 4 a reason to stay
rather than quietly checking out.

This is also the natural place for a break if you are taking one. Two hours
is long; a five-minute break here costs you nothing and buys back attention
for chapters 5 and 6.

Transition: "Right. You've got a vector. You need a word."
-->
