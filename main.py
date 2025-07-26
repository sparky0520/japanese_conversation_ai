from asr import VoiceActivatedASR
from llm import get_llm_response
from metrics import runtime_metrics
from tts import tts_stream

def main():
    
    asr = VoiceActivatedASR()
    
    while True:
        # Get transcription (blocks until speech is complete)
        transcription = asr.listen_for_speech()

        if transcription:
            print(f"You said: {transcription}")

            # Use transcription synchronously
            print("Fetching llm response...")
            llm_response = get_llm_response(transcription)
            print(f"LLM Response: {llm_response}")    
            tts_stream(llm_response)  # Blocks until complete
            print(f"Result: {llm_response}")
        else:
            print("No speech detected")

        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    runtime_metrics(main)