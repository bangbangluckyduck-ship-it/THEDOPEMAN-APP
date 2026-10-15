"""Images de partage (Open Graph) des guides du blog : une par guide et par langue.

Ce que LinkedIn, WhatsApp, X ou Slack affichent quand on colle le lien d'un
guide. Sans elles, les trente pages se partageaient avec le même logo.

Les images sont générées ICI, à la main, puis versionnées dans static/og/ —
pas au démarrage du serveur : Render n'a pas les polices, et une image de
partage n'a aucune raison d'être recalculée à chaque déploiement.

À relancer après avoir ajouté un guide ou modifié son titre :
    venv\\Scripts\\python.exe generate_og_images.py

test_blog_articles.py échoue si une image manque.
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

import blog_articles

SORTIE = Path("static/og")
LARGEUR, HAUTEUR = 1200, 630
NAVY, ACCENT, OR, BLANC = (31, 58, 112), (37, 99, 235), (212, 175, 55), (255, 255, 255)

# Polices système, la première trouvée gagne. Non versionnées : leurs licences
# n'autorisent pas la redistribution, et elles ne servent qu'à la génération.
GRAS = ["C:/Windows/Fonts/segoeuib.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
NORMAL = ["C:/Windows/Fonts/segoeui.ttf", "/System/Library/Fonts/Supplemental/Arial.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]

SIGNATURE = {
    "fr": "Analyse de vidéos TikTok Shop par IA",
    "en": "AI video analysis for TikTok Shop",
    "pt-br": "Análise de vídeos do TikTok Shop com IA",
    "es": "Análisis de vídeos de TikTok Shop con IA",
    "it": "Analisi dei video TikTok Shop con l'IA",
    "de": "KI-Videoanalyse für TikTok Shop",
}


def police(candidats: "list[str]", taille: int) -> ImageFont.FreeTypeFont:
    for c in candidats:
        if Path(c).exists():
            return ImageFont.truetype(c, taille)
    raise SystemExit("Aucune police trouvée — ajouter un chemin dans GRAS/NORMAL.")


def fond() -> Image.Image:
    """Dégradé diagonal navy → bleu, comme les encadrés d'appel à l'action du site."""
    petit = Image.new("RGB", (2, 2))
    petit.putdata([NAVY, NAVY, NAVY, ACCENT])
    return petit.resize((LARGEUR, HAUTEUR), Image.BILINEAR)


def couper(texte: str, f: ImageFont.FreeTypeFont, largeur: int) -> "list[str]":
    lignes, ligne = [], ""
    for mot in texte.split():
        essai = f"{ligne} {mot}".strip()
        if f.getlength(essai) <= largeur:
            ligne = essai
        else:
            lignes.append(ligne)
            ligne = mot
    lignes.append(ligne)
    return lignes


def titre_ajuste(texte: str) -> "tuple[ImageFont.FreeTypeFont, list[str]]":
    """La plus grande taille qui tient en quatre lignes."""
    for taille in (68, 62, 56, 50, 46):
        f = police(GRAS, taille)
        lignes = couper(texte, f, LARGEUR - 160)
        if len(lignes) <= 4:
            return f, lignes
    return f, lignes[:4]


def image(categorie: str, titre: str, signature: str) -> Image.Image:
    img = fond()
    d = ImageDraw.Draw(img)

    # Pastille de catégorie (sans l'émoji : les polices système ne le rendent pas).
    cat = categorie.split(" ", 1)[-1] if not categorie[0].isalnum() else categorie
    f_cat = police(GRAS, 26)
    l = f_cat.getlength(cat)
    d.rounded_rectangle((80, 70, 80 + l + 44, 70 + 50), radius=25, fill=OR)
    d.text((80 + 22, 70 + 25), cat, font=f_cat, fill=NAVY, anchor="lm")

    f_titre, lignes = titre_ajuste(titre)
    pas = int(f_titre.size * 1.18)
    y = 160 + (4 - len(lignes)) * pas // 2
    for ligne in lignes:
        d.text((80, y), ligne, font=f_titre, fill=BLANC)
        y += pas

    # Pied : logo, nom, signature.
    logo = Image.open("static/qeerah-logo-128.png").convert("RGBA").resize((76, 76))
    img.paste(logo, (80, HAUTEUR - 76 - 52), logo)
    d.text((176, HAUTEUR - 52 - 52), "Qeerah", font=police(GRAS, 34), fill=BLANC, anchor="lm")
    d.text((176, HAUTEUR - 52 - 18), signature, font=police(NORMAL, 24),
           fill=(214, 224, 245), anchor="lm")
    d.line((80, HAUTEUR - 150, LARGEUR - 80, HAUTEUR - 150), fill=(255, 255, 255, 60), width=1)
    return img


def main() -> None:
    SORTIE.mkdir(parents=True, exist_ok=True)
    for a in blog_articles.charger():
        for lang in blog_articles.LANGUES_REDIGEES:
            if lang not in a.corps:
                continue
            m = a.langues[lang]
            chemin = SORTIE / blog_articles.nom_image_og(a.id, lang)
            image(m["categorie"], m["h1"], SIGNATURE[lang]).save(
                chemin, "JPEG", quality=86, optimize=True, progressive=True)
            print(f"{chemin}  ({chemin.stat().st_size // 1024} Ko)")


if __name__ == "__main__":
    main()
