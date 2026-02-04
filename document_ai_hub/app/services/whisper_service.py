import whisper
import librosa
import subprocess
import tempfile
from fastapi import UploadFile

model = whisper.load_model("base")

async def text_from_audio(file: UploadFile) -> str:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".m4a") as input_audio:
        input_audio.write(await file.read())
        input_path = input_audio.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as output_audio:
        output_path = output_audio.name

    subprocess.run([
        "ffmpeg", "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ], check=True)

    result = model.transcribe(output_path)
    return result["text"]


