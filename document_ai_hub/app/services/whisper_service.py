import tempfile, io, whisper
import librosa
from fastapi import UploadFile

model = whisper.load_model("base")

async def text_from_audio(file: UploadFile) -> str:
    file_bytes = await file.read()
    audio_stream = io.BytesIO(file_bytes)

    audio_data, sample_rate = librosa.load(audio_stream, sr=16000)

    result = model.transcribe(audio_data)
    return result["text"]


