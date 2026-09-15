---
layout: cover
class: title-cover
---

<div class="cover-motif">
  <svg viewBox="0 0 720 210" xmlns="http://www.w3.org/2000/svg">
    <!-- the sentence, as a row of words -->
    <g fill="var(--ann-ink-soft)" opacity="0.5">
      <circle cx="80"  cy="160" r="7" />
      <circle cx="200" cy="160" r="7" />
      <circle cx="320" cy="160" r="7" />
      <circle cx="440" cy="160" r="7" />
      <circle cx="560" cy="160" r="7" />
    </g>
    <!-- one word asking: ember -->
    <circle cx="640" cy="160" r="11" fill="var(--ann-ember)" />
    <!-- and what it attends to: every word, at different strengths.
         Nothing is ever zero - that is the whole lecture in one picture. -->
    <g fill="none" stroke="var(--ann-circuit)" stroke-linecap="round">
      <path d="M640,160 C560,60 400,50 320,150" stroke-width="9" opacity="0.85" />
      <path d="M640,160 C580,90 500,80 440,150" stroke-width="4" opacity="0.5" />
      <path d="M640,160 C540,50 280,40 200,150" stroke-width="2.5" opacity="0.35" />
      <path d="M640,160 C520,30 180,30 80,150"  stroke-width="1.5" opacity="0.25" />
      <path d="M640,160 C620,110 590,105 560,150" stroke-width="2" opacity="0.3" />
    </g>
  </svg>
  <div class="motif-key">one word &#183; looking at all the others &#183; thicker = more</div>
</div>

# Transformers

### How a machine reads a sentence, decides which words matter, and chooses what to say next

<div class="cover-meta">No prior knowledge assumed &#183; every number on these slides is checkable</div>

<style>
.cover-motif { width: min(38%, 340px); margin: 0 0 1.4em; }
.cover-motif svg { width: 100%; height: auto; display: block; }
/* Without this the motif is decoration. With it, the whole talk is on screen
   before a word is spoken. */
.motif-key {
  margin-top: 0.35em;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.64rem;
  letter-spacing: 0.04em;
  color: var(--ann-muted);
  /* the motif is capped at 340px; the caption is allowed past it */
  width: max-content;
  white-space: nowrap;
}
.cover-meta {
  margin-top: 1.2em;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  letter-spacing: 0.04em;
  color: var(--ann-muted);
}
</style>

<!--
Welcome them. Two hours, one machine, taken apart completely.

Say the promise out loud, because the whole deck is built on keeping it:
"By the end of this you will know every step between you typing a question
and a word coming back. Not a cartoon of it - the actual steps, with the
actual arithmetic. And I am not going to assume you have seen any of this
before."

Point at the motif: "That orange dot is one word in a sentence. Those lines
are it looking at the other words - thick where it cares, thin where it
doesn't. Notice every line is still there. Hold onto that; a lot of people
get it wrong and we'll come back to it."

Housekeeping worth 20 seconds: the slides are downloadable as a PDF from the
same link, so nobody needs to photograph the screen. Say it now and you kill
the phones-up problem for the whole session.

Transition: "Let's start somewhere that will surprise you. Before any of the
clever stuff, there is a question nobody thinks to ask: what does the machine
actually SEE when you type a word?"
-->

---
layout: default
chapter: ''
clicks: 4
zoom: 0.92
---

# Where we're going

<span class="eyebrow structure">The shape of the next two hours</span>

<div class="key-message">Each chapter exists because the one before it ran into a problem.</div>

<div class="roadmap">
  <div><span class="rn">1</span><div><b>Text is not letters</b><span>The machine never sees words. It sees chunks &#8212; and almost everything strange about AI starts here.</span></div></div>
  <div><span class="rn">2</span><div><b>Turning words into numbers</b><span>Chunks become vectors. Similar meanings land near each other, and position gets added in.</span></div></div>
  <div><span class="rn">3</span><div><b>Which words matter?</b><span>Meaning depends on other words. We need a way to measure &#8220;how much does this word matter to that one?&#8221;</span></div></div>
  <div v-click="1"><span class="rn">4</span><div><b>Attention, mechanically</b><span>The answer, worked by hand on three real words. <b>This is the centre of the lecture.</b></span></div></div>
  <div v-click="2"><span class="rn">5</span><div><b>From numbers to the next word</b><span>The machine never picks an answer. It produces a probability for every word it knows.</span></div></div>
  <div v-click="2"><span class="rn">6</span><div><b>The knobs you actually turn</b><span>Temperature, top-k, top-p &#8212; the settings you meet in every AI tool, and what they really do.</span></div></div>
  <div v-click="3"><span class="rn">7</span><div><b>Inside the block, and how it learned</b><span>The rest of the machine, and where all those numbers came from in the first place.</span></div></div>
  <div v-click="3"><span class="rn">8</span><div><b>What it still gets wrong</b><span>Why a confident answer is not a true one.</span></div></div>
</div>

<div v-click="4" class="transition-line">You do not need to remember this list. <span class="arrow">There is a map at the bottom of the deck, and I will keep showing you where we are on it.</span></div>

<style>
.roadmap { display: flex; flex-direction: column; gap: 0.08em; margin-top: 0.15em; }
.roadmap > div { display: flex; align-items: flex-start; gap: 0.7em; }
.rn {
  flex-shrink: 0; width: 1.55em; height: 1.55em; border-radius: 999px;
  background: var(--ann-indigo-soft); color: var(--ann-indigo);
  font-family: 'Space Grotesk', sans-serif; font-weight: 700; font-size: 0.78rem;
  display: flex; align-items: center; justify-content: center;
}
.roadmap b { font-family: 'Space Grotesk', sans-serif; font-size: 0.82rem; display: block; line-height: 1.2; }
.roadmap span:last-child { font-size: 0.7rem; color: var(--ann-ink-soft); line-height: 1.25; }
.slidev-layout .key-message { margin: 0.3em 0 0.5em; }
.slidev-layout .transition-line { margin-top: 0.6em; padding-top: 0.5em; }
</style>

<!--
Ninety seconds, not more. This slide is orientation, not content.

The one thing to actually say: every chapter here exists because the previous
one hit a wall. That is not a stylistic claim, it is how the lecture is built,
and telling them makes the whole thing easier to follow.

[click] Chapter 4 is the centre. Flag it now: "If you take one thing away,
it will be from chapter four, and we are going to do it slowly, by hand, with
numbers small enough that you can check my arithmetic. If you catch me making
a mistake, say so."

[click] Chapters 5 and 6 are the ones they can use on Monday - this is where
temperature and top-p get explained, and most of the room has seen those
sliders in some tool without knowing what they do. Promise it explicitly.

[click] 7 and 8 are the ones that matter for being a sensible adult about
this technology. Chapter 8 is the honesty chapter.

[click] Then reassure them about the map. In a room this size somebody will
lose the thread for a couple of minutes; the recurring map is how they get
back on without asking. Say that out loud - it gives people permission to
stop panicking when they drift, which is most of what stops them re-engaging.

Transition: "So. What does a machine see when you type a word?"
-->
