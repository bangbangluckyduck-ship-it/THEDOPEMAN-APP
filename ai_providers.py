"""
🔀 Couche IA multi-fournisseurs (migration Mistral → Gemini + Claude, hybride + fallback).

Deux tiers :
- VISION (analyse vidéo/image) : Gemini 3.5 Flash si GEMINI_API_KEY, sinon Mistral pixtral.
- TEXTE (rédaction/plans)      : Claude Sonnet 4.6 si ANTHROPIC_API_KEY, sinon Mistral small.

TOLÉRANT AUX PANNES : si le fournisseur principal échoue (clé absente, erreur API,
package non installé, JSON cassé), on retombe AUTOMATIQUEMENT sur Mistral. Sans aucune
clé Gemini/Claude → comportement 100% identique à aujourd'hui. Réversible via env
AI_VISION_PROVIDER / AI_TEXT_PROVIDER (auto | gemini | claude | mistral).

Entrée commune : « content blocks » au format Mistral/OpenAI
  [{"type":"text","text":...}, {"type":"image_url","image_url":{"url":"data:..|https:.."}}]
ou un simple str (prompt). Sortie : texte brut (le caller fait son propre _extract_json).
"""
from __future__ import annotations

import base64
import os
from typing import Any, Optional

import httpx

# IDs modèles (overridables par env, sans redéploiement)
GEMINI_VISION_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
# Vidéo native (audio + visuel). Flash et non Pro, pour DEUX raisons distinctes :
# la vitesse, et surtout la disponibilité — la capacité Pro est la plus disputée
# chez Google, c'est elle qui renvoie « high demand » en premier lors des pics.
# Passer à Flash améliore donc à la fois le délai ET le taux de réussite.
# Repasser en Pro = variable GEMINI_VIDEO_MODEL sur Render, sans redéploiement.
GEMINI_VIDEO_MODEL = os.getenv("GEMINI_VIDEO_MODEL", "gemini-2.5-flash")
CLAUDE_TEXT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
CLAUDE_HAIKU_MODEL = os.getenv("CLAUDE_HAIKU_MODEL", "claude-haiku-4-5-20251001")
MISTRAL_VISION_MODEL = "pixtral-12b-2409"
MISTRAL_TEXT_MODEL = "mistral-small-latest"

# Dernier fournisseur réellement utilisé par tier (diagnostic /api/_admin/ai-selftest)
_LAST: dict = {"vision": None, "text": None}


def last_providers() -> dict:
    return dict(_LAST)


# Signatures d'une panne PASSAGÈRE côté fournisseur (saturation, capacité,
# quota instantané) — par opposition à une erreur de notre requête, qu'il ne
# sert à rien de rejouer. Rejouer à l'identique n'a de sens que pour celles-ci.
_TRANSIENT_MARKERS = ("503", "unavailable", "overload", "high demand",
                      "resource_exhausted", "429")


def _is_transient(e: Exception) -> bool:
    msg = str(e).lower()
    return any(m in msg for m in _TRANSIENT_MARKERS)


def _video_failure(err: Optional[Exception]) -> Exception:
    """Échec définitif d'analyse vidéo, formulé pour l'utilisateur final.

    Ce texte part TEL QUEL dans l'email d'échec (analysis_runner._send_error_email
    en encadre `str(e)` en rouge). Il ne doit donc contenir ni code HTTP, ni JSON,
    ni nom de fournisseur — seulement ce que le destinataire peut en faire. Le
    détail technique n'est pas perdu : on chaîne la cause avec `from`, Sentry la
    conserve dans l'incident.
    """
    if err is not None and _is_transient(err):
        return Exception("Le service d'analyse est saturé en ce moment — ça vient de "
                         "leur côté, pas de ta vidéo. Relance l'analyse dans quelques "
                         "minutes, elle devrait passer.")
    return Exception("L'analyse de cette vidéo n'a pas abouti. Relance-la ; si ça se "
                     "reproduit, envoie-nous le lien et on regarde.")


def any_ai_key() -> bool:
    """Au moins un fournisseur IA est configuré (sinon les features IA sont indispo)."""
    return bool(os.getenv("MISTRAL_API_KEY") or os.getenv("GEMINI_API_KEY")
                or os.getenv("ANTHROPIC_API_KEY"))


# ── Normalisation des blocks ─────────────────────────────────────────────────
def _blocks(content: Any) -> list:
    """Normalise l'entrée en liste de content-blocks. str → un bloc texte.
    Format messages ([{role, content}]) → on prend le content du dernier message."""
    if isinstance(content, str):
        return [{"type": "text", "text": content}]
    if isinstance(content, list) and content and isinstance(content[0], dict) and "role" in content[0]:
        return _blocks(content[-1].get("content"))
    return content or []


def _to_messages(content: Any) -> list:
    if isinstance(content, list) and content and isinstance(content[0], dict) and "role" in content[0]:
        return content
    return [{"role": "user", "content": content}]


def _img_bytes_and_mime(url: str):
    """data URI → (bytes, mime). http(s) → fetch → (bytes, mime)."""
    if url.startswith("data:"):
        head, b64 = url.split(",", 1)
        mime = head[5:].split(";")[0] or "image/jpeg"
        return base64.b64decode(b64), mime
    r = httpx.get(url, timeout=20.0, follow_redirects=True, headers={"User-Agent": "Mozilla/5.0"})
    r.raise_for_status()
    mime = (r.headers.get("content-type") or "image/jpeg").split(";")[0]
    return r.content, mime


# ── Mistral (fallback universel) ─────────────────────────────────────────────
def _mistral_chat(model: str, content: Any, timeout: float,
                  temperature: Optional[float] = None, seed: Optional[int] = None) -> str:
    key = os.getenv("MISTRAL_API_KEY")
    if not key:
        raise RuntimeError("MISTRAL_API_KEY manquant")
    body: dict = {"model": model, "messages": _to_messages(content)}
    if temperature is not None:
        body["temperature"] = temperature
    if seed is not None:
        body["random_seed"] = seed
    r = httpx.post("https://api.mistral.ai/v1/chat/completions",
                   headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                   json=body, timeout=timeout)
    if not r.is_success:
        raise Exception(f"Mistral {r.status_code}: {r.text[:300]}")
    return r.json()["choices"][0]["message"]["content"]


# ── Gemini 3.5 Flash (vision) ────────────────────────────────────────────────
def _gemini_vision(content: Any, timeout: float, temperature: Optional[float] = None) -> str:
    from google import genai
    from google.genai import types as gt
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),
                          http_options=gt.HttpOptions(timeout=int(timeout * 1000)))
    parts = []
    for b in _blocks(content):
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            parts.append(gt.Part.from_text(text=b.get("text", "")))
        elif b.get("type") == "image_url":
            url = (b.get("image_url") or {}).get("url", "")
            if url:
                data, mime = _img_bytes_and_mime(url)
                parts.append(gt.Part.from_bytes(data=data, mime_type=mime))
    cfg = gt.GenerateContentConfig(temperature=temperature) if temperature is not None else None
    resp = client.models.generate_content(model=GEMINI_VISION_MODEL, contents=parts, config=cfg)
    return resp.text or ""


# ── Gemini Pro (VIDÉO native + audio) ────────────────────────────────────────
def _gemini_video(video_path: str, prompt: str, timeout: float,
                  temperature: Optional[float] = None) -> str:
    """Envoie la vidéo entière (mp4) à Gemini Pro pour analyse multimodale
    native — vision + audio dans un seul appel. Pas d'extraction de frames,
    pas de transcription audio séparée.

    Gemini Pro voit le rythme, les transitions, écoute la piste audio,
    repère les CTA en fin de vidéo (visuels + audio) en un seul passage.

    Inline pour vidéos < 20 MB, Files API au-delà (TikTok Shop max 60s
    en 720p reste largement sous la limite inline).
    """
    from google import genai
    from google.genai import types as gt
    import time as _t
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"),
                          http_options=gt.HttpOptions(timeout=int(timeout * 1000)))

    # L'upload et le sondage d'état étaient les SEULS appels Gemini sans filet :
    # generate_content avait sa cascade de retries, mais un 503 « high demand »
    # pendant l'upload tuait le job instantanément, sans une seule reprise. Or
    # une saturation côté Google touche tous les endpoints en même temps — c'est
    # précisément au pire moment que l'étape la plus fragile n'était pas protégée.
    def _retry_transient(fn, what: str, attempts: int = 4):
        """Rejoue fn() sur saturation/indispo Google (503, 429, overload)."""
        delay = 2
        for i in range(attempts):
            try:
                return fn()
            except Exception as e:
                if not _is_transient(e) or i == attempts - 1:
                    raise
                print(f"[ai] {what} : {type(e).__name__} transitoire, "
                      f"nouvelle tentative dans {delay}s ({i + 1}/{attempts - 1})")
                _t.sleep(delay)
                delay *= 2

    # Toujours Files API : ne charge JAMAIS la vidéo en mémoire Python (Render
    # starter = 512 MB RAM, on doit éviter `f.read()` sur des fichiers vidéo qui
    # font 10-30 MB et risquent l'OOM quand combinés au reste de l'app).
    uploaded = _retry_transient(
        lambda: client.files.upload(file=video_path, config={"mime_type": "video/mp4"}),
        "upload vidéo")

    # Attente du passage à l'état ACTIVE — Google a besoin de quelques secondes
    # pour traiter la vidéo après upload. Sans ça, generate_content renvoie
    # 400 FAILED_PRECONDITION "File X is not in an ACTIVE state".
    _wait = 0
    while True:
        state = getattr(uploaded, "state", None)
        state_name = getattr(state, "name", str(state)) if state else "UNKNOWN"
        if state_name == "ACTIVE":
            break
        if state_name == "FAILED":
            raise Exception("Gemini Files API : traitement vidéo échoué")
        if _wait >= 60:
            raise Exception(f"Gemini Files API : timeout (état toujours {state_name} après 60s)")
        _t.sleep(2)
        _wait += 2
        uploaded = _retry_transient(lambda: client.files.get(name=uploaded.name),
                                    "état fichier", attempts=3)

    video_part = gt.Part.from_uri(file_uri=uploaded.uri, mime_type="video/mp4")
    parts = [video_part, gt.Part.from_text(text=prompt)]

    # Config de base : temperature
    base_kwargs = {}
    if temperature is not None:
        base_kwargs["temperature"] = temperature

    # Modèles à tester en cascade :
    # 1. Modèle primaire (Pro 2.5 par défaut, qualité max — cf. GEMINI_VIDEO_MODEL)
    # 2. Fallback Flash 2.0 (plus ancien, généralement plus stable côté capacité)
    # Override possible par env GEMINI_VIDEO_FALLBACK_MODEL.
    fallback_model = os.getenv("GEMINI_VIDEO_FALLBACK_MODEL", "gemini-2.0-flash")
    models_to_try = [GEMINI_VIDEO_MODEL]
    if fallback_model and fallback_model != GEMINI_VIDEO_MODEL:
        models_to_try.append(fallback_model)

    # VITESSE : par défaut on COUPE le raisonnement du modèle. Décrire ce qui se
    # passe dans une vidéo est une tâche d'observation, pas de déduction — le
    # raisonnement n'y ajoute presque rien et double le temps de réponse.
    # Deux garde-fous appris à nos dépens :
    #   - les modèles Pro REFUSENT budget 0 (400 « This model only works in
    #     thinking mode ») : on ne le leur envoie jamais, ils gardent leur mode
    #     dynamique — raison de plus pour ne pas les mettre en primaire ;
    #   - GEMINI_VIDEO_THINKING_BUDGET permet de forcer un réglage :
    #     0 = coupé (défaut), -1 = dynamique, 128-32768 = budget fixe.
    _budget_env = (os.getenv("GEMINI_VIDEO_THINKING_BUDGET", "") or "").strip()
    try:
        thinking_budget = int(_budget_env) if _budget_env else 0
    except ValueError:
        thinking_budget = 0

    def _thinking_for(model_name: str) -> Optional[int]:
        """Budget applicable à ce modèle, ou None s'il ne faut rien envoyer."""
        if "pro" in model_name.lower():
            return None
        return thinking_budget

    def _try_call(model_name: str):
        """Appel generate_content ; retry sans ThinkingConfig si le modèle le rejette."""
        budget = _thinking_for(model_name)
        if budget is None:
            cfg = gt.GenerateContentConfig(**base_kwargs) if base_kwargs else None
            return client.models.generate_content(model=model_name, contents=parts, config=cfg)
        try:
            thinking_cfg = gt.ThinkingConfig(thinking_budget=budget)
            cfg = gt.GenerateContentConfig(thinking_config=thinking_cfg, **base_kwargs)
            return client.models.generate_content(model=model_name, contents=parts, config=cfg)
        except Exception as e:
            if "thinking" in str(e).lower() or "budget" in str(e).lower():
                # Le modèle n'accepte pas ce réglage → on le laisse décider seul.
                cfg = gt.GenerateContentConfig(**base_kwargs) if base_kwargs else None
                return client.models.generate_content(model=model_name, contents=parts, config=cfg)
            raise

    # Plafond de temps GLOBAL sur la cascade. Sans lui : 3 tentatives × 2 modèles
    # × le timeout par appel = jusqu'à 12 minutes sur un job condamné, qui
    # monopolise pendant tout ce temps l'un des 2 créneaux d'analyse simultanés.
    # Quand Google sature, s'acharner ne sauve presque rien et propage la panne
    # aux autres utilisateurs : on abandonne vite et on invite à relancer.
    # 90s : une saturation se manifeste par un refus IMMÉDIAT (503 en moins d'une
    # seconde), pas par une lenteur — la cascade complète des deux modèles tient
    # donc largement dans ce budget et rien n'est sacrifié côté fiabilité. Ce
    # plafond ne borne en réalité qu'un seul cas : un appel qui se fige.
    # Il n'interrompt JAMAIS un appel en cours : il empêche seulement d'en
    # démarrer un nouveau. Une analyse lente mais qui va aboutir aboutit.
    deadline = _t.monotonic() + float(os.getenv("VIDEO_ANALYSIS_DEADLINE", "90"))

    last_err = None
    for model_name in models_to_try:
        # 2 tentatives par modèle, reprise courte, puis on passe au suivant.
        for delay in (0, 1.5):
            if _t.monotonic() >= deadline:
                break
            if delay:
                _t.sleep(delay)
            try:
                resp = _try_call(model_name)
                return resp.text or ""
            except Exception as e:
                last_err = e
                if _is_transient(e):
                    continue
                # Erreur non-récupérable → on passe au modèle suivant directement
                break
        if _t.monotonic() >= deadline:
            break
    # Message lisible pour l'utilisateur (il le reçoit par email), cause technique
    # chaînée pour Sentry. Avant, c'est « 503 UNAVAILABLE. {'error': {...}} » qui
    # partait dans l'email d'échec d'un client payant.
    raise _video_failure(last_err) from last_err


# ── Claude Sonnet 4.6 (texte, multimodal possible) ───────────────────────────
def _claude_text(content: Any, timeout: float, max_tokens: int = 4096,
                 temperature: Optional[float] = None, model: Optional[str] = None) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"), timeout=timeout)
    cblocks = []
    for b in _blocks(content):
        if not isinstance(b, dict):
            continue
        if b.get("type") == "text":
            cblocks.append({"type": "text", "text": b.get("text", "")})
        elif b.get("type") == "image_url":
            url = (b.get("image_url") or {}).get("url", "")
            if url.startswith("data:"):
                head, b64 = url.split(",", 1)
                mime = head[5:].split(";")[0] or "image/jpeg"
                cblocks.append({"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}})
            elif url:
                cblocks.append({"type": "image", "source": {"type": "url", "url": url}})
    if not cblocks:
        cblocks = [{"type": "text", "text": ""}]
    kwargs: dict = {"model": model or CLAUDE_TEXT_MODEL, "max_tokens": max_tokens,
                    "messages": [{"role": "user", "content": cblocks}]}
    if temperature is not None:
        kwargs["temperature"] = temperature
    msg = client.messages.create(**kwargs)
    return "".join(p.text for p in msg.content if getattr(p, "type", "") == "text")


# ── Résolution du fournisseur ────────────────────────────────────────────────
def _resolve(tier: str) -> str:
    env_name = "AI_VISION_PROVIDER" if tier == "vision" else "AI_TEXT_PROVIDER"
    choice = (os.getenv(env_name, "auto") or "auto").lower()
    if choice in ("mistral", "gemini", "claude"):
        return choice
    if tier == "vision":
        return "gemini" if os.getenv("GEMINI_API_KEY") else "mistral"
    return "claude" if os.getenv("ANTHROPIC_API_KEY") else "mistral"


# ── API publique ─────────────────────────────────────────────────────────────
def vision_complete(content: Any, timeout: float = 60.0,
                    temperature: Optional[float] = None, seed: Optional[int] = None,
                    provider: Optional[str] = None) -> str:
    """Analyse multimodale (frames vidéo / image produit + texte).
    Gemini 3.5 Flash si dispo, sinon Mistral pixtral. Fallback auto sur erreur.
    `provider` force un fournisseur ('mistral' / 'gemini')."""
    chosen = provider if provider in ("mistral", "gemini") else _resolve("vision")
    if chosen == "gemini":
        try:
            out = _gemini_vision(content, timeout, temperature=temperature)
            if out and out.strip():
                _LAST["vision"] = "gemini:" + GEMINI_VISION_MODEL
                return out
            raise Exception("réponse Gemini vide")
        except Exception as e:
            print(f"[ai] Gemini vision KO → fallback Mistral : {e}")
    out = _mistral_chat(MISTRAL_VISION_MODEL, content, timeout, temperature=temperature, seed=seed)
    _LAST["vision"] = "mistral:" + MISTRAL_VISION_MODEL
    return out


def video_complete(video_path: str, prompt: str, timeout: float = 90.0,
                   temperature: Optional[float] = None) -> str:
    """Analyse vidéo NATIVE via Gemini Pro (visuel + audio, un seul appel).
    Plus précis qu'une analyse de frames extraites + transcription séparée.

    Lève une exception si Gemini KO — pas de fallback automatique car les autres
    providers ne supportent pas la vidéo native. L'appelant peut retomber sur le
    pipeline frames+transcription si besoin."""
    out = _gemini_video(video_path, prompt, timeout, temperature=temperature)
    if not out or not out.strip():
        raise Exception("réponse Gemini vidéo vide")
    _LAST["vision"] = "gemini-video:" + GEMINI_VIDEO_MODEL
    return out


def text_complete(content: Any, timeout: float = 60.0, max_tokens: int = 8192,
                  temperature: Optional[float] = None, model: Optional[str] = None,
                  provider: Optional[str] = None) -> str:
    """Rédaction d'analyses / plans (texte, image éventuelle). Claude si dispo, sinon
    Mistral small. `model` force un modèle Claude précis (ex. Haiku pour la vitesse).
    `provider` force un fournisseur ('mistral' / 'claude') — utile en secours."""
    chosen = provider if provider in ("mistral", "claude") else _resolve("text")
    if chosen == "claude":
        try:
            out = _claude_text(content, timeout, max_tokens=max_tokens, temperature=temperature, model=model)
            if out and out.strip():
                _LAST["text"] = "claude:" + CLAUDE_TEXT_MODEL
                return out
            raise Exception("réponse Claude vide")
        except Exception as e:
            print(f"[ai] Claude texte KO → fallback Mistral : {e}")
    out = _mistral_chat(MISTRAL_TEXT_MODEL, content, timeout, temperature=temperature)
    _LAST["text"] = "mistral:" + MISTRAL_TEXT_MODEL
    return out
