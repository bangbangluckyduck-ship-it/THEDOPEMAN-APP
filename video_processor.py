from __future__ import annotations
import subprocess
import os
import re
import base64
import tempfile
from typing import List, Optional


def _ffmpeg() -> str:
    # Use system ffmpeg (installed via apt on Render)
    return "ffmpeg"


def get_duration(video_path: str) -> float:
    result = subprocess.run(
        [_ffmpeg(), "-i", video_path, "-hide_banner"],
        capture_output=True, text=True
    )
    match = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", result.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 0.0


def extract_frames(video_path: str, num_frames: int = 12) -> List[str]:
    """Extract evenly-spaced frames with extra density at start (hook) and end (CTA)."""
    duration = get_duration(video_path)
    if duration <= 0:
        duration = 30.0

    timestamps: List[float] = []

    # Hook: first 3 seconds (3 frames)
    for i in range(3):
        timestamps.append(min(i * 1.0, duration - 0.1))

    # Middle content
    mid = num_frames - 5
    for i in range(mid):
        t = 3.0 + (max(duration - 5.0, 0.1)) * i / max(mid - 1, 1)
        timestamps.append(min(t, duration - 0.1))

    # CTA: last 2 seconds (2 frames)
    timestamps.append(max(duration - 2.0, 0.1))
    timestamps.append(max(duration - 0.5, 0.1))

    frames: List[str] = []
    for ts in timestamps[:num_frames]:
        with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
            tmp_path = tmp.name

        subprocess.run(
            [
                _ffmpeg(), "-ss", str(ts), "-i", video_path,
                "-vframes", "1", "-q:v", "3",
                "-vf", "scale=480:-2",
                "-y", tmp_path,
            ],
            capture_output=True,
        )

        if os.path.exists(tmp_path) and os.path.getsize(tmp_path) > 0:
            with open(tmp_path, "rb") as f:
                frames.append(base64.b64encode(f.read()).decode())
            os.unlink(tmp_path)

    return frames


def extract_audio(video_path: str) -> Optional[str]:
    """Extract audio as 16kHz mono WAV. Returns temp file path or None."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name

    subprocess.run(
        [
            _ffmpeg(), "-i", video_path,
            "-ar", "16000", "-ac", "1",
            "-y", audio_path,
        ],
        capture_output=True,
    )

    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 100:
        return audio_path
    return None
