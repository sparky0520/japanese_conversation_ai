import whisper
import time

start_time = time.perf_counter()

model = whisper.load_model("tiny")
result = model.transcribe("../assets/audio/sample/japanese2.wav")
print(result["text"])

end_time = time.perf_counter()
elapsed_time = end_time - start_time
print(f"Elapsed Time: {elapsed_time:.6f} seconds.")