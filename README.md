<div align="center">

```
██████╗  █████╗ ██╗   ██╗    ██████╗     ██████╗ ██████╗ ██╗ ██████╗██╗  ██╗
██╔══██╗██╔══██╗╚██╗ ██╔╝    ╚════██╗    ██╔══██╗██╔══██╗██║██╔════╝██║ ██╔╝
██████╔╝███████║ ╚████╔╝      █████╔╝    ██████╔╝██████╔╝██║██║     █████╔╝ 
██╔═══╝ ██╔══██║  ╚██╔╝      ██╔═══╝     ██╔══██╗██╔══██╗██║██║     ██╔═██╗ 
██║     ██║  ██║   ██║       ███████╗    ██████╔╝██║  ██║██║╚██████╗██║  ██╗
╚═╝     ╚═╝  ╚═╝   ╚═╝       ╚══════╝   ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝
```

**A cross-platform cipher & hash toolkit — 65 ciphers, 10 hashes, one clean UI.**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)](https://python.org)
[![Kivy](https://img.shields.io/badge/UI-Kivy-brightgreen?style=flat-square)](https://kivy.org)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)]()

</div>

---

## ✨ Features

- 🔐 **65 ciphers** — from classic Caesar to Enigma, Playfair, XOR, Base64 and more
- #️⃣ **10 hash algorithms** — MD5, SHA-1, SHA-256, SHA-512, BLAKE2 and more
- 📱 **Fully responsive** — portrait stacks vertically, landscape splits side-by-side
- 🌙 **Dark / Light theme** toggle
- 🔑 **Smart key detection** — key input only appears when the selected cipher needs it
- 🔄 **Encode & Decode** modes with a single click
- 🌍 **Cross-platform** — Android (Pydroid 3), Windows, Linux, macOS

---

## 📸 Screenshots

| Dark mode — Landscape | Light mode — Portrait |
|:---------------------:|:---------------------:|
| *(side-by-side layout)* | *(stacked layout)* |

> UI automatically switches layout based on window orientation.

---

## 🚀 Installation

### 🖥️ Desktop (Windows / Linux / macOS)

```bash
pip install kivy
python pay2brick_kivy.py
```

### 📱 Android (Pydroid 3)

1. Open **Pydroid 3**
2. Go to **Pip** tab → install `kivy`
3. Open `pay2brick_kivy.py`
4. Press the **▶ Play** button *(not the terminal tab)*

> ⚠️ CustomTkinter does not work on Android — this Kivy version was built specifically for cross-platform support.

---

## 🔐 Cipher List (65 total)

### Substitution
| # | Name | Key needed |
|---|------|:----------:|
| 01 | Reverse | ✗ |
| 02 | ROT-13 | ✗ |
| 03 | ROT-5 (digits only) | ✗ |
| 04 | ROT-18 (letters + digits) | ✗ |
| 05 | ROT-47 (all printable ASCII) | ✗ |
| 06 | Atbash | ✗ |
| 07 | Leet Speak | ✗ |
| 08 | Swap Case | ✗ |
| 09 | Caesar | ✓ (shift number) |
| 10 | Caesar All-ASCII | ✓ (shift number) |
| 11 | Caesar Numbers | ✓ (shift number) |
| 12 | Affine | ✓ (a,b e.g. `5,8`) |
| 13 | Vigenere | ✓ (word) |
| 14 | Beaufort | ✓ (word) |
| 15 | Autokey | ✓ (word) |
| 16 | Gronsfeld | ✓ (digits e.g. `1234`) |
| 17 | Running Key | ✓ (phrase) |
| 18 | Trithemius | ✗ |
| 19 | Keyed ROT | ✓ (word) |
| 20 | Porta | ✓ (word) |
| 21 | Keyword Cipher | ✓ (word) |
| 22 | Simple Substitution | ✓ (26-letter alphabet) |
| 23 | Homophonic | ✗ |
| 24 | Chaocipher | ✓ (26-letter alphabet) |

### Transposition
| # | Name | Key needed |
|---|------|:----------:|
| 25 | Rail Fence | ✓ (number of rails) |
| 26 | Columnar Transposition | ✓ (word) |
| 27 | Double Transposition | ✓ (word) |
| 28 | Reverse Words | ✗ |
| 29 | Reverse Word Order | ✗ |
| 30 | Reverse Each Line | ✗ |
| 31 | Mirror | ✗ |
| 32 | Word Scramble | ✗ |

### Polygraphic & Complex
| # | Name | Key needed |
|---|------|:----------:|
| 33 | Playfair | ✓ (word) |
| 34 | Four-Square | ✓ (two words: `word1,word2`) |
| 35 | Bifid | ✓ (word) |
| 36 | Polybius Square | ✗ |
| 37 | Bacon Cipher | ✗ |
| 38 | Hill 2×2 | ✓ (matrix: `3,3,2,5`) |
| 39 | One-Time Pad | ✓ (comma-separated numbers) |
| 40 | Enigma (3-rotor) | ✓ (rotor positions: `0,0,0`) |

### XOR
| # | Name | Key needed |
|---|------|:----------:|
| 41 | XOR (decimal key) | ✓ (number 0–255) |
| 42 | XOR (hex key) | ✓ (hex byte e.g. `FF`) |

### Encoding
| # | Name | Key needed |
|---|------|:----------:|
| 43 | Base64 | ✗ |
| 44 | Base32 | ✗ |
| 45 | Base16 / Hex | ✗ |
| 46 | Base58 | ✗ |
| 47 | Base85 | ✗ |
| 48 | ASCII Codes | ✗ |
| 49 | Binary | ✗ |
| 50 | Octal | ✗ |
| 51 | URL Encode | ✗ |
| 52 | HTML Entities | ✗ |
| 53 | Unicode Escape | ✗ |

### Novelty & Steganographic
| # | Name | Key needed |
|---|------|:----------:|
| 54 | Morse Code | ✗ |
| 55 | Braille | ✗ |
| 56 | Tap Code | ✗ |
| 57 | Pigpen | ✗ |
| 58 | Null Cipher | ✗ |
| 59 | Pig Latin | ✗ |
| 60 | Flip Upside-Down | ✗ |
| 61 | Full-Width | ✗ |
| 62 | Discord Spoiler | ✗ |
| 63 | Zalgo | ✓ (intensity 1–10) |

### Compression & Checksum
| # | Name | Key needed |
|---|------|:----------:|
| 64 | Zlib + Base64 | ✗ |
| 65 | CRC32 Checksum | ✗ |

---

## #️⃣ Hash List (10 total)

| # | Algorithm | Output length |
|---|-----------|:-------------:|
| H01 | MD5 | 128-bit |
| H02 | SHA-1 | 160-bit |
| H03 | SHA-224 | 224-bit |
| H04 | SHA-256 | 256-bit |
| H05 | SHA-384 | 384-bit |
| H06 | SHA-512 | 512-bit |
| H07 | SHA3-256 | 256-bit |
| H08 | SHA3-512 | 512-bit |
| H09 | BLAKE2b | 512-bit |
| H10 | BLAKE2s | 256-bit |

> 🔒 Hash mode is one-way — decoding is not possible by design.

---

## 🗂️ File Structure

```
pay2brick/
├── pay2brick_kivy.py     # Main app (Kivy, cross-platform)
├── pay2brick.py          # Desktop-only version (CustomTkinter)
└── README.md
```

---

## 🎨 UI Overview

```
┌─────────────────────────────────────────────────────┐
│  pay 2 brick          65 ciphers · 10 hashes  [☀]  │
├──────────────┬──────────────────────────────────────┤
│  Mode        │  INPUT                               │
│ [Encode][Dec]│  ┌────────────────────────────────┐  │
│      ▼       │  │ Type or paste your text here…  │  │
│  Cipher      │  └────────────────────────────────┘  │
│ [01 Reverse▼]│                                      │
│              │         [  ▶  START  ]               │
│  ▼ key needed│                                      │
│ [key input ] │  OUTPUT                              │
│ ─────────────│  ┌────────────────────────────────┐  │
│ ⬤ [HASH MODE]│  │ result appears here…           │  │
└──────────────┴──────────────────────────────────────┘
         LANDSCAPE layout (side-by-side)

┌─────────────────────────────┐
│  pay 2 brick          [☀]  │
├─────────────────────────────┤
│  Mode: [Encode] [Decode]    │
│  ▼                          │
│  Cipher: [01 Reverse      ▼]│
│  ─────────────────────────  │
│  ⬤ [HASH MODE]              │
├─────────────────────────────┤
│  INPUT                      │
│  ┌─────────────────────────┐│
│  │ Type here…              ││
│  └─────────────────────────┘│
│       [ ▶  START ]          │
│  OUTPUT                     │
│  ┌─────────────────────────┐│
│  │ result…                 ││
│  └─────────────────────────┘│
└─────────────────────────────┘
         PORTRAIT layout (stacked)
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `kivy` | ≥ 2.0 | UI framework |
| `python` | ≥ 3.8 | Runtime |

All cipher logic uses **Python standard library only** — no extra packages needed for the crypto part.

---

## ⚠️ Disclaimer

This tool is intended for **educational and recreational purposes** — learning how classical ciphers work, CTF challenges, puzzles, and fun encoding.

> None of the ciphers in this app (except hashing) should be used for **real security** — classical ciphers are not cryptographically secure.

---

## 📄 License

MIT — do whatever you want with it.

---

<div align="center">
Made with ❤️ and too many ciphers
</div>
 
