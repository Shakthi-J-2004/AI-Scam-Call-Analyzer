import whisper
import os

model = None

def load_whisper_model():
    global model
    if model is None:
        try:
            model = whisper.load_model("base")
        except Exception as e:
            raise RuntimeError(f"Failed to load Whisper model. Ensure ffmpeg is installed. Error: {e}")

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the audio file using OpenAI Whisper Base model.
    """
    global model
    if model is None:
        load_whisper_model()
    
    try:
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        raise RuntimeError(f"Transcription failed: {e}. Please check if the audio format is supported and ffmpeg is installed.")
