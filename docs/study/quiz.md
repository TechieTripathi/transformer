# Transformers — self-check quiz

30 questions across both decks. Multiple choice (**MC**) and work-it-out (**compute**) — every
compute answer can be checked against `scripts/verify-attention.py`. Answers and explanations are
at the bottom. This file is also the source for the Quiz tab in
[`transformers-study.html`](transformers-study.html) (`npm run study` after editing).

Format, for anyone adding questions: `### Qn · MC` or `### Qn · compute`, the question, options as
`- A) …`, and a matching `**Qn — X.**` line in the answer key.

---

### Q1 · MC
Which tokenizer gives the *shortest* sequence for ordinary English text?

- A) Character-level
- B) Byte-level with no merges
- C) Word-level
- D) All three give the same length

### Q2 · MC
The main reason modern models use subword tokenization is that it…

- A) Matches how linguists split words into morphemes
- B) Balances vocabulary size against sequence length and avoids unknown words
- C) Makes every word exactly one token
- D) Removes the need for embeddings

### Q3 · compute
BPE corpus: `read×4, reading×3, bear×4, bears×2, ring×2, sing×3`. Starting from single letters, which adjacent pair is merged first, and how many times does it occur?

### Q4 · MC
After seven merges, how does the tokenizer split the unseen word *rings*?

- A) `<UNK>`
- B) `rings`
- C) `r | ing | s`
- D) `ri | ngs`

### Q5 · MC
Which special token tells a model that generation is finished?

- A) `<BOS>`
- B) `<PAD>`
- C) `<UNK>`
- D) `<EOS>`

### Q6 · MC
Why are one-hot vectors poor word representations?

- A) They are too short
- B) Every pair of them is orthogonal, so they cannot express similarity
- C) They change during training
- D) They depend on word order

### Q7 · MC
In Word2Vec, which part of the trained network becomes the word embedding?

- A) The softmax output
- B) The input one-hot vector
- C) The hidden (middle) layer
- D) The loss value

### Q8 · MC
"She sat on the river bank" / "She paid money into the bank". What does a static embedding table give *bank*?

- A) Two different vectors, chosen by context
- B) The same vector both times
- C) No vector — it is ambiguous
- D) A vector equal to *river* + *money*

### Q9 · MC
Which is **not** a limitation of a plain RNN?

- A) Early information fades over long sequences
- B) Steps must be computed one after another
- C) It cannot handle sequences of different lengths
- D) The training signal can vanish as it travels back through steps

### Q10 · compute
A training signal is multiplied by 0.5 at each step back through an RNN. Roughly what fraction remains after 10 steps?

### Q11 · MC
What did attention, as added to RNN translators in 2014, remove?

- A) The need for a vocabulary
- B) The single fixed-size vector between encoder and decoder
- C) The decoder
- D) Training altogether

### Q12 · compute
Worked example: `q_it = [3, −1]`, `k_glass = [1, −1]`, `d_k = 2`. Compute the scaled score q·k / √d_k.

### Q13 · MC
Dividing scores by √d_k mainly prevents…

- A) Negative scores
- B) Softmax saturating into a near one-hot distribution
- C) Rows summing to more than 1
- D) The model attending to itself

### Q14 · MC
For a sequence of n tokens, what is the shape of Q·Kᵀ in self-attention?

- A) n × d_k
- B) d_k × d_k
- C) n × n
- D) 1 × n

### Q15 · MC
In the worked example, "it" puts 0.85 of its attention on "glass". Its output vector is therefore close to…

- A) q_glass
- B) k_glass
- C) v_glass
- D) The average of all three value vectors

### Q16 · compute
A model has d_model = 512 and h = 8 heads. What is d_k per head, and what is √d_k?

### Q17 · MC
What does W_O do in multi-head attention?

- A) Masks the future
- B) Mixes the concatenated head outputs back into d_model
- C) Converts logits to probabilities
- D) Adds positional information

### Q18 · MC
In a causal mask, why are future positions set to −∞ rather than 0 before softmax?

- A) 0 would still receive weight because e⁰ = 1
- B) −∞ makes training faster
- C) 0 would make the row sum to 0
- D) There is no difference

### Q19 · MC
Temperature T → 0 is equivalent to…

- A) Uniform random sampling
- B) Top-p with p = 1
- C) Greedy (argmax) decoding
- D) Turning off the model

### Q20 · MC
Logits `blue 3.9, clear 1.8, dark 1.1, green 0.6, red 0.2` give P(blue) ≈ 0.80. With **top-p = 0.9**, how many tokens are kept?

- A) 1
- B) 2
- C) 3
- D) 5

### Q21 · compute
LayerNorm (γ = 1, β = 0) on `[20, 40, 40, 100]`. Give the mean, the standard deviation, and the normalised last entry.

### Q22 · MC
In the feed-forward network of the base Transformer, the hidden width is…

- A) 64
- B) 512
- C) 2048
- D) 37,000

### Q23 · MC
Why does the encoder use **unmasked** self-attention?

- A) It is cheaper
- B) It reads a given source and generates nothing, so there is no future to hide
- C) Masks only work with cross-attention
- D) It has no positional encoding

### Q24 · MC
In cross-attention, the queries come from ___ and the keys/values from ___.

- A) the encoder; the decoder
- B) the decoder; the encoder
- C) the decoder; the decoder
- D) the vocabulary; the encoder

### Q25 · compute
Base model, 7 source tokens, 8 decoder positions, 8 heads. What is the shape of the cross-attention score tensor?

### Q26 · MC
Which property of sinusoidal positional encodings is **true**?

- A) They must be learned during training
- B) They stop at a maximum position
- C) Nearby positions get similar vectors
- D) All dimensions oscillate at the same frequency

### Q27 · compute
Label smoothing, paper variant, ε = 0.1, K = 5 tokens. What target probability goes to the correct token, and to each of the others?

### Q28 · MC
Which component holds the largest share of the base Transformer's parameters?

- A) LayerNorm
- B) Attention projections
- C) Feed-forward networks
- D) Positional encodings

### Q29 · MC
GPT-style chat models are…

- A) Encoder-only
- B) Decoder-only
- C) Encoder–decoder
- D) Recurrent

### Q30 · MC
During training with teacher forcing, the decoder's input is…

- A) Its own previous predictions
- B) The true target sequence shifted right behind `<BOS>`
- C) The source sentence
- D) Random tokens

---

## Answer key

**Q1 — C.** Word-level: one token per word ("The teddy bears were reading" = 5, vs 6 subword, 28 characters). *(I-6)*

**Q2 — B.** Subwords sit between words and characters, and can always fall back to smaller pieces. The cuts are statistical, not linguistic (`ted|dy`). *(I-6)*

**Q3 — `e + a`, 13 times.** read(4) + reading(3) + bear(4) + bears(2) = 13. *(I-7)*

**Q4 — C.** Replaying the merges gives `r | ing | s`; no `<UNK>` needed. *(I-7)*

**Q5 — D.** `<EOS>` — generation stops when the model picks it. *(I-13, I-50)*

**Q6 — B.** No two one-hot rows share a 1, so every pair is equally different. *(I-17)*

**Q7 — C.** The predictions are thrown away; the hidden layer is kept. *(I-19)*

**Q8 — B.** One row per token, looked up identically; context must be added by later layers. *(I-23)*

**Q9 — C.** RNNs handle variable lengths naturally; their problems are fading memory, sequential computation and vanishing gradients. *(I-27, II-6)*

**Q10 — about 0.001 (0.5¹⁰ ≈ 0.00098).** A thousandth of the original signal. *(II-6)*

**Q11 — B.** The decoder could look back at every encoder state instead of one summary vector. *(II-8)*

**Q12 — 4 / √2 ≈ 2.83.** (3)(1) + (−1)(−1) = 4. *(I-38–39)*

**Q13 — B.** Large scores push softmax towards one-hot; scaling keeps it soft. *(I-39)*

**Q14 — C.** Every token's query against every token's key. *(I-38)*

**Q15 — C.** The output is a weighted average of value vectors: `[0.90, 1.10]` ≈ `v_glass = [1, 1]`. *(I-42)*

**Q16 — d_k = 64, √d_k = 8.** 512 / 8 = 64. *(II-18)*

**Q17 — B.** Concat(head₁…head_h) · W_O returns to n × d_model. *(II-19)*

**Q18 — A.** e⁰ = 1, so a zero score still takes a share; e^−∞ = 0 removes it and the row still sums to 1. *(I-68)*

**Q19 — C.** The distribution collapses onto the highest logit. *(I-56)*

**Q20 — B.** Cumulative: blue 0.80, + clear 0.10 = 0.90 ≥ 0.9 → 2 tokens. *(I-59)*

**Q21 — mean 50, std 30, last entry 1.67.** (100 − 50) / 30 = 1.67; full vector `[−1.00, −0.33, −0.33, 1.67]`. *(I-67)*

**Q22 — C.** d_ff = 2048 = 4 × 512. *(II-24)*

**Q23 — B.** Masking exists to stop next-token cheating; the encoder is reading, not predicting. *(II-23)*

**Q24 — B.** Decoder asks, encoder answers. *(II-30)*

**Q25 — 8 × 8 × 7** (heads × decoder positions × source tokens). *(II-37)*

**Q26 — C.** At d = 512, distance 1 → similarity 0.97, distance 20 → 0.62. They are fixed (not learned), defined for every position, and each pair has its own frequency. *(II-12–14)*

**Q27 — 0.9 to the correct token, 0.025 to each of the other four.** (PyTorch's variant spreads ε over all K: 0.92 / 0.02.) *(II-43)*

**Q28 — C.** FFN ≈ 40% (25.2M of 63.1M); embeddings and attention ≈ 30% each. *(II-47)*

**Q29 — B.** Decoder-only: prompt and answer are one stream. *(II-49)*

**Q30 — B.** The true target, shifted right, with the causal mask keeping it honest. *(II-29)*
