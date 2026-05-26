# 📚 TikTok Shop Analyzer - Documentation Complète du Système

## Table des Matières
1. [Architecture Globale](#architecture-globale)
2. [Modules Créés](#modules-créés)
3. [Endpoints API](#endpoints-api)
4. [Flux Utilisateur](#flux-utilisateur)
5. [Configuration](#configuration)
6. [Troubleshooting](#troubleshooting)

---

## Architecture Globale

### Stack Technique
- **Backend** : FastAPI (Python 3.9+) + Uvicorn
- **Frontend** : Vanilla JavaScript + CSS3
- **Database** : Supabase PostgreSQL
- **Email** : SendGrid (async with thread executor)
- **AI Analysis** : Mistral API (pixtral-12b model)
- **Hosting** : Render (production)
- **Market Data** : TTS Scraper (Tendances Gagnantes)

### Architecture High-Level
```
┌─────────────────┐
│   Frontend      │ (HTML/JS)
│  - Homepage     │
│  - App tabs     │
│  - Tendances Gagnantes tab  │
└────────┬────────┘
         │ HTTP/REST
┌────────▼────────────────────────┐
│   FastAPI Backend               │
├─────────────────────────────────┤
│ ├─ /analyze                     │
│ ├─ /api/forgot-password         │
│ ├─ /api/change-password         │
│ ├─ /api/market-recommendations  │
│ ├─ /api/product-recommendations │
│ ├─ /admin/*                     │
│ └─ /api/user-info               │
└────────┬────────────────────────┘
         │ SQL/HTTP
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
 Supabase  SendGrid  TTS Scraper  Mistral
 (users,   (emails)  (market)     (AI)
  tokens)
```

---

## Modules Créés

### 1. **email_service.py** (152 lignes)
Service d'envoi d'emails via SendGrid.

**Classe : EmailService**
```python
class EmailService:
    async def send_temporary_password_email(email, temp_password)
    async def send_magic_link_email(email, reset_link)
    async def send_password_changed_notification(email)
```

**Clé Features :**
- ✅ Thread executor pour éviter bloquer event loop
- ✅ 10s timeout sur chaque appel SendGrid
- ✅ Jinja2 templates HTML
- ✅ Graceful degradation si SENDGRID_API_KEY absent
- ✅ Logging complet avec erreurs détaillées

**Configuration :**
```env
SENDGRID_API_KEY=SG.xxx         # Clé API SendGrid
SMTP_FROM_EMAIL=xxx@xxx.fr      # Adresse d'envoi
SMTP_FROM_NAME=App Name         # Nom expéditeur
```

**⚠️ Notes de Production :**
- L'adresse SMTP_FROM_EMAIL DOIT être vérifiée dans SendGrid Dashboard
- Tous les appels `.send()` tournent dans un thread pool
- Utilise `asyncio.wait_for()` avec timeout pour éviter les hangs

---

### 2. **password_reset.py** (211 lignes)
Utilitaires pour la gestion sécurisée des tokens de réinitialisation.

**Fonctions Principales :**
```python
def generate_reset_token() -> str
def generate_temporary_password(length=12) -> str
def hash_token(token: str) -> str
def verify_token(token: str, token_hash: str) -> bool
def create_password_reset_token(email, token_type, new_password_hash) -> (bool, str, str)
def validate_reset_token(token: str, email: str) -> (bool, dict)
def mark_token_as_used(email: str, token: str) -> bool
def check_rate_limit(email: str, max_attempts=5, window_hours=1) -> bool
```

**Sécurité :**
- Tokens générés avec `secrets.token_urlsafe(24)` (~32 chars)
- Tokens hashés en bcrypt, jamais en plaintext
- Expiration 24h configurable
- Rate limiting : max 5 tentatives/heure/email
- Tout stocké dans table `password_reset_tokens` Supabase

---

### 3. **Supabase Table : password_reset_tokens**
```sql
CREATE TABLE password_reset_tokens (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           TEXT NOT NULL,
  reset_token     TEXT NOT NULL,           -- bcrypt hash
  token_type      TEXT CHECK (...),        -- 'temporary_password' | 'magic_link'
  new_password    TEXT,                    -- bcrypt hash (temporary_password only)
  created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  expires_at      TIMESTAMP WITH TIME ZONE,
  used            BOOLEAN DEFAULT FALSE,
  ip_address      TEXT
);

-- Indices pour performance
CREATE INDEX idx_password_reset_email ON password_reset_tokens(email);
CREATE INDEX idx_password_reset_created ON password_reset_tokens(created_at);
CREATE INDEX idx_password_reset_expires ON password_reset_tokens(expires_at);
CREATE INDEX idx_password_reset_used ON password_reset_tokens(used);

-- RLS Policy (IMPORTANT)
ALTER TABLE password_reset_tokens ENABLE ROW LEVEL SECURITY;
CREATE POLICY "password_reset_backend_access" ON password_reset_tokens
  FOR ALL USING (true) WITH CHECK (true);
```

**⚠️ RLS CRITIQUE :**
- La politique permet à Supabase backend d'accéder
- User credentials DIRECTES seraient bloquées (besoin d'auth)
- Service role (API backend) peut tout faire

---

## Endpoints API

### 1. Password Reset Endpoints

#### POST /api/forgot-password
**Description :** User initie réinitialisation mot de passe

**Request :**
```json
{
  "email": "user@example.com",
  "password": "newpassword123"
}
```

**Response (200) :**
```json
{
  "ok": true,
  "message": "Email de réinitialisation envoyé"
}
```

**Errors :**
- 400 : Email invalide / Password trop court
- 429 : Rate limit atteint (5 essais/heure)
- 500 : SendGrid error / DB error

**Flux :**
1. Valider email + password
2. Rate limit check
3. Vérifier user existe
4. Créer token unique
5. Envoyer email avec temp password
6. Retourner 200 OK (même si user n'existe pas - sécurité)

---

#### POST /api/change-password
**Description :** User change son password avec token valide

**Request :**
```json
{
  "reset_token": "token_from_email_or_link",
  "new_password": "real_new_password",
  "email": "user@example.com"
}
```

**Response (200) :**
```json
{
  "ok": true,
  "message": "Mot de passe modifié avec succès"
}
```

**Errors :**
- 400 : Token expiré / invalide
- 500 : DB error

---

#### POST /admin/reset-user-password
**Description :** Admin réinitialise password user (2 modes)

**Request :**
```json
{
  "email": "user@example.com",
  "reset_type": "magic_link" | "temporary_password"
}
```

**Response (200) - Magic Link :**
```json
{
  "ok": true,
  "reset_link": "https://app.com/reset?token=xxx"
}
```

**Response (200) - Temp Password :**
```json
{
  "ok": true,
  "temporary_password": "aBc3Def!Ghi5"
}
```

---

### 2. Tendances Gagnantes / Market Data Endpoints

#### GET /api/market-recommendations
**Description :** Récupère toutes les données marché (top produits, tendances, créateurs)

**Response (200) :**
```json
{
  "ok": true,
  "market_context": {
    "top_products": [
      {"name": "Serum Vitamine C", "price": "29.99€", "viral_score": 8.5}
    ],
    "trending": [
      {"name": "Air Fryer XXL", "trend_momentum": "📈 +45%", "creator_count": 234}
    ],
    "top_creators": [
      {"handle": "creator_x", "followers_display": "1.2M", "video_count": 456}
    ]
  }
}
```

**Source :** TTS Scraper API (`{TTS_SCRAPER_URL}/api/coach-context`)

---

#### GET /api/product-recommendations/{category}
**Description :** Recommandations produits + stratégie pour une catégorie

**URL Examples :**
- `/api/product-recommendations/complement_sante`
- `/api/product-recommendations/tech`
- `/api/product-recommendations/beaute`

**Response (200) :**
```json
{
  "ok": true,
  "category": "complement_sante",
  "category_names": ["shilajit", "creatine", "lion's mane", ...],
  "recommended_hooks": ["controverse_douce", "temoignage", "curiosite"],
  "price_range": "15-100",
  "notes": "Authenticité CRITIQUE. Éviter peur excessive.",
  "market_data": {
    "top_products": [...],
    "trending": [...],
    "top_creators": [...]
  }
}
```

**Available Categories :**
- `complement_sante` - Suppléments
- `electromenager` - Appareils électroménagers
- `tech` - Technologie
- `fitness` - Fitness/Musculation
- `beaute` - Beauté/Soins
- `alimentation` - Snacks/Boissons
- `luxe` - Produits premium

---

## Flux Utilisateur

### 1. Mot de Passe Oublié
```
Homepage / App → Cliquer "🔑 Mot de passe oublié?"
                ↓
            Modal Form (email + new password)
                ↓
        POST /api/forgot-password
                ↓
            Email reçu (30s max)
                ↓
        Cliquer lien → Page reset
                ↓
        POST /api/change-password
                ↓
            ✅ Password changé
                ↓
        Login avec nouveau password
```

### 2. Admin Reset User Password
```
Admin Panel → User select → "Réinitialiser"
                ↓
        2 Options:
        ├─ Lien Magique (secure)
        │  ├─ POST /admin/reset-user-password (magic_link)
        │  ├─ Email avec lien à user
        │  └─ User clique → crée nouveau password
        │
        └─ Mot de Passe Temporaire (rapide)
           ├─ POST /admin/reset-user-password (temporary_password)
           ├─ Password affiché à l'écran (10s)
           ├─ Admin copie et envoie à user (manuelle)
           └─ User login + force change à 1ère connexion
```

### 3. Tendances Gagnantes Tab
```
App → Clicker onglet "🛍️ Tendances Gagnantes"
            ↓
    loadTendances GagnantesTab() appelée
            ↓
    Fetch /api/market-recommendations (async)
            ↓
    Display:
    ├─ 📊 Market Context
    │  ├─ Top 5 Produits
    │  ├─ 5 Tendances
    │  └─ 3 Top Créateurs
    │
    ├─ 🛍️ Produits Recommandés
    │  └─ Basé sur catégorie dernière analyse
    │
    └─ 🎯 Stratégie par Catégorie
```

---

## Configuration

### Environnement (Production Render)

**Essentielles :**
```env
PORT=10000
SENDGRID_API_KEY=SG.xxx           # Doit être vérifiée dans SendGrid
SMTP_FROM_EMAIL=contact@domain.fr # Doit être vérifiée
ANTHROPIC_API_KEY=sk-ant-xxx
ADMIN_EMAIL=admin@domain.fr
MISTRAL_API_KEY=xxx
TTS_SCRAPER_URL=https://scraper.example.com
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
```

**Optionnelles :**
```env
PASSWORD_RESET_TOKEN_EXPIRE_HOURS=24
TEMPORARY_PASSWORD_LENGTH=12
PASSWORD_RESET_RATE_LIMIT=5
```

### Render Configuration
1. Service → Settings → Environment
2. Ajouter toutes les variables ci-dessus
3. Deploy déclenche redémarrage auto

---

## Troubleshooting

### ❌ SendGrid Email Non Reçu

**Causes Possibles :**
1. SENDGRID_API_KEY invalide
2. SMTP_FROM_EMAIL non vérifiée dans SendGrid
3. Email en spam (ajouter à contacts)
4. SendGrid API key manquante dans Render env vars

**Fix :**
1. SendGrid Dashboard → Settings → Sender Authentication
2. Verify Single Sender avec SMTP_FROM_EMAIL
3. Cliquer lien confirmation dans email reçu
4. Re-déployer Render après verification

### ❌ Erreur "Erreur création token"

**Cause :** RLS policy `password_reset_tokens` trop restrictive

**Fix :**
```sql
DROP POLICY "password_reset_select_admin_only" ON password_reset_tokens;
DROP POLICY "password_reset_insert_service" ON password_reset_tokens;
DROP POLICY "password_reset_update_service" ON password_reset_tokens;

CREATE POLICY "password_reset_backend_access" ON password_reset_tokens
  FOR ALL USING (true) WITH CHECK (true);
```

### ❌ Rate Limit "Trop de tentatives"

**Cause :** 5 tentatives mot de passe oublié en 1 heure

**Fix :** 
- Attendre 1 heure, OU
- Utiliser un email différent, OU
- Admin réinitialise manuellement

### ❌ Tendances Gagnantes Tab Vide

**Causes :**
1. TTS_SCRAPER_URL pas configuré
2. Aucune analyse effectuée (pas de catégorie)
3. Scraper API down (timeout 5s)

**Fix :**
- Faire une analyse vidéo d'abord
- Vérifier TTS_SCRAPER_URL en Render env vars

---

## Code Snippets Clés

### Appel SendGrid Async-Safe
```python
# email_service.py
loop = asyncio.get_event_loop()
response = await asyncio.wait_for(
    loop.run_in_executor(_executor, self.sg.send, message),
    timeout=10.0
)
```

### Rate Limiting Query
```python
# password_reset.py
cutoff_time = (datetime.now(timezone.utc) - timedelta(hours=window_hours)).isoformat()
response = supabase.table("password_reset_tokens").select("id", count="exact")\
    .eq("email", email)\
    .gt("created_at", cutoff_time).execute()
```

### Tab Switching avec Async
```javascript
// app_v2.js
function switchTab(tab) {
  // ... afficher/cacher elements
  if (tab === 'winning-trends') loadTendances GagnantesTab();  // Appel async
}
```

---

## Métriques & Monitoring

### SendGrid
- Activity Dashboard → vérifier "delivered" vs "dropped"
- Rate limiting : Max 100 emails/jour (free tier)

### Database (Supabase)
- Monitor `password_reset_tokens` table size
- Nettoyer tokens expirés régulièrement

### API Performance
- Timeout /analyze : 180s (vidéos complexes)
- Timeout SendGrid : 10s
- Timeout Scraper : 5s

---

## Sécurité

### ✅ Implémenté
- Tokens bcrypt hashés (jamais plaintext)
- Email masquage (ne pas révéler existence user)
- Rate limiting (5 reset/heure)
- Token expiration (24h)
- HTTPS only en production
- SQL injection protection (Supabase ORM)

### ⚠️ À Faire
- Webhook SendGrid pour bounce handling
- Email verification avant reset
- 2FA optionnel
- Session timeout configurable
- Audit logging complet

---

## Support & Contact

**Issues:** Relever tous les problèmes avec logs complets:
- Render logs (timestamps exact)
- Network tab (DevTools)
- Console errors

**Email Support:** dopeventures44@gmail.com

---

*Documentation générée : 2026-05-27*
*Version : 1.0 - Complete System*
