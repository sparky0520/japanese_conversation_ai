from murf import Murf
import pygame
import io

# Initialize pygame mixer and murf client
pygame.mixer.init()
client = Murf()

def tts_stream(paragraph: str):
    try:
        res = client.text_to_speech.stream(
                text=paragraph,
                voice_id="ja-JP-kimi", 
                style="Conversational"
            )

        # Collect all audio chunks
        audio_data = b""
        for audio_chunk in res:
            audio_data += audio_chunk

        # Create a BytesIO object and play the audio
        audio_buffer = io.BytesIO(audio_data)
        pygame.mixer.music.load(audio_buffer)
        pygame.mixer.music.play()

        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        print(f"❌ TTS Error: {e}")