# Transformers — flashcards

Click a question to reveal the answer. **Core** cards cover Part I (no prior knowledge); **Deeper**
cards cover Part II and the Stanford CME 295 material. **I-n** / **II-n** point to the slide.

This file is also the source for the Flashcards tab in
[`transformers-study.html`](transformers-study.html) — run `npm run study` after editing it.
Keep the format: one `## ` heading per group, one `<details>` block per card, the level in `<b>`.

## History and motivation

<details><summary><b>Core</b> · Before 2017, how were different language tasks usually handled?</summary>

One model per task — a separate translator, sentiment classifier, name-finder — typically recurrent networks (RNNs). *(I-3)*

</details>

<details><summary><b>Core</b> · What was the key property that made the 2017 Transformer take over?</summary>

It scaled: more data, more compute and more parameters kept making it better, and it trains in parallel instead of one word at a time. *(I-3, I-75)*

</details>

<details><summary><b>Deeper</b> · What is the difference between "a Transformer" and "an LLM"?</summary>

The Transformer is the architecture. An LLM is that architecture built at very large size and trained on a very large amount of text. *(I-79)*

</details>

## Tokenization

<details><summary><b>Core</b> · Why does a model need tokenization at all?</summary>

Neural networks operate on numbers. Tokenization cuts text into pieces (tokens), each with an integer id, which then become vectors. *(I-5)*

</details>

<details><summary><b>Core</b> · What trade-off does every tokenizer make?</summary>

Vocabulary size against sequence length: more distinct pieces means fewer tokens per sentence, and vice versa. *(I-6)*

</details>

<details><summary><b>Core</b> · Two problems with word-level tokenization?</summary>

A huge vocabulary in which related forms (bear / bears) are unrelated entries, and out-of-vocabulary words that become `<UNK>`. *(I-6)*

</details>

<details><summary><b>Core</b> · Main cost of character-level tokenization?</summary>

Very long sequences ("The teddy bears were reading" = 28 tokens vs 5 words), and attention's work grows with the square of the length. *(I-6)*

</details>

<details><summary><b>Core</b> · Describe byte-pair encoding in one sentence.</summary>

Start from single characters (or bytes), repeatedly merge the most frequent adjacent pair into a new token, until the vocabulary is the desired size. *(I-7)*

</details>

<details><summary><b>Core</b> · In the toy corpus, what are the first three BPE merges?</summary>

`e+a → ea` (13 times), `i+n → in` (8), `in+g → ing` (8). *(I-7)*

</details>

<details><summary><b>Core</b> · How does BPE handle a word it never saw, like "bearing"?</summary>

Replay the learned merges in order: `bear|ing`. In the worst case it falls back to single characters, so `<UNK>` is almost never needed. *(I-7)*

</details>

<details><summary><b>Core</b> · Why does the same greeting cost 4 tokens in English and 14 in Korean (GPT-2)?</summary>

The tokenizer's merges reflect its training data, which was mostly English; under-represented languages are left in small, byte-level pieces. *(I-10)*

</details>

<details><summary><b>Core</b> · What are `<BOS>`, `<EOS>`, `<PAD>` and `<UNK>` for?</summary>

Begin a sequence; end it (generation stops when the model picks it); pad a batch to equal length (masked out); stand for something unknown. Names vary by model. *(I-13)*

</details>

<details><summary><b>Deeper</b> · How big is GPT-2's vocabulary and where does the number come from?</summary>

50,257 = 256 bytes + 50,000 merges + 1 special token (`<|endoftext|>`, id 50256). *(I-13)*

</details>

## Embeddings

<details><summary><b>Core</b> · Why are raw token ids a bad representation?</summary>

They impose an arbitrary order: id distance says nothing about meaning. *(I-16)*

</details>

<details><summary><b>Core</b> · What is wrong with one-hot vectors?</summary>

Every pair is orthogonal — equally different — so they can never express similarity, and each one is as long as the vocabulary. *(I-17)*

</details>

<details><summary><b>Core</b> · What is an embedding?</summary>

A short, dense, learned vector per token, arranged so that tokens used in similar ways end up close together. *(I-16, I-18)*

</details>

<details><summary><b>Core</b> · What is a proxy task? Give the Word2Vec example.</summary>

A made-up training task whose by-product is what you actually want. Word2Vec predicts words from neighbours; the hidden layer it learns is the embedding. *(I-19)*

</details>

<details><summary><b>Deeper</b> · CBOW vs skip-gram?</summary>

CBOW predicts the middle word from its context; skip-gram predicts the context words from the middle word. *(I-19)*

</details>

<details><summary><b>Core</b> · Three limits of static (Word2Vec-style) embeddings?</summary>

One vector per word regardless of context (river bank vs money bank), no notion of word order, and no vector for unseen words. *(I-21, I-23)*

</details>

<details><summary><b>Core</b> · How does the model know word order?</summary>

A position vector is added to each token embedding before the first layer. *(I-22)*

</details>

## Before attention: RNNs and LSTMs

<details><summary><b>Core</b> · How does an RNN process a sentence?</summary>

One word at a time, updating a single hidden state that carries everything seen so far. *(I-27)*

</details>

<details><summary><b>Core</b> · Two main weaknesses of RNNs?</summary>

Information from far back fades (long-range dependency / vanishing gradients), and processing is sequential, so it cannot be parallelised. *(I-27)*

</details>

<details><summary><b>Deeper</b> · What is the vanishing-gradient problem?</summary>

The training signal is multiplied by roughly the same factor at each step back; below 1 it shrinks geometrically (0.5¹⁰ ≈ 0.001), so distant words stop teaching anything. *(II-6)*

</details>

<details><summary><b>Deeper</b> · What does an LSTM add to an RNN?</summary>

A cell state — a memory lane updated by addition — controlled by forget, input and output gates. It eases vanishing gradients but stays sequential. *(II-7)*

</details>

<details><summary><b>Deeper</b> · What was the seq2seq bottleneck?</summary>

The whole source sentence had to be squeezed into one fixed-size vector before the decoder began; long sentences lost detail. *(II-5)*

</details>

<details><summary><b>Deeper</b> · What did attention (2014) change in RNN translators?</summary>

The decoder kept every encoder state and, for each output word, took a learned weighted blend of them — no single-vector bottleneck. *(II-8)*

</details>

## Attention

<details><summary><b>Core</b> · What do query, key and value represent?</summary>

Query: what this word is looking for. Key: what a word advertises so others can find it. Value: what a word passes on if attended to. *(I-33)*

</details>

<details><summary><b>Core</b> · Write the scaled dot-product attention formula.</summary>

`Attention(Q,K,V) = softmax(Q·Kᵀ / √d_k) · V` *(I-44)*

</details>

<details><summary><b>Core</b> · In the worked example, what is q_it · k_glass, and what weight does it become?</summary>

(3)(1) + (−1)(−1) = 4; ÷ √2 = 2.83; after softmax over the row, **0.85**. *(I-38–41)*

</details>

<details><summary><b>Core</b> · Why divide by √d_k?</summary>

Dot products grow with dimension; large scores saturate softmax into a near one-hot. Scaling keeps it soft. *(I-39)*

</details>

<details><summary><b>Core</b> · What shape is Q·Kᵀ for n tokens, and how do you read it?</summary>

n × n. Row = the word asking, column = the word being asked; each row becomes a distribution after softmax. *(I-38)*

</details>

<details><summary><b>Core</b> · What is the output of attention, in words?</summary>

For each word, a weighted average of all value vectors, with weights the model computed itself. *(I-42–43)*

</details>

<details><summary><b>Core</b> · Why is it called *self*-attention?</summary>

Queries, keys and values all come from the same sequence. *(I-44)*

</details>

<details><summary><b>Core</b> · Why use multiple heads?</summary>

Each head has its own W_Q, W_K, W_V and can learn a different relationship (pronoun → noun, subject → verb …). *(I-45, II-17)*

</details>

<details><summary><b>Deeper</b> · How is d_k chosen in multi-head attention, and what does that do to cost?</summary>

d_k = d_model / h (512/8 = 64 in the base model), so all heads together cost about the same as one full-width head. *(II-18)*

</details>

<details><summary><b>Deeper</b> · What is W_O?</summary>

The learned output projection: concatenated head outputs (n × h·d_k) × W_O → back to n × d_model. *(II-19)*

</details>

<details><summary><b>Deeper</b> · What analogy does CME 295 use for multi-head attention?</summary>

Multiple filters in a convolutional network — each detects a different pattern. *(II-19)*

</details>

## Generation and decoding

<details><summary><b>Core</b> · What does the model output at each step?</summary>

A score (logit) for every vocabulary token, turned into probabilities by softmax. *(I-48–49)*

</details>

<details><summary><b>Core</b> · How does generation proceed, and when does it stop?</summary>

Autoregressively: pick a token, append it, run again — until the picked token is `<EOS>` or a length limit is hit. *(I-50)*

</details>

<details><summary><b>Core</b> · What is greedy decoding?</summary>

Always take the argmax (highest-probability token). Predictable but flat and repetitive. *(I-55)*

</details>

<details><summary><b>Core</b> · What does temperature do?</summary>

Divides logits by T before softmax: T < 1 sharpens, T > 1 flattens, T → 0 becomes greedy. It does not change the model. *(I-56–57)*

</details>

<details><summary><b>Core</b> · Top-k vs top-p?</summary>

Top-k keeps a fixed number of tokens; top-p keeps the smallest set covering probability p, so it adapts to the distribution's shape. *(I-58–60)*

</details>

<details><summary><b>Core</b> · Name the two different jobs softmax does in a Transformer.</summary>

Inside attention: weights over keys. At the output: a distribution over the vocabulary. *(I-48, II-48)*

</details>

## The block and training

<details><summary><b>Core</b> · What are the two main sub-layers of a block?</summary>

Attention (tokens communicate) and the feed-forward network (each token computed on separately). *(I-65)*

</details>

<details><summary><b>Core</b> · What does the feed-forward network do to the vector's width?</summary>

Widens it about 4× (512 → 2048), applies ReLU, and projects back. *(I-65, II-24)*

</details>

<details><summary><b>Core</b> · What is a residual connection and why does it help?</summary>

output = x + Sublayer(x). Each layer learns a change, and gradients flow straight back through the addition, so deep stacks train. *(I-66)*

</details>

<details><summary><b>Core</b> · What does LayerNorm do to [20, 40, 40, 100]?</summary>

Mean 50, std 30 → [−1.00, −0.33, −0.33, 1.67], then a learned scale and shift. *(I-67)*

</details>

<details><summary><b>Core</b> · How does a causal mask work, and why −∞ rather than 0?</summary>

Future scores are set to −∞ before softmax so they become exactly 0; setting them to 0 would still give them weight because e⁰ = 1. *(I-68–69)*

</details>

<details><summary><b>Core</b> · What loss trains a language model?</summary>

Cross-entropy: −log P(correct next token), averaged over positions. *(I-72)*

</details>

<details><summary><b>Deeper</b> · Post-norm vs pre-norm?</summary>

2017: LayerNorm(x + Sublayer(x)). Modern: x + Sublayer(LayerNorm(x)), which is more stable for very deep models. *(II-41)*

</details>

<details><summary><b>Deeper</b> · What is dropout, and what rate did the base model use?</summary>

Randomly zeroing units during training (not at inference) to prevent over-reliance on any unit; p = 0.1. *(II-42)*

</details>

<details><summary><b>Deeper</b> · What is label smoothing (ε = 0.1)?</summary>

Train towards a softened target — 0.9 on the correct token, 0.1 shared among the rest — instead of 1 / 0. *(II-43)*

</details>

<details><summary><b>Deeper</b> · Why does label smoothing help translation?</summary>

Many outputs are valid; demanding 100% on one makes the model over-confident. It worsened perplexity but improved BLEU in the 2017 paper. *(II-44)*

</details>

## Positions, properly

<details><summary><b>Deeper</b> · Learned vs sinusoidal positional encodings?</summary>

Learned: a trained vector per position, flexible but no row past the maximum length. Sinusoidal: fixed sin/cos formula, nothing learned, defined for any position. *(II-11–12)*

</details>

<details><summary><b>Deeper</b> · Explain the clock analogy for sinusoidal encodings.</summary>

Each sin/cos pair is a clock hand turning at a different speed; fast hands distinguish neighbours, slow hands distinguish distant positions; together they identify the position uniquely. *(II-12–13)*

</details>

<details><summary><b>Deeper</b> · What useful property do sinusoidal encodings have?</summary>

Nearby positions have similar vectors (d=512: distance 1 → 0.97, distance 20 → 0.62), and a shift by k is the same rotation for every position. *(II-14)*

</details>

## Encoder, decoder, cross-attention

<details><summary><b>Deeper</b> · What does the encoder produce?</summary>

One context-aware d_model vector per source token, after N = 6 blocks of unmasked self-attention + FFN with Add & Norm. *(II-22–25)*

</details>

<details><summary><b>Deeper</b> · Why does the encoder not use a mask?</summary>

It is not generating — the whole source is given — so every word may attend to words before and after it. *(II-23)*

</details>

<details><summary><b>Deeper</b> · List the three sub-layers of a decoder block in order.</summary>

Masked self-attention → cross-attention → feed-forward, each with Add & Norm. *(II-33)*

</details>

<details><summary><b>Deeper</b> · In cross-attention, where do Q, K and V come from?</summary>

Q from the decoder; K and V from the encoder output. *(II-30)*

</details>

<details><summary><b>Deeper</b> · Shape of the cross-attention score matrix for 8 decoder positions and 7 source tokens?</summary>

8 × 7 per head (8 × 8 × 7 for 8 heads) — rectangular, not square. *(II-37)*

</details>

<details><summary><b>Deeper</b> · What is teacher forcing?</summary>

During training the decoder receives the true target shifted right behind `<BOS>`, and predicts every next token in parallel under the causal mask. *(II-29, II-38)*

</details>

<details><summary><b>Deeper</b> · Base model hyper-parameters?</summary>

d_model 512, h 8, d_k 64, d_ff 2048, N 6, vocab 37,000 — about 63–65M parameters. *(II-35, II-47)*

</details>

<details><summary><b>Deeper</b> · Encoder-only, decoder-only, encoder–decoder: one example each?</summary>

BERT; GPT (and most chat models); the 2017 translator / T5. *(II-49)*

</details>
