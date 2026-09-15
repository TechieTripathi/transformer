---
layout: section
chapter: '3 · Which words matter?'
---

# Chapter 3

## Which words matter?

<div v-click class="thesis" style="margin-top:0.8em">No word means anything on its own. To understand one word, you have to look at the others &#8212; and not at all of them equally.</div>

<!--
Twenty seconds.

"Chapter two left every word frozen and alone. This chapter is about what the
neighbours do to it - and I want to start by making you do the work, not the
machine."

Transition: "Read this."
-->

---
layout: statement
chapter: '3 · Which words matter?'
clicks: 3
---

# The boy dropped the glass because <span style="color:var(--ann-ember)">it</span> was slippery.

<div v-click="1" class="ask">What does <b>it</b> refer to?</div>

<div v-click="2" class="opts">
  <span>the boy?</span>
  <span>the glass?</span>
</div>

<div v-click="3" class="settle">You knew instantly. <b>You did not check every word to find out.</b></div>

<style>
h1 { font-size: 1.85rem; line-height: 1.4; max-width: 22em; margin-left: auto; margin-right: auto; }
.ask { margin-top: 1.1em; font-size: 1.15rem; color: var(--ann-ink-soft); }
.opts { display: flex; gap: 2.5em; justify-content: center; margin-top: 0.7em; font-family: 'Space Grotesk', sans-serif; font-size: 1.25rem; font-weight: 600; color: var(--ann-indigo); }
.settle { margin-top: 1.2em; font-size: 1rem; color: var(--ann-ink-soft); max-width: 30em; margin-left: auto; margin-right: auto; }
.settle b { color: var(--ann-ember); }
</style>

<!--
SLOW DOWN. This is the question the entire lecture answers, and chapter 4
answers it with an actual number. Set it up properly.

Read the sentence out loud.

[click] Ask the question. Then WAIT. Genuinely wait - five full seconds of
silence in a room of 500 is uncomfortable for you and productive for them.

[click] Offer the two options and take a show of hands. Almost everyone says
glass. A few will say boy, and it is worth saying that "boy" is not insane -
boys can be slippery - it is just much less likely given "dropped".

[click] The observation that matters. They did not scan the sentence. They
did not weigh "the" against "because". Something in their reading jumped
straight to the connection.

MAKE THE PROMISE, LOUDLY AND SPECIFICALLY: "By the end of chapter four I am
going to put a number on that connection. Not a hand-wave - an actual number,
computed from these words, on this slide, and you will be able to check the
arithmetic." Then pay it on the payoff slide.

Transition: "So how DID you know?"
-->

---
chapter: '3 · Which words matter?'
clicks: 4
---

# You weighted the words

<span class="eyebrow intuition">Intuition</span>

<div v-click="1">

<SpotlightSentence
  :words="['The','boy','dropped','the','glass','because','it','was','slippery']"
  :weights="[0.02,0.10,0.05,0.02,0.55,0.03,0,0.03,0.20]"
  :query="6"
  note="Roughly what your reading did: most of the work on glass, some on slippery, a little on boy, and never quite nothing on anything." />

</div>

<div v-click="2" class="obs">
  <div><b>glass</b> got most of your attention &#8212; it is the thing that was dropped, and things that are dropped are the things that are slippery.</div>
  <div><b>slippery</b> got a good share too, because it is the word that made the question worth asking.</div>
  <div><b>boy</b> got a little. You did consider it. You just rejected it fast.</div>
</div>

<div v-click="3" class="key-message">That uneven weighting <i>is</i> the idea. It has a name: <b>attention</b>.</div>

<div v-click="4" class="transition-line">And because these are weights, they can be numbers. <span class="arrow">Which is the only reason a machine can do this at all.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.5em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-ember); }
.slidev-layout .key-message { margin: 0.5em 0 0.35em; }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.4em; }
</style>

<!--
[click] The picture. Let them read it before you talk.

[click] Walk the three observations. The third one is doing quiet but
important work: "boy" is not zero. They considered it. Point at the small bar
and say so - you are pre-loading the correction that arrives two slides from
now, so that when it lands it feels obvious rather than pedantic.

[click] Name it. Attention. Write it down.

[click] The bridge to arithmetic.

Note the word "it" has no bar of its own here - it is the word doing the
asking, not one of the words being looked at. Somebody will ask; the honest
answer is that in the real mechanism a word does attend to itself, and we
will see exactly that in chapter 4, where "it" gives itself 0.05.

Transition: "Now, the usual way this gets explained - and why I'm going to
take it away from you."
-->

---
chapter: '3 · Which words matter?'
clicks: 5
---

# The spotlight &#8212; and what is wrong with it

<span class="eyebrow attention">Careful</span>

<div v-click="1" class="metaphor">
  <span class="mi">&#128295;</span>
  <div>The usual picture: attention is a <b>spotlight</b>. It shines on the important word and leaves the rest of the stage dark.</div>
</div>

<div v-click="2" class="quote">
  &#8220;Actual human attention is <b>selective</b>, but this gives <b>some weight to every available vector</b>.&#8221;
  <span class="attr">&#8212; Cosma Shalizi, statistician</span>
</div>

<div v-click="3">

<Callout>
  <template #misconception>Attention picks the important word and ignores the others.</template>
  <template #clarification>It <b>never ignores anything</b>. Every word gets a share, and the shares always add up to exactly 1. A word can get 0.001 &#8212; it can never get 0. What comes out is a <b>blend of every word in the sentence</b>, mixed in proportion. The spotlight leaves the stage dark; this leaves every light on, at different brightness.</template>
</Callout>

</div>

<div v-click="4" class="obs">Why does this matter? Because &#8220;it picks the right word&#8221; makes you expect a machine that <b>decides</b>. What it actually does is <b>average</b> &#8212; and that explains far more of its behaviour, including its failures.</div>

<div v-click="5" class="transition-line">Keep the spotlight if it helps you. <span class="arrow">But remember the stage is never dark.</span></div>

<style>
.metaphor { display: flex; align-items: center; gap: 0.8em; font-size: 0.95rem; color: var(--ann-ink-soft); margin-top: -0.2em; }
.mi { font-size: 2.1rem; line-height: 1; }
.metaphor b { color: var(--ann-ink); }
.quote {
  margin: 0.6em 0; padding: 0.55em 1em;
  border-left: 4px solid var(--ann-ember); background: var(--ann-ember-soft);
  border-radius: 0.4em; font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem; line-height: 1.45;
}
.quote b { color: var(--ann-ember); }
.attr { display: block; margin-top: 0.25em; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--ann-ink-soft); }
.obs { margin-top: 0.5em; font-size: 0.82rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .callout { font-size: 0.76rem; }
.slidev-layout .callout-row { padding: 0.38em 0.9em; }
.slidev-layout .transition-line { margin-top: 0.45em; padding-top: 0.4em; }
</style>

<!--
This slide is the most valuable correction in the deck. Do not rush it, and
do not apologise for it.

[click] Offer the spotlight metaphor as the thing they will meet everywhere -
because they will, it is in almost every explainer online.

[click] The quote. Read it out loud, both halves. Shalizi is a statistician
who has written at length about how badly the word "attention" was chosen; he
is worth quoting because he is not a hater, he is precise.

[click] The callout. The clarification has the two facts that matter: the
weights sum to 1, and none of them is ever zero. The second follows from the
first plus the maths we meet in chapter 4 - exp of anything is positive - so
you can promise them a proof shortly.

[click] The "why it matters" line. This is the payload: the wrong metaphor
makes you expect a decider, and then every failure looks like stupidity. The
right one - a weighted average - makes the failures predictable.

[click] Be generous in the close. Metaphors are allowed to be imperfect; they
just have to be imperfect in a way you have told people about.

Likely student question: "If it never ignores anything, why does it work at
all? Isn't it drowning in irrelevant words?" Brilliant question - flag it as
such: "Partly yes, and that is a real cost. With a very long input the useful
signal does get diluted, which is one reason long documents are hard. The
weights do get extremely small, so in practice irrelevant words contribute
almost nothing - but 'almost nothing' is not nothing, and at scale that
difference shows up."

Transition: "Right. You've all got hands. Let's compute one of these."
-->

---
chapter: '3 · Which words matter?'
clicks: 5
---

# Everyone: hold up a number

<span class="eyebrow intuition">All of us &#183; two minutes</span>

<div class="sent">The &#183; cat &#183; sat &#183; on &#183; the &#183; <span class="q">mat</span></div>

<div v-click="1" class="steps">
  <div><span class="sn">1</span>Look at the word <b>mat</b>. For each <i>other</i> word, hold up fingers: <b>0</b> = tells me nothing about the mat, <b>5</b> = tells me a lot.</div>
  <div v-click="2"><span class="sn">2</span>I add up the fingers in the room for each word. Six totals.</div>
  <div v-click="3"><span class="sn">3</span>I divide each total by the sum of all of them, so they add to <b>1</b>.</div>
</div>

<div v-click="4" class="done">You have just computed an <b>attention row</b>, by hand, with 500 people.</div>

<div v-click="5" class="obs">
  <div>Notice what happened: <b>no word got zero</b>. Somebody in this room voted for &#8220;the&#8221;.</div>
  <div>Notice what we did <b>not</b> do: nobody picked a winner. We <b>pooled and normalised</b>.</div>
  <div>The machine does exactly this. The only difference is where the fingers come from.</div>
</div>

<style>
.sent {
  font-family: 'Space Grotesk', sans-serif; font-size: 1.7rem; font-weight: 600;
  text-align: center; margin: 0.3em 0 0.6em; color: var(--ann-circuit);
}
.sent .q { color: var(--ann-ember); border-bottom: 3px solid var(--ann-ember); }
.steps { display: flex; flex-direction: column; gap: 0.35em; font-size: 0.87rem; }
.steps > div { display: flex; align-items: flex-start; gap: 0.7em; }
.sn {
  flex-shrink: 0; width: 1.6em; height: 1.6em; border-radius: 999px;
  background: var(--ann-circuit-soft); color: var(--ann-circuit);
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.8rem;
  display: flex; align-items: center; justify-content: center;
}
.steps b { color: var(--ann-indigo); }
.done {
  margin: 0.7em 0 0.4em; padding: 0.5em 1em;
  background: var(--ann-indigo-soft); color: var(--ann-indigo);
  border-radius: 0.5em; font-family: 'Space Grotesk', sans-serif;
  font-weight: 600; font-size: 1.05rem; text-align: center;
}
.obs { display: flex; flex-direction: column; gap: 0.25em; font-size: 0.8rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-ember); }
</style>

<!--
DO THIS. It takes two minutes, it wakes the room up at exactly the point
where attention spans dip, and it plants the mechanism physically before any
notation arrives. In a hall of 500 it also produces a very satisfying amount
of noise.

Run it briskly:

[click] Step 1. Say the word, count to three, "fingers up". You are not
collecting accurate data, you are collecting a shape. Eyeball each word and
call out a rough total - "cat, lots; sat, quite a lot; on, some; the, a
couple of you, thank you, that is exactly the point."

[click] Step 2. Adding up = pooling everyone's opinion.

[click] Step 3. Dividing = normalising. This is softmax, without the
exponential, and you can say so: "there's one more wrinkle in the real thing
which we'll meet in a moment, but this is genuinely the operation."

[click] Tell them what they did. Be a bit triumphant about it.

[click] The three observations, and they are the point of the whole exercise:
nothing got zero; nobody picked a winner; the machine does this. Land the
last one and then say the sentence that sets up chapter 4:

"So the only question left - the ONLY one - is where the machine's fingers
come from. It has no opinions. It has to compute that number from the words
themselves. That is chapter four, and that is the hardest and best idea in
this lecture."

If the room is too big or too quiet for hands, run it as a thought experiment
with the same three steps; it still works, it is just less fun.

Transition: "Where do the fingers come from?"
-->

---
chapter: '3 · Which words matter?'
clicks: 2
---

# Where we are

<span class="eyebrow structure">Chapter 3 &#183; takeaway</span>

<PipelineMap :highlight="['tokens','embed','position']" pending="attention" />

<div v-click="1" class="recap">
  <div>To understand a word, look at the others &#8212; <b>weighted</b>, not equally.</div>
  <div>The weights add up to <b>1</b>, and none of them is ever <b>0</b>.</div>
  <div>The output is a <b>blend</b>, not a choice.</div>
</div>

<div v-click="2" class="transition-line">We know what we <b>want</b>. We have no idea yet how to <b>compute</b> it. <span class="arrow">That box is still empty. Chapter 4 fills it in.</span></div>

<style>
.recap { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.6em; font-size: 0.9rem; color: var(--ann-ink-soft); }
.recap b { color: var(--ann-indigo); }
</style>

<!--
Thirty seconds.

[click] Three lines. These are the three things a student should be able to
say back if you stopped them in the corridor.

[click] The hand-off. Be honest that we have described a wish, not a
mechanism - that honesty is what makes chapter 4 feel like a payoff rather
than more assertion.

Transition: "Chapter four is the centre of the lecture. Everything before it
was setup and everything after it is consequences."
-->
