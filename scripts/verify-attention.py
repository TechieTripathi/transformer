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
}


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

    eng = len(TOKEN_EXAMPLES["english"]["ids"])
    kor = len(TOKEN_EXAMPLES["korean"]["ids"])
    print(f"\n   Equity: the same greeting costs {eng} tokens in English and {kor} in Korean")
    print(f"   under GPT-2 - a {kor / eng:.1f}x tax, paid by the speaker, in money and in")
    print("   context length. Tokenizers are trained mostly on English text.")
    print("\n   'strawberry' is str|aw|berry. The model was never shown the letters,")
    print("   so 'how many r's' is a question about something it cannot see.")
    return bad


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

    failures += cross_check_torch() if args.torch else 0

    if args.emit_ts:
        emit_ts(Path(__file__).resolve().parent.parent / "composables" / "useDeckNumbers.ts")

    print("\n" + "=" * 74)
    print("Remember: if a slide disagrees with this script, the SLIDE is wrong.")
    print("=" * 74)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
