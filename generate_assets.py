"""Generate PWA icons and QR code. Called at server startup."""
from __future__ import annotations
import io
import base64
import socket
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont


def _local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return socket.gethostbyname(socket.gethostname())


def make_icon(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Dark rounded background
    r = size // 5
    draw.rounded_rectangle([0, 0, size, size], radius=r, fill="#0d1220")

    # Royal blue outer ring
    pad = size // 12
    draw.ellipse([pad, pad, size - pad, size - pad], fill="#2952cc")

    # Slightly smaller darker blue inner circle
    pad2 = size // 6
    draw.ellipse([pad2, pad2, size - pad2, size - pad2], fill="#1a3a9e")

    # Gold ring accent
    ring = size // 7
    draw.ellipse([ring, ring, size - ring, size - ring], outline="#d4af37",
                 width=max(2, size // 32))

    # Gold play triangle
    cx, cy = size // 2, size // 2
    half = size // 5
    draw.polygon([
        (cx - half + size // 20, cy - half),
        (cx - half + size // 20, cy + half),
        (cx + half + size // 20, cy),
    ], fill="#d4af37")

    return img


def generate_icons():
    static = Path(__file__).parent / "static"
    static.mkdir(exist_ok=True)

    # ── Front office (PWA Qeerah) : icon-192/512 sont commités dans le repo
    # depuis le rebrand. On ne les régénère QUE s'ils sont absents (fresh clone)
    # — sinon on écraserait la version Qeerah avec un fallback "play button".
    logo = static / "qeerah-logo.png"
    for sz in (192, 512):
        out = static / f"icon-{sz}.png"
        if out.exists() or not logo.exists():
            continue
        img = Image.open(logo).convert("RGBA").resize((sz, sz), Image.LANCZOS)
        img.save(out, "PNG")

    # ── Back office (Dope Admin) : même logo Qeerah (l'ancien logo.png
    # distinctif a été supprimé lors du rebrand).
    for sz in (192, 512):
        out = static / f"admin-icon-{sz}.png"
        if out.exists() or not logo.exists():
            continue
        img = Image.open(logo).convert("RGBA").resize((sz, sz), Image.LANCZOS)
        img.save(out, "PNG")


def generate_qr_b64(url: str) -> str:
    import qrcode
    qr = qrcode.QRCode(box_size=8, border=2,
                       error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0a0a0a", back_color="white")
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return base64.b64encode(buf.getvalue()).decode()


def get_app_url() -> str:
    return f"http://{_local_ip()}:8000"


if __name__ == "__main__":
    generate_icons()
    print("Icons generated.")
