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

    # Rounded background gradient (simulate with two rects)
    r = size // 6
    draw.rounded_rectangle([0, 0, size, size], radius=r, fill="#0a0a0a")

    # Pink glow circle
    pad = size // 8
    draw.ellipse([pad, pad, size - pad, size - pad], fill="#fe2c55")

    # Cyan accent circle (offset)
    off = size // 10
    draw.ellipse([pad + off, pad + off, size - pad + off, size - pad + off],
                 fill="#25f4ee")

    # Re-draw pink on top slightly smaller for overlap effect
    inner = size // 5
    draw.ellipse([inner, inner, size - inner, size - inner], fill="#fe2c55")

    # Play triangle
    cx, cy = size // 2, size // 2
    half = size // 5
    draw.polygon([
        (cx - half + 4, cy - half),
        (cx - half + 4, cy + half),
        (cx + half + 4, cy),
    ], fill="white")

    return img


def generate_icons():
    static = Path(__file__).parent / "static"
    for sz in (192, 512):
        path = static / f"icon-{sz}.png"
        if not path.exists():
            make_icon(sz).save(path, "PNG")


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
