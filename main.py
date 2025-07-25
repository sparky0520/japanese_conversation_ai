from asr import asr_transcript
from llm import get_llm_response
from metrics import runtime_metrics
from tts import tts_stream
import asyncio

def main():
    print("Transcribing audio...")
    transcribe = asr_transcript("assets/audio/sample/japanese2.wav")
    print(f"Transcribed audio: {transcribe}")
    print("Fetching llm response...")
    llm_response = get_llm_response(transcribe)
    print(f"LLM Response: {llm_response}")
    asyncio.run(tts_stream(llm_response))

if __name__ == "__main__":
    runtime_metrics(main)