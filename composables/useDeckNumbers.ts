// GENERATED FILE -- DO NOT EDIT BY HAND.
// Regenerate with:  python3 scripts/verify-attention.py --emit-ts
//
// Every number in the deck lives here, and every component imports it from
// here, so the deck has exactly one source of truth. If a slide disagrees
// with scripts/verify-attention.py, THE SLIDE IS WRONG.

export const N = {
  "worked": {
    "tokens": [
      "glass",
      "dropped",
      "it"
    ],
    "dModel": 4,
    "dK": 2,
    "sqrtDK": 1.4142,
    "x": [
      [
        0.0,
        2.0,
        0.0,
        1.0
      ],
      [
        1.0,
        0.0,
        1.0,
        0.0
      ],
      [
        2.0,
        0.0,
        2.0,
        1.0
      ]
    ],
    "wQ": [
      [
        1.0,
        -1.0
      ],
      [
        0.0,
        0.0
      ],
      [
        1.0,
        0.0
      ],
      [
        -1.0,
        1.0
      ]
    ],
    "wK": [
      [
        0.0,
        0.0
      ],
      [
        1.0,
        0.0
      ],
      [
        0.0,
        -1.0
      ],
      [
        -1.0,
        -1.0
      ]
    ],
    "wV": [
      [
        0.0,
        0.0
      ],
      [
        0.0,
        0.0
      ],
      [
        0.0,
        1.0
      ],
      [
        1.0,
        1.0
      ]
    ],
    "q": [
      [
        -1.0,
        1.0
      ],
      [
        2.0,
        -1.0
      ],
      [
        3.0,
        -1.0
      ]
    ],
    "k": [
      [
        1.0,
        -1.0
      ],
      [
        0.0,
        -1.0
      ],
      [
        -1.0,
        -3.0
      ]
    ],
    "v": [
      [
        1.0,
        1.0
      ],
      [
        0.0,
        1.0
      ],
      [
        1.0,
        3.0
      ]
    ],
    "scores": [
      [
        -2.0,
        -1.0,
        -2.0
      ],
      [
        3.0,
        1.0,
        1.0
      ],
      [
        4.0,
        1.0,
        0.0
      ]
    ],
    "scaled": [
      [
        -1.4142,
        -0.7071,
        -1.4142
      ],
      [
        2.1213,
        0.7071,
        0.7071
      ],
      [
        2.8284,
        0.7071,
        0.0
      ]
    ],
    "weights": [
      [
        0.2483,
        0.5035,
        0.2483
      ],
      [
        0.6728,
        0.1636,
        0.1636
      ],
      [
        0.8482,
        0.1017,
        0.0501
      ]
    ],
    "output": [
      [
        0.4965,
        1.4965
      ],
      [
        0.8364,
        1.3272
      ],
      [
        0.8983,
        1.1003
      ]
    ],
    "causalWeights": [
      [
        1.0,
        0.0,
        0.0
      ],
      [
        0.8044,
        0.1956,
        0.0
      ],
      [
        0.8482,
        0.1017,
        0.0501
      ]
    ],
    "causalOutput": [
      [
        1.0,
        1.0
      ],
      [
        0.8044,
        1.0
      ],
      [
        0.8983,
        1.1003
      ]
    ],
    "headline": {
      "query": "it",
      "key": "glass",
      "weight": 0.8482
    }
  },
  "decode": {
    "tokens": [
      "blue",
      "clear",
      "dark",
      "green",
      "red"
    ],
    "logits": [
      3.9,
      1.8,
      1.1,
      0.6,
      0.2
    ],
    "byTemperature": {
      "0.2": [
        1.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "0.5": [
        0.9798,
        0.0147,
        0.0036,
        0.0013,
        0.0006
      ],
      "1.0": [
        0.8033,
        0.0984,
        0.0488,
        0.0296,
        0.0199
      ],
      "1.5": [
        0.6262,
        0.1544,
        0.0968,
        0.0694,
        0.0531
      ],
      "2.0": [
        0.5139,
        0.1798,
        0.1267,
        0.0987,
        0.0808
      ]
    },
    "topK": {
      "k": 3,
      "kept": [
        "blue",
        "clear",
        "dark"
      ],
      "renormalised": [
        0.8451,
        0.1035,
        0.0514
      ]
    },
    "topP": {
      "p": 0.9,
      "cumulative": [
        0.8033,
        0.9017,
        0.9505,
        0.9801,
        1.0
      ],
      "keptCount": 2,
      "kept": [
        "blue",
        "clear"
      ],
      "mass": 0.9017
    }
  },
  "saturation": {
    "input": [
      0.1,
      -0.2,
      0.3,
      -0.2,
      0.5
    ],
    "scale": 8,
    "soft": [
      0.1925,
      0.1426,
      0.2351,
      0.1426,
      0.2872
    ],
    "peaky": [
      0.0326,
      0.003,
      0.1615,
      0.003,
      0.8
    ]
  },
  "paris": {
    "tokens": [
      "Paris",
      "London",
      "Berlin",
      "Rome",
      "other"
    ],
    "probs": [
      0.95,
      0.01,
      0.01,
      0.01,
      0.02
    ]
  },
  "loss": [
    [
      0.9,
      0.1054
    ],
    [
      0.5,
      0.6931
    ],
    [
      0.1,
      2.3026
    ],
    [
      0.01,
      4.6052
    ]
  ],
  "tokens": {
    "plain": {
      "encoding": "cl100k_base",
      "text": "The cat sat on the mat",
      "tokens": [
        "The",
        " cat",
        " sat",
        " on",
        " the",
        " mat"
      ],
      "ids": [
        791,
        8415,
        7731,
        389,
        279,
        5634
      ]
    },
    "egg": {
      "encoding": "cl100k_base",
      "text": "Egg. I have an Egg. egg. EGG.",
      "tokens": [
        "E",
        "gg",
        ".",
        " I",
        " have",
        " an",
        " Egg",
        ".",
        " egg",
        ".",
        " E",
        "GG",
        "."
      ],
      "ids": [
        36,
        14736,
        13,
        358,
        617,
        459,
        42313,
        13,
        19151,
        13,
        469,
        23050,
        13
      ]
    },
    "arithmetic": {
      "encoding": "gpt2",
      "text": "127 + 677 = 804",
      "tokens": [
        "127",
        " +",
        " 6",
        "77",
        " =",
        " 8",
        "04"
      ],
      "ids": [
        16799,
        1343,
        718,
        3324,
        796,
        807,
        3023
      ]
    },
    "english": {
      "encoding": "gpt2",
      "text": "hello how are you",
      "tokens": [
        "hello",
        " how",
        " are",
        " you"
      ],
      "ids": [
        31373,
        703,
        389,
        345
      ]
    },
    "korean": {
      "encoding": "gpt2",
      "text": "\uc548\ub155\ud558\uc138\uc694",
      "tokens": [
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd",
        "\ufffd"
      ],
      "ids": [
        168,
        243,
        230,
        167,
        227,
        243,
        47991,
        246,
        168,
        226,
        116,
        168,
        248,
        242
      ]
    },
    "magikarp_gpt2": {
      "encoding": "gpt2",
      "text": "SolidGoldMagikarp",
      "tokens": [
        "Solid",
        "GoldMagikarp"
      ],
      "ids": [
        46933,
        42202
      ]
    },
    "magikarp_gpt4": {
      "encoding": "cl100k_base",
      "text": "SolidGoldMagikarp",
      "tokens": [
        "Solid",
        "Gold",
        "Mag",
        "ik",
        "arp"
      ],
      "ids": [
        47041,
        26509,
        34015,
        1609,
        8035
      ]
    },
    "strawberry": {
      "encoding": "cl100k_base",
      "text": "strawberry",
      "tokens": [
        "str",
        "aw",
        "berry"
      ],
      "ids": [
        496,
        675,
        15717
      ]
    },
    "defaultcellstyle": {
      "encoding": "cl100k_base",
      "text": ".DefaultCellStyle",
      "tokens": [
        ".DefaultCellStyle"
      ],
      "ids": [
        98518
      ]
    }
  }
} as const

export function useDeckNumbers() {
  return N
}
