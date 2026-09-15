---
theme: default
title: Transformers — How AI Understands and Generates Text
info: A simple visual introduction to Transformers and LLMs
class: text-center
transition: slide-left
mdc: true
---

# How Does AI Understand Text?

## Understanding Transformers

<div class="mt-10 text-xl opacity-70">

From **words → attention → probabilities → answers**

</div>

---

# Imagine You Are Reading This Sentence

> **The boy dropped the glass because it was slippery.**

What does **"it"** refer to?

Is it:

- the boy?
- the glass?

Your brain looks at the sentence and decides which words are important.

---

# How Did You Know?

You didn't give equal attention to every word.

You probably connected:

**it → glass**

Your brain found a relationship.

<div class="mt-8 text-2xl">

A Transformer tries to do something similar.

</div>

---

# The Big Idea

## Attention

Attention means:

> **"Look at the words that are important for understanding this word."**

For example:

> The **boy** dropped the **glass** because **it** was slippery.

The word **"it"** should pay more attention to:

**glass**

---

# Imagine Highlighting Words

```text
The boy dropped the glass because it was slippery.
                         █████
                           ↑
                      important
```

The Transformer does something similar mathematically.

It gives different words different **attention scores**.

---

# Attention Score

Imagine:

```text
"It" is looking at:

boy       → 0.10
dropped   → 0.05
glass     → 0.70
slippery  → 0.15
```

The numbers tell us:

> How much attention should "it" give to each word?

---

# Why Numbers?

Computers work with numbers.

So instead of saying:

> "glass is very important"

we can say:

$$
attention(glass)=0.70
$$

Instead of:

> "boy is not very important"

we might say:

$$
attention(boy)=0.10
$$

---

# A Simple Attention Picture

```text
             boy
              │
             0.10
              ↓
"It" ────────► glass
              0.70
              ↑
           important

             dropped
              0.05
```

The Transformer calculates these numbers automatically.

---

# But Words Are Not Numbers...

How can a computer work with:

> cat

or:

> elephant

?

We turn words into numbers.

This is called an:

# Embedding

---

# Word → Numbers

Imagine:

```text
cat

↓

[0.2, 0.8, 0.1, 0.6]
```

Another word:

```text
dog

↓

[0.3, 0.7, 0.2, 0.5]
```

The actual models use vectors with many more numbers.

---

# Why Use Vectors?

Think about a map.

```text
             Animals
                ↑

       dog ●    │    ● cat

                │

                │

   car ●────────┼────────● bus

                ↓
             Vehicles
```

The numbers allow the model to represent relationships between things.

---

# The Transformer Sees Numbers

So the journey starts like this:

```text
Sentence
   ↓
Words / Tokens
   ↓
Numbers
   ↓
Vectors
   ↓
Transformer
```

---

# Now We Have a New Problem

Suppose we have:

> **The dog chased the cat because it was angry.**

Who is **"it"**?

The Transformer needs to figure out which words are related.

This is where **Attention** helps.

---

# Attention Is Like a Spotlight

Imagine a student reading a textbook.

They don't focus equally on every sentence.

They focus more on the information that helps answer the question.

Attention works like a:

# Spotlight 🔦

---

# Attention Spotlight

For the word:

> **it**

The Transformer might give:

```text
The       0.02
dog       0.60
chased    0.05
the       0.02
cat       0.20
angry     0.11
```

The biggest spotlight is on:

**dog**

---

# But How Does It Decide?

This is where we introduce three simple ideas.

## Query

> **What am I looking for?**

## Key

> **What do I have?**

## Value

> **What information can I give?**

---

# Think About a Library

You walk into a library.

You ask:

> "I want a book about space."

That's your:

# Query

---

# Books Have Information

Each book has:

**Title / Keywords**

These are like:

# Keys

You compare your question with the books' keywords.

---

# Then You Pick the Book

The useful book gives you:

# Value

So:

```text
Question
   ↓
Query
   ↓
Compare with Keys
   ↓
Find useful information
   ↓
Value
```

That's the basic idea of Q, K and V.

---

# Q, K and V in a Sentence

For every word, the Transformer creates:

```text
             Word
               │
       ┌───────┼───────┐
       ↓       ↓       ↓
     Query    Key    Value
       │       │       │
       └───┬───┘       │
           ↓           │
       Compare         │
           ↓           │
       Importance      │
           └─────┬─────┘
                 ↓
             New Meaning
```

---

# The Mathematics Behind It

We compare Query and Key using a:

# Dot Product

For two simple vectors:

$$
A=[2,3]
$$

$$
B=[4,1]
$$

Their dot product is:

$$
A\cdot B
=
(2\times4)+(3\times1)
$$

$$
=8+3
$$

$$
=11
$$

---

# What Does a Big Number Mean?

A larger dot product means:

> **These two vectors are more similar / compatible according to the learned representation.**

So we can use the dot product as an:

# Attention Score

---

# Attention Scores

The Transformer calculates:

$$
QK^T
$$

Don't worry about the notation yet.

The simple idea is:

> **Compare every Query with every Key.**

---

# Attention Matrix

For:

```text
The cat sat down
```

we might get:

```text
          The   cat   sat   down

The       0.8   0.1   0.1   0.0
cat       0.1   0.6   0.2   0.1
sat       0.0   0.3   0.5   0.2
down      0.0   0.2   0.4   0.4
```

This is an:

# Attention Matrix

---

# Why Do We Need Softmax?

Our scores are just numbers.

For example:

```text
cat      7
dog      3
mouse    1
```

We want something easier to understand:

```text
cat      0.88
dog      0.10
mouse    0.02
```

Numbers that add up to:

$$
1
$$

---

# Softmax

Softmax converts scores into a probability-like distribution.

$$
P_i=
\frac{e^{z_i}}
{\sum_j e^{z_j}}
$$

You don't need to memorize the equation yet.

Remember:

> **Softmax turns scores into percentages/probabilities.**

---

# Probability Distribution

Suppose an AI sees:

> The sky is...

It might produce:

```text
blue       0.80
clear      0.10
dark       0.05
green      0.03
red        0.02
```

Visual:

```text
blue   ████████████████
clear  ██
dark   █
green  ▌
red    ▌
```

---

# The AI Doesn't "Know" One Answer

It has a distribution.

It is saying:

> Blue is very likely.

> Clear is possible.

> Dark is less likely.

> Green is unlikely.

This is extremely important for understanding how LLMs work.

---

# Logits

Before Softmax, the model produces:

# Logits

Example:

```text
blue      5.2
clear     2.4
dark      1.1
green    -0.3
```

These are simply:

> **Raw scores before turning them into probabilities.**

---

# The Pipeline

```text
Transformer
     ↓
Raw Scores
   (Logits)
     ↓
 Softmax
     ↓
Probabilities
     ↓
Choose Next Token
```

---

# Now Let's Generate a Sentence

Input:

> The sky is

The Transformer produces:

```text
blue      0.80
clear     0.10
dark      0.05
green     0.03
red       0.02
```

It chooses:

# blue

Now we have:

> The sky is blue

---

# Then What?

The model runs again.

Input:

> The sky is blue

It predicts the next token.

Maybe:

```text
and       0.45
today     0.20
.         0.15
above     0.10
...
```

Choose one.

Then repeat.

---

# This Is How Text Is Generated

```text
The sky is
     ↓
The sky is blue
     ↓
The sky is blue today
     ↓
The sky is blue today.
```

One token at a time.

---

# Next-Token Prediction

The central job of a language model is:

$$
P(next\ token|previous\ tokens)
$$

In simple English:

> **"Given everything I've seen so far, what token should come next?"**

---

# But Who Controls the Randomness?

Suppose:

```text
blue      80%
clear     10%
dark       5%
green      3%
red        2%
```

Should the model always choose:

**blue**?

Not necessarily.

This is where:

# Temperature

comes in.

---

# Temperature

Temperature controls how strongly the model prefers high-probability choices.

Think of it like:

> **A creativity/randomness knob.**

---

# Low Temperature

Example:

$$
T=0.2
$$

The distribution becomes very sharp.

```text
blue      ███████████████████
clear     █
dark      ▏
green     ▏
```

The model strongly prefers the most likely answer.

---

# High Temperature

Example:

$$
T=1.5
$$

The distribution becomes flatter.

```text
blue      █████████
clear     █████
dark      ███
green     ██
red       ██
```

Other possibilities become more likely.

---

# Temperature Mathematics

Temperature is applied to logits:

$$
P_i=
\frac{e^{z_i/T}}
{\sum_j e^{z_j/T}}
$$

where:

$$
T = temperature
$$

The important idea:

```text
Low T → sharper distribution

High T → flatter distribution
```

---

# Temperature Does NOT Change the Model

This is important.

Temperature does **not** change:

- the model's weights
- its training
- its knowledge
- its architecture

It changes:

> **How we choose from the model's predicted probabilities.**

---

# Temperature Experiment

Same model.

Same prompt.

Different temperature.

```text
             T=0.2       T=1.0       T=1.5

blue         ████████     ██████      █████
clear        █            ██          ████
dark         ▏            █           ███
green        ▏            ▌           ██
```

Same model.

Different generation behavior.

---

# What Is Top-K?

Suppose the model gives:

```text
blue       0.50
clear      0.20
dark       0.12
green      0.08
red        0.05
yellow     0.03
```

If:

$$
K=3
$$

we keep only:

```text
blue
clear
dark
```

---

# Top-K

Think:

> **"Only consider the K best choices."**

```text
All choices

blue
clear
dark
green
red
yellow

      ↓ Top-K = 3

blue
clear
dark
```

---

# What Is Top-P?

Top-P asks:

> **"How many of the best choices do I need to cover most of the probability?"**

Example:

```text
blue       0.50
clear      0.25
dark       0.12
green      0.06
red        0.04
yellow     0.03
```

For:

$$
P=0.90
$$

we keep:

```text
blue     0.50
clear    0.25
dark     0.12
green    0.06

Total = 0.93
```

---

# Top-K vs Top-P

### Top-K

> Keep a fixed number of choices.

### Top-P

> Keep enough choices to reach a probability limit.

```text
Top-K

"Give me the best 3."

Top-P

"Give me enough choices
to cover 90% of the probability."
```

---

# Greedy Decoding

There is another simple strategy.

Always choose the biggest probability.

$$
x=\arg\max P(x)
$$

Example:

```text
blue       0.80 ← choose
clear      0.10
dark       0.05
green      0.03
```

This is called:

# Greedy Decoding

---

# Sampling

Instead of always choosing the biggest one:

> Pick according to the probabilities.

Example:

```text
blue      80%
clear     10%
dark       5%
green      3%
red        2%
```

Most of the time:

**blue**

But sometimes:

**clear**

---

# Greedy vs Sampling

```text
             Probability
                  ↓
          ┌───────┴───────┐
          ↓               ↓
       Greedy          Sampling
          ↓               ↓
   Highest choice     Random choice
```

This is one reason AI responses can differ.

---

# What Is a Context Window?

Imagine the model has a notebook.

It can only fit a certain number of tokens in that notebook.

That is the:

# Context Window

---

# Context Window

```text
┌─────────────────────────────┐
│ Context                      │
│                             │
│ Previous conversation        │
│ Documents                    │
│ User question                │
│ Instructions                 │
│                             │
└─────────────────────────────┘
```

If the context is too large, something has to be removed or handled differently.

---

# Context Window Mathematics

If the model has capacity:

$$
C
$$

then roughly:

$$
Input\ Tokens + Output\ Tokens
\leq C
$$

The exact rules depend on the model and system.

---

# What Are Model Parameters?

Here is another meaning of the word:

# Parameters

A model contains many learned numbers.

Imagine:

```text
0.21
-0.73
0.45
0.91
-0.12
...
```

These numbers are adjusted during training.

---

# Parameters Are Like Tiny Knobs

Imagine millions of tiny knobs:

```text
○ ○ ○ ○ ○ ○ ○ ○ ○ ○
○ ○ ○ ○ ○ ○ ○ ○ ○ ○
○ ○ ○ ○ ○ ○ ○ ○ ○ ○
```

During training, the model adjusts these knobs.

Eventually they contain learned patterns.

---

# Training

The model sees:

> The cat is ___

Maybe it predicts:

> running

But the correct answer is:

> sleeping

The model calculates how wrong it was.

Then adjusts its parameters.

---

# Training Loop

```text
Example
   ↓
Model prediction
   ↓
Compare with correct answer
   ↓
Calculate error
   ↓
Backpropagation
   ↓
Adjust parameters
   ↓
Try again
```

Repeat this billions of times.

---

# Loss

Loss tells us:

> **How wrong was the model?**

If the correct answer has probability:

$$
P(correct)=0.9
$$

loss is low.

If:

$$
P(correct)=0.01
$$

loss is high.

A simple language-model loss is:

$$
L=-\log P(correct)
$$

---

# Why Log?

Consider:

```text
Probability     Loss

0.90            low
0.50            medium
0.10            high
0.01            very high
```

The logarithm gives us a useful way to strongly penalize very small probabilities.

---

# Backpropagation

After calculating loss:

> Which parameters caused the error?

Backpropagation calculates:

$$
\frac{\partial L}{\partial W}
$$

In simple words:

> **"How should each weight change to reduce the error?"**

---

# The Transformer Block

Now we can finally see the whole structure.

```text
Input
  ↓
Attention
  ↓
Add Information
  ↓
Feed-Forward Network
  ↓
Add Information
  ↓
Output
```

This block is repeated many times.

---

# Feed-Forward Network

Attention asks:

> **"Which information is important?"**

The feed-forward network helps transform that information.

Very simply:

```text
Attention
   ↓
"What should I look at?"
   ↓
Feed Forward
   ↓
"What should I do with it?"
```

---

# Why Multiple Attention Heads?

Imagine a group of students reading a sentence.

One student looks for:

> grammar

Another:

> people

Another:

> actions

Another:

> relationships

Transformers use multiple attention heads.

---

# Multi-Head Attention

```text
                 Sentence
                    ↓
       ┌────────────┼────────────┐
       ↓            ↓            ↓
    Head 1        Head 2       Head 3
       ↓            ↓            ↓
    Pattern       Pattern      Pattern
       └────────────┼────────────┘
                    ↓
                 Combine
```

Different heads can learn different patterns.

---

# Why Does Position Matter?

Consider:

> Dog bites man.

and:

> Man bites dog.

Same words.

Different meaning.

So the model needs to know:

> **Where is each word?**

---

# Position

We add position information to the token representation.

```text
The   → Position 1
dog   → Position 2
bites → Position 3
man   → Position 4
```

So the model knows:

> "dog" came before "bites".

---

# The Full Transformer Idea

```text
Text
 ↓
Tokens
 ↓
Numbers
 ↓
Embeddings
 ↓
Position
 ↓
Attention
 ↓
Multiple Attention Heads
 ↓
Feed Forward
 ↓
Repeat
 ↓
Logits
 ↓
Probability Distribution
 ↓
Temperature / Top-K / Top-P
 ↓
Next Token
```

---

# Encoder and Decoder

The original Transformer had two major parts:

```text
        Transformer
             │
      ┌──────┴──────┐
      ↓             ↓
   Encoder       Decoder
      ↓             ↓
 Understand      Generate
```

Modern LLMs such as GPT-style models primarily use the decoder side.

---

# Why Can't the Decoder See the Future?

Suppose we want:

> The cat is sleeping.

When predicting:

> sleeping

the model can see:

```text
The
cat
is
```

but not:

```text
sleeping
```

because that is the answer it is trying to predict.

---

# Causal Mask

```text
          The  cat  is  sleeping

The        ✓    ✗    ✗      ✗
cat        ✓    ✓    ✗      ✗
is         ✓    ✓    ✓      ✗
sleeping   ✓    ✓    ✓      ✓
```

The model can look backward.

Not forward.

---

# Why Is This Called "Causal"?

Because the model generates:

```text
Past → Present → Future
```

It cannot use information from the future to predict the future.

---

# KV Cache

Imagine writing a story.

You don't want to reread the entire story from the beginning every time you write one new word.

So the model can remember useful intermediate information.

This is called:

# KV Cache

---

# KV Cache — Simple Idea

```text
Previous tokens
      ↓
Previously calculated K and V
      ↓
      Cache
      ↓
Reuse them
```

This makes generation faster.

---

# Why Are Transformers Powerful?

### 1. They can look at relationships

### 2. They can process many tokens efficiently during training

### 3. They scale to huge models

### 4. The same basic idea works for:

- language
- code
- images
- audio
- video

---

# But There Is a Big Problem

The model produces:

> **probable text**

Not necessarily:

> **true information**

For example:

```text
Probability

Answer A    0.80
Answer B    0.10
Answer C    0.10
```

Answer A can still be wrong.

---

# Probability ≠ Truth

This is one of the most important ideas about LLMs.

The model asks:

> "What is a likely next token?"

It does not directly ask:

> "Is this statement objectively true?"

This is one reason hallucinations can happen.

---

# Transformer vs LLM

These terms are related but not identical.

### Transformer

The neural-network architecture.

### LLM

A large language model built using an architecture such as the Transformer and trained on huge amounts of data.

```text
Transformer
     +
Huge Dataset
     +
Training
     ↓
LLM
```

---

# Generation Parameters

When using an LLM, you may see:

```text
temperature
top_k
top_p
max_tokens
stop
seed
```

These are **generation settings**.

They are not the same as the model's learned parameters.

---

# Two Types of Parameters

## Learned Parameters

The model learns these:

```text
Weights
Biases
Attention matrices
Feed-forward matrices
...
```

## Generation Parameters

We choose these:

```text
Temperature
Top-K
Top-P
Max tokens
Stop sequences
```

---

# A Simple Analogy

Think about a student.

### Learned parameters

Everything the student learned in school.

### Generation parameters

How you ask the student to answer:

> "Answer briefly."

> "Give me several possibilities."

> "Be creative."

The student's knowledge didn't change.

The way they respond changed.

---

# One Complete Example

Question:

> What is the capital of France?

The model processes the question.

```text
Text
 ↓
Tokens
 ↓
Embeddings
 ↓
Attention
 ↓
Transformer Layers
 ↓
Logits
 ↓
Softmax
 ↓
Probability Distribution
```

---

# Probability Distribution

The model might internally produce something like:

```text
Paris       ████████████████  0.95
London      █                  0.01
Berlin      █                  0.01
Rome        █                  0.01
Other       ██                 0.02
```

Then generation selects:

# Paris

---

# One More Interesting Example

Prompt:

> Write a funny story about a cat.

Now many answers are possible.

```text
funny cat
    ↓
Many possible continuations
    ↓
Probability distribution
    ↓
Temperature / Sampling
    ↓
One continuation
```

Higher temperature can allow more unusual choices.

---

# Temperature in One Sentence

> **Temperature controls how sharply the model prefers its most likely choices.**

```text
Low temperature
      ↓
Safer / more predictable

High temperature
      ↓
More varied / unpredictable
```

---

# Top-K in One Sentence

> **Top-K says: only consider the best K choices.**

Example:

$$
K=5
$$

Keep the five most likely tokens.

---

# Top-P in One Sentence

> **Top-P says: keep enough likely choices to cover a chosen probability mass.**

Example:

$$
P=0.90
$$

Keep enough tokens to cover roughly 90% of the probability.

---

# The Important Generation Controls

```text
              Probability
              Distribution
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
 Temperature      Top-K        Top-P
       │            │            │
       ↓            ↓            ↓
   Sharpness     Number       Probability
                 of choices      mass
```

---

# The Mathematics Map

```text
Tokens
  ↓
Embeddings
  ↓
Vectors
  ↓
Q, K, V
  ↓
Dot Product
  ↓
Attention Scores
  ↓
Softmax
  ↓
Probability Distribution
  ↓
Logits + Temperature
  ↓
Sampling
  ↓
Next Token
```

---

# The Visual Artifacts We Should Remember

### Artifact 1

**Tokenization**

```text
Text → Tokens
```

### Artifact 2

**Embedding space**

```text
Words → Vectors
```

### Artifact 3

**Attention matrix**

```text
Word × Word
```

### Artifact 4

**Probability distribution**

```text
Token → Probability
```

---

# More Artifacts

### Artifact 5

**Temperature comparison**

```text
T=0.2 vs T=1 vs T=1.5
```

### Artifact 6

**Top-K**

```text
Keep K choices
```

### Artifact 7

**Top-P**

```text
Keep probability mass
```

### Artifact 8

**Causal mask**

```text
Can see ←
Cannot see →
```

---

# The Entire Story

```text
                 Human Language
                       ↓
                    Tokens
                       ↓
                  Embeddings
                       ↓
              Transformer Layers
                       ↓
                  Attention
                       ↓
                Understanding
                       ↓
                    Logits
                       ↓
              Probability Distribution
                       ↓
          Temperature / Top-K / Top-P
                       ↓
                  Next Token
                       ↓
                    Repeat
```

---

# If You Remember Only This...

### 1.

**Tokens** turn text into pieces.

### 2.

**Embeddings** turn pieces into numbers.

### 3.

**Attention** finds relationships.

### 4.

**Softmax** turns scores into probabilities.

### 5.

**The model predicts the next token.**

### 6.

**Temperature controls how sharply we choose.**

### 7.

**Top-K and Top-P limit the choices.**

---

# Final Mental Model

Imagine the Transformer saying:

> "I have read these words."

↓

> "Which words are important to each other?"

↓

> "What should the next word probably be?"

↓

> "Here are the probabilities."

↓

> "How should I choose from them?"

↓

> **"Here is the next token."**

↓

Repeat.

---

# The Transformer in One Picture

```text
       Words
         ↓
      Tokens
         ↓
    Embeddings
         ↓
      Attention
         ↓
   Transformer
         ↓
       Logits
         ↓
      Softmax
         ↓
 Probability Distribution
         ↓
 Temperature / Top-K / Top-P
         ↓
     Next Token
         ↓
       Repeat
```

---

# Final Thought

<div class="text-3xl text-center mt-16">

### A Transformer is a machine for finding relationships.

<br>

### An LLM uses those relationships to predict what comes next.

<br>

### Generation parameters decide how we choose that next token.

</div>

---

# Questions?

## Thank You

### Let's explore the Transformer.
---