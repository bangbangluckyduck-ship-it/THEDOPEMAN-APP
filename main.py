from __future__ import annotations
import os
import shutil
import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from video_processor import extract_audio, extract_frames
from analyzer import analyze_video, transcribe_audio
from generate_assets import generate_icons

generate_icons()

app = FastAPI(title="TikTok Shop Analyzer")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

_HTML = Path("templates/index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(_HTML)


@app.post("/analyze")
async def analyze(video: UploadFile = File(...)):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(
            status_code=400,
            detail="Clé API Anthropic manquante.",
        )

    suffix = Path(video.filename or "video.mp4").suffix.lower() or ".mp4"
    tmp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False, dir=UPLOAD_DIR)
    try:
        shutil.copyfileobj(video.file, tmp_file)
        tmp_file.close()
        video_path = tmp_file.name

        frames = extract_frames(video_path, num_frames=6)
        if not frames:
            raise HTTPException(status_code=400, detail="Impossible d'extraire les frames. Vérifiez que le fichier est une vidéo valide.")

        result = analyze_video(frames)
        result["transcript"] = None
        result["frames_analyzed"] = len(frames)
        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        try:
            os.unlink(tmp_file.name)
        except OSError:
            pass


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
