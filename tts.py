import asyncio
import websockets
import json
import base64
import pyaudio
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("MURF_TTS_API_KEY") # Or use os.getenv("MURF_API_KEY") if you have set the API key as an environment variable
WS_URL = "wss://api.murf.ai/v1/speech/stream-input"
PARAGRAPH = """こんにちは！アキだよ。言語交換、楽しみにしてたんだ！

今日はどうだった？何か面白いことあった？"""

# Audio format settings (must match your API output)
SAMPLE_RATE = 44100
CHANNELS = 2
CHANNEL_TYPE="MONO" if CHANNELS == 1 else "STEREO"
FORMAT = pyaudio.paInt16

async def tts_stream():
  async with websockets.connect(
      f"{WS_URL}?api-key={API_KEY}&sample_rate={SAMPLE_RATE}&channel_type={CHANNEL_TYPE}&format=WAV"
  ) as ws:
      # Send voice config first (optional)
      voice_config_msg = {
          "voice_config": {
              "voiceId": "ja-JP-kimi",
              "style": "Conversational",
              "rate": 0,
              "pitch": 0,
              "variation": 1
          }
      }
      print(f'Sending payload : {voice_config_msg}')
      await ws.send(json.dumps(voice_config_msg))

      # Send text in one go (or chunk if you want streaming)
      text_msg = {
          "text": PARAGRAPH,
          "end" : True # This will close the context. So you can re-run and concurrency is available.
      }
      print(f'Sending payload : {text_msg}')
      await ws.send(json.dumps(text_msg))

      # Setup audio stream
      pa = pyaudio.PyAudio()
      stream = pa.open(format=FORMAT, channels=CHANNELS, rate=SAMPLE_RATE, output=True)

      first_chunk = True
      try:
          while True:
              response = await ws.recv()
              data = json.loads(response)
              print(f'Received data:  {data}')
              if "audio" in data:
                  audio_bytes = base64.b64decode(data["audio"])
                  # Skip the first 44 bytes (WAV header) only for the first chunk
                  if first_chunk and len(audio_bytes) > 44:
                      audio_bytes = audio_bytes[44:]
                      first_chunk = False
                  stream.write(audio_bytes)
              if data.get("isFinalAudio"):
                  break
      finally:
          stream.stop_stream()
          stream.close()
          pa.terminate()

      asyncio.run(tts_stream())
