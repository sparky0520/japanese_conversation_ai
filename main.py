from asr import asr_transcript
from llm import get_llm_response
from metrics import runtime_metrics

def main():
    print("Transcribing audio...")
    transcribe = asr_transcript("assets/audio/sample/japanese2.wav")
    print("Fetching llm response...")
    llm_response = get_llm_response(transcribe)

    print(llm_response)


if __name__ == "__main__":
    runtime_metrics(main)