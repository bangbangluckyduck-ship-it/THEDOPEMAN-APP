"""
Service d'emails transactionnels — SMTP Hostinger via bibliothèques natives Python.

Aucune dépendance externe (smtplib + email.mime), connexion SSL (port 465).
Toutes les fonctions sont robustes : une erreur d'envoi est loguée mais ne fait
jamais planter l'appelant (inscription, reset, etc.).

Variables d'environnement (configurées sur Render) :
  SMTP_SERVER    (défaut "smtp.hostinger.com")
  SMTP_PORT      (défaut 465 — SSL)
  SMTP_USERNAME  (ex. contact@qeerah.com)
  SMTP_PASSWORD  (jamais hardcodé)
  SMTP_FROM_NAME (défaut "Qeerah")
"""

import os
import ssl
import smtplib
import logging
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

# Sur Render/uvicorn, aucun handler n'est attaché à nos loggers custom : par
# défaut seuls les WARNING+ remontent (les INFO de succès sont masqués). On
# attache un StreamHandler dédié pour garantir la visibilité des logs d'envoi.
if not logger.handlers:
    _h = logging.StreamHandler()
    _h.setFormatter(logging.Formatter("%(levelname)s:%(name)s:%(message)s"))
    logger.addHandler(_h)
    logger.setLevel(logging.INFO)
    logger.propagate = False

_executor = ThreadPoolExecutor(max_workers=2)

# ── Configuration SMTP (lue depuis l'environnement, aucun secret hardcodé) ──
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.hostinger.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "465"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "contact@qeerah.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "Qeerah")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", SMTP_USERNAME)

# Le service est « actif » uniquement si un mot de passe SMTP est fourni.
SMTP_ENABLED = bool(SMTP_PASSWORD)

# ── Resend (transport PRIORITAIRE si RESEND_API_KEY est posée sur Render) ──
# ⚠️ `from` doit être sur un domaine VÉRIFIÉ dans Resend, sinon l'envoi échoue.
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "").strip()
EMAIL_FROM = os.getenv("EMAIL_FROM", f"{SMTP_FROM_NAME} <noreply@qeerah.com>")
RESEND_ENABLED = bool(RESEND_API_KEY)

# Le service email est actif si AU MOINS un transport est configuré (Resend OU SMTP).
SERVICE_ENABLED = RESEND_ENABLED or SMTP_ENABLED

APP_URL = os.getenv("APP_PUBLIC_URL", "https://qeerah.com")


# ════════════════════════════════════════════════════════════════════════════
# GABARIT HTML COMMUN — design épuré, responsive, inline CSS (compatibilité mail)
# ════════════════════════════════════════════════════════════════════════════
def _wrap(title: str, body_html: str) -> str:
    """Enveloppe un contenu HTML dans un gabarit d'email propre et sobre."""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:#1a1a2e;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f5f7;padding:24px 0;">
    <tr><td align="center">
      <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:540px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.06);">
        <tr><td style="background:#1a1a2e;padding:28px 32px;text-align:center;">
          <span style="font-size:20px;font-weight:800;color:#ffffff;letter-spacing:-0.4px;"><span style="color:#6c5ce7;">Qeerah</span></span>
        </td></tr>
        <tr><td style="padding:32px;">
          <h1 style="font-size:21px;font-weight:800;margin:0 0 16px;color:#1a1a2e;">{title}</h1>
          <div style="font-size:15px;line-height:1.6;color:#3a3a4a;">{body_html}</div>
        </td></tr>
        <tr><td style="padding:20px 32px;border-top:1px solid #ecedf2;text-align:center;">
          <p style="font-size:12px;color:#9a9ab0;margin:0;">
            Qeerah · Cet email vous est envoyé par <a href="mailto:{SUPPORT_EMAIL}" style="color:#6c5ce7;text-decoration:none;">{SUPPORT_EMAIL}</a>
          </p>
        </td></tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


def _button(label: str, url: str) -> str:
    return (
        f'<table role="presentation" cellpadding="0" cellspacing="0" style="margin:24px 0;"><tr><td '
        f'style="border-radius:10px;background:#6c5ce7;"><a href="{url}" '
        f'style="display:inline-block;padding:13px 28px;font-size:15px;font-weight:700;color:#ffffff;'
        f'text-decoration:none;border-radius:10px;">{label}</a></td></tr></table>'
    )


# ── Contenus des emails ──────────────────────────────────────────────────────
def _welcome_body() -> str:
    return (
        "<p>Bonjour,</p>"
        "<p>Bienvenue sur <strong>Qeerah</strong> 🎉 Votre compte est prêt.</p>"
        "<p>Vous pouvez dès maintenant analyser vos vidéos TikTok Shop grâce à l'IA : "
        "détection produit, accroche optimale, potentiel viral et conseils personnalisés.</p>"
        f"{_button('Lancer ma première analyse', APP_URL + '/app')}"
        "<p style=\"font-size:13px;color:#9a9ab0;\">Si vous n'êtes pas à l'origine de cette inscription, "
        "vous pouvez ignorer cet email.</p>"
        "<p>À très vite,<br>L'équipe Qeerah</p>"
    )


def _temporary_password_body(temp_password: str) -> str:
    return (
        "<p>Bonjour,</p>"
        "<p>Vous avez demandé la réinitialisation de votre mot de passe.</p>"
        "<p>Votre <strong>mot de passe temporaire</strong> est :</p>"
        f'<div style="background:#f4f5f7;padding:16px;border-radius:10px;font-family:monospace;'
        f'font-size:18px;letter-spacing:2px;text-align:center;margin:18px 0;font-weight:700;">{temp_password}</div>'
        "<ul style=\"padding-left:18px;\">"
        "<li>Connectez-vous avec ce mot de passe temporaire.</li>"
        "<li>Pensez à le remplacer par un nouveau mot de passe.</li>"
        "<li>Ce mot de passe expire dans 24 heures.</li>"
        "</ul>"
        "<p style=\"font-size:13px;color:#9a9ab0;\">Si vous n'avez pas fait cette demande, ignorez cet email.</p>"
        "<p>Cordialement,<br>L'équipe Qeerah</p>"
    )


def _magic_link_body(reset_link: str) -> str:
    return (
        "<p>Bonjour,</p>"
        "<p>Vous avez demandé la réinitialisation de votre mot de passe. "
        "Cliquez sur le bouton ci-dessous pour en définir un nouveau :</p>"
        f"{_button('Réinitialiser mon mot de passe', reset_link)}"
        "<p style=\"font-size:13px;color:#3a3a4a;\">Ou copiez ce lien dans votre navigateur :</p>"
        f'<p style="background:#f4f5f7;padding:12px;border-radius:8px;word-break:break-all;font-size:13px;">{reset_link}</p>'
        "<p style=\"font-size:13px;color:#9a9ab0;\">Ce lien expire dans 24 heures. "
        "Si vous n'avez pas fait cette demande, ignorez cet email.</p>"
        "<p>Cordialement,<br>L'équipe Qeerah</p>"
    )


def _password_changed_body() -> str:
    return (
        "<p>Bonjour,</p>"
        "<p>Votre mot de passe a bien été <strong>modifié avec succès</strong>.</p>"
        f"<p>Si vous n'êtes pas à l'origine de ce changement, contactez immédiatement le support à "
        f'<a href="mailto:{SUPPORT_EMAIL}" style="color:#6c5ce7;">{SUPPORT_EMAIL}</a>.</p>'
        "<p>Cordialement,<br>L'équipe Qeerah</p>"
    )


def _upsell_body(kind: str, unsubscribe_url: str) -> str:
    """Email promotionnel free → payant. kind: 'quota' (limite atteinte) | 'j3' (relance J+3)."""
    if kind == "quota":
        intro = (
            "<p>Bonjour,</p>"
            "<p>Tu viens d'utiliser tes <strong>3 analyses gratuites du mois</strong> 🎉 "
            "— bon signe, l'outil te sert vraiment !</p>"
            "<p>Pour continuer <strong>sans attendre le mois prochain</strong> et débloquer tout le reste :</p>"
        )
    else:  # j3
        intro = (
            "<p>Bonjour,</p>"
            "<p>Tu as créé ton compte il y a quelques jours 👋 Prêt à passer à la vitesse supérieure ?</p>"
            "<p>Avec un plan payant, tu débloques :</p>"
        )
    benefits = (
        "<ul style=\"padding-left:18px;line-height:1.8;\">"
        "<li>📈 <strong>Beaucoup plus d'analyses</strong> par mois (jusqu'à l'illimité)</li>"
        "<li>🔗 <strong>Analyse par lien TikTok</strong> — sans rien télécharger</li>"
        "<li>🤖 <strong>Coach IA</strong> + scripts personnalisés</li>"
        "<li>📸 <strong>Photo Slide Coach</strong> &amp; 🎬 <strong>AI Prompt Studio</strong></li>"
        "<li>📊 Données marché : produits &amp; créateurs gagnants</li>"
        "</ul>"
        "<p style=\"background:#f4f5f7;padding:14px;border-radius:10px;\">🔥 <strong>Offre de lancement</strong> : "
        "PRO à <strong>9,99€</strong> (au lieu de 12,99€) · GOLD à <strong>79,99€</strong> — "
        "et des <strong>accès à vie</strong> pour les 50 premiers.</p>"
    )
    cta = _button("Voir les offres", APP_URL + "/#pricing")
    foot = (
        f'<p style="font-size:12px;color:#9a9ab0;margin-top:22px;">Tu reçois cet email car tu as un compte '
        f'Qeerah. <a href="{unsubscribe_url}" style="color:#9a9ab0;">Se désinscrire des emails '
        f'promotionnels</a>.</p>'
    )
    return intro + benefits + cta + foot


# ════════════════════════════════════════════════════════════════════════════
# ENVOI (synchrone) — Resend prioritaire, sinon SMTP Hostinger. Cœur du service.
# ════════════════════════════════════════════════════════════════════════════
def _send_via_resend(to_email: str, subject: str, html_content: str) -> bool:
    """Envoi via l'API HTTP Resend. Ne lève jamais d'exception."""
    try:
        import httpx
        r = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {RESEND_API_KEY}", "Content-Type": "application/json"},
            json={"from": EMAIL_FROM, "to": [to_email], "subject": subject, "html": html_content},
            timeout=15.0,
        )
        if r.is_success:
            logger.info("[email] ✅ Resend → %s (sujet: %s)", to_email, subject)
            return True
        logger.error("[email] ❌ Resend %s → %s : %s", r.status_code, to_email, r.text[:300])
        return False
    except Exception as e:
        logger.error("[email] ❌ Resend erreur → %s : %s", to_email, str(e))
        return False


def send_transactional_email(to_email: str, subject: str, html_content: str) -> bool:
    """
    Envoie un email transactionnel HTML. Transport : Resend (si RESEND_API_KEY),
    sinon SMTP Hostinger (SSL/465). Ne lève jamais d'exception : une panne d'email
    ne doit jamais faire planter l'application appelante.
    """
    if RESEND_ENABLED:
        return _send_via_resend(to_email, subject, html_content)

    if not SMTP_ENABLED:
        logger.warning(
            "[email] aucun transport configuré (ni Resend ni SMTP) — email NON envoyé à %s (sujet: %s)",
            to_email, subject,
        )
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = formataddr((SMTP_FROM_NAME, SMTP_USERNAME))
        msg["To"] = to_email

        # Version texte minimale (fallback) + version HTML
        plain_fallback = "Cet email nécessite un client compatible HTML."
        msg.attach(MIMEText(plain_fallback, "plain", "utf-8"))
        msg.attach(MIMEText(html_content, "html", "utf-8"))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context, timeout=15) as server:
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, [to_email], msg.as_string())

        logger.info("[email] ✅ envoyé à %s (sujet: %s)", to_email, subject)
        return True

    except (smtplib.SMTPException, ssl.SSLError, OSError) as e:
        logger.error("[email] ❌ échec SMTP vers %s : %s", to_email, str(e))
        return False
    except Exception as e:  # garde-fou ultime
        logger.error("[email] ❌ erreur inattendue vers %s : %s", to_email, str(e))
        return False


# ════════════════════════════════════════════════════════════════════════════
# SERVICE ASYNC — wrappe l'envoi synchrone dans un thread pour ne pas bloquer
# l'event loop FastAPI. Conserve l'API attendue par main.py & admin_routes.py.
# ════════════════════════════════════════════════════════════════════════════
class EmailService:
    """Service d'emails transactionnels (Hostinger SMTP), interface async-safe."""

    def __init__(self):
        self.enabled = SERVICE_ENABLED

    async def _send(self, to_email: str, subject: str, html_content: str) -> bool:
        """Exécute l'envoi SMTP (bloquant) dans un thread, avec timeout."""
        if not self.enabled:
            logger.warning("[email] service désactivé — simulerait l'envoi à %s", to_email)
            return True  # comportement dev : on ne bloque pas les flux

        try:
            loop = asyncio.get_event_loop()
            return await asyncio.wait_for(
                loop.run_in_executor(_executor, send_transactional_email, to_email, subject, html_content),
                timeout=20.0,
            )
        except asyncio.TimeoutError:
            logger.error("[email] ❌ timeout envoi vers %s", to_email)
            return False
        except Exception as e:
            logger.error("[email] ❌ erreur async vers %s : %s", to_email, str(e))
            return False

    async def send_welcome_email(self, email: str) -> bool:
        """Email de bienvenue après création de compte."""
        return await self._send(
            email,
            "Bienvenue sur Qeerah 🎉",
            _wrap("Bienvenue à bord 🎉", _welcome_body()),
        )

    async def send_temporary_password_email(self, email: str, temp_password: str) -> bool:
        """Email contenant un mot de passe temporaire."""
        return await self._send(
            email,
            "Réinitialisation de mot de passe — Qeerah",
            _wrap("Réinitialisation de mot de passe", _temporary_password_body(temp_password)),
        )

    async def send_magic_link_email(self, email: str, reset_link: str) -> bool:
        """Email contenant un lien magique de réinitialisation."""
        return await self._send(
            email,
            "Réinitialiser votre mot de passe — Qeerah",
            _wrap("Réinitialisation de mot de passe", _magic_link_body(reset_link)),
        )

    async def send_password_changed_notification(self, email: str) -> bool:
        """Confirmation après changement de mot de passe."""
        return await self._send(
            email,
            "Votre mot de passe a été modifié — Qeerah",
            _wrap("Mot de passe modifié", _password_changed_body()),
        )

    async def send_upsell_email(self, email: str, unsubscribe_url: str, kind: str = "quota") -> bool:
        """Email promotionnel free → payant (avec lien de désinscription RGPD)."""
        subject = ("Tu as atteint ta limite gratuite 🚀" if kind == "quota"
                   else "Débloque tout le potentiel de Qeerah 🚀")
        return await self._send(
            email, subject,
            _wrap("Passe à la vitesse supérieure 🚀", _upsell_body(kind, unsubscribe_url)),
        )


# Instance globale réutilisée par l'application
email_service = EmailService()
