# Lightweight Text-to-Speech (TTS) for Low-End GPUs

This repository contains a simple, lightweight text-to-speech script optimized for systems with low-end graphics cards, specifically tested for constraints like the NVIDIA M2000 (4GB VRAM).

## Why this model?

The script uses `microsoft/speecht5_tts`.

1. **Memory Efficiency**: SpeechT5 is relatively small and can easily run inference within 4GB of VRAM. It generates high-quality speech without needing the massive resources that larger, more complex diffusion or auto-regressive models require.
2. **Speed**: Due to its small parameter count, it can generate speech quickly even on older GPUs or fallback CPUs.
3. **Quality**: It still uses a neural vocoder (HiFi-GAN) to produce natural-sounding 16kHz audio.

## Installation

1. Clone this repository.
2. Ensure you have Python 3.8+ installed.
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the script from the command line. By default, it will synthesize a test sentence and save it as `output.wav`.

```bash
python tts.py
```

You can specify your own text and output filename:

```bash
python tts.py --text "This is a custom sentence to synthesize." --output custom_audio.wav
```

## How it works

The script automatically detects if a CUDA-enabled GPU is available. If it finds one (like the NVIDIA M2000), it loads the model into VRAM and processes the text to speech on the GPU. If no GPU is available, it falls back to the CPU seamlessly.

It uses a default speaker embedding from the CMU ARCTIC dataset to give the voice its specific tonal characteristics.

---

# Multi-Agent DeFi Portfolio Management & CTF Solver (Simulation)

This repository also includes a multi-agent CLI tool designed for autonomous DeFi portfolio management and solving cryptographic challenges. **Note: For safety and educational purposes, this tool strictly operates in a simulated environment and does not interact with real seed phrases or live mainnet funds.**

## Architecture

The system is built on a modular multi-agent architecture:

1. **Sentinel Agent**: Monitors registered wallet addresses to ensure they maintain a specified liquidity floor.
2. **Solver Agent**: Simulates the analysis and solving of verified cryptographic puzzles (CTFs or bounty smart contracts).
3. **Executor Agent**: Simulates signing and broadcasting transactions to claim rewards.
4. **Governor Agent**: Manages the Reward/Penalty ledger, adjusting agent scores based on their performance (e.g., successful claims vs. wasted gas on failed transactions).

## Installation

Ensure you have Python 3.8+ installed, and install the requirements (which includes `typer` for the CLI):

```bash
pip install -r requirements.txt
```

## Usage

You can interact with the multi-agent system using the provided CLI tool located at `crypto_agents/main.py`.

### 1. Run the Simulation

To start the multi-agent system and simulate the monitoring of wallets and solving of puzzles over multiple cycles:

```bash
PYTHONPATH=. python crypto_agents/main.py run
```

You can customize the simulation parameters:

```bash
PYTHONPATH=. python crypto_agents/main.py run --wallets 10 --floor 5000.0
```

*Note: The `--live` flag is disabled for safety and will just output a warning.*

### 2. Check System Status

To view the current scores and history of the agents (Executor, Solver) from the Governor's ledger:

```bash
PYTHONPATH=. python crypto_agents/main.py status
```

### 3. Manually Dispatch the Solver

You can manually trigger the Solver agent to analyze a specific puzzle URL:

```bash
PYTHONPATH=. python crypto_agents/main.py solve "https://example.com/ctf/challenge_1"
```

## Design Document

For more details on the communication protocols between agents and the JSON schema used for the ledger, please refer to the `design.md` file included in this repository.
