# Configuration du Système de Réinitialisation de Mot de Passe

Ce document explique comment configurer complètement le système de gestion des mots de passe.

## 1️⃣ Dépendances Installées ✅

Les bibliothèques suivantes ont déjà été ajoutées à `requirements.txt`:
- `sendgrid>=6.10.0` - Client SendGrid pour email
- `email-validator>=2.0.0` - Validation des adresses email
- `jinja2>=3.1.0` - Templates HTML pour emails

## 2️⃣ Configurer SendGrid (Service Email)

### Option A: Utiliser SendGrid (Recommandé - 100 emails/jour gratuit)

1. **Créer un compte SendGrid** : https://sendgrid.com/free
2. **Générer une clé API** :
   - Settings → API Keys → Create API Key
   - Copier la clé (format: `SG.xxxxx`)
3. **Ajouter à `.env`** :
   ```
   SENDGRID_API_KEY=SG.votre_cle_ici
   ```

### Option B: Utiliser Gmail SMTP (Plus simple mais limité)

**Pour development seulement** - remplacer dans `.env`:
```
SENDGRID_API_KEY=  # (laisser vide)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre_email@gmail.com
SMTP_PASSWORD=votre_mot_de_passe  # ou app-password pour 2FA
```

Puis modifier `email_service.py` pour utiliser `smtplib` au lieu de SendGrid.

## 3️⃣ Configurer Supabase (Base de Données)

### Créer la table `password_reset_tokens`

1. Aller sur **Supabase Dashboard** → votre projet
2. **SQL Editor** → New Query
3. Copier le contenu de `supabase_migrations_password_reset.sql`
4. Exécuter (Run)
5. Vérifier que la table est créée sous **Table Editor**

**Schéma de la table:**
```
id              UUID (clé primaire)
email           TEXT (FK vers users.email)
reset_token     TEXT (hash bcrypt du token)
token_type      TEXT ('temporary_password' ou 'magic_link')
new_password    TEXT (hash bcrypt du nouveau password)
created_at      TIMESTAMP
expires_at      TIMESTAMP
used            BOOLEAN
ip_address      TEXT
```

## 4️⃣ Vérifier les Variables d'Environnement

Ajouter/mettre à jour dans `.env`:

```bash
# Email / Password Reset
SENDGRID_API_KEY=SG.votre_cle_ici
SMTP_FROM_EMAIL=noreply@tts-analyzer.fr
SMTP_FROM_NAME=TikTok Shop Analyzer
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=24
PASSWORD_RESET_RATE_LIMIT=5
TEMPORARY_PASSWORD_LENGTH=12
```

**Explications:**
- `SENDGRID_API_KEY` : Clé API SendGrid
- `SMTP_FROM_EMAIL` : Adresse email d'envoi
- `PASSWORD_RESET_TOKEN_EXPIRE_HOURS` : Durée de validité du token (24h recommandé)
- `PASSWORD_RESET_RATE_LIMIT` : Max tentatives par heure (5 par défaut)
- `TEMPORARY_PASSWORD_LENGTH` : Longueur du password temporaire (12 caractères)

## 5️⃣ Installer les Dépendances

```bash
pip install -r requirements.txt
```

## 6️⃣ Tester le Système

### Test 1: Utilisateur oublie mot de passe

1. **Page de login** → Cliquer "Mot de passe oublié?"
2. **Remplir le form** :
   - Email: votre@email.com
   - Nouveau mot de passe: MajMin123!
   - Confirmer: MajMin123!
3. **Cliquer "Envoyer par email"**
4. **Vérifier la boîte mail** (ou console SendGrid)
5. **Se connecter** avec le nouveau mot de passe

### Test 2: Admin réinitialise utilisateur (Lien magique)

1. **Login en admin** (email = `ADMIN_EMAIL` de .env)
2. **Onglet Admin** → Chercher un utilisateur
3. **Cliquer le bouton "Changer plan"** du user
4. **Cliquer "📧 Envoyer lien magique"**
5. **Email reçu** : Cliquer le lien
6. **Remplir le formulaire** pour créer un nouveau password

### Test 3: Admin réinitialise utilisateur (Mot de passe temporaire)

1. **Admin panel** → Chercher utilisateur
2. **Cliquer "🔑 Générer mot de passe temporaire"**
3. **Copier le password** affiché à l'écran
4. **Email reçu** : User a aussi la password
5. **User se connecte** avec le password temporaire
6. **À première connexion** : Peut changer son password

## 7️⃣ Fichiers Modifiés

### Backend
- ✅ `main.py` : Endpoints `/api/forgot-password`, `/api/change-password`
- ✅ `admin_routes.py` : Endpoint `/admin/reset-user-password`
- ✅ `security.py` : Logging des tentatives reset
- ✅ `requirements.txt` : Dépendances email
- ✅ `.env.example` : Variables d'env

### Nouveaux fichiers
- ✅ `email_service.py` : Service d'envoi email
- ✅ `password_reset.py` : Utilitaires tokens/validation
- ✅ `supabase_migrations_password_reset.sql` : Migration DB
- ✅ `PASSWORD_RESET_SETUP.md` : Ce fichier

### Frontend
- ✅ `templates/index.html` : Modals et formulaires
- ✅ `static/app_v2.js` : Fonctions JS pour password reset

## 8️⃣ Sécurité et Bonnes Pratiques

### ✅ Implémenté
- Tokens URL-safe et expirables (24h par défaut)
- Hash bcrypt pour les tokens et passwords
- Rate limiting (max 5 tentatives/heure par email)
- Logging de sécurité pour chaque tentative
- Ne pas révéler si email existe (sécurité)
- Emails avec templates HTML professionnels

### ⚠️ À faire pour Production

1. **HTTPS obligatoire** - Les tokens ne doivent jamais passer en HTTP
2. **Monitoring** - Surveiller `security.log` pour abus
3. **Nettoyage** - Exécuter `cleanup_expired_reset_tokens()` régulièrement
4. **IP Logging** - Utiliser pour détecter abus (voir `ip_address` dans token)
5. **Email Template** - Personnaliser avec logo/branding

### 🚫 Ne jamais faire
- ❌ Stocker tokens en plaintext
- ❌ Envoyer passwords par email (utiliser tokens)
- ❌ Désactiver le rate limiting
- ❌ Augmenter expiration > 24h
- ❌ Utiliser HTTP (toujours HTTPS)

## 9️⃣ Dépannage

### "Email service disabled"
- Vérifier `SENDGRID_API_KEY` dans `.env`
- Les emails seront loggés mais non envoyés (dev mode)

### "BD non disponible"
- Vérifier connexion Supabase dans `supabase_client.py`
- Vérifier que `password_reset_tokens` table existe

### "Lien expiré"
- Tokens expirent après 24h (configurable via `PASSWORD_RESET_TOKEN_EXPIRE_HOURS`)
- User doit demander un nouveau reset

### "Trop de tentatives"
- Max 5 tentatives par heure (configurable via `PASSWORD_RESET_RATE_LIMIT`)
- Attendre 1 heure ou contacter admin

## 🔟 Support

Pour questions/problèmes:
- Email: dopeventure44@gmail.com
- Check logs: `security.log` pour événements
- Supabase logs: Voir l'onglet "Logs" dans dashboard

---

**Status**: ✅ Complètement implémenté et prêt à tester
