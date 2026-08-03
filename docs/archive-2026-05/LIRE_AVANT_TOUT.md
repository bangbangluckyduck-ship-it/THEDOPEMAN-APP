# ⚠️ Documentation périmée — mai 2026

**Ne pas se fier au contenu de ce dossier.** Il décrit une architecture qui
n'existe plus, et il a été déplacé ici précisément parce qu'il induisait en
erreur quiconque ouvrait le dépôt — humain comme assistant.

Ce qui a changé depuis, et que ces fichiers ignorent :

| Le dossier décrit | La réalité aujourd'hui |
|---|---|
| Analyse par extraction d'images + transcription, moteur Mistral | Analyse vidéo native (le modèle voit et entend la vidéo entière) puis synthèse par un second modèle |
| Analyse synchrone en streaming | Jobs asynchrones (`analysis_jobs`, `analysis_runner`), notification par e-mail, « Mes analyses » multi-appareils |
| Grille à quatre paliers avec lancement échelonné | Offre unique **Qeerah Pro** — 29,99 €/mois ou 299 €/an, essai 7 jours |
| Historique des analyses en `localStorage` | Persistance en base, consultable depuis n'importe quel appareil |
| Marque « TikTok Shop Vidéo Analyzer » / « TTS Analyzer » | **Qeerah** (rebrand imposé par une plainte pour marque — l'ancien nom ne doit réapparaître nulle part) |
| Quota au mois calendaire | Quota par cycle de facturation Stripe (`analysis_quota.py`) |

## Où trouver l'information à jour

- **Architecture et décisions** : `WORKLOG.md` à la racine.
- **Fournisseur de données** : `DATA_API_BRIEF.md`.
- **Contenu du site** (prix, promesse d'essai, mentions légales) : `site_content.py`
  — source de vérité unique, à lire plutôt que n'importe quelle doc.
- **Ce qui est réellement testé** : `test_parcours_critique.py`.

Ces fichiers sont conservés pour l'historique du projet, pas comme référence.
