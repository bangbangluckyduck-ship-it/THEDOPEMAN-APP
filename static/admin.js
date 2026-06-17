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
  if (view === 'hooks') initHooksView();
}

/* ── FEATURE 1 — Banque de Hooks (admin CRUD) ─────────────────────────── */
const HOOK_CATS = [
  ['sante', 'Santé / Bien-être'], ['beaute', 'Beauté / Cosmétique'], ['mode', 'Mode / Vêtements'],
  ['tech', 'Tech / Gadgets'], ['fitness', 'Fitness / Sport'], ['maison', 'Maison / Déco'],
  ['mobilier', 'Mobilier'], ['food', 'Food / Cuisine'], ['autre', 'Autre'],
];
let _hooksInit = false;

function initHooksView() {
  if (!_hooksInit) {
    const catSel = document.getElementById('hook-categorie');
    if (catSel) catSel.innerHTML = HOOK_CATS.map(c => `<option value="${c[0]}">${c[1]}</option>`).join('');
    const filt = document.getElementById('hook-filter');
    if (filt) filt.innerHTML = '<option value="">Toutes les catégories</option>' + HOOK_CATS.map(c => `<option value="${c[0]}">${c[1]}</option>`).join('');
    onHookAccesChange();
    _hooksInit = true;
  }
  loadHooks();
}

function onHookAccesChange() {
  const v = document.getElementById('hook-acces').value;
  document.getElementById('hook-planmin-wrap').style.display = v === 'plan_minimum' ? 'block' : 'none';
  document.getElementById('hook-plans-wrap').style.display = v === 'plans_specifiques' ? 'block' : 'none';
}

function resetHookForm() {
  document.getElementById('hook-id').value = '';
  document.getElementById('hook-texte').value = '';
  document.getElementById('hook-video').value = '';
  document.getElementById('hook-acces').value = 'plan_minimum';
  document.getElementById('hook-planmin').value = 'pro';
  document.querySelectorAll('.hook-plan-cb').forEach(cb => cb.checked = false);
  document.getElementById('hook-save-btn').textContent = '➕ Ajouter le hook';
  onHookAccesChange();
}

async function loadHooks() {
  const list = document.getElementById('hooks-admin-list');
  if (!list) return;
  list.innerHTML = '<div class="empty">Chargement…</div>';
  const cat = document.getElementById('hook-filter')?.value || '';
  try {
    const res = await fetch('/admin/hooks' + (cat ? '?category=' + encodeURIComponent(cat) : ''), { headers: authHeaders() });
    if (!res.ok) { if (res.status === 403) { showLogin(); return; } list.innerHTML = '<div class="empty">❌ Erreur</div>'; return; }
    const data = await res.json();
    const hooks = data.hooks || [];
    if (!hooks.length) { list.innerHTML = '<div class="empty">Aucun hook.</div>'; return; }
    const catLabel = k => (HOOK_CATS.find(c => c[0] === k) || [k, k])[1];
    const accLabel = h => h.type_acces === 'tous' ? 'Tous (payants)' :
      h.type_acces === 'plan_minimum' ? ('À partir de ' + (h.plan_min || 'pro').toUpperCase()) :
        ('Plans: ' + (h.plans_autorises || []).join(', ').toUpperCase());
    list.innerHTML = hooks.map(h => `
      <div class="user-card">
        <div style="font-size:11px;font-weight:700;color:#7C3AED">${esc(catLabel(h.categorie))} · ${esc(accLabel(h))}${h.url_video ? ' · 🎬' : ''}</div>
        <div style="font-size:14px;margin:6px 0">${esc(h.texte)}</div>
        <div class="actions">
          <button class="btn btn-block" onclick='editHook(${JSON.stringify(h).replace(/'/g, "&#39;")})'>✏️ Éditer</button>
          <button class="btn btn-block" onclick="deleteHook(${h.id})">🗑️ Supprimer</button>
        </div>
      </div>`).join('');
  } catch (e) { list.innerHTML = '<div class="empty">❌ Erreur réseau</div>'; }
}

function editHook(h) {
  document.getElementById('hook-id').value = h.id;
  document.getElementById('hook-texte').value = h.texte || '';
  document.getElementById('hook-categorie').value = h.categorie || 'autre';
  document.getElementById('hook-video').value = h.url_video || '';
  document.getElementById('hook-acces').value = h.type_acces || 'plan_minimum';
  document.getElementById('hook-planmin').value = h.plan_min || 'pro';
  const allowed = h.plans_autorises || [];
  document.querySelectorAll('.hook-plan-cb').forEach(cb => cb.checked = allowed.includes(cb.value));
  document.getElementById('hook-save-btn').textContent = '💾 Enregistrer les modifications';
  onHookAccesChange();
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function saveHook() {
  const id = document.getElementById('hook-id').value;
  const texte = document.getElementById('hook-texte').value.trim();
  if (!texte) { showToast('Texte obligatoire'); return; }
  const body = {
    texte,
    categorie: document.getElementById('hook-categorie').value,
    url_video: document.getElementById('hook-video').value.trim() || null,
    type_acces: document.getElementById('hook-acces').value,
    plan_min: document.getElementById('hook-planmin').value,
    plans_autorises: Array.from(document.querySelectorAll('.hook-plan-cb')).filter(cb => cb.checked).map(cb => cb.value),
  };
  try {
    const res = await fetch('/admin/hooks' + (id ? '/' + id : ''), {
      method: id ? 'PUT' : 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(body),
    });
    if (!res.ok) { const d = await res.json().catch(() => ({})); showToast('❌ ' + (d.detail || 'Erreur')); return; }
    showToast(id ? '✅ Hook modifié' : '✅ Hook ajouté');
    resetHookForm();
    loadHooks();
  } catch (e) { showToast('❌ Erreur réseau'); }
}

async function deleteHook(id) {
  if (!confirm('Supprimer ce hook ?')) return;
  try {
    const res = await fetch('/admin/hooks/' + id, { method: 'DELETE', headers: authHeaders() });
    if (!res.ok) { showToast('❌ Erreur'); return; }
    showToast('✅ Supprimé'); loadHooks();
  } catch (e) { showToast('❌ Erreur réseau'); }
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

    // Note transparence : comptes internes/bots exclus des chiffres
    const note = document.getElementById('excluded-note');
    if (note) {
      const n = data.excluded_accounts || 0;
      if (n > 0) {
        note.textContent = `${n} compte${n > 1 ? 's' : ''} interne${n > 1 ? 's' : ''}/bot exclu${n > 1 ? 's' : ''} des statistiques.`;
        note.style.display = 'block';
      } else {
        note.style.display = 'none';
      }
    }
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
            <button class="btn btn-block" onclick="resetUserPassword('${safeEmail}')">🔑 Réinitialiser le MDP</button>
          </div>
        </div>`;
    }).join('');
  } catch (e) {
    list.innerHTML = '<div class="empty">❌ Erreur réseau</div>';
  }
}

/* ── RÉINITIALISATION MOT DE PASSE (admin) ────────────────────────────── */
async function resetUserPassword(email) {
  if (!confirm(`Réinitialiser le mot de passe de ${email} ?\n\nUn mot de passe temporaire sera généré, appliqué immédiatement, et envoyé par email à l'utilisateur.`)) return;
  try {
    const res = await fetch('/admin/reset-user-password', {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ email, reset_type: 'temporary_password' }),
    });
    const d = await res.json().catch(() => ({}));
    if (!res.ok) { showToast('❌ ' + (d.detail || 'Erreur')); return; }
    if (d.temp_password) {
      alert(`✅ Email envoyé à ${email}.\n\nMot de passe temporaire : ${d.temp_password}\n\n(Tu peux le communiquer directement à l'utilisateur si besoin.)`);
    }
    showToast('✅ ' + (d.message || 'Mot de passe réinitialisé'));
  } catch (e) {
    showToast('❌ Erreur réseau');
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
