#!/usr/bin/env python3
"""
Authoritative source for every number in the Transformers deck.

    IF A SLIDE DISAGREES WITH THIS SCRIPT, THE SLIDE IS WRONG.

The same rule is restated in the header of every component under components/
and in README.md. `composables/useDeckNumbers.ts` is GENERATED from this file
(`python3 scripts/verify-attention.py --emit-ts`) and must never be hand-edited.

It re-derives, from scratch:

  1. The worked attention example  (Chapter 4 centrepiece)
     Three tokens from "The boy dropped the glass because it was slippery",
     d_model = 4, d_k = 2 -- chosen so every dot product is a two-term sum a
     student can check in their head. The punchline is that the row for "it"
     puts 0.85 of its attention on "glass", which answers the question the
     deck opens with, and that the resulting output vector for "it" is very
     nearly a copy of glass's value vector.

  2. The decoding distribution     (Chapters 5-6)
     ONE logit vector, from which the T=1 probabilities, every other
     temperature, the top-k cut and the top-p cut are all derived. The source
     draft stated logits and probabilities that were mutually inconsistent;
     these logits reproduce the draft's stated probabilities exactly.

  3. Softmax saturation            (the sqrt(d_k) justification)
  4. The Paris example, and the -log P loss table.
  5. Tokenizations, vocabulary sizes, special tokens (asserted vs tiktoken).
  6. A byte-pair-encoding merge trace on a toy corpus.
  7. Sinusoidal positional encoding, with a rotation property test.
  8. Multi-head attention (h = 2) on the worked example.
  9. Cross-attention: decoder queries over encoder keys/values.
 10. Layer normalisation.   11. Label smoothing.
 12. Shapes (measured by a real forward pass) and parameter count of the
     original base Transformer -- the backbone of the Part II deck.

Usage:
    python3 scripts/verify-attention.py            # print everything
    python3 scripts/verify-attention.py --torch    # cross-check vs PyTorch, float64
    python3 scripts/verify-attention.py --emit-ts  # regenerate useDeckNumbers.ts
"""

import argparse
import json
import math
import sys
from pathlib import Path

import numpy as np

np.set_printoptions(precision=4, suppress=True)

# --------------------------------------------------------------------------
# 1. The worked attention example
# --------------------------------------------------------------------------

TOKENS = ["glass", "dropped", "it"]

# Token representations AFTER embedding + positional information have been
# added -- the deck is explicit that these are already the sum of the two.
# Real embeddings are decimals with hundreds of entries; these are small whole
# numbers precisely so the arithmetic is checkable on the slide.
X = np.array([
    [0, 2, 0, 1],   # glass
    [1, 0, 1, 0],   # dropped
    [2, 0, 2, 1],   # it
], dtype=float)

# The three learned projection matrices. These are the PARAMETERS -- the only
# things training ever changes. d_model = 4 -> d_k = 2.
W_Q = np.array([[1, -1], [0, 0], [1, 0], [-1, 1]], dtype=float)
W_K = np.array([[0, 0], [1, 0], [0, -1], [-1, -1]], dtype=float)
W_V = np.array([[0, 0], [0, 0], [0, 1], [1, 1]], dtype=float)

D_K = W_Q.shape[1]


def softmax(z, axis=-1):
    z = np.asarray(z, dtype=float)
    z = z - np.max(z, axis=axis, keepdims=True)
    e = np.exp(z)
    return e / np.sum(e, axis=axis, keepdims=True)


def attention(mask_future=False):
    Q, K, V = X @ W_Q, X @ W_K, X @ W_V
    scores = Q @ K.T
    scaled = scores / math.sqrt(D_K)
    if mask_future:
        n = scaled.shape[0]
        scaled = np.where(np.triu(np.ones((n, n)), 1) > 0, -np.inf, scaled)
    weights = softmax(scaled)
    return Q, K, V, scores, scaled, weights, weights @ V


def report_worked_example():
    Q, K, V, scores, scaled, A, Z = attention()
    _, _, _, _, _, Ac, Zc = attention(mask_future=True)

    print("=" * 74)
    print("1. WORKED ATTENTION EXAMPLE  (Chapter 4)")
    print("=" * 74)
    print('   "The boy dropped the glass because it was slippery"')
    print(f"   tokens = {TOKENS}   d_model = {X.shape[1]}   d_k = {D_K}\n")

    for name, M in (("X (embedding + position)", X), ("W_Q", W_Q), ("W_K", W_K), ("W_V", W_V)):
        print(f"   {name}\n{_indent(M)}\n")

    print("   Q = X W_Q        K = X W_K        V = X W_V")
    for i, t in enumerate(TOKENS):
        print(f"     {t:<8} q={_vec(Q[i])}   k={_vec(K[i])}   v={_vec(V[i])}")

    print("\n   Scores  S = Q K^T           (every entry is a two-term dot product)")
    _matrix(scores, "%5.0f")
    print("\n   Hand-check the headline entry:")
    print(f"     q_it . k_glass = ({Q[2,0]:.0f})({K[0,0]:.0f}) + ({Q[2,1]:.0f})({K[0,1]:.0f})"
          f" = {Q[2,0]*K[0,0]:.0f} + {Q[2,1]*K[0,1]:.0f} = {scores[2,0]:.0f}")

    print(f"\n   Scaled  S / sqrt(d_k) = S / {math.sqrt(D_K):.4f}")
    _matrix(scaled, "%8.4f")
    print("\n   Attention weights  A = softmax(S / sqrt(d_k))   [rows sum to 1]")
    _matrix(A, "%8.4f")
    print(f"     row sums: {np.round(A.sum(axis=1), 10)}")

    print(f"\n   *** THE PAYOFF:  it -> glass = {A[2,0]:.4f}  ({A[2,0]*100:.0f}%) ***")
    print("       The question the deck opens with, answered by arithmetic.")

    print("\n   Output  Z = A V   (each row is a weighted blend of ALL value vectors)")
    for i, t in enumerate(TOKENS):
        print(f"     {t:<8} z={_vec(Z[i])}")
    print(f"\n   Compare z_it = {_vec(Z[2])}  with  v_glass = {_vec(V[0])}")
    print("       The vector for 'it' has become very nearly a copy of 'glass'.")
    print("       THIS is what attention is for.")

    print("\n   Causal mask applied (future scores set to -inf BEFORE softmax):")
    _matrix(Ac, "%8.4f")
    print(f"     row sums: {np.round(Ac.sum(axis=1), 10)}   <- still 1; that is why -inf, not 0")
    print("\n   Causal output Z:")
    for i, t in enumerate(TOKENS):
        print(f"     {t:<8} z={_vec(Zc[i])}")

    print("\n   Why not just set masked scores to zero? Because exp(0) = 1, so they")
    print("   would still take a share of the softmax and the row would not be a")
    print("   distribution over the visible tokens. exp(-inf) = 0 is what we want.")
    naive = softmax(np.where(np.triu(np.ones((3, 3)), 1) > 0, 0.0, scaled))
    print(f"     naive 'set to 0' row for glass: {np.round(naive[0], 4)}  <- leaks onto the future")


# --------------------------------------------------------------------------
# 2. The decoding distribution
# --------------------------------------------------------------------------

DECODE_TOKENS = ["blue", "clear", "dark", "green", "red"]
# Chosen so that softmax at T=1 reproduces the source draft's stated
# 0.80 / 0.10 / 0.05 / 0.03 / 0.02 -- which its own stated logits did not.
LOGITS = np.array([3.9, 1.8, 1.1, 0.6, 0.2])
TEMPERATURES = [0.2, 0.5, 1.0, 1.5, 2.0]
TOP_K = 3
TOP_P = 0.90


def report_decoding():
    print("\n" + "=" * 74)
    print("2. DECODING  (Chapters 5-6)   prompt: 'The sky is ___'")
    print("=" * 74)
    print("   ONE logit vector. Everything below is derived from it.\n")
    print("   logits: " + "  ".join(f"{t}={z}" for t, z in zip(DECODE_TOKENS, LOGITS)))

    print("\n   Temperature:  P_i = exp(z_i / T) / sum_j exp(z_j / T)")
    print(f"     {'T':>5}  " + "".join(f"{t:>9}" for t in DECODE_TOKENS))
    for T in TEMPERATURES:
        p = softmax(LOGITS / T)
        print(f"     {T:>5}  " + "".join(f"{v:>9.4f}" for v in p))
    print("\n     T = 0.2 is effectively [1, 0, 0, 0, 0]. That IS greedy decoding:")
    print("     as T -> 0 the distribution collapses onto the argmax. Use T = 0.5 /")
    print("     1.0 / 1.5 for the three-way comparison chart so all columns are legible.")

    p1 = softmax(LOGITS)
    order = np.argsort(-p1)

    print(f"\n   Top-K (K = {TOP_K}) -- keep a FIXED NUMBER of choices:")
    keep = order[:TOP_K]
    renorm = p1[keep] / p1[keep].sum()
    for idx, r in zip(keep, renorm):
        print(f"     {DECODE_TOKENS[idx]:<8} {p1[idx]:.4f}  ->  {r:.4f}   (renormalised)")
    print(f"     discarded: {', '.join(DECODE_TOKENS[i] for i in order[TOP_K:])}")

    print(f"\n   Top-P (P = {TOP_P}) -- keep ENOUGH choices to cover the mass:")
    cum = np.cumsum(p1[order])
    n_keep = int(np.searchsorted(cum, TOP_P) + 1)
    for rank, idx in enumerate(order):
        mark = "keep" if rank < n_keep else "drop"
        print(f"     {DECODE_TOKENS[idx]:<8} {p1[idx]:.4f}   cumulative {cum[rank]:.4f}   {mark}")
    print(f"     -> keeps {n_keep} tokens, covering {cum[n_keep-1]:.4f} of the probability.")
    print(f"\n   *** On the SAME distribution: Top-K={TOP_K} keeps 3, Top-P={TOP_P} keeps {n_keep}.")
    print("       That contrast is the Top-K vs Top-P slide. ***")

    flat = softmax(np.array([1.6, 1.3, 1.1, 0.9, 0.7, 0.4, 0.1, -0.3]))
    fcum = np.cumsum(np.sort(flat)[::-1])
    fkeep = int(np.searchsorted(fcum, TOP_P) + 1)
    print(f"\n   A FLATTER distribution ('write a funny story about a cat'):")
    print(f"     {np.round(flat, 4)}")
    print(f"     Top-P = {TOP_P} now keeps {fkeep} of {len(flat)} tokens -- it ADAPTS to the")
    print("     shape of the distribution. Top-K cannot. That is the whole point.")


# --------------------------------------------------------------------------
# 3. Softmax saturation -- why we divide by sqrt(d_k)
# --------------------------------------------------------------------------

SAT_BASE = np.array([0.1, -0.2, 0.3, -0.2, 0.5])
SAT_SCALE = 8


def report_saturation():
    print("\n" + "=" * 74)
    print("3. WHY DIVIDE BY sqrt(d_k)  (Chapter 4)")
    print("=" * 74)
    print(f"   softmax({SAT_BASE})")
    print(f"     = {np.round(softmax(SAT_BASE), 4)}          <- diffuse; every token contributes")
    print(f"   softmax({SAT_BASE} x {SAT_SCALE})")
    print(f"     = {np.round(softmax(SAT_BASE * SAT_SCALE), 4)}  <- peaky; collapses to one-hot")
    print("\n   Large dot products push softmax towards one-hot, and a one-hot")
    print("   attention row means each token reads from exactly one other token.")
    print("   Dividing by sqrt(d_k) keeps the scores in a range where softmax stays")
    print("   soft. This is not hand-waving: the two rows above are the argument.")


# --------------------------------------------------------------------------
# 4. Paris, and the loss table
# --------------------------------------------------------------------------

PARIS_TOKENS = ["Paris", "London", "Berlin", "Rome", "other"]
PARIS_PROBS = np.array([0.95, 0.01, 0.01, 0.01, 0.02])
LOSS_PROBS = [0.9, 0.5, 0.1, 0.01]


def report_misc():
    print("\n" + "=" * 74)
    print("4. PARIS, AND THE LOSS TABLE  (Chapters 5, 7)")
    print("=" * 74)
    print("   'What is the capital of France?'")
    for t, p in zip(PARIS_TOKENS, PARIS_PROBS):
        print(f"     {t:<8} {p:.2f}  {'#' * int(round(p * 40))}")
    print(f"     sum = {PARIS_PROBS.sum():.2f}")
    print("\n   Loss  L = -log P(correct)")
    print(f"     {'P(correct)':>12}  {'L':>8}")
    for p in LOSS_PROBS:
        print(f"     {p:>12.2f}  {-math.log(p):>8.4f}")
    print("\n   Confidently wrong is punished without limit: as P(correct) -> 0,")
    print("   L -> infinity. That asymmetry is why the logarithm is there.")


# --------------------------------------------------------------------------
# 5. Tokenization  (Chapter 1)
# --------------------------------------------------------------------------
# These are FROZEN, so the deck renders with or without tiktoken installed.
# When tiktoken IS installed the script ASSERTS them rather than regenerating
# them, so drift in a tokenizer version is caught rather than silently
# absorbed. Every one was measured, not remembered.

TOKEN_EXAMPLES = {
    "plain": {
        "encoding": "cl100k_base",
        "text": "The cat sat on the mat",
        "tokens": ["The", " cat", " sat", " on", " the", " mat"],
        "ids": [791, 8415, 7731, 389, 279, 5634],
    },
    "egg": {
        "encoding": "cl100k_base",
        "text": "Egg. I have an Egg. egg. EGG.",
        "tokens": ["E", "gg", ".", " I", " have", " an", " Egg", ".", " egg", ".", " E", "GG", "."],
        "ids": [36, 14736, 13, 358, 617, 459, 42313, 13, 19151, 13, 469, 23050, 13],
    },
    "arithmetic": {
        "encoding": "gpt2",
        "text": "127 + 677 = 804",
        "tokens": ["127", " +", " 6", "77", " =", " 8", "04"],
        "ids": [16799, 1343, 718, 3324, 796, 807, 3023],
    },
    "english": {
        "encoding": "gpt2",
        "text": "hello how are you",
        "tokens": ["hello", " how", " are", " you"],
        "ids": [31373, 703, 389, 345],
    },
    "korean": {
        "encoding": "gpt2",
        "text": "\uc548\ub155\ud558\uc138\uc694",
        "tokens": ["\ufffd"] * 14,
        "ids": [168, 243, 230, 167, 227, 243, 47991, 246, 168, 226, 116, 168, 248, 242],
    },
    "magikarp_gpt2": {
        "encoding": "gpt2",
        "text": "SolidGoldMagikarp",
        "tokens": ["Solid", "GoldMagikarp"],
        "ids": [46933, 42202],
    },
    "magikarp_gpt4": {
        "encoding": "cl100k_base",
        "text": "SolidGoldMagikarp",
        "tokens": ["Solid", "Gold", "Mag", "ik", "arp"],
        "ids": [47041, 26509, 34015, 1609, 8035],
    },
    "strawberry": {
        "encoding": "cl100k_base",
        "text": "strawberry",
        "tokens": ["str", "aw", "berry"],
        "ids": [496, 675, 15717],
    },
    "defaultcellstyle": {
        "encoding": "cl100k_base",
        "text": ".DefaultCellStyle",
        "tokens": [".DefaultCellStyle"],
        "ids": [98518],
    },
    "threeways": {
        "encoding": "cl100k_base",
        "text": "The teddy bears were reading",
        "tokens": ["The", " ted", "dy", " bears", " were", " reading"],
        "ids": [791, 42323, 10470, 30824, 1051, 5403],
    },
    "unbearable": {
        "encoding": "cl100k_base",
        "text": "unbearable",
        "tokens": ["un", "bear", "able"],
        "ids": [359, 68760, 481],
    },
}

# Vocabulary sizes and the end-of-text special token, also frozen + asserted.
VOCAB_SIZES = {"gpt2": 50257, "cl100k_base": 100277}
SPECIAL_EOT = {"gpt2": 50256, "cl100k_base": 100257}


def report_tokens():
    print("\n" + "=" * 74)
    print("5. TOKENIZATION  (Chapter 1)")
    print("=" * 74)
    try:
        import tiktoken
        live = True
    except ImportError:
        tiktoken = None
        live = False
        print("   tiktoken not installed - printing frozen values without re-checking.")
        print("   (pip install tiktoken to have this script verify them.)\n")

    bad = 0
    for name, ex in TOKEN_EXAMPLES.items():
        status = ""
        if live:
            enc = tiktoken.get_encoding(ex["encoding"])
            ids = enc.encode(ex["text"])
            ok = ids == ex["ids"]
            bad += 0 if ok else 1
            status = "  OK" if ok else f"  MISMATCH -> {ids}"
        n = len(ex["ids"])
        print(f"   {name:<18} [{ex['encoding']:<11}] {ex['text']!r}")
        print(f"   {'':<18} {n:>2} tokens  {ex['tokens']}{status}")

    for enc_name, size in VOCAB_SIZES.items():
        status = ""
        if live:
            enc = tiktoken.get_encoding(enc_name)
            eot = enc.encode("<|endoftext|>", allowed_special="all")
            ok = enc.n_vocab == size and eot == [SPECIAL_EOT[enc_name]]
            bad += 0 if ok else 1
            status = "  OK" if ok else f"  MISMATCH -> n_vocab={enc.n_vocab} eot={eot}"
        print(f"   vocab {enc_name:<12} {size:>7} entries   <|endoftext|> = {SPECIAL_EOT[enc_name]}{status}")

    tw = TOKEN_EXAMPLES["threeways"]["text"]
    print(f"\n   Three ways to cut {tw!r}:")
    print(f"     word-level  {len(tw.split()):>2} tokens  {tw.split()}")
    print(f"     char-level  {len(tw):>2} tokens  (spaces count)")
    print(f"     subword     {len(TOKEN_EXAMPLES['threeways']['ids']):>2} tokens  {TOKEN_EXAMPLES['threeways']['tokens']}")

    eng = len(TOKEN_EXAMPLES["english"]["ids"])
    kor = len(TOKEN_EXAMPLES["korean"]["ids"])
    print(f"\n   Equity: the same greeting costs {eng} tokens in English and {kor} in Korean")
    print(f"   under GPT-2 - a {kor / eng:.1f}x tax, paid by the speaker, in money and in")
    print("   context length. Tokenizers are trained mostly on English text.")
    print("\n   'strawberry' is str|aw|berry. The model was never shown the letters,")
    print("   so 'how many r's' is a question about something it cannot see.")
    return bad


# --------------------------------------------------------------------------
# 6. Byte-pair encoding, by hand  (Chapter 1)
# --------------------------------------------------------------------------
# A toy corpus small enough to count on a slide. Each word starts as single
# characters; every step merges the most frequent adjacent pair everywhere.
# Ties are broken alphabetically so the trace is deterministic -- real
# tokenizers break ties by their own rules, which is a detail, not the idea.

BPE_CORPUS = {"read": 4, "reading": 3, "bear": 4, "bears": 2, "ring": 2, "sing": 3}
BPE_MERGES = 7
BPE_UNSEEN = ["bearing", "rings"]   # never in the corpus; tokenized by replaying merges
BPE_EXPECTED = ["ea", "in", "ing", "ead", "read", "bea", "bear"]


def _bpe_merge(symbols, pair):
    a, b = pair
    out, i = [], 0
    while i < len(symbols):
        if i < len(symbols) - 1 and symbols[i] == a and symbols[i + 1] == b:
            out.append(a + b)
            i += 2
        else:
            out.append(symbols[i])
            i += 1
    return out


def bpe_trace():
    words = {w: list(w) for w in BPE_CORPUS}
    steps = []
    for _ in range(BPE_MERGES):
        counts = {}
        for w, f in BPE_CORPUS.items():
            s = words[w]
            for pair in zip(s, s[1:]):
                counts[pair] = counts.get(pair, 0) + f
        ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
        pair, count = ranked[0]
        words = {w: _bpe_merge(s, pair) for w, s in words.items()}
        steps.append({
            "pair": list(pair),
            "merged": pair[0] + pair[1],
            "count": count,
            "top": [["".join(p), c] for p, c in ranked[:4]],
            "words": {w: list(s) for w, s in words.items()},
        })
    unseen = {}
    for w in BPE_UNSEEN:
        s = list(w)
        for st in steps:
            s = _bpe_merge(s, tuple(st["pair"]))
        unseen[w] = s
    return steps, unseen


def report_bpe():
    print("\n" + "=" * 74)
    print("6. BYTE-PAIR ENCODING BY HAND  (Chapter 1)")
    print("=" * 74)
    print("   corpus (word: count): " + ", ".join(f"{w}:{c}" for w, c in BPE_CORPUS.items()))
    steps, unseen = bpe_trace()
    for i, st in enumerate(steps, 1):
        top = "  ".join(f"{p}={c}" for p, c in st["top"])
        print(f"   step {i}: merge {st['pair'][0]!r}+{st['pair'][1]!r} -> {st['merged']!r:<8}"
              f" (seen {st['count']}x)   top pairs: {top}")
    print("\n   after all merges:")
    for w, s in steps[-1]["words"].items():
        print(f"     {w:<8} {' | '.join(s)}")
    print("\n   words the tokenizer NEVER saw, replaying the merges in order:")
    for w, s in unseen.items():
        print(f"     {w:<8} {' | '.join(s)}   <- no <UNK> needed")
    got = [st["merged"] for st in steps]
    ok = got == BPE_EXPECTED
    print(f"\n   merge order {got}  {'OK' if ok else 'MISMATCH vs ' + str(BPE_EXPECTED)}")
    return 0 if ok else 1


# --------------------------------------------------------------------------
# 7. Sinusoidal positional encoding  (Part II, Chapter 2)
# --------------------------------------------------------------------------

PE_STRIP_POSITIONS, PE_STRIP_DIM = 24, 16   # the heat strip on the slide
PE_CURVE_DIM, PE_CURVE_LEN, PE_CURVE_REF = 512, 41, 20   # the similarity curve


def sinusoidal_pe(n_pos, d):
    pos = np.arange(n_pos)[:, None]
    i = np.arange(d // 2)[None, :]
    angle = pos / (10000 ** (2 * i / d))
    pe = np.zeros((n_pos, d))
    pe[:, 0::2] = np.sin(angle)
    pe[:, 1::2] = np.cos(angle)
    return pe


def report_posenc():
    print("\n" + "=" * 74)
    print("7. SINUSOIDAL POSITIONAL ENCODING  (Part II, Chapter 2)")
    print("=" * 74)
    print("   PE[pos, 2i] = sin(pos / 10000^(2i/d))     PE[pos, 2i+1] = cos(same)")
    d = PE_STRIP_DIM
    periods = 2 * np.pi * 10000 ** (2 * np.arange(d // 2) / d)
    print(f"   d = {d}: each sin/cos pair is one clock hand. Periods (positions per turn):")
    print("     " + "  ".join(f"{p:,.1f}" for p in periods))
    pe = sinusoidal_pe(PE_STRIP_POSITIONS, d)
    print("   first rows (pos x dim), 2 d.p.:")
    for p in range(4):
        print(f"     pos {p}: {np.round(pe[p, :8], 2)} ...")

    # Property test: a shift by k is the same rotation for every position.
    failures = 0
    for k in (1, 3, 7):
        R = np.zeros((d, d))
        for i in range(d // 2):
            w = 1 / 10000 ** (2 * i / d)
            c, s = math.cos(w * k), math.sin(w * k)
            R[2 * i:2 * i + 2, 2 * i:2 * i + 2] = [[c, -s], [s, c]]
        delta = np.abs(pe[:-k] @ R - pe[k:]).max()
        ok = delta < 1e-12
        failures += 0 if ok else 1
        print(f"   PE(pos+{k}) == PE(pos) @ R_{k} for every pos: max|delta| = {delta:.1e}  {'OK' if ok else 'MISMATCH'}")

    big = sinusoidal_pe(PE_CURVE_LEN, PE_CURVE_DIM)
    sim = big @ big[PE_CURVE_REF] / (PE_CURVE_DIM / 2)
    print(f"\n   d = {PE_CURVE_DIM}: similarity of position {PE_CURVE_REF} to its neighbours (1 = identical):")
    for off in (0, 1, 2, 5, 10, 20):
        print(f"     distance {off:>2}: {sim[PE_CURVE_REF + off]:.2f}")
    print("   Nearby positions look alike; far ones look different. No position is learned,")
    print("   so the formula still produces a vector for a position never seen in training.")
    return failures


# --------------------------------------------------------------------------
# 8. Multi-head attention on the worked example  (Chapter 4, Part II Ch 3)
# --------------------------------------------------------------------------
# Head 1 is the Chapter 4 head (W_Q, W_K, W_V above): the pronoun head.
# Head 2 is a second, different set of weights in which every token looks at
# the verb. Same input X, same arithmetic, different question.

W_Q2 = np.array([[0, 0], [1, 0], [1, 0], [0, 0]], dtype=float)
W_K2 = np.array([[1, 0], [0, 0], [0, 0], [-2, 0]], dtype=float)
W_V2 = np.array([[1, 0], [0, 1], [0, 0], [0, 0]], dtype=float)
# Output projection: blends the two heads back into d_model = 4.
W_O = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, -1, 0], [0, 1, 0, -1]], dtype=float)


def _head(Wq, Wk, Wv, Xq, Xkv=None, causal=False):
    Xkv = Xq if Xkv is None else Xkv
    Q, K, V = Xq @ Wq, Xkv @ Wk, Xkv @ Wv
    S = Q @ K.T / math.sqrt(Wq.shape[1])
    if causal:
        S = np.where(np.triu(np.ones(S.shape), 1) > 0, -np.inf, S)
    A = softmax(S)
    return Q, K, V, S, A, A @ V


def multihead():
    h1 = _head(W_Q, W_K, W_V, X)
    h2 = _head(W_Q2, W_K2, W_V2, X)
    concat = np.concatenate([h1[5], h2[5]], axis=1)
    return h1, h2, concat, concat @ W_O


def report_multihead():
    print("\n" + "=" * 74)
    print("8. MULTI-HEAD ATTENTION, h = 2  (Chapter 4 / Part II Chapter 3)")
    print("=" * 74)
    h1, h2, concat, out = multihead()
    print(f"   d_model = {X.shape[1]}, h = 2, d_k = d_model / h = {X.shape[1] // 2}")
    print("   head 1 weights (the Chapter 4 head -- 'what does it refer to?'):")
    _matrix(h1[4], "%8.4f")
    print("   head 2 weights (a different head -- every token looks at the verb):")
    _matrix(h2[4], "%8.4f")
    print(f"\n   concat [head1 | head2]  shape {concat.shape}")
    for i, t in enumerate(TOKENS):
        print(f"     {t:<8} {_vec(np.round(concat[i], 4))}")
    print(f"   times W_O (4x4)  ->  output shape {out.shape}  (back to d_model)")
    for i, t in enumerate(TOKENS):
        print(f"     {t:<8} {_vec(np.round(out[i], 4))}")
    return 0


# --------------------------------------------------------------------------
# 9. Cross-attention  (Part II, Chapter 5)
# --------------------------------------------------------------------------
# Already-projected toy vectors, d_k = 2. The encoder has read "the cat sleeps";
# the decoder has written "<BOS> le" and must now produce "chat".

CROSS_ENC_TOKENS = ["the", "cat", "sleeps"]
CROSS_DEC_TOKENS = ["<BOS>", "le"]
CROSS_Q = np.array([[1, 0], [0, 2]], dtype=float)            # from the DECODER
CROSS_K = np.array([[2, 0], [0, 2], [-1, 1]], dtype=float)   # from the ENCODER
CROSS_V = np.array([[1, 0], [0, 1], [1, 1]], dtype=float)    # from the ENCODER


def cross_attention():
    S = CROSS_Q @ CROSS_K.T
    scaled = S / math.sqrt(CROSS_Q.shape[1])
    A = softmax(scaled)
    return S, scaled, A, A @ CROSS_V


def report_crossattn():
    print("\n" + "=" * 74)
    print("9. CROSS-ATTENTION  (Part II, Chapter 5)")
    print("=" * 74)
    S, scaled, A, Z = cross_attention()
    print(f"   queries from the decoder {CROSS_DEC_TOKENS}, keys/values from the encoder {CROSS_ENC_TOKENS}")
    print(f"   score matrix is {S.shape[0]} x {S.shape[1]}  (decoder length x encoder length, NOT square)")
    print("   raw scores:")
    for i, t in enumerate(CROSS_DEC_TOKENS):
        print(f"     {t:<6} {_vec(S[i])}")
    print("   weights (softmax of scores / sqrt 2):")
    for i, t in enumerate(CROSS_DEC_TOKENS):
        print(f"     {t:<6} {_vec(np.round(A[i], 4))}")
    print(f"\n   *** 'le' puts {A[1, 1]:.2f} of its attention on 'cat' -- the word it must translate next.")
    return 0


# --------------------------------------------------------------------------
# 10. Layer normalisation  (Chapter 7, Part II Chapter 7)
# --------------------------------------------------------------------------

LN_X = np.array([20, 40, 40, 100], dtype=float)
LN_EPS = 1e-5   # PyTorch's default, so the cross-check is exact


def layernorm(x, gamma=1.0, beta=0.0, eps=LN_EPS):
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    return gamma * (x - mu) / np.sqrt(var + eps) + beta


def report_layernorm():
    print("\n" + "=" * 74)
    print("10. LAYER NORMALISATION  (Chapter 7)")
    print("=" * 74)
    mu, sd = LN_X.mean(), LN_X.std()
    y = layernorm(LN_X)
    print(f"   x = {_vec(LN_X)}   mean = {mu:g}   std = {sd:g}")
    print(f"   (x - mean) / std = {_vec(np.round(y, 2))}")
    print(f"   new mean = {y.mean():.1e}   new std = {y.std():.4f}")
    print("   Then a learned scale (gamma) and shift (beta) per dimension; at init 1 and 0.")
    print("   Same shape, sensible size -- whatever the previous layer did to the scale.")
    return 0


# --------------------------------------------------------------------------
# 11. Label smoothing  (Part II, Chapter 7)
# --------------------------------------------------------------------------

SMOOTH_EPS = 0.1
SMOOTH_CORRECT = 0   # "blue" in DECODE_TOKENS


def smoothing_targets():
    K = len(DECODE_TOKENS)
    hard = np.zeros(K)
    hard[SMOOTH_CORRECT] = 1.0
    paper = np.full(K, SMOOTH_EPS / (K - 1))       # Vaswani et al.: eps over the OTHER classes
    paper[SMOOTH_CORRECT] = 1 - SMOOTH_EPS
    torch_style = (1 - SMOOTH_EPS) * hard + SMOOTH_EPS / K   # PyTorch: eps over ALL classes
    return hard, paper, torch_style


def report_smoothing():
    print("\n" + "=" * 74)
    print("11. LABEL SMOOTHING  (Part II, Chapter 7)")
    print("=" * 74)
    hard, paper, torch_style = smoothing_targets()
    logp = np.log(softmax(LOGITS))
    print(f"   eps = {SMOOTH_EPS}, correct token = {DECODE_TOKENS[SMOOTH_CORRECT]!r}, K = {len(hard)}")
    print(f"   hard target            {_vec(hard)}")
    print(f"   smoothed (paper)       {_vec(np.round(paper, 4))}")
    print(f"   smoothed (PyTorch)     {_vec(np.round(torch_style, 4))}")
    print(f"\n   model's T=1 distribution {_vec(np.round(softmax(LOGITS), 4))}")
    print(f"   loss vs hard target     {-(hard * logp).sum():.4f}")
    print(f"   loss vs smoothed target {-(paper * logp).sum():.4f}")
    print("   With a hard target the loss only reaches 0 at 100% confidence; with a smoothed")
    print("   target, 100% confidence is penalised. Many continuations are acceptable.")
    return 0


# Part II, Chapter 1: a signal passed back through k recurrent steps gets
# multiplied by (roughly) the same factor each time. Below 1 it vanishes,
# above 1 it explodes. Pure arithmetic, but kept here so the slide has a source.
VANISH_STEPS = 10


# --------------------------------------------------------------------------
# 12. Shapes and parameters of the original base Transformer  (Part II)
# --------------------------------------------------------------------------
# Shapes are MEASURED by running an actual forward pass with random weights
# at the paper's base dimensions -- not written down from memory. The same
# layer weights are reused for all N layers; that changes no shape.

BASE = {"d_model": 512, "h": 8, "d_k": 64, "d_ff": 2048, "N": 6, "vocab": 37000}
SRC_TOKENS = ["A", "cute", "teddy", "bear", "is", "reading", "."]
TGT_TOKENS = ["Un", "ours", "en", "peluche", "mignon", "lit", "."]


def _param_spec():
    d, f = BASE["d_model"], BASE["d_ff"]
    mha = {"W_Q": (d, d), "W_K": (d, d), "W_V": (d, d), "W_O": (d, d),
           "b_Q": (d,), "b_K": (d,), "b_V": (d,), "b_O": (d,)}
    ffn = {"W_1": (d, f), "b_1": (f,), "W_2": (f, d), "b_2": (d,)}
    ln = {"gamma": (d,), "beta": (d,)}
    return mha, ffn, ln


def parameter_count():
    mha, ffn, ln = _param_spec()
    size = lambda spec: sum(int(np.prod(s)) for s in spec.values())
    N = BASE["N"]
    parts = {
        "embeddings": BASE["vocab"] * BASE["d_model"],   # shared: source, target, output
        "attention": N * size(mha) + N * 2 * size(mha),  # encoder self + decoder self & cross
        "ffn": N * size(ffn) + N * size(ffn),
        "layernorm": N * 2 * size(ln) + N * 3 * size(ln),
    }
    parts["total"] = sum(parts.values())
    return parts


def shape_trace():
    rng = np.random.default_rng(0)
    d, h, dk, N, V = BASE["d_model"], BASE["h"], BASE["d_k"], BASE["N"], BASE["vocab"]
    mha_s, ffn_s, ln_s = _param_spec()
    init = lambda spec: {k: rng.standard_normal(s).astype(np.float32) * 0.02 for k, s in spec.items()}
    enc_attn, dec_self, dec_cross = init(mha_s), init(mha_s), init(mha_s)
    ffn_w = init(ffn_s)
    E = rng.standard_normal((V, d)).astype(np.float32) * 0.02
    trace = []
    log = lambda stage, name, a, note: trace.append(
        {"stage": stage, "tensor": name, "shape": list(a.shape), "note": note})

    def mha(xq, xkv, W, causal, tag):
        Q = xq @ W["W_Q"] + W["b_Q"]
        K = xkv @ W["W_K"] + W["b_K"]
        Vv = xkv @ W["W_V"] + W["b_V"]
        Qh = Q.reshape(len(xq), h, dk).transpose(1, 0, 2)
        Kh = K.reshape(len(xkv), h, dk).transpose(1, 0, 2)
        Vh = Vv.reshape(len(xkv), h, dk).transpose(1, 0, 2)
        S = Qh @ Kh.transpose(0, 2, 1) / math.sqrt(dk)
        if causal:
            S = np.where(np.triu(np.ones(S.shape[1:]), 1) > 0, -np.inf, S)
        A = softmax(S)
        heads = A @ Vh
        concat = heads.transpose(1, 0, 2).reshape(len(xq), h * dk)
        if tag:
            log(tag, "Q (one head)", Qh[0], "rows = tokens asking")
            log(tag, "K (one head)", Kh[0], "rows = tokens being asked")
            log(tag, "scores per head", S, "h x queries x keys")
            log(tag, "concat heads", concat, "h * d_k = d_model")
        return concat @ W["W_O"] + W["b_O"]

    ffn = lambda x: np.maximum(0, x @ ffn_w["W_1"] + ffn_w["b_1"]) @ ffn_w["W_2"] + ffn_w["b_2"]
    pe = lambda n: sinusoidal_pe(n, d).astype(np.float32)

    src_ids = np.arange(len(SRC_TOKENS))
    log("encoder", "source token ids", src_ids, f"{len(SRC_TOKENS)} source tokens")
    x = E[src_ids] * math.sqrt(d) + pe(len(src_ids))
    log("encoder", "embedding + position", x, "one row per token")
    for layer in range(N):
        tag = "encoder self-attention" if layer == 0 else None
        x = layernorm(x + mha(x, x, enc_attn, False, tag))
        if layer == 0:
            hid = np.maximum(0, x @ ffn_w["W_1"] + ffn_w["b_1"])
            log("encoder", "FFN hidden", hid, "expanded 4x")
        x = layernorm(x + ffn(x))
    memory = x
    log("encoder", f"encoder output (after {N} layers)", memory, "context-aware source")

    tgt_in = np.arange(len(TGT_TOKENS) + 1)   # <BOS> + every target token (training view)
    y = E[tgt_in] * math.sqrt(d) + pe(len(tgt_in))
    log("decoder", "<BOS> + target so far", y, "teacher forcing during training")
    for layer in range(N):
        y = layernorm(y + mha(y, y, dec_self, True, "decoder masked self-attention" if layer == 0 else None))
        y = layernorm(y + mha(y, memory, dec_cross, False, "cross-attention" if layer == 0 else None))
        y = layernorm(y + ffn(y))
    log("decoder", f"decoder output (after {N} layers)", y, "one row per position")
    logits = y @ E.T
    log("output", "logits", logits, "one score per vocabulary entry")
    probs = softmax(logits)
    log("output", "probabilities", probs, "each row sums to 1")
    assert np.allclose(probs.sum(-1), 1, atol=1e-5)
    return trace


def report_shapes():
    print("\n" + "=" * 74)
    print("12. THE BASE TRANSFORMER: SHAPES AND PARAMETERS  (Part II)")
    print("=" * 74)
    print("   " + "  ".join(f"{k}={v}" for k, v in BASE.items()))
    print(f"   source: {SRC_TOKENS}")
    print(f"   target: {TGT_TOKENS}\n")
    for row in shape_trace():
        shape = " x ".join(str(s) for s in row["shape"])
        print(f"   [{row['stage']:<30}] {row['tensor']:<34} {shape:<14} {row['note']}")
    p = parameter_count()
    print("\n   parameters (embeddings shared between source, target and output):")
    for k, v in p.items():
        share = f"{100 * v / p['total']:5.1f}%" if k != "total" else ""
        print(f"     {k:<11} {v:>12,}  {share}")
    lo, hi = 60_000_000, 66_000_000
    ok = lo < p["total"] < hi
    print(f"   total ~{p['total'] / 1e6:.0f}M; the paper reports 65M for 'base'. {'OK' if ok else 'OUT OF RANGE'}")
    return 0 if ok else 1


# --------------------------------------------------------------------------
# PyTorch cross-check
# --------------------------------------------------------------------------

def cross_check_torch():
    try:
        import torch
        import torch.nn.functional as F
    except ImportError:
        print("\n[--torch] PyTorch is not installed; skipping cross-check.", file=sys.stderr)
        return 0

    print("\n" + "=" * 74)
    print("CROSS-CHECK vs PyTorch (float64)")
    print("=" * 74)

    t = lambda a: torch.tensor(a, dtype=torch.float64)
    Xt, Qt, Kt, Vt = t(X), t(X @ W_Q), t(X @ W_K), t(X @ W_V)
    failures = 0

    for label, is_causal in (("unmasked", False), ("causal  ", True)):
        ours = attention(mask_future=is_causal)[6]
        theirs = F.scaled_dot_product_attention(Qt, Kt, Vt, is_causal=is_causal).numpy()
        delta = np.abs(ours - theirs).max()
        ok = delta < 1e-12
        failures += 0 if ok else 1
        print(f"  attention output ({label}): max|delta| = {delta:.3e}   {'OK' if ok else 'MISMATCH'}")

    for T in TEMPERATURES:
        ours = softmax(LOGITS / T)
        theirs = F.softmax(t(LOGITS) / T, dim=-1).numpy()
        delta = np.abs(ours - theirs).max()
        ok = delta < 1e-12
        failures += 0 if ok else 1
        print(f"  softmax at T={T:<4}       : max|delta| = {delta:.3e}   {'OK' if ok else 'MISMATCH'}")

    def check(label, ours, theirs):
        nonlocal failures
        delta = np.abs(np.asarray(ours) - np.asarray(theirs)).max()
        ok = delta < 1e-12
        failures += 0 if ok else 1
        print(f"  {label:<25}: max|delta| = {delta:.3e}   {'OK' if ok else 'MISMATCH'}")

    # Multi-head: load our per-head matrices into nn.MultiheadAttention.
    # PyTorch computes x @ W.T, and splits the projected d_model into heads in
    # order, so the input weight is [head1 | head2] transposed.
    mha = torch.nn.MultiheadAttention(embed_dim=4, num_heads=2, bias=False,
                                      batch_first=True, dtype=torch.float64)
    with torch.no_grad():
        wq = np.concatenate([W_Q, W_Q2], axis=1).T
        wk = np.concatenate([W_K, W_K2], axis=1).T
        wv = np.concatenate([W_V, W_V2], axis=1).T
        mha.in_proj_weight.copy_(t(np.concatenate([wq, wk, wv], axis=0)))
        mha.out_proj.weight.copy_(t(W_O.T))
        theirs, _ = mha(Xt[None], Xt[None], Xt[None])
    check("multi-head output (h=2)", multihead()[3], theirs[0].numpy())

    S, scaled, A, Z = cross_attention()
    theirs = F.scaled_dot_product_attention(t(CROSS_Q), t(CROSS_K), t(CROSS_V)).numpy()
    check("cross-attention output", Z, theirs)

    check("layer norm", layernorm(LN_X),
          F.layer_norm(t(LN_X), (len(LN_X),), eps=LN_EPS).numpy())

    _, _, torch_style = smoothing_targets()
    logp = np.log(softmax(LOGITS))
    theirs = F.cross_entropy(t(LOGITS)[None], torch.tensor([SMOOTH_CORRECT]),
                             label_smoothing=SMOOTH_EPS).item()
    check("label-smoothed loss", -(torch_style * logp).sum(), theirs)

    print("\n  " + ("All PyTorch cross-checks passed." if not failures
                    else f"{failures} MISMATCH(ES) -- do not ship."))
    return failures


# --------------------------------------------------------------------------
# TypeScript emission
# --------------------------------------------------------------------------

def emit_ts(path: Path):
    Q, K, V, scores, scaled, A, Z = attention()
    _, _, _, _, _, Ac, Zc = attention(mask_future=True)
    p1 = softmax(LOGITS)
    order = np.argsort(-p1)
    cum = np.cumsum(p1[order])
    n_keep = int(np.searchsorted(cum, TOP_P) + 1)
    keep = order[:TOP_K]

    r = lambda a, n=4: np.round(np.asarray(a, dtype=float), n).tolist()

    bpe_steps, bpe_unseen = bpe_trace()
    pe_big = sinusoidal_pe(PE_CURVE_LEN, PE_CURVE_DIM)
    h1, h2, mh_concat, mh_out = multihead()
    cS, cScaled, cA, cZ = cross_attention()
    s_hard, s_paper, s_torch = smoothing_targets()
    logp1 = np.log(p1)

    data = {
        "worked": {
            "tokens": TOKENS,
            "dModel": int(X.shape[1]),
            "dK": int(D_K),
            "sqrtDK": round(math.sqrt(D_K), 4),
            "x": r(X, 0), "wQ": r(W_Q, 0), "wK": r(W_K, 0), "wV": r(W_V, 0),
            "q": r(Q, 0), "k": r(K, 0), "v": r(V, 0),
            "scores": r(scores, 0),
            "scaled": r(scaled),
            "weights": r(A),
            "output": r(Z),
            "causalWeights": r(np.where(np.isfinite(Ac), Ac, 0.0)),
            "causalOutput": r(Zc),
            "headline": {"query": "it", "key": "glass", "weight": round(float(A[2, 0]), 4)},
        },
        "decode": {
            "tokens": DECODE_TOKENS,
            "logits": r(LOGITS, 1),
            "byTemperature": {str(T): r(softmax(LOGITS / T)) for T in TEMPERATURES},
            "topK": {
                "k": TOP_K,
                "kept": [DECODE_TOKENS[i] for i in keep],
                "renormalised": r(p1[keep] / p1[keep].sum()),
            },
            "topP": {
                "p": TOP_P,
                "cumulative": r(cum),
                "keptCount": n_keep,
                "kept": [DECODE_TOKENS[i] for i in order[:n_keep]],
                "mass": round(float(cum[n_keep - 1]), 4),
            },
        },
        "saturation": {
            "input": r(SAT_BASE, 1),
            "scale": SAT_SCALE,
            "soft": r(softmax(SAT_BASE)),
            "peaky": r(softmax(SAT_BASE * SAT_SCALE)),
        },
        "paris": {"tokens": PARIS_TOKENS, "probs": r(PARIS_PROBS, 2)},
        "loss": [[p, round(-math.log(p), 4)] for p in LOSS_PROBS],
        "tokens": TOKEN_EXAMPLES,
        "vocab": {"sizes": VOCAB_SIZES, "endOfText": SPECIAL_EOT},
        "bpe": {"corpus": BPE_CORPUS, "steps": bpe_steps, "unseen": bpe_unseen},
        "posenc": {
            "dim": PE_STRIP_DIM,
            "strip": r(sinusoidal_pe(PE_STRIP_POSITIONS, PE_STRIP_DIM), 3),
            "periods": r(2 * np.pi * 10000 ** (2 * np.arange(PE_STRIP_DIM // 2) / PE_STRIP_DIM), 1),
            "curve": {"dim": PE_CURVE_DIM, "ref": PE_CURVE_REF,
                      "similarity": r(pe_big @ pe_big[PE_CURVE_REF] / (PE_CURVE_DIM / 2), 3)},
        },
        "multihead": {
            "h": 2,
            "dK": int(D_K),
            "wQ2": r(W_Q2, 0), "wK2": r(W_K2, 0), "wV2": r(W_V2, 0), "wO": r(W_O, 0),
            "head1": {"weights": r(h1[4]), "output": r(h1[5])},
            "head2": {"q": r(h2[0], 0), "k": r(h2[1], 0), "v": r(h2[2], 0),
                      "scores": r(h2[3] * math.sqrt(D_K), 0),
                      "weights": r(h2[4]), "output": r(h2[5])},
            "concat": r(mh_concat),
            "output": r(mh_out),
        },
        "crossattn": {
            "encTokens": CROSS_ENC_TOKENS, "decTokens": CROSS_DEC_TOKENS,
            "q": r(CROSS_Q, 0), "k": r(CROSS_K, 0), "v": r(CROSS_V, 0),
            "scores": r(cS, 0), "scaled": r(cScaled), "weights": r(cA), "output": r(cZ),
        },
        "layernorm": {
            "x": r(LN_X, 0), "mean": float(LN_X.mean()), "std": round(float(LN_X.std()), 4),
            "y": r(layernorm(LN_X), 2),
        },
        "smoothing": {
            "eps": SMOOTH_EPS, "tokens": DECODE_TOKENS,
            "hard": r(s_hard, 0), "paper": r(s_paper), "torch": r(s_torch),
            "lossHard": round(float(-(s_hard * logp1).sum()), 4),
            "lossSmoothed": round(float(-(s_paper * logp1).sum()), 4),
        },
        "vanishing": {
            "steps": VANISH_STEPS,
            "shrink": {"factor": 0.5, "values": [round(0.5 ** k, 6) for k in range(VANISH_STEPS + 1)]},
            "grow": {"factor": 1.5, "values": [round(1.5 ** k, 3) for k in range(VANISH_STEPS + 1)]},
        },
        "base": {
            "dims": BASE, "src": SRC_TOKENS, "tgt": TGT_TOKENS,
            "trace": shape_trace(),
            "params": parameter_count(),
        },
    }

    body = json.dumps(data, indent=2)
    path.write_text(
        "// GENERATED FILE -- DO NOT EDIT BY HAND.\n"
        "// Regenerate with:  python3 scripts/verify-attention.py --emit-ts\n"
        "//\n"
        "// Every number in the deck lives here, and every component imports it from\n"
        "// here, so the deck has exactly one source of truth. If a slide disagrees\n"
        "// with scripts/verify-attention.py, THE SLIDE IS WRONG.\n\n"
        f"export const N = {body} as const\n\n"
        "export function useDeckNumbers() {\n  return N\n}\n",
        encoding="utf-8",
    )
    print(f"wrote {path}")


# --------------------------------------------------------------------------

def _indent(M, fmt="%5.0f"):
    return "\n".join("     " + "  ".join(fmt % v for v in row) for row in M)


def _matrix(M, fmt):
    head = "            " + "".join(f"{t:>9}" for t in TOKENS)
    print(head)
    for i, t in enumerate(TOKENS):
        cells = "".join(f"{(fmt % v).rjust(9)}" for v in M[i])
        print(f"     {t:<7}{cells}")


def _vec(v):
    return "[" + ", ".join(f"{x:g}" for x in v) + "]"


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--torch", action="store_true", help="cross-check against PyTorch in float64")
    ap.add_argument("--emit-ts", action="store_true", help="regenerate composables/useDeckNumbers.ts")
    args = ap.parse_args()

    report_worked_example()
    report_decoding()
    report_saturation()
    report_misc()
    failures = report_tokens()
    failures += report_bpe()
    failures += report_posenc()
    failures += report_multihead()
    failures += report_crossattn()
    failures += report_layernorm()
    failures += report_smoothing()
    failures += report_shapes()

    failures += cross_check_torch() if args.torch else 0

    if args.emit_ts:
        emit_ts(Path(__file__).resolve().parent.parent / "composables" / "useDeckNumbers.ts")

    print("\n" + "=" * 74)
    print("Remember: if a slide disagrees with this script, the SLIDE is wrong.")
    print("=" * 74)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
