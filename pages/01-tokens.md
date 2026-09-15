---
layout: section
chapter: '1 · Text is not letters'
---

# Chapter 1

## Text is not letters

<div v-click class="thesis" style="margin-top:0.8em">Before a machine can be clever about language, it has to chop it up. Almost everything strange about AI starts with where the cuts fall.</div>

<!--
Twenty seconds. Say the thesis and move.

Frame the surprise: "Every explanation of AI you have ever seen starts with
'the model reads your words'. That is the first thing I am going to take away
from you, because it is false, and because almost every weird failure you have
laughed at online is a direct consequence of it being false."

Transition: "Here is a sentence."
-->

---
chapter: '1 · Text is not letters'
clicks: 3
---

# What the machine actually sees

<span class="eyebrow why">Start here</span>

<div class="key-message">Text is cut into <b>tokens</b> &#8212; chunks that are often words, but not always, and not reliably.</div>

<div v-click="1">

<TokenStrip
  :tokens="['The', ' cat', ' sat', ' on', ' the', ' mat']"
  :ids="[791, 8415, 7731, 389, 279, 5634]"
  :show-ids="true" />

</div>

<div v-click="2" class="obs">
  <div><b>The colours mean nothing.</b> They only show you where the cuts fall.</div>
  <div><b>The <span class="dot">&#8901;</span> is a space</b> &#8212; and look where it sits: the space belongs to the word <i>after</i> it. <code>&#8901;cat</code> is one token.</div>
  <div><b>Those numbers are the whole input.</b> Not letters. Not words. Six numbers.</div>
</div>

<div v-click="3" class="transition-line">The machine never sees &#8220;cat&#8221;. It sees <b>8415</b>. <span class="arrow">And it has to learn everything about cats from how 8415 behaves.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.3em; margin-top: 0.6em; font-size: 0.86rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.dot { font-family: 'JetBrains Mono', monospace; background: #f0f0f0; padding: 0 0.25em; border-radius: 3px; color: #111827; }
.slidev-layout .key-message { margin: 0.35em 0 0.6em; }
.slidev-layout .transition-line { margin-top: 0.7em; padding-top: 0.5em; }
</style>

<!--
This is the slide that resets their mental model, so do not rush it.

Read the sentence out loud first, then reveal.

[click] The strip. Let them look for a second before saying anything. Then:
"Six chunks. In this case they happen to line up with the six words - that is
luck, and it runs out fast."

[click] Three observations, in this order, because the third is the payload:
- colours are a partition marker, nothing more. Say it explicitly or three
  hundred people will spend the next ten minutes hunting for the meaning of
  blue.
- the space. Point at it. "The token is not 'cat', it is 'space-cat'. That
  sounds like trivia. It is the reason that if you leave a trailing space at
  the end of your prompt, some models get measurably worse - you have handed
  them a chunk they almost never saw in training."
- the numbers. This is the real reset: the input to the entire machine is a
  short list of integers. Everything from here on is arithmetic on those.

[click] The transition line. Land it slowly: whatever the machine knows about
cats, it learned from the behaviour of the number 8415 across the internet.
Nobody ever told it what a cat is.

Likely student question: "Why not just use letters? Or whole words?" Answer:
"Both were tried. Letters make the sequences enormously long - and the longer
the sequence, the more expensive attention gets, as we'll see in chapter 4.
Whole words means a dictionary of millions, and you're helpless the first time
someone invents a word. Chunks are the compromise, and they're chosen by a
compression algorithm that just looks for common byte patterns. Nobody sat
down and designed these."

Transition: "The compromise has consequences. Here is the first one."
-->

---
chapter: '1 · Text is not letters'
clicks: 4
zoom: 0.93
---

# Four times the same word

<span class="eyebrow why">Consequence 1</span>

<div v-click="1">

<TokenStrip
  :tokens="['E', 'gg', '.', ' I', ' have', ' an', ' Egg', '.', ' egg', '.', ' E', 'GG', '.']"
  :ids="[36, 14736, 13, 358, 617, 459, 42313, 13, 19151, 13, 469, 23050, 13]"
  :show-ids="true"
  :size="19"
  caption="GPT-4's tokenizer. Thirteen tokens for six words." />

</div>

<div v-click="2" class="eggs">
  <div><code>Egg</code> at the start of a sentence</div><div><b>2 tokens</b> &#8212; <code>E</code> + <code>gg</code></div>
  <div><code>&#8901;Egg</code> mid-sentence</div><div><b>1 token</b>, id <span class="num">42313</span></div>
  <div><code>&#8901;egg</code> lower-case</div><div><b>1 token</b>, id <span class="num">19151</span> &#8212; a <i>different</i> number</div>
  <div><code>&#8901;EGG</code> shouted</div><div><b>2 tokens</b> &#8212; <code>&#8901;E</code> + <code>GG</code></div>
</div>

<div v-click="3">

<Callout>
  <template #misconception>The model knows these are all the word &#8220;egg&#8221;, because obviously they are.</template>
  <template #clarification>Nothing tells it that. Those are four <b>unrelated</b> numbers as far as the machine is concerned. It has to <b>learn from scratch</b>, out of billions of examples, that <span class="num">42313</span> and <span class="num">19151</span> mean the same thing &#8212; and it has to learn that separately for every single word you can capitalise.</template>
</Callout>

</div>

<div v-click="4" class="transition-line">This is a surprising amount of a model&#39;s effort. <span class="arrow">Just working out that the same word, dressed differently, is the same word.</span></div>

<style>
.eggs {
  display: grid; grid-template-columns: auto 1fr; gap: 0.02em 1.4em;
  margin: 0.35em 0; font-size: 0.8rem; align-items: baseline;
}
.eggs code { font-family: 'JetBrains Mono', monospace; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); padding: 0 0.3em; border-radius: 3px; }
.eggs b { color: var(--ann-indigo); }
.slidev-layout .callout { font-size: 0.78rem; }
.slidev-layout .callout-row { padding: 0.42em 0.9em; }
</style>

<!--
This is the slide that earns you the room's attention for the next two hours,
because it is a genuinely surprising fact about something they use weekly.

Before revealing anything, put the sentence up and ask the hall:
"Egg, Egg, egg, EGG. How many of these does the computer think are the same
word?" Take a show of hands for 4, for 2, for 1. Let them commit.

[click] The strip. Let them count.

[click] The breakdown. The answer to the question is NONE - all four are
different, and two of them are not even single tokens. Say the answer out
loud; do not make them infer it.

[click] The callout. The clarification is the real content: this is not a
quirk, it is a tax. Every irregular capitalisation is a separate thing to
learn. And it learned it - that is the impressive part - but it spent
capacity doing so.

[click] Transition.

Likely student question: "Couldn't they just lowercase everything first?"
Excellent question, take it seriously: "Early systems did. But then you lose
the difference between 'polish' and 'Polish', between 'us' and 'US', and you
can't reproduce capitalisation in the output. It's a real trade-off, and
modern tokenizers chose to keep the case and pay the cost."

Transition: "That's words. Now watch what it does to numbers."
-->

---
chapter: '1 · Text is not letters'
clicks: 4
---

# Why it is bad at arithmetic

<span class="eyebrow why">Consequence 2</span>

<div v-click="1">

<TokenStrip
  :tokens="['127', ' +', ' 6', '77', ' =', ' 8', '04']"
  :ids="[16799, 1343, 718, 3324, 796, 807, 3023]"
  :show-ids="true"
  caption="GPT-2's tokenizer." />

</div>

<div v-click="2" class="key-message">
<span class="num">127</span> is one chunk. <span class="num">677</span> is <span class="num">6</span> then <span class="num">77</span>. <span class="num">804</span> is <span class="num">8</span> then <span class="num">04</span>.
</div>

<div v-click="3" class="obs">
  <div>There is no rule here. The chunks are whatever the compression algorithm happened to find common on the internet.</div>
  <div><b>The model never sees the number.</b> It sees pieces, cut in a place that has nothing to do with hundreds, tens and units.</div>
  <div>Now imagine doing long addition when the digits arrive in arbitrary clumps and you are not allowed to write anything down.</div>
</div>

<div v-click="4" class="transition-line">It is not bad at arithmetic because it is stupid. <span class="arrow">It is bad at arithmetic because of where the cuts fell.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.5em; font-size: 0.85rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.5em 0; font-size: 1.02rem; }
</style>

<!--
[click] The strip. Give them a beat to spot it themselves - somebody always
does, and it lands better from a student than from you.

[click] Spell the split out. The contrast between 127 (whole) and 677 (split)
is the thing: it is inconsistent, and the inconsistency is arbitrary.

[click] The three observations. The third is the one that creates empathy -
ask them to actually picture doing column addition with the digits grouped
wrongly and no paper. That is the model's situation.

[click] The punchline. Deliver it as a defence of the machine, not an attack:
this is a design consequence, not a lack of intelligence.

TERMINOLOGY worth planting for chapter 7: this is also why giving a model a
calculator tool helps so much. It isn't a patch over stupidity, it's routing
around a representation problem.

Likely student question: "Newer models are better at maths though?" Answer:
"Yes, and partly for this exact reason - several newer tokenizers deliberately
force digits into groups of three, or into single digits, instead of letting
the compression algorithm choose. Changing where the cuts fall changed how
well it can count. That should tell you how much the cuts matter."

Transition: "Same story, much less funny, for anyone who doesn't speak
English."
-->

---
chapter: '1 · Text is not letters'
clicks: 4
---

# Not everyone pays the same price

<span class="eyebrow why">Consequence 3</span>

<div class="key-message" style="margin-top:-0.5em">A greeting costs <b>3.5&#215;</b> more in Korean than in English &#8212; for the same meaning.</div>

<div class="pricing">
  <div v-click="1" class="pc">
    <div class="lang">English</div>
    <div class="phrase">hello how are you</div>
    <div class="bar"><span style="width:28.6%"></span></div>
    <div class="cost"><b>4</b> tokens</div>
  </div>
  <div v-click="2" class="pc">
    <div class="lang">Korean</div>
    <div class="phrase">&#50504;&#45397;&#54616;&#49464;&#50836;</div>
    <div class="bar"><span style="width:100%"></span></div>
    <div class="cost"><b>14</b> tokens</div>
  </div>
</div>

<div v-click="3" class="obs">
  <div>Tokenizers are trained mostly on English text, so English gets the efficient chunks. Other scripts fall back to raw <b>bytes</b> &#8212; often several per character.</div>
  <div>You pay per token. You are also <b>limited</b> per token. So the same conversation costs a Korean speaker more money <i>and</i> gives them less room to work in.</div>
</div>

<div v-click="4" class="transition-line">Nobody decided this. <span class="arrow">It fell out of which text the chunks were counted on &#8212; which is exactly the kind of decision that deserves to be noticed.</span></div>

<style>
.pricing { display: flex; flex-direction: column; gap: 0.5em; margin: 0.5em 0; }
.pc { display: grid; grid-template-columns: 5.5em 11em 1fr 6em; align-items: center; gap: 0.9em; }
.lang { font-family: 'Space Grotesk', sans-serif; font-weight: 600; color: var(--ann-indigo); font-size: 0.9rem; }
.phrase { font-family: 'JetBrains Mono', monospace; font-size: 1rem; }
.bar { height: 16px; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); border-radius: 3px; overflow: hidden; }
.bar span { display: block; height: 100%; background: var(--ann-ember); border-radius: 0 4px 4px 0; }
.cost { font-family: 'JetBrains Mono', monospace; font-size: 0.86rem; color: var(--ann-ink-soft); }
.cost b { font-size: 1.15rem; color: var(--ann-ember); }
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.6em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.slidev-layout .key-message { margin: 0.3em 0 0.5em; }
</style>

<!--
Do not skip this one. It is thirty seconds of technical content and a large
amount of "why this subject matters", and in a room of 500 there will be
students who speak a language on the wrong side of this.

[click] English: four tokens.
[click] Korean: fourteen, for a shorter greeting. Let the bars do the work.

[click] The two consequences. Be precise that it is BOTH money and context -
people usually only hear the money one. Less context means the model can hold
less of their conversation in mind, for the same conversation.

[click] The point is the last line: this is an emergent consequence of a
technical choice nobody framed as a fairness decision. That is how most
unfairness in software happens, and noticing it is a skill.

Keep it factual, not preachy. The numbers are doing the arguing.

Likely student question: "Is it being fixed?" Answer: "Newer tokenizers are
much better - GPT-4's is roughly three times more efficient on Korean than
GPT-2's. So yes, and it got fixed because people measured it and complained."

Transition: "One more. This one explains a joke you have definitely seen."
-->

---
chapter: '1 · Text is not letters'
clicks: 5
zoom: 0.92
---

# &#8220;How many R&#8217;s in strawberry?&#8221;

<span class="eyebrow why">Consequence 4</span>

<div v-click="1" style="margin-top:-0.75em">

<TokenStrip
  :tokens="['str', 'aw', 'berry']"
  :ids="[496, 675, 15717]"
  :show-ids="true"
  :show-whitespace="false"
  :size="20" />

</div>

<div v-click="2" class="statement-box" style="margin-top:0.35em">

It is not looking at <span class="big-mono">s-t-r-a-w-b-e-r-r-y</span>. It is looking at <span class="big-mono">496, 675, 15717</span>.

</div>

<div v-click="3" class="obs">
  <div>Asking it to count letters is like asking you to count the letters in a word you have only ever <i>heard spoken</i>. It can often still answer &#8212; because somewhere in its training someone wrote the spelling down. It is <b>recalling</b>, not looking.</div>
</div>

<div v-click="4" style="margin-top:0.35em">

<Callout>
  <template #misconception>It got that wrong because it isn&#39;t very smart yet.</template>
  <template #clarification>It got it wrong because <b>the letters were never in the input.</b> This is a whole category of failure: anything about spelling, reversing a word, counting characters, or rhyming is a question about something the model was never shown. Knowing <i>which</i> failures are like this is most of knowing how to use the thing well.</template>
</Callout>

</div>

<div v-click="5" class="transition-line">One more, and this one is genuinely strange. <span class="arrow">There are tokens that break the machine.</span></div>

<style>
.obs { display: flex; flex-direction: column; gap: 0.35em; margin-top: 0.5em; font-size: 0.84rem; color: var(--ann-ink-soft); }
.slidev-layout .statement-box { padding: 0.4em 1em; font-size: 0.92rem; }
.slidev-layout .callout { font-size: 0.76rem; }
.slidev-layout .callout-row { padding: 0.38em 0.9em; }
</style>

<!--
They will know this one. Use that - ask who has seen an AI fail this question.
Lots of hands. Then: "Right. Here is why, and it is not what you think."

[click] Three chunks. Point at 'berry' holding two of the three R's and
'str' holding the first.

[click] The box. This is the sentence to say slowly.

[click] The analogy - a word you've only ever heard. This is the one that
lands with the whole ability range, so give it a breath. And the second line
is important for honesty: modern models often DO get it right now, and it is
worth saying why, because otherwise you look out of date and they stop
trusting you. They get it right by having memorised spellings from text, not
by looking.

[click] The callout. The clarification generalises it into something useful:
a category of question the machine is structurally bad at. That is a takeaway
they can actually use.

[click] Transition.

Likely student question: "So could you just tell it to spell the word out
first?" Answer: "Yes! And that works, and it's a real technique - make it
write s-t-r-a-w-b-e-r-r-y with spaces, which forces each letter into its own
token, and then it can count. You've just invented a prompting trick from
first principles, which is the best possible reason to understand this stuff."

Transition: "Last one."
-->

---
chapter: '1 · Text is not letters'
clicks: 5
zoom: 0.89
---

# The token that was never trained

<span class="eyebrow why">Consequence 5</span>

<div class="mk">
  <div v-click="1">
    <div class="mklbl">GPT-2 saw this as <b>two</b> tokens</div>
    <TokenStrip :tokens="['Solid', 'GoldMagikarp']" :ids="[46933, 42202]" :show-ids="true" :show-whitespace="false" :size="17" />
  </div>
  <div v-click="3">
    <div class="mklbl">GPT-4 chops it into <b>five</b></div>
    <TokenStrip :tokens="['Solid', 'Gold', 'Mag', 'ik', 'arp']" :ids="[47041, 26509, 34015, 1609, 8035]" :show-ids="true" :show-whitespace="false" :size="17" />
  </div>
</div>

<div v-click="2" class="obs">
  <div><code>GoldMagikarp</code> was a username. It appeared often enough when the <b>chunks were counted</b> to earn its own token &#8212; but the text it appeared in was then <b>filtered out</b> before training.</div>
  <div>So the model had a token it was <b>never shown</b>, whose entry kept the random numbers it started with. Ask GPT-2 about it and you got evasion, insults, nonsense.</div>
</div>

<div v-click="4" class="statement-box">It is the machine-learning equivalent of reading uninitialised memory.</div>

<div v-click="5" class="transition-line">Fixed, in the end, by chopping it up. <span class="arrow">Which tells you the bug was never in the model &#8212; it was in the chunking.</span></div>

<style>
.mk { display: flex; flex-direction: column; gap: 0.45em; margin-top: 0.2em; }
.mklbl { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--ann-muted); margin-bottom: 0.2em; }
.mklbl b { color: var(--ann-ember); }
.obs { display: flex; flex-direction: column; gap: 0.28em; margin-top: 0.5em; font-size: 0.8rem; color: var(--ann-ink-soft); }
.obs b { color: var(--ann-indigo); }
.obs code { font-family: 'JetBrains Mono', monospace; background: var(--ann-paper-raised); border: 1px solid var(--ann-line); padding: 0 0.3em; border-radius: 3px; }
.slidev-layout .statement-box { padding: 0.35em 1em; font-size: 0.88rem; margin-top: 0.4em; }
.slidev-layout .transition-line { margin-top: 0.5em; padding-top: 0.4em; }
</style>

<!--
This is the story students retell afterwards, so tell it properly. It is also
a genuinely good detective story, discovered by researchers poking at the
embedding table in 2023.

[click] GPT-2's view: two tokens, and the second one is an entire username.

[click] The explanation, in three beats. The crucial mechanism: the tokenizer
is trained on ONE pile of text, the model on ANOTHER. This username was
frequent in the first pile and absent from the second. So the token existed,
and the model never once saw it in use.

[click] GPT-4's view: five ordinary chunks. The weird token is gone.

[click] The one-liner. If anyone in the room codes, this analogy will land
hard; for everyone else, gloss it as "reading a page in a notebook that was
never written on - you get whatever noise happens to be there."

[click] The closing point is the one worth remembering: the fix was to the
chunking, not the model. Chapter 1's whole thesis in one sentence.

Likely student question: "Are there still tokens like this?" Answer: "Almost
certainly a few, in every model. People go looking for them - it's a small
research sport. But they're much rarer now that people know to check."

Transition: "Let me put all five of those together."
-->

---
chapter: '1 · Text is not letters'
clicks: 3
---

# One word explains all of it

<span class="eyebrow structure">Chapter 1 &#183; takeaway</span>

<div class="qlist">
  <div v-click="1">Why can&#8217;t it spell a word backwards?</div>
  <div v-click="1">Why is it bad at arithmetic?</div>
  <div v-click="1">Why does it cost more in Japanese?</div>
  <div v-click="1">Why did a trailing space make it worse?</div>
  <div v-click="1">Why did one username break it?</div>
  <div v-click="1">Why can&#8217;t it count the R&#8217;s?</div>
</div>

<div v-click="2" class="answer">Tokenization.</div>

<div v-click="3">

<PipelineMap highlight="tokens" compact />

<div class="transition-line">We have chunks, and each chunk is a number. <span class="arrow">But an id like 8415 is just a label &#8212; it says nothing about what a cat <i>is</i>. That is the next problem.</span></div>

</div>

<style>
.qlist { display: grid; grid-template-columns: 1fr 1fr; gap: 0.18em 1.6em; margin: 0.4em 0; font-size: 0.9rem; color: var(--ann-ink-soft); }
.answer {
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 2.1rem;
  color: var(--ann-ember); text-align: center; margin: 0.25em 0 0.1em;
}
.slidev-layout .transition-line { margin-top: 0.4em; padding-top: 0.4em; }
</style>

<!--
The rhythm is the point here. Read the six questions out loud, one after
another, without pausing for answers - let the list build.

[click] All six arrive together. Read them as a list, quickly, building.

[click] One word. Land it and then be quiet for a second.

This device is borrowed from Andrej Karpathy's tokenizer lecture, where the
same list runs to eleven items and ends with "What is the real root of
suffering? Tokenization." Worth crediting out loud - students like knowing
where things come from, and it points them at a good next resource.

[click] The map appears for the first time. Introduce it properly, because
they will see it six more times: "This is the whole machine. Every time it
comes back, the lit box is where we are. Right now we've done exactly one
box." Then the transition.

Transition: "So we have numbers. But 8415 is just a label - it's the cat's
seat number, not anything about cats. How do we get from a label to meaning?"
-->
