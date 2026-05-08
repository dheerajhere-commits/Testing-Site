import torch
from transformers import SpeechT5Processor, SpeechT5ForTextToSpeech, SpeechT5HifiGan
from datasets import load_dataset
import soundfile as sf
import argparse

def main():
    parser = argparse.ArgumentParser(description="Text to Speech using SpeechT5")
    parser.add_argument("--text", type=str, default="Hello, this is a test of the text to speech model.", help="Text to convert to speech")
    parser.add_argument("--output", type=str, default="output.wav", help="Output file name")
    args = parser.parse_args()

    # Detect device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    # Load the processor and model
    # We use SpeechT5 because it's relatively small and fast, perfect for a 4GB VRAM GPU like the NVIDIA M2000
    print("Loading models...")
    processor = SpeechT5Processor.from_pretrained("microsoft/speecht5_tts")
    model = SpeechT5ForTextToSpeech.from_pretrained("microsoft/speecht5_tts").to(device)
    vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan").to(device)

    # Process text
    print(f"Processing text: '{args.text}'")
    inputs = processor(text=args.text, return_tensors="pt").to(device)

    # Load speaker embeddings. The model requires these to determine the voice characteristics.
    # We use a default speaker from the CMU ARCTIC dataset.
    print("Loading speaker embeddings...")
    embeddings_dataset = load_dataset("Matthijs/cmu-arctic-xvectors", split="validation", trust_remote_code=True)
    speaker_embeddings = torch.tensor(embeddings_dataset[7306]["xvector"]).unsqueeze(0).to(device)

    # Generate speech
    print("Generating speech...")
    with torch.no_grad(): # Use no_grad to save memory during inference
        speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    # Save to file
    print(f"Saving audio to {args.output}...")
    # The output is a tensor, we need to convert it to numpy array
    sf.write(args.output, speech.cpu().numpy(), samplerate=16000)
    print("Done!")

if __name__ == "__main__":
    main()
