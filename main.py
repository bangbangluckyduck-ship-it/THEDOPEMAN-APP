from __future__ import annotations
import asyncio
import json
import os
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from analyzer import analyze_video, transcribe_audio
from generate_assets import generate_icons

generate_icons()

app = FastAPI(title="TikTok Shop Analyzer")
app.mount("/static", StaticFiles(directory="static"), name="static")

_HTML = Path("templates/index.html").read_text(encoding="utf-8")


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(_HTML)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze")
async def analyze(
    frames: str = Form(...),       # JSON array of base64 JPEG strings
    audio: Optional[UploadFile] = File(None),  # WAV audio extracted client-side
):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Anthropic manquante.")

    frames_list: list[str] = json.loads(frames)
    if not frames_list:
        raise HTTPException(status_code=400, detail="Aucune frame reçue.")

    loop = asyncio.get_event_loop()
    audio_path: Optional[str] = None

    try:
        # Save audio to temp file if provided
        if audio:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio_path = tmp.name
                tmp.write(await audio.read())

        # Transcription with 20s timeout
        transcript: Optional[str] = None
        if audio_path:
            try:
                transcript = await asyncio.wait_for(
                    loop.run_in_executor(None, transcribe_audio, audio_path),
                    timeout=20.0,
                )
            except asyncio.TimeoutError:
                transcript = None

        # Claude analysis
        result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video, frames_list, transcript),
            timeout=30.0,
        )
        result["transcript"] = transcript
        result["frames_analyzed"] = len(frames_list)
        return result

    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Analyse trop longue. Réessaie.")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if audio_path:
            try:
                os.unlink(audio_path)
            except OSError:
                pass


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
