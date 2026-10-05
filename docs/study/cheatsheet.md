# Transformers — cheat sheet

One page covering both decks. **I-n** = Part I (`transformers.md`) slide *n*; **II-n** = Part II
(`transformers-2.md`) slide *n*; **▶ mm:ss** = Stanford CME 295 lecture 1
([YouTube](https://www.youtube.com/watch?v=114i2Kz-LZA)), approximate times from
[the organized notes](../Stanford_CME295_Transformers_LLMs_Organized_Notes.md).
Every number below comes from `scripts/verify-attention.py`.

---

## The pipeline

```
text → tokens → embeddings + position → [ attention → feed-forward ] × N → logits → softmax → next token
                                          (each wrapped in residual + LayerNorm)        └── loop until <EOS>
```

Encoder–decoder (2017 original, II-2): the **encoder** reads the source with unmasked self-attention;
the **decoder** writes with masked self-attention, then **cross-attention** to the encoder output, then FFN.
GPT-style models are the decoder alone (I-81).

## Formulas

| What | Formula | Where |
|---|---|---|
| Model input | `X = TokenEmbedding + PositionEncoding` | I-22, II-15 · ▶ 1:13 |
| Projections | `Q = X·W_Q   K = X·W_K   V = X·W_V` | I-37 · ▶ 1:00 |
| Scaled dot-product attention | `Attention(Q,K,V) = softmax(Q·Kᵀ / √d_k) · V` | I-44 · ▶ 1:03 |
| Multi-head | `MultiHead = Concat(head_1 … head_h) · W_O`, `head_i = Attention(Q_i, K_i, V_i)`, `d_k = d_model / h` | I-45, II-18–19 |
| Causal mask | future scores → `−∞` before softmax, so `e^−∞ = 0` and rows still sum to 1 | I-68–69, II-29 |
| Sinusoidal position | `PE(pos,2i) = sin(pos / 10000^(2i/d))`, `PE(pos,2i+1) = cos(…)` | II-12 · ▶ 1:15 |
| Residual | `out = x + Sublayer(x)` | I-66, II-41 · ▶ 1:23 |
| LayerNorm | `(x − mean) / std`, then learned scale γ and shift β | I-67, II-41 |
| Add & Norm (2017, post-norm) | `LayerNorm(x + Sublayer(x))` | II-22 |
| Feed-forward | `FFN(x) = max(0, x·W₁ + b₁)·W₂ + b₂`, width `d_model → 4·d_model → d_model` | I-65, II-24 |
| Output | `P(token | context) = softmax(h · W_vocab)` | I-48–49, II-32 |
| Temperature | `softmax(z / T)`; `T → 0` is greedy (argmax) | I-56–57 |
| Loss | `L = −log P(correct token)` | I-72 |
| Label smoothing (ε = 0.1, paper) | target: correct `1 − ε = 0.9`, each other `ε/(K−1)` | II-43 · ▶ 1:26 |

## The worked examples (memorise one)

- **Attention (I-36–42):** tokens *glass, dropped, it*; `d_model = 4`, `d_k = 2`.
  `q_it · k_glass = (3)(1) + (−1)(−1) = 4` → `÷ √2 = 2.83` → softmax → **0.85**. Output for *it* ≈ `[0.90, 1.10]` ≈ `v_glass = [1, 1]`.
- **Second head (II-17):** different W's send every token to *dropped* (0.80 / 0.62 / 0.80).
- **Cross-attention (II-31):** decoder *“&lt;BOS&gt; le”* over encoder *“the cat sleeps”*: *le* puts **0.77** on *cat*. Score grid is 2 × 3 — not square.
- **BPE (I-7):** corpus `read×4 reading×3 bear×4 bears×2 ring×2 sing×3`; merges `ea, in, ing, ead, read, bea, bear`. Unseen *bearing* → `bear|ing`.
- **LayerNorm (I-67):** `[20, 40, 40, 100]` → mean 50, std 30 → `[−1.00, −0.33, −0.33, 1.67]`.
- **Decoding (I-49–60):** logits `blue 3.9, clear 1.8, dark 1.1, green 0.6, red 0.2` → P(blue) = 0.80. Top-k = 3 keeps 3; top-p = 0.9 keeps 2.

## Base Transformer (2017) — shapes measured by a forward pass (II-35–38)

`d_model 512 · h 8 · d_k 64 · d_ff 2048 · N 6 · vocab 37,000` · source 7 tokens, target 7 + `<BOS>` = 8 positions.

| Tensor | Shape |
|---|---|
| encoder input / every encoder layer output | 7 × 512 |
| Q or K of one head (encoder) | 7 × 64 |
| encoder self-attention scores | 8 heads × 7 × 7 |
| FFN hidden | 7 × 2048 |
| decoder input / every decoder layer output | 8 × 512 |
| masked self-attention scores | 8 × 8 × 8 |
| **cross-attention scores** (Q from decoder, K from encoder) | **8 × 8 × 7** |
| logits / probabilities | 8 × 37,000 (inference uses the last row) |

**Parameters** (II-47): 63.1M by our count (paper: 65M) — FFN 40%, shared embeddings 30%, attention 30%, LayerNorm ≈ 0.

## Tokenization facts (I-5–13 · ▶ 16:59–37:26)

| Tokenizer | Vocabulary | “The teddy bears were reading” | Problem |
|---|---|---|---|
| word | 100,000s+ | 5 tokens | OOV → `<UNK>`, *bear* ≠ *bears* |
| character | a few hundred | 28 tokens | long sequences, attention cost ∝ n² |
| subword (BPE) | 50,257 (GPT-2) / 100,277 (GPT-4) | 6 tokens (`ted|dy`) | learned from data; language bias |

Special tokens (I-13): `<BOS>` start · `<EOS>` stop · `<PAD>` filler (masked) · `<UNK>` unknown. GPT-2's `<|endoftext|>` = id 50256. Conventions differ per model.

## Problem → fix ladder (II-50)

| Problem | Fix |
|---|---|
| text isn't numbers | tokenization |
| huge vocab / unknown words | subwords (BPE) |
| one-hot says nothing about similarity (I-17) | learned embeddings (Word2Vec proxy task, I-19 · ▶ 39:35) |
| one vector per word ignores context (I-23) | contextual models |
| RNN: fades over distance, queues, one-vector bottleneck (I-27, II-5–7 · ▶ 48:21) | LSTM, then attention (2014, II-8) |
| sequential = slow | self-attention only (2017) |
| attention ignores order | positional encoding |
| one relation per head | multi-head + W_O |
| deep stacks won't train | residual + LayerNorm |
| decoder could see the answer | causal mask |
| decoder must read the source | cross-attention |
| over-confident on one phrasing | label smoothing |

## Glossary

- **Token** — a chunk of text with an integer id. **Vocabulary** — the set of all tokens.
- **Embedding** — the learned vector for a token. **One-hot** — all zeros except one 1; orthogonal, so no similarity.
- **Proxy task** — a made-up training task whose by-product (e.g. Word2Vec's middle layer) is the real goal. **CBOW**: context → word. **Skip-gram**: word → context.
- **Hidden state / cell state** — an RNN's running memory / an LSTM's protected memory lane.
- **Vanishing gradient** — training signal shrinking as it passes back through many steps (0.5¹⁰ ≈ 0.001, II-6).
- **Self-attention** — Q, K, V from the same sequence. **Cross-attention** — Q from one sequence, K and V from another.
- **Head** — one attention computation with its own W_Q, W_K, W_V. **W_O** — mixes concatenated heads back to d_model.
- **Causal / masked attention** — no looking at later positions. **Teacher forcing** — training the decoder on the true target, shifted right behind `<BOS>`.
- **Logits** — raw scores, one per vocabulary entry. **Softmax** — `eˣ / Σeˣ`; used for attention weights *and* the output distribution (II-48).
- **Greedy / argmax** — always take the top token. **Sampling** — draw from the distribution (temperature, top-k, top-p).
- **Residual** — add the input back. **LayerNorm** — re-centre and re-scale each vector. **Dropout** — zero 10% of units at random during training.
- **Label smoothing** — train towards 0.9 / spread rather than 1 / 0. Lower confidence, better BLEU.
- **Encoder-only** (BERT) · **decoder-only** (GPT) · **encoder–decoder** (2017, T5) (II-49).
