import whisper

def asr_transcript(file_path: str) -> str:
    model = whisper.load_model("tiny")
    result = model.transcribe(file_path)
    return str(result["text"])
