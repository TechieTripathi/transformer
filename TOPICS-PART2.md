# Transformers II — Topic Summary

One idea per slide, in the order of `transformers-2.md`. Part I is indexed in
[TOPICS.md](TOPICS.md).

**The spine.** Part I built the decoder-only machine. Part II draws the 2017
original: chapter 1 shows what the Transformer replaced, and removing the
recurrence leaves no sense of order, so chapter 2 restores it properly.
Chapter 3 scales one attention head to many with real shapes. Chapters 4 and
5 assemble the two towers, and chapter 5 adds the one genuinely new box,
cross-attention. Chapter 6 traces one sentence through every tensor.
Chapter 7 covers the training details, and chapter 8 asks what actually does
the work.

**The map.** `EncDecMap` is to Part II what `PipelineMap` is to Part I: one
fixed picture of both towers, re-shown at the end of every chapter with a
different box lit.

---

## Opening

- **Part I drew half the machine** — The decoder column is Part I. The 2017
  translator also had an encoder and a bridge between the two: cross-attention.
- **The plan** — Eight chapters. Same rule as Part I: every number comes from
  `scripts/verify-attention.py`.

## Chapter 1 · Before attention

- **Translation, 2014** — An encoder RNN squeezes the source into one vector,
  and a decoder RNN unrolls it. Long sentences don't fit through the bottleneck.
- **Why far-away words are hard to learn** — A signal multiplied by 0.5 per step
  for 10 steps is about 0.001; by 1.5, it is about 58. Vanishing and exploding
  gradients.
- **The LSTM patch** — A cell state that is updated by addition, plus forget,
  input and output gates. Better plumbing, but the same one-step-at-a-time queue.
- **The 2014 fix** — Let the decoder look back at every encoder state (Bahdanau
  attention). Writing *ours*, it leans on *bear*.

## Chapter 2 · Position, properly

- **Option 1: learned positions** — A table with one row per slot. It works
  well, but it has a last row.
- **Option 2: a clock with many hands** — Sinusoidal encoding. Each sin/cos pair
  is a hand turning at its own speed. Nothing is learned and nothing runs out.
- **What the encoding looks like** — A 16 × 16 heat strip. The hands' periods
  run from 6.3 to 19,869 positions.
- **Nearby positions look alike** — With d = 512, similarity is 0.97 at
  distance 1 and 0.62 at distance 20. RoPE rotates Q and K instead.

## Chapter 3 · Many heads, with shapes

- **Same three words, two different questions** — Head 1 is Part I's (*it →
  glass* 0.85). Head 2 sends every word to *dropped* (0.80).
- **Slice the vector, don't copy it** — `d_k = d_model / h`: 4/2 = 2, 512/8 = 64,
  12,288/96 = 128. Many heads cost about the same as one.
- **Lay the answers side by side, then mix** — Concatenate the heads to 3 × 4,
  multiply by W_O, and you are back at d_model. Like CNN filters.

## Chapter 4 · The encoder

- **One encoder block** — Self-attention → Add & Norm → FFN → Add & Norm.
  `LayerNorm(x + Sublayer(x))`.
- **No mask** — The source is given, so every word sees every word. That is
  bidirectional, and it is why BERT works.
- **The feed-forward widens 4×** — 7 × 512 → 7 × 2048 → 7 × 512. Per layer it
  has twice the parameters of attention.
- **Six times, then hand over** — N = 6. The output is a 7 × 512 memory that
  every decoder layer reads.

## Chapter 5 · The decoder

- **Start from `<BOS>`** — The decoder's input is everything written so far,
  beginning with the begin token.
- **Masked self-attention** — The mask is essential in training (teacher
  forcing) and harmless at inference.
- **Cross-attention: ask the encoder** — Q comes from the decoder; K and V come
  from the encoder. The score matrix is decoder length × encoder length.
- **Cross-attention, by hand** — The decoder has written "&lt;BOS&gt; le" and
  the encoder holds "the cat sleeps": *le* puts 0.77 on *cat*. The grid is
  2 × 3.
- **From vector to word, until `<EOS>`** — 1 × 512 → 1 × 37,000 → softmax →
  pick → append. The output matrix is shared with the embeddings.

## Chapter 6 · One sentence, end to end

- **The sentence and the settings** — *A cute teddy bear is reading .* →
  *Un ours en peluche mignon lit .* The base model: d_model 512, h 8, d_k 64,
  d_ff 2048, N 6, vocab 37,000.
- **Through the encoder** — 7 × 512 throughout, except 8 × 7 × 7 for the scores
  and 7 × 2048 for the FFN.
- **Through the decoder, and across** — Masked scores are 8 × 8 × 8;
  cross-attention scores are 8 × 8 × 7.
- **Out the top** — Logits are 8 × 37,000. Training uses every row; inference
  uses the last row, and the encoder runs only once.

## Chapter 7 · Tricks that make it train

- **Add & Norm, revisited** — The residual gives the gradient a factor-1 road
  back. LayerNorm keeps the scale sane. The 2017 model is post-norm; modern
  models are pre-norm.
- **Dropout** — Zero 10% of units at random during training, and none at
  inference.
- **Label smoothing** — Train towards 0.9 on the right token and 0.025 on each
  of the others. The loss against the smoothed target can never reach 0.
- **Why smoothing helps** — Translations have many valid phrasings. Perplexity
  got worse and BLEU got better.

## Chapter 8 · What it all adds up to

- **Where the 63 million numbers live** — FFN 40%, shared embeddings 30%,
  attention 30%, LayerNorm about 0 (the paper says 65M). Data quality is part
  of the system.
- **The same softmax, two jobs** — Inside attention it gives mixing weights
  over keys; at the top it gives a prediction over the vocabulary.
- **Keep one tower, or both** — Encoder-only (BERT), encoder–decoder (2017, T5)
  and decoder-only (GPT). Decoder-only scaled into LLMs, and then agents.
- **Every fix, and the problem it fixed** — The whole argument of both decks as
  one problem → fix table.
- **Credits** — Stanford CME 295, Vaswani et al., Bahdanau et al., The
  Annotated Transformer, The Illustrated Transformer.
