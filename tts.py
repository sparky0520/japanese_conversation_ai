import asyncio
import websockets
import json
import base64
import pyaudio
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MURF_TTS_API_KEY")
WS_URL = "wss://api.murf.ai/v1/speech/stream-input"

# Audio format settings
SAMPLE_RATE = 44100
CHANNELS = 1
CHANNEL_TYPE = "MONO"# if CHANNELS == 1 else "STEREO"
FORMAT = pyaudio.paInt16

async def _tts_stream_async(paragraph: str):
    async with websockets.connect(
        f"{WS_URL}?api-key={API_KEY}&sample_rate={SAMPLE_RATE}&channel_type={CHANNEL_TYPE}&format=WAV"
    ) as ws:
        # Send voice config first
        voice_config_msg = {
            "voice_config": {
                "voiceId": "ja-JP-kimi",
                "style": "Conversational",
                "rate": 0,
                "pitch": 0,
                "variation": 1
            }
        }
        await ws.send(json.dumps(voice_config_msg))

        # Send text
        text_msg = {
            "text": paragraph,
            "end": True
        }
        await ws.send(json.dumps(text_msg))

        # Setup audio stream
        pa = pyaudio.PyAudio()
        stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, output=True)

        first_chunk = True
        try:
            while True:
                try:
                    # Add timeout to prevent hanging
                    response = await asyncio.wait_for(ws.recv(), timeout=10.0)
                    data = json.loads(response)
                    
                    if "audio" in data:
                        audio_bytes = base64.b64decode(data["audio"])
                        if first_chunk and len(audio_bytes) > 44:
                            audio_bytes = audio_bytes[44:]
                            first_chunk = False
                        stream.write(audio_bytes)
                    
                    if data.get("isFinalAudio"):
                        print("Final audio received, closing...")
                        break
                        
                except asyncio.TimeoutError:
                    print("TTS timeout, closing connection")
                    break
                except websockets.exceptions.ConnectionClosed:
                    print("WebSocket connection closed")
                    break
                    
        except Exception as e:
            print(f"TTS error: {e}")
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()

def tts_stream(paragraph: str):
    """Synchronous wrapper with proper cleanup"""
    try:
        # Create new event loop for this call
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            loop.run_until_complete(_tts_stream_async(paragraph))
        finally:
            # Proper cleanup
            loop.close()
            
    except Exception as e:
        print(f"TTS stream error: {e}")