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
