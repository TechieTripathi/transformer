# Stanford CME 295 — Transformers and LLMs
## Organized Lecture Notes: From Tokenization to the Transformer

> **Source:** User-provided transcript of the Stanford CME 295 lecture.  
> **Organization:** The original captions have been cleaned and reorganized into a consistent conceptual flow. Filler, repeated classroom confirmations, and most conversational interruptions have been removed, while the lecturer's examples and terminology are retained.
>
> **Core story of the lecture:**  
> **Text → Tokens → Token Representations → Context → Attention → Self-Attention → Transformer → Autoregressive Generation**

---

# 1. From Task-Specific Models to Modern LLMs
**Approx. 12:58–16:51**

## 1.1 The 2010s: One Model per Use Case

Around the 2010s, NLP systems were generally organized around individual tasks.

Typical examples:

- **Sentiment analysis:** determine whether a review is positive, negative, or neutral.
- **Machine translation:** use a dedicated model to translate text.
- **Named-entity recognition:** identify names, locations, organizations, etc.

Recurrent Neural Networks (RNNs) were among the dominant model families during this period.

The important characteristic was:

> **Different use cases generally required different models.**

---

## 1.2 2017: The Transformer

A major turning point came in **2017** with the paper:

> **“Attention Is All You Need”**

The paper introduced the **Transformer** architecture.

The important idea was scalability. Increasing:

- training data,
- computation,
- and model parameters

could produce much larger performance gains than earlier approaches.

The Transformer became a scalable architecture that could subsequently be expanded in:

- model size,
- number of training tokens,
- and computational resources.

---

## 1.3 From Transformers to LLMs

Scaling Transformer-based architectures led to modern **Large Language Models (LLMs)** capable of:

- generating text,
- generating code,
- and performing increasingly general language tasks.

The lecture highlights **ChatGPT's release in 2022** as another major turning point, particularly from a product and user-interaction perspective.

The interaction paradigm shifted toward people directly interacting with general-purpose conversational models.

---

## 1.4 From Conversational Assistants to Agents

The lecture then connects the historical progression to the present:

**Task-specific models → Transformers → LLMs → conversational assistants → agentic systems**

The later part of the course will examine how LLMs can move beyond conversation toward **agentic behavior**.

---

# 2. Tokenization
**Approx. 16:59–37:26**

Tokenization is the first foundational concept.

## 2.1 Why Do We Need Tokenization?

Models operate on **numbers**, not raw text.

Therefore, we need a way to convert text into numerical representations.

The first step is to divide text into units that can be represented mathematically.

This process is called **tokenization**.

Example:

> “A cute Teddy bear is reading.”

One possible tokenization could be:

- `A`
- `cute`
- `Teddy bear`
- `is`
- `reading`

Each unit is a **token**.

Eventually, each token will be represented using a vector of numbers.

---

## 2.2 Vocabulary and Sequence Length

A tokenizer needs a **vocabulary**: the set of tokens it is allowed to use.

Two important quantities are therefore:

### Vocabulary size

The number of possible tokens.

### Sequence length

The number of tokens produced for a particular input.

The choice of tokenizer creates a trade-off between vocabulary size and sequence length.

---

# 3. Three Ways to Tokenize Text

## 3.1 Word-Level Tokenization

The simplest approach is to use spaces as delimiters.

Example:

> “A cute Teddy bear is reading.”

becomes approximately:

`A | cute | Teddy | bear | is | reading`

### Advantages

- Simple.
- Easy to interpret.
- A token corresponds naturally to a word.

### Problems

#### 1. Large vocabulary

Words can have many variations:

- singular/plural,
- masculine/feminine forms,
- different morphological forms,
- etc.

This can make the vocabulary very large.

#### 2. Similar words are treated separately

For example:

- `bear`
- `bears`

represent closely related concepts, but they are separate tokens.

Nothing automatically guarantees that their learned representations will be close.

#### 3. Out-of-vocabulary (OOV)

A word may occur during inference that never appeared during tokenizer/model training.

Then the system may not have a learned representation for that word.

---

## 3.2 Character-Level Tokenization

Instead of words, represent text using individual characters.

Example:

`bear`

becomes approximately:

`b | e | a | r`

### Advantages

- Small vocabulary.
- Less risk of out-of-vocabulary words.
- More robust to spelling variations and misspellings.

### Problems

The sequence becomes much longer.

Since model computation depends strongly on sequence length, longer sequences can make processing much slower.

Character-level representations are also less directly interpretable than word-level representations.

---

## 3.3 Subword Tokenization

Subword tokenization attempts to find a middle ground.

Instead of:

- one token = entire word, or
- one token = one character,

we learn useful pieces of words.

Example:

`reading`

could be represented approximately as:

`read | ing`

This gives several advantages:

- related words can share subword pieces;
- vocabulary does not need to contain every complete word;
- sequence length is generally much shorter than character-level tokenization.

The trade-off is that the tokenizer itself needs to be learned from data.

The resulting vocabulary depends on the corpus used to train the tokenizer.

---

# 4. Byte Pair Encoding (BPE)

BPE is presented as a very common type of **subword tokenizer**.

BPE stands for:

> **Byte Pair Encoding**

## 4.1 Basic Idea

Start with an initial vocabulary, such as characters.

Then:

1. Find frequently occurring pairs.
2. Merge those pairs into a new token.
3. Add the merged token to the vocabulary.
4. Repeat until the desired vocabulary size is reached.

For example, if a pair of symbols frequently occurs together, the tokenizer can create a token representing that pair.

Repeated merging produces useful subword units.

---

## 4.2 Why BPE Helps

Because frequent combinations become tokens:

- common patterns require fewer tokens;
- sequence lengths can become shorter;
- computation becomes more efficient.

The tokenizer therefore depends strongly on the data used to train it.

### Multilingual implication

If the tokenizer needs to support multiple languages, its training corpus should represent those languages.

Otherwise, some languages may be represented inefficiently and produce longer token sequences.

---

# 5. Special Tokens

Tokenizers can also contain tokens whose purpose is not ordinary text.

## 5.1 Unknown Token

The **unknown token** represents text that is not represented in the vocabulary.

Often written conceptually as:

`<UNK>`

---

## 5.2 Beginning of Sequence (BOS)

A **beginning-of-sequence** token indicates that generation is starting.

Conceptually:

`<BOS>`

---

## 5.3 End of Sequence (EOS)

An **end-of-sequence** token tells the model that generation is finished.

Conceptually:

`<EOS>`

---

## 5.4 Padding Token

A padding token can make sequences the same length.

This can be useful because hardware and tensor operations work efficiently with consistent dimensions.

The lecture emphasizes that these conventions are **not universal**. Different models can use different special-token conventions.

---

# 6. From Tokens to Token Representations
**Approx. 37:26 onward**

Once text has been converted into tokens, we need to represent those tokens numerically.

## 6.1 One-Hot Encoding

A simple approach is **one-hot encoding**.

If the vocabulary has size `V`, each token can be represented by a vector of length `V`.

For example:

`soft → [1, 0, 0, ...]`

The problem is that one-hot vectors do not express semantic relationships.

Different tokens are orthogonal to one another.

Therefore, one-hot encoding tells us:

> “These are different.”

but not:

> “These two tokens are semantically related.”

---

# 7. Word2Vec: Learning Meaningful Representations
**Approx. 39:35–48:21**

An earlier approach for learning useful token representations is **Word2Vec**.

The main goal is to learn representations in which similar words have similar vectors.

For example, we would like related concepts to have related representations.

---

## 7.1 Proxy Tasks

Word2Vec learns representations through a **proxy task**.

A proxy task is not necessarily the final task we care about.

Instead, we train the model on a simpler task whose solution helps us learn useful representations.

Two variants are highlighted:

### CBOW — Continuous Bag of Words

Predict a word from its surrounding context.

### Skip-gram

Predict surrounding words from a given word.

---

## 7.2 Simplified Neural-Network View

Suppose:

> “A cute Teddy bear is reading.”

We want to predict `cute` from `A`.

The input token can initially be represented as a one-hot vector.

The neural network maps it into a smaller hidden representation.

Conceptually:

**One-hot input → hidden representation → vocabulary probabilities**

The predicted probabilities are compared against the actual target word using a loss such as cross-entropy.

Training updates the network parameters.

This process is repeated across the corpus.

---

## 7.3 Why the Hidden Representation Becomes Useful

After training, the intermediate representation can contain meaningful semantic structure.

Similar words can have similar representations.

The lecture gives examples of relationships such as:

> Paris : France :: Berlin : Germany

The important idea is:

> The model can learn useful relationships between words from contextual prediction.

---

# 8. Limitations of Word2Vec

Word2Vec-style representations have important limitations.

## 8.1 One Word → One Representation

A word receives the same representation regardless of its context.

Example:

> river bank

versus

> going to the bank

The word `bank` has different meanings, but a static word embedding gives it the same representation.

---

## 8.2 Word Order Is Not Properly Represented

Consider:

> “The child is hugging the Teddy bear.”

versus:

> “The Teddy bear is hugging the child.”

The same words occur, but the meaning is different.

A static embedding approach does not inherently encode this sequence-level word order.

---

## 8.3 Out-of-Vocabulary Problems

If the model encounters something that was not present during training, it cannot simply rely on a learned representation for it.

These limitations motivate models that incorporate **sequence context**.

---

# 9. RNNs and LSTMs
**Approx. 48:21–55:17**

RNNs address the word-order problem by maintaining a **hidden state**.

## 9.1 Basic RNN Idea

Instead of processing every token independently, the model maintains a representation of what it has seen so far.

For:

> “A cute Teddy bear is reading.”

the model processes tokens sequentially.

At each step it uses:

- the current token,
- the previous hidden state.

The hidden state attempts to encode the meaning of the sequence seen so far.

Therefore:

> **Current representation = current token + information carried from previous tokens**

---

## 9.2 What RNNs Improve

Because the hidden state evolves through the sequence, RNNs can account for:

- token order,
- previous context,
- sequential dependencies.

This made them useful for:

- classification,
- sequence labeling,
- generation,
- translation,
- sentiment analysis,
- and other sequence tasks.

---

# 10. The Long-Range Dependency Problem

The main limitation is that the model tries to compress everything seen so far into a single evolving hidden state.

If relevant information occurred far earlier in the sequence, it can become difficult to recover.

Example:

> “My Teddy bear is so cute. It is 3 feet tall.”

The word `it` needs to refer back to information from earlier in the sequence.

As the sequence becomes longer, maintaining the relevant information becomes difficult.

This is the **long-range dependency** problem.

The lecture connects this to the **vanishing-gradient problem**, which makes learning long-range dependencies difficult during backpropagation.

---

# 11. LSTM

One variation of RNNs is:

> **Long Short-Term Memory (LSTM)**

LSTMs maintain:

- a hidden state,
- and a **cell state**.

The cell state is intended to carry information for longer periods.

This helps address some long-range dependency problems, but it does not completely eliminate the limitations of recurrent architectures.

---

# 12. Another RNN Limitation: Sequential Computation

RNNs must process tokens sequentially.

To predict the next token, the model needs the hidden state produced by processing the previous tokens.

Therefore:

> Token 1 → Token 2 → Token 3 → Token 4 → ...

This makes training and computation difficult to parallelize and can be slow.

This motivates another idea:

> **Attention**

---

# 13. Attention
**Approx. 55:17–57:21**

The key idea of attention is:

> Instead of relying only on a single hidden state to remember the past, allow the model to directly connect to relevant previous tokens.

For example, in translation, when predicting a target word, it can be useful to directly access the source words that are relevant to that prediction.

Instead of:

**Past information → hidden state → prediction**

we can have:

**Prediction → direct connections → relevant past tokens**

The model learns which tokens matter.

This is the basic concept of **attention**.

---

# 14. Self-Attention
**Approx. 57:21–1:09:35**

The 2017 Transformer relies on **self-attention**.

The key change is:

> A token's representation can be computed as a function of the other tokens in the sequence.

Instead of maintaining one recurrent hidden state, tokens can directly interact with one another.

---

## 14.1 The Word-Order Question

If every token can interact with every other token, then a basic self-attention mechanism does not inherently know the order of tokens.

For example, the model needs to distinguish:

> “A eats B.”

from:

> “B eats A.”

The Transformer addresses this later using **positional information**.

---

# 15. Query, Key, and Value

Self-attention is usually described using three quantities:

- **Query (Q)**
- **Key (K)**
- **Value (V)**

## 15.1 Query

The query represents what a token is looking for.

For example:

> “What information is useful for understanding this token?”

---

## 15.2 Key

Each token has a key that represents what it can be matched against.

The query is compared with keys to determine relevance.

---

## 15.3 Value

Each token also has a value.

Once attention determines how relevant each token is, the corresponding values are combined according to those relevance weights.

---

## 15.4 Intuition

Suppose we want a good representation for:

> `Teddy bear`

The query can ask:

> “Which tokens help describe Teddy bear?”

The token `cute` may be highly relevant.

Therefore, its key may have high similarity with the query, causing its value to receive a larger weight.

The resulting representation is therefore a weighted combination of information from the sequence.

---

# 16. Learning Q, K, and V

Q, K, and V are obtained through learned projection matrices.

Starting from token representations:

- project into **query space** using `W_Q`;
- project into **key space** using `W_K`;
- project into **value space** using `W_V`.

Conceptually:

```text
X → Q = XW_Q
X → K = XW_K
X → V = XW_V
```

The model learns these projection matrices.

---

# 17. Scaled Dot-Product Attention

The central Transformer formula is:

\[
Attention(Q,K,V)
=
softmax\left(
\frac{QK^T}{\sqrt{d_k}}
\right)V
\]

This formula can be understood in three steps.

### Step 1 — Similarity

\[
QK^T
\]

computes query-key similarities using dot products.

### Step 2 — Scaling

\[
\frac{QK^T}{\sqrt{d_k}}
\]

normalizes the scores based on the key dimension.

### Step 3 — Softmax

\[
softmax(...)
\]

converts the scores into normalized attention weights.

### Step 4 — Weighted Values

The attention weights are multiplied by `V`.

The result is a weighted combination of value vectors.

---

# 18. Matrix Interpretation of Attention

Suppose the sequence contains `n` tokens.

Then:

- `Q` contains the queries for all tokens.
- `K` contains the keys for all tokens.
- `V` contains the values for all tokens.

The matrix:

\[
QK^T
\]

has shape:

\[
n \times n
\]

Each cell represents the similarity between:

> one query token and one key token.

After softmax, each row can be interpreted as a distribution over the tokens being attended to.

Multiplying this by `V` creates the new context-aware representations.

---

# 19. Transformer Architecture
**Approx. 1:09:35–1:22:18**

The Transformer was introduced in the context of **machine translation**.

The original architecture has two major components:

1. **Encoder**
2. **Decoder**

The encoder processes the source text.

The decoder uses the encoder representations to generate the target text.

---

# 20. Transformer Input

Suppose the source sentence is:

> “A cute Teddy bear is reading.”

The first stage is:

### Step 1 — Tokenize

Convert the text into tokens.

### Step 2 — Token Embeddings

Map each token to a learned embedding vector.

These embeddings are initially token-specific and are not yet context-aware.

### Step 3 — Positional Information

Add information about where each token occurs in the sequence.

Therefore:

\[
Input = TokenEmbedding + PositionEmbedding
\]

---

# 21. Positional Embeddings

The original Transformer uses positional information so that the model can distinguish different positions.

Two approaches discussed are:

### Learned positional embeddings

The model learns a representation for each position.

A limitation is that if the model only learned positions up to a certain length, it may not directly represent positions beyond that range.

### Sinusoidal positional representations

Position can be represented using sine and cosine functions at different frequencies.

The lecture uses a clock analogy:

- hours,
- minutes,
- seconds

change at different frequencies.

Combining different frequencies provides information about the position.

A useful property is:

> nearby positions have similar representations, while distant positions are more dissimilar.

---

# 22. Transformer Encoder

The encoder's purpose is:

> **Compute meaningful, context-aware representations of the input tokens.**

A simplified encoder block contains:

1. Self-attention
2. Feedforward neural network

with additional architectural mechanisms such as:

- residual connections,
- layer normalization.

---

## 22.1 Encoder Self-Attention

Each token can interact with the other tokens in the sequence.

Therefore, after self-attention, a token's representation can depend on the entire sequence.

For example, the representation of `Teddy bear` can incorporate information from `cute`, `reading`, and other relevant tokens.

---

## 22.2 Feedforward Neural Network

After attention, the representation passes through a feedforward neural network.

Its purpose is to transform the representation and learn nonlinear relationships.

The feedforward network typically expands the representation into a higher-dimensional space before projecting it back.

---

## 22.3 Encoder Output

After passing through the encoder stack, each token has a:

> **context-aware, learned representation**

that reflects the other tokens in the sequence.

---

# 23. Transformer Decoder

The decoder is responsible for generating the target sequence.

Generation begins with a special token:

> `<BOS>` — Beginning of Sequence

The decoder then repeatedly predicts the next token.

---

## 23.1 Decoder Input

The decoder token receives:

\[
TokenEmbedding + PositionEmbedding
\]

The representation is then passed through the decoder block.

---

# 24. Masked Self-Attention

The decoder uses **masked self-attention**.

The key constraint is:

> A token can attend only to itself and tokens that have already been generated.

It cannot look at future tokens.

This makes generation **causal**.

For example:

```text
Token 1 → can see Token 1
Token 2 → can see Tokens 1–2
Token 3 → can see Tokens 1–3
Token 4 → can see Tokens 1–4
```

The future positions are masked.

---

# 25. Cross-Attention

After masked self-attention, the decoder performs another attention operation:

> **Cross-attention**

Here:

- **Queries** come from the decoder.
- **Keys** come from the encoder.
- **Values** come from the encoder.

The purpose is to allow the generated representation to access relevant information from the source sequence.

Conceptually:

```text
Decoder representation
        ↓
      Query
        ↓
     Attention
        ↑
 Encoder Keys + Values
```

This connects the target-generation process to the source text.

---

# 26. Decoder Feedforward Network

After cross-attention, the representation passes through a feedforward neural network.

The result is a context-aware representation for the token currently being processed.

---

# 27. Predicting the Next Token

The decoder output is projected into vocabulary space.

A final softmax produces probabilities over all possible tokens.

Conceptually:

```text
Decoder representation
        ↓
Linear projection
        ↓
Softmax
        ↓
Probability for every vocabulary token
        ↓
Choose next token
```

The predicted token is then fed back into the decoder.

This process repeats **autoregressively**.

Generation stops when the model produces:

> `<EOS>`

---

# 28. Computational and Architectural Tricks
**Approx. 1:22:19–1:27:34**

The Transformer contains several mechanisms that make deep learning easier and more stable.

---

## 28.1 Residual Connections

Instead of:

\[
output = f(x)
\]

a residual connection gives something conceptually like:

\[
output = f(x) + x
\]

The original input can therefore pass through directly while the sublayer learns a modification.

This helps:

- backpropagation,
- optimization,
- learning in deep networks.

A useful intuition is:

> The layer modifies the representation rather than having to completely replace it.

---

## 28.2 Layer Normalization

Layer normalization normalizes activations.

The lecture presents it as a mechanism that helps with:

> **convergence and stable learning.**

---

## 28.3 Masked Attention

The decoder uses masking so that a token cannot access information from future tokens.

This preserves the causal nature of autoregressive generation.

---

## 28.4 Multi-Head Attention

Instead of performing attention only once, the model can learn multiple attention projections.

Each head can learn a different way of relating tokens.

The lecture compares this conceptually with using multiple filters in convolutional neural networks.

For `h` heads:

1. project into different Q/K/V spaces;
2. perform attention in parallel;
3. concatenate the resulting representations;
4. apply a final projection.

The multi-head result can be written conceptually as:

\[
MultiHead(Q,K,V)
=
Concat(head_1,\ldots,head_h)W_O
\]

where each head performs:

\[
head_i =
softmax
\left(
\frac{Q_iK_i^T}{\sqrt{d_k}}
\right)V_i
\]

---

## 28.5 Dropout

Dropout is a general regularization technique.

During training, some units are intentionally dropped with some probability.

The goal is to prevent the model from relying too heavily on particular features and to improve generalization.

---

## 28.6 Label Smoothing

Instead of requiring the correct token to receive probability 100%, label smoothing softens the target distribution.

For example, instead of:

```text
Correct token: 100%
Everything else: 0%
```

the target can be more like:

```text
Correct token: 90%
Remaining probability: distributed among other tokens
```

The motivation is that language can have multiple valid continuations.

The lecture notes that label smoothing was used in the original Transformer context and could improve machine-translation metrics such as BLEU.

---

# 29. End-to-End Transformer Example
**Approx. 1:27:40–1:40:06**

This section connects all the concepts into one computation.

The example is machine translation.

Source sentence:

> **“A cute Teddy bear is reading.”**

The original Transformer was introduced for translation between languages such as English, French, and German.

---

# 30. Step 1 — Tokenization

First, the source sentence is split into tokens.

Special tokens such as:

- `<BOS>`
- `<EOS>`

can indicate sequence boundaries.

The exact token split is not the important point in the toy example; the lecture uses a simplified split to demonstrate the architecture.

---

# 31. Step 2 — Token Embeddings

The Transformer has a learnable embedding lookup table.

Each token is mapped to a vector of dimension:

\[
D_{model}
\]

These embeddings are learned during training.

---

# 32. Step 3 — Add Position Information

Position embeddings have the same dimensionality as the token embeddings.

They are added:

\[
X = TokenEmbedding + PositionEmbedding
\]

The resulting matrix is the input to the encoder.

---

# 33. Step 4 — Project Into Q, K, V

The encoder input is projected using learned matrices:

\[
Q = XW_Q
\]

\[
K = XW_K
\]

\[
V = XW_V
\]

If the sequence length is `n`, the resulting matrices contain `n` rows.

The query and key dimensions need to match for the dot-product operation:

\[
D_Q = D_K
\]

---

# 34. Step 5 — Compute Attention Scores

Calculate:

\[
QK^T
\]

This creates an:

\[
n \times n
\]

matrix.

Each cell represents the similarity between a query and a key.

Then:

\[
\frac{QK^T}{\sqrt{D_K}}
\]

scales the scores.

Softmax converts each row into normalized attention weights.

---

# 35. Step 6 — Combine Values

The normalized attention weights are multiplied by `V`.

Therefore:

\[
Attention(Q,K,V)
=
softmax
\left(
\frac{QK^T}{\sqrt{D_K}}
\right)V
\]

The output has the same sequence length as the input.

---

# 36. Step 7 — Multi-Head Attention

The Q/K/V process is performed multiple times in parallel.

For `h` attention heads:

1. learn separate projections;
2. calculate attention for each head;
3. concatenate the results;
4. project them back to the model dimension.

The final projection is commonly represented by:

\[
W_O
\]

The resulting representation returns to the model dimension:

\[
D_{model}
\]

---

# 37. Step 8 — Feedforward Network

The resulting representation passes through a feedforward network.

The lecture describes this as a one-hidden-layer network that typically expands:

\[
D_{model} \rightarrow D_{FF}
\]

where `D_FF` is typically larger than `D_model`.

This larger intermediate space provides capacity for learning more complex representations.

---

# 38. Step 9 — Repeat the Encoder Block

The encoder block is repeated multiple times.

In the original Transformer architecture, the lecture notes:

\[
N = 6
\]

After the encoder stack, each source token has a:

> **context-aware learned representation**

---

# 39. Step 10 — Start the Decoder

To begin generating the translated sentence, feed the decoder:

> `<BOS>`

The token receives:

\[
TokenEmbedding + PositionEmbedding
\]

and enters the decoder.

---

# 40. Step 11 — Masked Self-Attention

The decoder first performs causal self-attention.

At the beginning, only `<BOS>` has been generated.

After generating one token, the decoder can attend to:

- `<BOS>`
- that first generated token.

After generating two tokens, it can attend to:

- `<BOS>`
- token 1
- token 2.

And so on.

---

# 41. Step 12 — Cross-Attention

The decoder then attends to the encoder output.

Here:

- decoder representation → **Query**
- encoder representations → **Keys**
- encoder representations → **Values**

This allows the decoder to determine which parts of the source sentence are relevant for generating the next target token.

---

# 42. Step 13 — Feedforward Network

The decoder representation passes through its feedforward network.

The result is a representation suitable for predicting the next token.

---

# 43. Step 14 — Vocabulary Projection

A linear layer projects the decoder representation into vocabulary space.

Softmax then produces:

\[
P(token_i \mid context)
\]

for every token in the vocabulary.

The system chooses the next token according to the probability distribution.

The lecture uses selecting the maximum-probability token as a simple example.

---

# 44. Step 15 — Autoregressive Generation

The predicted token is fed back into the decoder.

The process repeats:

```text
<BOS>
   ↓
Predict token 1
   ↓
Predict token 2
   ↓
Predict token 3
   ↓
...
   ↓
<EOS>
```

The decoder stops when it produces `<EOS>`.

This is how the Transformer turns a source sentence into a generated target sentence.

---

# 45. What Is the Core of the Transformer?

Near the end, the lecture asks what actually makes the architecture work.

The main answer is:

## 45.1 Attention

The attention mechanism is the central idea.

It allows tokens to directly interact rather than forcing all information through a recurrent hidden state.

This is the key idea captured by the title:

> **“Attention Is All You Need.”**

---

## 45.2 Feedforward Network

The feedforward network contains a large portion of the model's parameters and provides substantial representational capacity.

Therefore, the lecture identifies two especially important components:

1. **Attention**
2. **Feedforward neural network**

Other mechanisms—residual connections, normalization, dropout, masking, etc.—are important architectural and optimization techniques that help the model learn effectively.

The quality of the training data is also an important part of the overall system.

---

# 46. Masking: Mental Model

A simple mental model for causal masking is:

> **A token cannot look at tokens that come after it.**

Computationally, a triangular mask can prevent those connections.

One implementation approach is to assign masked positions a very negative value (conceptually `-∞`) before softmax.

Because:

\[
softmax(-\infty) = 0
\]

those future connections receive zero attention weight.

---

# 47. Two Different Uses of Softmax

The lecture emphasizes that softmax appears in multiple places, but the purpose is different.

## In Attention

Softmax converts attention scores into weights over keys.

It answers approximately:

> **How much should this token attend to each other token?**

## At the Final Output

Softmax converts the decoder's vocabulary scores into a probability distribution over possible next tokens.

It answers:

> **What token should be generated next?**

So the same mathematical function is being used for different purposes.

---

# 48. The Complete Conceptual Flow

The entire lecture can be compressed into this dependency chain:

```text
RAW TEXT
   │
   ▼
TOKENIZATION
   │
   ├── Word-level
   ├── Character-level
   └── Subword / BPE
   │
   ▼
TOKENS
   │
   ▼
TOKEN EMBEDDINGS
   │
   ├── One-hot: too limited
   ├── Word2Vec: meaningful but static
   └── RNN/LSTM: contextual but sequential
   │
   ▼
ATTENTION
   │
   ▼
SELF-ATTENTION
   │
   ├── Query
   ├── Key
   └── Value
   │
   ▼
QKᵀ / √dₖ
   │
   ▼
SOFTMAX
   │
   ▼
WEIGHTED VALUES
   │
   ▼
MULTI-HEAD ATTENTION
   │
   ▼
FEEDFORWARD NETWORK
   │
   ▼
TRANSFORMER
   │
   ├── Encoder
   │     └── Context-aware source representations
   │
   └── Decoder
         ├── Masked self-attention
         ├── Cross-attention
         ├── Feedforward network
         └── Vocabulary projection
                 │
                 ▼
          NEXT-TOKEN PROBABILITY
                 │
                 ▼
          AUTOREGRESSIVE GENERATION
                 │
                 ▼
                EOS
```

---

# 49. The Main Problems and How the Lecture Progresses Through Them

| Problem | Earlier Approach | Limitation | Next Idea |
|---|---|---|---|
| Text is not numerical | Raw text | Neural networks need numbers | Tokenization |
| Words are too rigid | Word-level tokens | Large vocabulary, OOV | Character/subword tokens |
| Characters are too long | Character tokens | Very long sequences | Subwords/BPE |
| Tokens need meaning | One-hot | No semantic relationship | Word2Vec |
| Meaning depends on context | Word2Vec | Static representations | RNN |
| Long-range context | RNN | Long-range dependency / vanishing gradients | LSTM |
| Sequential computation | RNN/LSTM | Slow and difficult to parallelize | Attention |
| Need direct token interaction | Attention | Need a scalable architecture | Self-attention |
| Need word order | Self-attention alone | Tokens do not inherently have positions | Positional encoding |
| Need multiple relationships | Single attention | Limited view | Multi-head attention |
| Need deep, trainable networks | Deep Transformer | Optimization difficulty | Residual connections + normalization |
| Need controlled generation | Decoder attention | Future-token leakage | Masked self-attention |

---

# 50. Key Formulas to Remember

## Token representation

\[
X = TokenEmbedding + PositionEmbedding
\]

## Query, Key, Value

\[
Q = XW_Q
\]

\[
K = XW_K
\]

\[
V = XW_V
\]

## Scaled dot-product attention

\[
\boxed{
Attention(Q,K,V)
=
softmax
\left(
\frac{QK^T}{\sqrt{d_k}}
\right)V
}
\]

## Multi-head attention

\[
\boxed{
MultiHead(Q,K,V)
=
Concat(head_1,\ldots,head_h)W_O
}
\]

where:

\[
head_i =
softmax
\left(
\frac{Q_iK_i^T}{\sqrt{d_k}}
\right)V_i
\]

---

# 51. Final Takeaway

The lecture is essentially building one continuous argument:

1. **We start with text.**
2. We need to turn text into **tokens**.
3. Tokens need **numerical representations**.
4. Static representations such as Word2Vec cannot fully capture **context and word order**.
5. RNNs introduce sequence context but suffer from **long-range dependencies and sequential computation**.
6. Attention allows direct access to relevant tokens.
7. Self-attention allows every token to build a representation using other tokens.
8. Q/K/V provides the mathematical mechanism for deciding **what information matters**.
9. Positional information restores **order**.
10. Multi-head attention lets the model learn multiple relationships in parallel.
11. Feedforward networks provide additional representational capacity.
12. Encoder-decoder Transformers use these components for sequence-to-sequence tasks such as translation.
13. The decoder generates text **autoregressively**, one token at a time.
14. This Transformer architecture became the foundation on which modern LLMs were subsequently scaled.

The lecture closes by emphasizing that this is only the beginning: the following lectures move toward **how such models are trained**, and the later part of the course addresses how they can power **agents and larger systems**.
