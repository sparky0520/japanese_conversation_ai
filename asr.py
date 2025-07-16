import whisper
from metrics import runtime_metrics

def asr_transcript():
    model = whisper.load_model("tiny")
    result = model.transcribe("assets/audio/sample/japanese2.wav")
    print(result["text"])

runtime_metrics(asr_transcript)