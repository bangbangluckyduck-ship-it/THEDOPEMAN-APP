"""Build des assets statiques (favicon multi-résolution + minification JS).

À lancer après chaque modification d'un gros fichier JS servi au client :

    python build_assets.py

Produit :
  • static/favicon.ico       → vrai .ico multi-résolution (16/32/48 px, quelques Ko)
  • static/<name>.min.js      → versions minifiées des JS volumineux

main.py sert automatiquement la version .min.js quand elle existe (sinon il retombe
sur le fichier original) : la minification est donc optionnelle et sans risque de
casse — si ce script n'a pas tourné, l'app fonctionne avec les fichiers d'origine.
"""
from __future__ import annotations
from pathlib import Path

STATIC = Path(__file__).parent / "static"

# JS à minifier (fichiers servis au navigateur). On garde l'original ; on écrit à côté.
JS_TO_MINIFY = ["app_v3.js", "app_v2.js", "admin.js"]

# Source haute qualité pour le favicon (logo carré 512×512).
FAVICON_SOURCE = STATIC / "qeerah-logo.png"
FAVICON_SIZES = [16, 32, 48]


def build_favicon() -> None:
    from PIL import Image
    src = Image.open(FAVICON_SOURCE).convert("RGBA")
    out = STATIC / "favicon.ico"
    # Pillow génère un .ico contenant toutes les tailles demandées.
    src.save(out, format="ICO", sizes=[(s, s) for s in FAVICON_SIZES])
    print(f"✓ favicon.ico généré ({', '.join(str(s) for s in FAVICON_SIZES)} px) — {out.stat().st_size} o")


def minify_js() -> None:
    from rjsmin import jsmin
    for name in JS_TO_MINIFY:
        src = STATIC / name
        if not src.exists():
            print(f"· {name} absent — ignoré")
            continue
        original = src.read_text(encoding="utf-8")
        minified = jsmin(original)
        out = src.with_suffix(".min.js")
        out.write_text(minified, encoding="utf-8")
        gain = 100 * (1 - len(minified) / max(1, len(original)))
        print(f"✓ {out.name} — {len(original)} → {len(minified)} o (-{gain:.0f}%)")


if __name__ == "__main__":
    build_favicon()
    minify_js()
