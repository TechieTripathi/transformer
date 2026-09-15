# Transformers — Topic Summary

A concise, one-idea-per-topic index. Mirrors the slide order in
`transformers.md`.

**The spine.** Each chapter's opening problem is created by the previous
chapter's ending. Chapter 1 leaves us with arbitrary integer labels, so
chapter 2 turns them into meaningful vectors. Chapter 2 leaves every word
isolated at its dictionary meaning, so chapter 3 asks which other words matter.
Chapter 3 states a wish without a mechanism, so chapter 4 builds one and runs it
by hand. Chapter 4 produces enriched vectors, so chapter 5 turns them into a
word. Chapter 5 ends at a probability distribution without choosing from it, so
chapter 6 covers the choosing. Chapter 7 fills in the rest of the architecture
and where every number came from. Chapter 8 is the calibration chapter.

**The question the deck is built around.** Chapter 3 asks what *it* refers to in
*"The boy dropped the glass because it was slippery."* Chapter 4 answers with
**0.85**, computed on screen.

---

## Chapter 1 · Text is not letters

- **What the machine actually sees** — Text is cut into tokens; the input to the
  whole machine is a short list of integers, and the space belongs to the word
  after it.
- **Four times the same word** — `Egg`, `␣Egg`, `␣egg`, `␣EGG` are four
  unrelated ids, two of which are not even single tokens. The model learns they
  mean the same thing only from use.
- **Why it is bad at arithmetic** — `127` is one chunk, `677` is `␣6`+`77`. The
  cuts have nothing to do with hundreds, tens and units.
- **Not everyone pays the same price** — The same greeting is 4 tokens in
  English and 14 in Korean: a 3.5× tax in money and in context, paid by the
  speaker.
- **"How many R's in strawberry?"** — `str`+`aw`+`berry`. The letters were never
  in the input; a whole category of failure follows.
- **The token that was never trained** — `GoldMagikarp` earned a token when the
  chunks were counted, then its text was filtered out before training. The
  machine-learning equivalent of reading uninitialised memory.
- **One word explains all of it** — Six questions, one answer: tokenization.

## Chapter 2 · Turning words into numbers

- **A label is not a meaning** — Token ids order words arbitrarily; a vector of
  numbers lets similar words agree slot by slot. That vector is an *embedding*.
- **Words become places** — Similar words land near each other. Distributional
  similarity is not meaning, and the distinction matters.
- **Directions mean things** — `sushi − Japan + Germany ≈ bratwurst`. The famous
  `king − man + woman` version is partly an artefact of the search being
  forbidden to return its own inputs — paid off in chapter 8.
- **The bag-of-words problem** — *Dog bites man* and *Man bites dog* have
  identical words and identical embeddings. Attention sees a set, not a
  sequence.
- **Just add the position in** — A position vector is added to the word vector,
  so one vector carries both facts. Modern models rotate instead of adding.

## Chapter 3 · Which words matter?

- **The boy dropped the glass because *it* was slippery** — The question the
  talk is built around. You knew instantly, without checking every word.
- **You weighted the words** — Uneven weighting is the idea, and it has a name.
- **The spotlight — and what is wrong with it** — A spotlight leaves the stage
  dark; attention leaves every light on. *"Actual human attention is selective,
  but this gives some weight to every available vector."* The shares sum to 1
  and none is ever 0.
- **Everyone: hold up a number** — 500 students compute an attention row by
  hand: rate each word 0–5, total, normalise. Nothing gets zero; nobody picks a
  winner.

## Chapter 4 · Attention, mechanically

The centrepiece. Three words from the running sentence, `d_model = 4`,
`d_k = 2`, every dot product a two-term sum. All figures come from
`scripts/verify-attention.py`, cross-checked against PyTorch.

```
x_glass   [0,2,0,1]     q [-1, 1]   k [ 1,-1]   v [1,1]
x_dropped [1,0,1,0]     q [ 2,-1]   k [ 0,-1]   v [0,1]
x_it      [2,0,2,1]     q [ 3,-1]   k [-1,-3]   v [1,3]

QK^T row for "it":  4, 1, 0   →   ÷√2   →   softmax   →   0.8482, 0.1017, 0.0501
output for "it": [0.8983, 1.1003]   ≈   v_glass = [1, 1]
```

- **Every word plays three roles** — query asks, key advertises, value delivers.
  Keys and values differ on purpose.
- **The library — and the smoothie** — Keep the three roles, discard the part
  where you take one book. You take 85% of one, 10% of another, 5% of a third.
- **Measuring a match: the dot product** — Multiply matching slots, add up.
  `[2,3]·[4,1] = 11`.
- **The worked example** (1–6) — setup, the three projections, the nine scores,
  the √d_k division, softmax, and the blend.
- **Why we divide first** — `softmax(x)` spreads; `softmax(8x)` collapses onto
  one winner. Scaling keeps softmax soft, and a saturated row has nothing left
  to learn from.
- **0.85** — The payoff. The chapter-3 question, answered by arithmetic.
- **What the weights are for** — The new vector for *it* is `[0.90, 1.10]`,
  almost exactly `v_glass`. Attention moves meaning from where it is to where it
  is needed.
- **It is a weighted average — that is all** — A one-hot weighting is a lookup
  table; a flat one is a plain average; attention is the continuum between, and
  the model learns where on it to sit.
- **One set of weights is not enough** — Multi-head. A few heads do something
  nameable, most do not, and you need them all *while it is learning*.

## Chapter 5 · From numbers to the next word

- **One score for every word it knows** — Logits: the same dot product as
  chapter 4, now against the whole vocabulary.
- **It does not know the answer. It has odds.** — There is no answer inside it,
  only a distribution. "Knowing" is a high number, not a fact.
- **One word at a time, and then again** — Each output is glued onto the input
  and the whole machine runs again. The typing effect is the mechanism, not an
  animation.
- **The whole job, in one line** — `P(next token | everything before it)`.
  Everything else is a side effect of doing that very well.
- **One complete example** — *What is the capital of France?* end to end.

## Chapter 6 · The knobs you actually turn

- **Always take the best one?** — Greedy is deterministic and reads flat;
  sampling rolls a weighted die. Human text is not the most probable text.
- **Temperature: how sharp the odds are** — Same model, same prompt, same
  logits; only a division changed. `T → 0` *is* greedy.
- **Temperature does not change the model** — One line of real library code:
  `scores = scores / temperature`, applied after the network has finished. It is
  a variety knob, not a quality knob.
- **Top-K** — Keep the best K, delete the rest; probability becomes exactly
  zero, which temperature can never achieve.
- **Top-P** — Keep enough to cover P. On a confident distribution that is two
  tokens; on a flat one, hundreds. It adapts; Top-K cannot.
- **The same five words, two rules** — Identical input, Top-K=3 keeps three and
  Top-P=0.9 keeps two. How many, how much, how sharp.
- **Two completely different kinds of number** — 175 billion learned parameters
  versus six generation settings. The exam instruction changes the answer, not
  the student.
- **The context window** — Input + output ≤ the limit. Quadratic cost from
  chapter 4, counted in tokens from chapter 1.

## Chapter 7 · Inside the block

- **Look, then think** — Attention is communication, feed-forward is
  computation. Two thirds of the parameters are in the feed-forward parts, and
  that is where facts appear to live.
- **The road that runs through everything** — Residual connections add rather
  than replace, which is what makes ninety-six layers possible. A vector that
  starts as *king* is nudged until it means Macbeth.
- **"Isn't that cheating?"** — Setting future scores to zero fails, because
  `e⁰ = 1`. Setting them to −∞ before softmax works exactly. It sees everything;
  we blindfold it.
- **The causal mask** — A rule, not learned weights. It is also why one sentence
  of *n* words is *n* training examples in one pass.
- **The KV cache** — Keys and values never change once computed, *because of the
  mask*. The speed-up is bought by the blindfold.
- **Millions of knobs** — Predict, compare, nudge, repeat. Nobody wrote a
  grammar.
- **How wrong, and which way** — Loss and backpropagation. Calculus, not
  awareness.

## Chapter 8 · What it still gets wrong

- **Why this design took over** — Any-distance relationships, parallel training,
  scaling, and generality. Nothing in chapter 4 mentioned words.
- **Probable is not the same as true** — No step anywhere checks truth. A
  confident wrong answer and a confident right one come from the same process.
- **The famous demo that is partly a trick** — `king − man + woman`: lift the
  exclusion and one standard score falls from ~72% to ~19%. Real effect, bad
  thermometer.
- **The attention picture is not an explanation** — It shows what the model
  looked at, not what it used. Different weights can give the same answer; big
  weights can carry tiny values; layers mix. And the most-attended token is
  often the meaningless first one, because softmax must hand out 100%.
- **Transformer, or LLM?** — A shape, versus that shape at scale. The
  architecture is not the achievement; it is what made the achievement
  affordable.
- **If you remember only this** — Seven things, and seven is the ceiling.
