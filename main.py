from __future__ import annotations
import asyncio
import os
from pathlib import Path
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from analyzer import analyze_video
from generate_assets import generate_icons

generate_icons()

app = FastAPI(title="TikTok Shop Analyzer")
app.mount("/static", StaticFiles(directory="static"), name="static")

_HTML = Path("templates/index.html").read_text(encoding="utf-8")


class FramesPayload(BaseModel):
    frames: List[str]  # base64 JPEG frames extracted client-side


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(_HTML)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/analyze-frames")
async def analyze_frames(payload: FramesPayload):
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise HTTPException(status_code=400, detail="Clé API Anthropic manquante.")
    if not payload.frames:
        raise HTTPException(status_code=400, detail="Aucune frame reçue.")

    loop = asyncio.get_event_loop()
    try:
        result = await asyncio.wait_for(
            loop.run_in_executor(None, analyze_video, payload.frames, None),
            timeout=30.0,
        )
        result["frames_analyzed"] = len(payload.frames)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Analyse trop longue. Réessaie.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
