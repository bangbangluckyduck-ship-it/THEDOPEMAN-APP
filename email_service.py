"""Email service for sending password reset and notification emails using SendGrid."""

import os
import logging
from typing import Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from jinja2 import Template

logger = logging.getLogger(__name__)

SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "noreply@tts-analyzer.fr")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "TikTok Shop Analyzer")


# Email templates
TEMPORARY_PASSWORD_EMAIL_TEMPLATE = """
<h1>Réinitialisation de mot de passe</h1>
<p>Bonjour,</p>
<p>Vous avez demandé une réinitialisation de votre mot de passe pour <strong>TikTok Shop Analyzer</strong>.</p>
<p>Votre <strong>mot de passe temporaire</strong> est :</p>
<div style="background: #f5f5f5; padding: 16px; border-radius: 8px; font-family: monospace; font-size: 18px; letter-spacing: 2px; margin: 20px 0;">
  <strong>{{ temp_password }}</strong>
</div>
<p><strong>⚠️ Importants :</strong></p>
<ul>
  <li>Connectez-vous avec ce mot de passe temporaire</li>
  <li>À votre première connexion, vous serez invité à définir un nouveau mot de passe</li>
  <li>Ce mot de passe temporaire expirera dans 24 heures</li>
</ul>
<p>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer ce message.</p>
<p>Cordialement,<br>L'équipe TikTok Shop Analyzer</p>
"""

MAGIC_LINK_EMAIL_TEMPLATE = """
<h1>Réinitialisation de mot de passe</h1>
<p>Bonjour,</p>
<p>Vous avez demandé une réinitialisation de votre mot de passe pour <strong>TikTok Shop Analyzer</strong>.</p>
<p>Cliquez sur le lien ci-dessous pour créer un nouveau mot de passe :</p>
<div style="margin: 30px 0;">
  <a href="{{ reset_link }}" style="background: #D4AF37; color: white; padding: 12px 24px; text-decoration: none; border-radius: 8px; font-weight: bold; display: inline-block;">
    Réinitialiser mon mot de passe
  </a>
</div>
<p><strong>Ou copiez ce lien :</strong></p>
<p style="background: #f5f5f5; padding: 12px; border-radius: 8px; word-break: break-all;">
  {{ reset_link }}
</p>
<p><strong>⚠️ Important :</strong></p>
<ul>
  <li>Ce lien expirera dans 24 heures</li>
  <li>Si vous n'avez pas demandé cette réinitialisation, veuillez ignorer ce message</li>
</ul>
<p>Cordialement,<br>L'équipe TikTok Shop Analyzer</p>
"""

PASSWORD_CHANGED_EMAIL_TEMPLATE = """
<h1>Mot de passe modifié</h1>
<p>Bonjour,</p>
<p>Votre mot de passe pour <strong>TikTok Shop Analyzer</strong> a été modifié avec succès.</p>
<p>Si vous n'avez pas fait cette modification, veuillez contacter le support immédiatement à <strong>dopeventure44@gmail.com</strong>.</p>
<p>Cordialement,<br>L'équipe TikTok Shop Analyzer</p>
"""


class EmailService:
    """Service pour envoyer des emails via SendGrid."""

    def __init__(self):
        self.sg = SendGridAPIClient(SENDGRID_API_KEY) if SENDGRID_API_KEY else None
        self.enabled = bool(SENDGRID_API_KEY)

    async def send_temporary_password_email(self, email: str, temp_password: str) -> bool:
        """Send temporary password email to user."""
        if not self.enabled:
            logger.warning(f"Email service disabled. Would send to {email}: temp password reset")
            return True  # Pretend success for development

        try:
            template = Template(TEMPORARY_PASSWORD_EMAIL_TEMPLATE)
            html_content = template.render(temp_password=temp_password)

            message = Mail(
                from_email=Email(SMTP_FROM_EMAIL, SMTP_FROM_NAME),
                to_emails=To(email),
                subject="Réinitialisation de mot de passe - TikTok Shop Analyzer",
                html_content=html_content,
            )

            response = self.sg.send(message)
            logger.info(f"✅ Password reset email sent to {email} (status: {response.status_code})")
            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"❌ Failed to send password reset email to {email}: {str(e)}")
            return False

    async def send_magic_link_email(self, email: str, reset_link: str) -> bool:
        """Send magic link email to user."""
        if not self.enabled:
            logger.warning(f"Email service disabled. Would send magic link to {email}")
            return True

        try:
            template = Template(MAGIC_LINK_EMAIL_TEMPLATE)
            html_content = template.render(reset_link=reset_link)

            message = Mail(
                from_email=Email(SMTP_FROM_EMAIL, SMTP_FROM_NAME),
                to_emails=To(email),
                subject="Réinitialiser votre mot de passe - TikTok Shop Analyzer",
                html_content=html_content,
            )

            response = self.sg.send(message)
            logger.info(f"✅ Magic link email sent to {email} (status: {response.status_code})")
            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"❌ Failed to send magic link email to {email}: {str(e)}")
            return False

    async def send_password_changed_notification(self, email: str) -> bool:
        """Send password change confirmation email."""
        if not self.enabled:
            logger.warning(f"Email service disabled. Would send confirmation to {email}")
            return True

        try:
            template = Template(PASSWORD_CHANGED_EMAIL_TEMPLATE)
            html_content = template.render()

            message = Mail(
                from_email=Email(SMTP_FROM_EMAIL, SMTP_FROM_NAME),
                to_emails=To(email),
                subject="Votre mot de passe a été modifié - TikTok Shop Analyzer",
                html_content=html_content,
            )

            response = self.sg.send(message)
            logger.info(f"✅ Password change confirmation sent to {email} (status: {response.status_code})")
            return response.status_code in [200, 201]

        except Exception as e:
            logger.error(f"❌ Failed to send password change confirmation to {email}: {str(e)}")
            return False


# Global instance
email_service = EmailService()
