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
    },
    "threeways": {
      "encoding": "cl100k_base",
      "text": "The teddy bears were reading",
      "tokens": [
        "The",
        " ted",
        "dy",
        " bears",
        " were",
        " reading"
      ],
      "ids": [
        791,
        42323,
        10470,
        30824,
        1051,
        5403
      ]
    },
    "unbearable": {
      "encoding": "cl100k_base",
      "text": "unbearable",
      "tokens": [
        "un",
        "bear",
        "able"
      ],
      "ids": [
        359,
        68760,
        481
      ]
    }
  },
  "vocab": {
    "sizes": {
      "gpt2": 50257,
      "cl100k_base": 100277
    },
    "endOfText": {
      "gpt2": 50256,
      "cl100k_base": 100257
    }
  },
  "bpe": {
    "corpus": {
      "read": 4,
      "reading": 3,
      "bear": 4,
      "bears": 2,
      "ring": 2,
      "sing": 3
    },
    "steps": [
      {
        "pair": [
          "e",
          "a"
        ],
        "merged": "ea",
        "count": 13,
        "top": [
          [
            "ea",
            13
          ],
          [
            "in",
            8
          ],
          [
            "ng",
            8
          ],
          [
            "ad",
            7
          ]
        ],
        "words": {
          "read": [
            "r",
            "ea",
            "d"
          ],
          "reading": [
            "r",
            "ea",
            "d",
            "i",
            "n",
            "g"
          ],
          "bear": [
            "b",
            "ea",
            "r"
          ],
          "bears": [
            "b",
            "ea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "i",
            "n",
            "g"
          ],
          "sing": [
            "s",
            "i",
            "n",
            "g"
          ]
        }
      },
      {
        "pair": [
          "i",
          "n"
        ],
        "merged": "in",
        "count": 8,
        "top": [
          [
            "in",
            8
          ],
          [
            "ng",
            8
          ],
          [
            "ead",
            7
          ],
          [
            "rea",
            7
          ]
        ],
        "words": {
          "read": [
            "r",
            "ea",
            "d"
          ],
          "reading": [
            "r",
            "ea",
            "d",
            "in",
            "g"
          ],
          "bear": [
            "b",
            "ea",
            "r"
          ],
          "bears": [
            "b",
            "ea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "in",
            "g"
          ],
          "sing": [
            "s",
            "in",
            "g"
          ]
        }
      },
      {
        "pair": [
          "in",
          "g"
        ],
        "merged": "ing",
        "count": 8,
        "top": [
          [
            "ing",
            8
          ],
          [
            "ead",
            7
          ],
          [
            "rea",
            7
          ],
          [
            "bea",
            6
          ]
        ],
        "words": {
          "read": [
            "r",
            "ea",
            "d"
          ],
          "reading": [
            "r",
            "ea",
            "d",
            "ing"
          ],
          "bear": [
            "b",
            "ea",
            "r"
          ],
          "bears": [
            "b",
            "ea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "ing"
          ],
          "sing": [
            "s",
            "ing"
          ]
        }
      },
      {
        "pair": [
          "ea",
          "d"
        ],
        "merged": "ead",
        "count": 7,
        "top": [
          [
            "ead",
            7
          ],
          [
            "rea",
            7
          ],
          [
            "bea",
            6
          ],
          [
            "ear",
            6
          ]
        ],
        "words": {
          "read": [
            "r",
            "ead"
          ],
          "reading": [
            "r",
            "ead",
            "ing"
          ],
          "bear": [
            "b",
            "ea",
            "r"
          ],
          "bears": [
            "b",
            "ea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "ing"
          ],
          "sing": [
            "s",
            "ing"
          ]
        }
      },
      {
        "pair": [
          "r",
          "ead"
        ],
        "merged": "read",
        "count": 7,
        "top": [
          [
            "read",
            7
          ],
          [
            "bea",
            6
          ],
          [
            "ear",
            6
          ],
          [
            "eading",
            3
          ]
        ],
        "words": {
          "read": [
            "read"
          ],
          "reading": [
            "read",
            "ing"
          ],
          "bear": [
            "b",
            "ea",
            "r"
          ],
          "bears": [
            "b",
            "ea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "ing"
          ],
          "sing": [
            "s",
            "ing"
          ]
        }
      },
      {
        "pair": [
          "b",
          "ea"
        ],
        "merged": "bea",
        "count": 6,
        "top": [
          [
            "bea",
            6
          ],
          [
            "ear",
            6
          ],
          [
            "reading",
            3
          ],
          [
            "sing",
            3
          ]
        ],
        "words": {
          "read": [
            "read"
          ],
          "reading": [
            "read",
            "ing"
          ],
          "bear": [
            "bea",
            "r"
          ],
          "bears": [
            "bea",
            "r",
            "s"
          ],
          "ring": [
            "r",
            "ing"
          ],
          "sing": [
            "s",
            "ing"
          ]
        }
      },
      {
        "pair": [
          "bea",
          "r"
        ],
        "merged": "bear",
        "count": 6,
        "top": [
          [
            "bear",
            6
          ],
          [
            "reading",
            3
          ],
          [
            "sing",
            3
          ],
          [
            "ring",
            2
          ]
        ],
        "words": {
          "read": [
            "read"
          ],
          "reading": [
            "read",
            "ing"
          ],
          "bear": [
            "bear"
          ],
          "bears": [
            "bear",
            "s"
          ],
          "ring": [
            "r",
            "ing"
          ],
          "sing": [
            "s",
            "ing"
          ]
        }
      }
    ],
    "unseen": {
      "bearing": [
        "bear",
        "ing"
      ],
      "rings": [
        "r",
        "ing",
        "s"
      ]
    }
  },
  "posenc": {
    "dim": 16,
    "strip": [
      [
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0
      ],
      [
        0.841,
        0.54,
        0.311,
        0.95,
        0.1,
        0.995,
        0.032,
        1.0,
        0.01,
        1.0,
        0.003,
        1.0,
        0.001,
        1.0,
        0.0,
        1.0
      ],
      [
        0.909,
        -0.416,
        0.591,
        0.807,
        0.199,
        0.98,
        0.063,
        0.998,
        0.02,
        1.0,
        0.006,
        1.0,
        0.002,
        1.0,
        0.001,
        1.0
      ],
      [
        0.141,
        -0.99,
        0.813,
        0.583,
        0.296,
        0.955,
        0.095,
        0.996,
        0.03,
        1.0,
        0.009,
        1.0,
        0.003,
        1.0,
        0.001,
        1.0
      ],
      [
        -0.757,
        -0.654,
        0.954,
        0.301,
        0.389,
        0.921,
        0.126,
        0.992,
        0.04,
        0.999,
        0.013,
        1.0,
        0.004,
        1.0,
        0.001,
        1.0
      ],
      [
        -0.959,
        0.284,
        1.0,
        -0.01,
        0.479,
        0.878,
        0.157,
        0.988,
        0.05,
        0.999,
        0.016,
        1.0,
        0.005,
        1.0,
        0.002,
        1.0
      ],
      [
        -0.279,
        0.96,
        0.947,
        -0.321,
        0.565,
        0.825,
        0.189,
        0.982,
        0.06,
        0.998,
        0.019,
        1.0,
        0.006,
        1.0,
        0.002,
        1.0
      ],
      [
        0.657,
        0.754,
        0.8,
        -0.599,
        0.644,
        0.765,
        0.22,
        0.976,
        0.07,
        0.998,
        0.022,
        1.0,
        0.007,
        1.0,
        0.002,
        1.0
      ],
      [
        0.989,
        -0.146,
        0.574,
        -0.819,
        0.717,
        0.697,
        0.25,
        0.968,
        0.08,
        0.997,
        0.025,
        1.0,
        0.008,
        1.0,
        0.003,
        1.0
      ],
      [
        0.412,
        -0.911,
        0.291,
        -0.957,
        0.783,
        0.622,
        0.281,
        0.96,
        0.09,
        0.996,
        0.028,
        1.0,
        0.009,
        1.0,
        0.003,
        1.0
      ],
      [
        -0.544,
        -0.839,
        -0.021,
        -1.0,
        0.841,
        0.54,
        0.311,
        0.95,
        0.1,
        0.995,
        0.032,
        1.0,
        0.01,
        1.0,
        0.003,
        1.0
      ],
      [
        -1.0,
        0.004,
        -0.331,
        -0.944,
        0.891,
        0.454,
        0.341,
        0.94,
        0.11,
        0.994,
        0.035,
        0.999,
        0.011,
        1.0,
        0.003,
        1.0
      ],
      [
        -0.537,
        0.844,
        -0.608,
        -0.794,
        0.932,
        0.362,
        0.37,
        0.929,
        0.12,
        0.993,
        0.038,
        0.999,
        0.012,
        1.0,
        0.004,
        1.0
      ],
      [
        0.42,
        0.907,
        -0.825,
        -0.566,
        0.964,
        0.267,
        0.4,
        0.917,
        0.13,
        0.992,
        0.041,
        0.999,
        0.013,
        1.0,
        0.004,
        1.0
      ],
      [
        0.991,
        0.137,
        -0.96,
        -0.281,
        0.985,
        0.17,
        0.428,
        0.904,
        0.14,
        0.99,
        0.044,
        0.999,
        0.014,
        1.0,
        0.004,
        1.0
      ],
      [
        0.65,
        -0.76,
        -1.0,
        0.031,
        0.997,
        0.071,
        0.457,
        0.89,
        0.149,
        0.989,
        0.047,
        0.999,
        0.015,
        1.0,
        0.005,
        1.0
      ],
      [
        -0.288,
        -0.958,
        -0.94,
        0.34,
        1.0,
        -0.029,
        0.485,
        0.875,
        0.159,
        0.987,
        0.051,
        0.999,
        0.016,
        1.0,
        0.005,
        1.0
      ],
      [
        -0.961,
        -0.275,
        -0.788,
        0.616,
        0.992,
        -0.129,
        0.512,
        0.859,
        0.169,
        0.986,
        0.054,
        0.999,
        0.017,
        1.0,
        0.005,
        1.0
      ],
      [
        -0.751,
        0.66,
        -0.557,
        0.83,
        0.974,
        -0.227,
        0.539,
        0.842,
        0.179,
        0.984,
        0.057,
        0.998,
        0.018,
        1.0,
        0.006,
        1.0
      ],
      [
        0.15,
        0.989,
        -0.271,
        0.962,
        0.946,
        -0.323,
        0.565,
        0.825,
        0.189,
        0.982,
        0.06,
        0.998,
        0.019,
        1.0,
        0.006,
        1.0
      ],
      [
        0.913,
        0.408,
        0.041,
        0.999,
        0.909,
        -0.416,
        0.591,
        0.807,
        0.199,
        0.98,
        0.063,
        0.998,
        0.02,
        1.0,
        0.006,
        1.0
      ],
      [
        0.837,
        -0.548,
        0.35,
        0.937,
        0.863,
        -0.505,
        0.616,
        0.787,
        0.208,
        0.978,
        0.066,
        0.998,
        0.021,
        1.0,
        0.007,
        1.0
      ],
      [
        -0.009,
        -1.0,
        0.624,
        0.781,
        0.808,
        -0.589,
        0.641,
        0.768,
        0.218,
        0.976,
        0.07,
        0.998,
        0.022,
        1.0,
        0.007,
        1.0
      ],
      [
        -0.846,
        -0.533,
        0.836,
        0.549,
        0.746,
        -0.666,
        0.665,
        0.747,
        0.228,
        0.974,
        0.073,
        0.997,
        0.023,
        1.0,
        0.007,
        1.0
      ]
    ],
    "periods": [
      6.3,
      19.9,
      62.8,
      198.7,
      628.3,
      1986.9,
      6283.2,
      19869.2
    ],
    "curve": {
      "dim": 512,
      "ref": 20,
      "similarity": [
        0.616,
        0.618,
        0.618,
        0.621,
        0.631,
        0.645,
        0.656,
        0.662,
        0.662,
        0.665,
        0.679,
        0.701,
        0.723,
        0.734,
        0.735,
        0.741,
        0.768,
        0.827,
        0.905,
        0.973,
        1.0,
        0.973,
        0.905,
        0.827,
        0.768,
        0.741,
        0.735,
        0.734,
        0.723,
        0.701,
        0.679,
        0.665,
        0.662,
        0.662,
        0.656,
        0.645,
        0.631,
        0.621,
        0.618,
        0.618,
        0.616
      ]
    }
  },
  "multihead": {
    "h": 2,
    "dK": 2,
    "wQ2": [
      [
        0.0,
        0.0
      ],
      [
        1.0,
        0.0
      ],
      [
        1.0,
        0.0
      ],
      [
        0.0,
        0.0
      ]
    ],
    "wK2": [
      [
        1.0,
        0.0
      ],
      [
        0.0,
        0.0
      ],
      [
        0.0,
        0.0
      ],
      [
        -2.0,
        0.0
      ]
    ],
    "wV2": [
      [
        1.0,
        0.0
      ],
      [
        0.0,
        1.0
      ],
      [
        0.0,
        0.0
      ],
      [
        0.0,
        0.0
      ]
    ],
    "wO": [
      [
        1.0,
        0.0,
        1.0,
        0.0
      ],
      [
        0.0,
        1.0,
        0.0,
        1.0
      ],
      [
        1.0,
        0.0,
        -1.0,
        0.0
      ],
      [
        0.0,
        1.0,
        0.0,
        -1.0
      ]
    ],
    "head1": {
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
      ]
    },
    "head2": {
      "q": [
        [
          2.0,
          0.0
        ],
        [
          1.0,
          0.0
        ],
        [
          2.0,
          0.0
        ]
      ],
      "k": [
        [
          -2.0,
          0.0
        ],
        [
          1.0,
          0.0
        ],
        [
          0.0,
          0.0
        ]
      ],
      "v": [
        [
          0.0,
          2.0
        ],
        [
          1.0,
          0.0
        ],
        [
          2.0,
          0.0
        ]
      ],
      "scores": [
        [
          -4.0,
          2.0,
          0.0
        ],
        [
          -2.0,
          1.0,
          0.0
        ],
        [
          -4.0,
          2.0,
          0.0
        ]
      ],
      "weights": [
        [
          0.0114,
          0.7952,
          0.1933
        ],
        [
          0.0743,
          0.62,
          0.3057
        ],
        [
          0.0114,
          0.7952,
          0.1933
        ]
      ],
      "output": [
        [
          1.1819,
          0.0229
        ],
        [
          1.2314,
          0.1486
        ],
        [
          1.1819,
          0.0229
        ]
      ]
    },
    "concat": [
      [
        0.4965,
        1.4965,
        1.1819,
        0.0229
      ],
      [
        0.8364,
        1.3272,
        1.2314,
        0.1486
      ],
      [
        0.8983,
        1.1003,
        1.1819,
        0.0229
      ]
    ],
    "output": [
      [
        1.6784,
        1.5194,
        -0.6854,
        1.4737
      ],
      [
        2.0678,
        1.4758,
        -0.395,
        1.1785
      ],
      [
        2.0802,
        1.1231,
        -0.2836,
        1.0774
      ]
    ]
  },
  "crossattn": {
    "encTokens": [
      "the",
      "cat",
      "sleeps"
    ],
    "decTokens": [
      "<BOS>",
      "le"
    ],
    "q": [
      [
        1.0,
        0.0
      ],
      [
        0.0,
        2.0
      ]
    ],
    "k": [
      [
        2.0,
        0.0
      ],
      [
        0.0,
        2.0
      ],
      [
        -1.0,
        1.0
      ]
    ],
    "v": [
      [
        1.0,
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
    "scores": [
      [
        2.0,
        0.0,
        -1.0
      ],
      [
        0.0,
        4.0,
        2.0
      ]
    ],
    "scaled": [
      [
        1.4142,
        0.0,
        -0.7071
      ],
      [
        0.0,
        2.8284,
        1.4142
      ]
    ],
    "weights": [
      [
        0.7337,
        0.1784,
        0.0879
      ],
      [
        0.0454,
        0.7679,
        0.1867
      ]
    ],
    "output": [
      [
        0.8216,
        0.2663
      ],
      [
        0.2321,
        0.9546
      ]
    ]
  },
  "layernorm": {
    "x": [
      20.0,
      40.0,
      40.0,
      100.0
    ],
    "mean": 50.0,
    "std": 30.0,
    "y": [
      -1.0,
      -0.33,
      -0.33,
      1.67
    ]
  },
  "smoothing": {
    "eps": 0.1,
    "tokens": [
      "blue",
      "clear",
      "dark",
      "green",
      "red"
    ],
    "hard": [
      1.0,
      0.0,
      0.0,
      0.0,
      0.0
    ],
    "paper": [
      0.9,
      0.025,
      0.025,
      0.025,
      0.025
    ],
    "torch": [
      0.92,
      0.02,
      0.02,
      0.02,
      0.02
    ],
    "lossHard": 0.219,
    "lossSmoothed": 0.5165
  },
  "vanishing": {
    "steps": 10,
    "shrink": {
      "factor": 0.5,
      "values": [
        1.0,
        0.5,
        0.25,
        0.125,
        0.0625,
        0.03125,
        0.015625,
        0.007812,
        0.003906,
        0.001953,
        0.000977
      ]
    },
    "grow": {
      "factor": 1.5,
      "values": [
        1.0,
        1.5,
        2.25,
        3.375,
        5.062,
        7.594,
        11.391,
        17.086,
        25.629,
        38.443,
        57.665
      ]
    }
  },
  "base": {
    "dims": {
      "d_model": 512,
      "h": 8,
      "d_k": 64,
      "d_ff": 2048,
      "N": 6,
      "vocab": 37000
    },
    "src": [
      "A",
      "cute",
      "teddy",
      "bear",
      "is",
      "reading",
      "."
    ],
    "tgt": [
      "Un",
      "ours",
      "en",
      "peluche",
      "mignon",
      "lit",
      "."
    ],
    "trace": [
      {
        "stage": "encoder",
        "tensor": "source token ids",
        "shape": [
          7
        ],
        "note": "7 source tokens"
      },
      {
        "stage": "encoder",
        "tensor": "embedding + position",
        "shape": [
          7,
          512
        ],
        "note": "one row per token"
      },
      {
        "stage": "encoder self-attention",
        "tensor": "Q (one head)",
        "shape": [
          7,
          64
        ],
        "note": "rows = tokens asking"
      },
      {
        "stage": "encoder self-attention",
        "tensor": "K (one head)",
        "shape": [
          7,
          64
        ],
        "note": "rows = tokens being asked"
      },
      {
        "stage": "encoder self-attention",
        "tensor": "scores per head",
        "shape": [
          8,
          7,
          7
        ],
        "note": "h x queries x keys"
      },
      {
        "stage": "encoder self-attention",
        "tensor": "concat heads",
        "shape": [
          7,
          512
        ],
        "note": "h * d_k = d_model"
      },
      {
        "stage": "encoder",
        "tensor": "FFN hidden",
        "shape": [
          7,
          2048
        ],
        "note": "expanded 4x"
      },
      {
        "stage": "encoder",
        "tensor": "encoder output (after 6 layers)",
        "shape": [
          7,
          512
        ],
        "note": "context-aware source"
      },
      {
        "stage": "decoder",
        "tensor": "<BOS> + target so far",
        "shape": [
          8,
          512
        ],
        "note": "teacher forcing during training"
      },
      {
        "stage": "decoder masked self-attention",
        "tensor": "Q (one head)",
        "shape": [
          8,
          64
        ],
        "note": "rows = tokens asking"
      },
      {
        "stage": "decoder masked self-attention",
        "tensor": "K (one head)",
        "shape": [
          8,
          64
        ],
        "note": "rows = tokens being asked"
      },
      {
        "stage": "decoder masked self-attention",
        "tensor": "scores per head",
        "shape": [
          8,
          8,
          8
        ],
        "note": "h x queries x keys"
      },
      {
        "stage": "decoder masked self-attention",
        "tensor": "concat heads",
        "shape": [
          8,
          512
        ],
        "note": "h * d_k = d_model"
      },
      {
        "stage": "cross-attention",
        "tensor": "Q (one head)",
        "shape": [
          8,
          64
        ],
        "note": "rows = tokens asking"
      },
      {
        "stage": "cross-attention",
        "tensor": "K (one head)",
        "shape": [
          7,
          64
        ],
        "note": "rows = tokens being asked"
      },
      {
        "stage": "cross-attention",
        "tensor": "scores per head",
        "shape": [
          8,
          8,
          7
        ],
        "note": "h x queries x keys"
      },
      {
        "stage": "cross-attention",
        "tensor": "concat heads",
        "shape": [
          8,
          512
        ],
        "note": "h * d_k = d_model"
      },
      {
        "stage": "decoder",
        "tensor": "decoder output (after 6 layers)",
        "shape": [
          8,
          512
        ],
        "note": "one row per position"
      },
      {
        "stage": "output",
        "tensor": "logits",
        "shape": [
          8,
          37000
        ],
        "note": "one score per vocabulary entry"
      },
      {
        "stage": "output",
        "tensor": "probabilities",
        "shape": [
          8,
          37000
        ],
        "note": "each row sums to 1"
      }
    ],
    "params": {
      "embeddings": 18944000,
      "attention": 18911232,
      "ffn": 25196544,
      "layernorm": 30720,
      "total": 63082496
    }
  }
} as const

export function useDeckNumbers() {
  return N
}
