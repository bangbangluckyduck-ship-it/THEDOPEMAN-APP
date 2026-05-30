/* ════════════════════════════════════════════════════════════════════════
 * Dope Admin — script de contrôle du back-office isolé (/dope-admin)
 * App autonome : écran de connexion intégré + vérification du rôle admin.
 * Si non connecté/non admin → écran de login (jamais de redirection hors scope,
 * pour rester fonctionnel en mode PWA installé sur l'écran d'accueil).
 * RÈGLE : toutes les requêtes incluent le header Authorization: Bearer <token>.
 * ════════════════════════════════════════════════════════════════════════ */
'use strict';

const TOKEN_KEY = 'tts_token';

function getToken() {
  return localStorage.getItem(TOKEN_KEY) || '';
}

function authHeaders(extra) {
  const h = Object.assign({}, extra || {});
  const token = getToken();
  if (token) h['Authorization'] = 'Bearer ' + token;
  return h;
}

const TIER_LABELS = { free: 'FREE', pro: 'PRO', gold: 'GOLD', agency: 'AGENCY', beta: 'BETA', admin: 'ADMIN' };
const TIER_COLORS = { free: '#6B7280', pro: '#3b82f6', gold: '#f59e0b', agency: '#7C3AED', beta: '#22c55e', admin: '#ef4444' };
const PAYING_TIERS = ['pro', 'gold', 'agency'];

function tierBadge(tier) {
  const label = TIER_LABELS[tier] || (tier || 'FREE').toUpperCase();
  const color = TIER_COLORS[tier] || '#6B7280';
  return `<span class="tier-badge" style="background:${color}">${label}</span>`;
}

function esc(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

let _toastTimer = null;
function showToast(msg) {
  const el = document.getElementById('toast');
  if (!el) return;
  el.textContent = msg;
  el.style.display = 'block';
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => { el.style.display = 'none'; }, 3200);
}

/* ── AFFICHAGE : écran de connexion vs back-office ────────────────────── */
function showLogin() {
  const shell = document.getElementById('app-shell');
  const login = document.getElementById('login-screen');
  if (shell) shell.style.display = 'none';
  if (login) login.style.display = 'flex';
}

function showShell() {
  const shell = document.getElementById('app-shell');
  const login = document.getElementById('login-screen');
  if (login) login.style.display = 'none';
  if (shell) shell.style.display = 'block';
}

/* ── SÉCURITÉ : vérifie le rôle admin via le token courant ────────────── */
async function checkIsAdmin() {
  const token = getToken();
  if (!token) return false;
  try {
    const res = await fetch('/api/user-info', { headers: authHeaders() });
    if (!res.ok) return false;
    const data = await res.json();
    return !!(data && (data.is_admin === true || data.tier === 'admin'));
  } catch (e) {
    return false;
  }
}

/* ── CONNEXION INTÉGRÉE (app autonome sur l'écran d'accueil) ──────────── */
async function doLogin() {
  const email = (document.getElementById('login-email').value || '').trim();
  const password = document.getElementById('login-password').value || '';
  const errEl = document.getElementById('login-error');
  errEl.style.display = 'none';
  if (!email || !password) {
    errEl.textContent = 'Email et mot de passe requis.';
    errEl.style.display = 'block';
    return;
  }
  try {
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const e = await res.json().catch(() => ({}));
      errEl.textContent = '❌ ' + (e.detail || 'Identifiants invalides.');
      errEl.style.display = 'block';
      return;
    }
    const data = await res.json();
    if (data.token) localStorage.setItem(TOKEN_KEY, data.token);

    // Vérifie que ce compte est bien admin
    const isAdmin = await checkIsAdmin();
    if (!isAdmin) {
      localStorage.removeItem(TOKEN_KEY);
      errEl.textContent = '🔒 Ce compte n\'a pas les droits administrateur.';
      errEl.style.display = 'block';
      return;
    }
    document.getElementById('login-password').value = '';
    showShell();
    showView('stats');
  } catch (e) {
    errEl.textContent = '❌ Erreur réseau.';
    errEl.style.display = 'block';
  }
}

function adminLogout() {
  localStorage.removeItem(TOKEN_KEY);
  showLogin();
}

/* ── NAVIGATION ENTRE LES VUES ────────────────────────────────────────── */
function showView(view) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-item[data-view]').forEach(n => n.classList.remove('active'));
  const section = document.getElementById('view-' + view);
  const navBtn = document.querySelector(`.nav-item[data-view="${view}"]`);
  if (section) section.classList.add('active');
  if (navBtn) navBtn.classList.add('active');
  if (view === 'stats') loadStats();
  if (view === 'users') loadUsers();
}

/* ── VUE STATISTIQUES ─────────────────────────────────────────────────── */
async function loadStats() {
  try {
    const res = await fetch('/admin/stats', { headers: authHeaders() });
    if (!res.ok) {
      if (res.status === 403) { showLogin(); return; }
      showToast('❌ Erreur chargement stats');
      return;
    }
    const data = await res.json();

    document.getElementById('kpi-total-users').textContent = data.total_users ?? 0;
    document.getElementById('kpi-total-analyses').textContent = data.total_analyses ?? 0;

    const byTier = data.by_tier || {};
    const paying = PAYING_TIERS.reduce((sum, t) => sum + (byTier[t] || 0), 0);
    document.getElementById('kpi-paying').textContent = paying;

    // Répartition par plan
    const order = ['free', 'pro', 'gold', 'agency', 'beta', 'admin'];
    const wrap = document.getElementById('tier-breakdown');
    wrap.innerHTML = order.map(t => `
      <div class="tier-row">
        <span>${tierBadge(t)}</span>
        <span class="tier-count">${byTier[t] || 0}</span>
      </div>
    `).join('');
  } catch (e) {
    showToast('❌ Erreur réseau (stats)');
  }
}

/* ── VUE UTILISATEURS ─────────────────────────────────────────────────── */
async function loadUsers() {
  const list = document.getElementById('users-list');
  list.innerHTML = '<div class="empty">Chargement…</div>';
  try {
    const res = await fetch('/admin/users', { headers: authHeaders() });
    if (!res.ok) {
      if (res.status === 403) { showLogin(); return; }
      list.innerHTML = '<div class="empty">❌ Erreur de chargement</div>';
      return;
    }
    const data = await res.json();
    const users = (data && data.users) || [];
    if (!users.length) {
      list.innerHTML = '<div class="empty">Aucun utilisateur</div>';
      return;
    }
    list.innerHTML = users.map(u => {
      const email = esc(u.email || '');
      const safeEmail = email.replace(/'/g, "\\'");
      const expiry = u.expiry ? `Expire le ${esc(u.expiry)}` : 'Sans expiration';
      return `
        <div class="user-card">
          <div class="email">${email}</div>
          <div class="meta">
            ${tierBadge(u.tier)}
            <span class="exp">${expiry}</span>
          </div>
          <div class="actions">
            <button class="btn btn-block" onclick="changeUserTier('${safeEmail}', '${esc(u.tier)}')">⚙️ Changer le plan</button>
          </div>
        </div>`;
    }).join('');
  } catch (e) {
    list.innerHTML = '<div class="empty">❌ Erreur réseau</div>';
  }
}

/* ── MODALE CHANGEMENT DE PLAN ────────────────────────────────────────── */
function changeUserTier(email, currentTier) {
  document.getElementById('tier-modal-email').textContent = email;
  const sel = document.getElementById('tier-modal-select');
  if (currentTier && sel.querySelector(`option[value="${currentTier}"]`)) sel.value = currentTier;
  document.getElementById('tier-modal-expiry').value = '';
  document.getElementById('tier-modal').classList.add('active');
}

function closeTierModal() {
  document.getElementById('tier-modal').classList.remove('active');
}

async function confirmTierChange() {
  const email = document.getElementById('tier-modal-email').textContent.trim();
  const tier = document.getElementById('tier-modal-select').value;
  const expiry = document.getElementById('tier-modal-expiry').value || null;
  if (!email) return;

  try {
    const res = await fetch('/admin/set-tier', {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ email, tier, expiry }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      showToast('❌ ' + (err.detail || 'Erreur'));
      return;
    }
    const result = await res.json();
    showToast('✅ ' + (result.message || 'Plan mis à jour'));
    closeTierModal();
    loadUsers();
  } catch (e) {
    showToast('❌ Erreur réseau');
  }
}

/* ── INITIALISATION ───────────────────────────────────────────────────── */
document.addEventListener('DOMContentLoaded', async () => {
  const isAdmin = await checkIsAdmin();
  if (isAdmin) {
    showShell();
    loadStats();
  } else {
    showLogin();
  }
});
