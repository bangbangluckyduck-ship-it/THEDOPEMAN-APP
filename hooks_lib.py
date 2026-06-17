from __future__ import annotations

"""
FEATURE 1 — Banque de Hooks : logique d'accès (100 % serveur, jamais de
confiance dans le front) + helpers de payload.

Règle produit (choix utilisateur) : FREE = tout verrouillé. Le champ
`type_acces` d'un hook ne discrimine donc QUE les plans payants.
"""

# Rang des plans pour comparer "à partir de X"
TIER_RANK = {"free": 0, "pro": 1, "gold": 2, "agency": 3, "beta": 9, "admin": 9}

# Catégories produit (alignées sur la détection existante de l'analyse + spec)
HOOK_CATEGORIES = [
    "sante", "beaute", "mode", "tech", "fitness", "maison", "mobilier", "food", "autre",
]

CATEGORY_LABELS = {
    "sante": "Santé / Bien-être", "beaute": "Beauté / Cosmétique", "mode": "Mode / Vêtements",
    "tech": "Tech / Gadgets", "fitness": "Fitness / Sport", "maison": "Maison / Déco",
    "mobilier": "Mobilier", "food": "Food / Cuisine", "autre": "Autre",
}

PLAN_LABELS = {"pro": "PRO", "gold": "GOLD", "agency": "AGENCY"}


def can_access(tier: str | None, hook: dict) -> bool:
    """Le tier courant a-t-il accès au contenu de ce hook ?"""
    tier = (tier or "free").lower()
    if tier in ("admin", "beta"):
        return True
    if TIER_RANK.get(tier, 0) <= 0:          # FREE → tout verrouillé
        return False
    ta = (hook.get("type_acces") or "plan_minimum").lower()
    if ta == "tous":                         # tous les plans PAYANTS
        return True
    if ta == "plan_minimum":
        need = (hook.get("plan_min") or "pro").lower()
        return TIER_RANK.get(tier, 0) >= TIER_RANK.get(need, 1)
    if ta == "plans_specifiques":
        allowed = [str(p).lower() for p in (hook.get("plans_autorises") or [])]
        return tier in allowed
    return False


def required_label(hook: dict) -> str:
    """Libellé du plan requis (pour l'état verrouillé / incitation upgrade)."""
    ta = (hook.get("type_acces") or "plan_minimum").lower()
    if ta == "plan_minimum":
        return f"À partir de {PLAN_LABELS.get((hook.get('plan_min') or 'pro').lower(), 'PRO')}"
    if ta == "plans_specifiques":
        labels = [PLAN_LABELS.get(str(p).lower(), str(p).upper()) for p in (hook.get("plans_autorises") or [])]
        return "Réservé : " + (", ".join(labels) if labels else "plan supérieur")
    return "Réservé aux abonnés"


def public_payload(hook: dict, tier: str | None) -> dict:
    """Payload renvoyé au front : le texte/vidéo n'est exposé QUE si accès."""
    accessible = can_access(tier, hook)
    out = {
        "id": hook.get("id"),
        "categorie": hook.get("categorie"),
        "has_video": bool(hook.get("url_video")),
        "locked": not accessible,
    }
    if accessible:
        out["texte"] = hook.get("texte")
        out["url_video"] = hook.get("url_video")
    else:
        out["required"] = required_label(hook)
    return out
