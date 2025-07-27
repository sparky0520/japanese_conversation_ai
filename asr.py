import whisper
import sounddevice as sd
import numpy as np
import time

class VoiceActivatedASR:
    def __init__(self):
        self.model = whisper.load_model("tiny")
        self.samplerate = 16000
        self.silence_threshold = 0.01
        self.min_speech_duration = 1.0
        self.max_silence_duration = 2.0
    
    def listen_for_speech(self):
        """Listen continuously and return transcription when speech ends"""
        print("Listening... (speak now)")
        
        audio_buffer = []
        silence_counter = 0
        recording_started = False
        
        def audio_callback(indata, frames, time, status):
            nonlocal audio_buffer, silence_counter, recording_started
            
            audio_level = np.mean(np.abs(indata))
            
            if audio_level > self.silence_threshold:
                # Speech detected
                if not recording_started:
                    print("Speech detected, recording...")
                    recording_started = True
                
                audio_buffer.append(indata.copy())
                silence_counter = 0
            else:
                # Silence detected
                if recording_started:
                    silence_counter += 1
                    audio_buffer.append(indata.copy())  # Keep some silence
        
        with sd.InputStream(samplerate=self.samplerate, channels=1, 
                           callback=audio_callback, blocksize=1024):
            
            while True:
                time.sleep(0.1)
                
                # Check if we should stop recording
                if (recording_started and 
                    silence_counter > (self.max_silence_duration * 10) and  # 10 = 1/0.1
                    len(audio_buffer) > (self.min_speech_duration * self.samplerate / 1024)):
                    break
        
        if not audio_buffer:
            return ""
        
        # Process recorded audio
        full_audio = np.concatenate(audio_buffer).flatten()
        
        print("Transcribing...")
        result = self.model.transcribe(full_audio, language="ja")
        
        return result['text'].strip() # type: ignore
