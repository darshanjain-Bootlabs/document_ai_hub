import  io, whisper
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

    audio_data, sample_rate = librosa.load(output_path, sr=16000)

    result = model.transcribe(audio_data)
    return result["text"]


