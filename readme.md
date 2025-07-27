# Japanese AI Tutor

This is a japanese ai tutor bot made for purpose of practicing conversation in japanse or just casual talk. This is a friendly and polite bot who'll talk to you in japanese and suggest you new and better ways of saying things to make you proficient. Enjoy!

## Algorithm

1. Get user speech stream
2. Perform Automatic Speech Recognition (ASR)
3. Give the transcript to LLM in a turn-based chat
4. Give the response from LLM to a TTS engine
5. Play the tts stream
6. Repeat from 1

## Tech Stack

Python is the primary language used to keep things simple and use SDKs seemlessly. Below are the technologies used:

- ASR -> OpenAI Whisper (stream)
- LLM -> Gemini API (gemini-2.5-flash)
- TTS -> Murf API (stream)

## Improvements

- Make Gemini also a stream to implement a stream pipeline which focuses on a chunk to do everything in near-realtime.
- Desktop app to display
- Website for landing page, distribution
