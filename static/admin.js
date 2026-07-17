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
  if (view === 'temoignages') loadTemoignages();
  if (view === 'notifs') initNotifsView();
  if (view === 'affiliates') loadAffiliates();
}

/* ── NOTIFICATIONS — broadcast (admin) ────────────────────────────────── */
async function initNotifsView() {
  try {
    const res = await fetch('/admin/push/stats', { headers: authHeaders() });
    if (res.status === 403) { showLogin(); return; }
    const d = await res.json();
    const cnt = document.getElementById('push-count');
    if (cnt) cnt.textContent = d.subscribers ?? 0;
    const warn = document.getElementById('push-config-warn');
    if (warn) warn.style.display = d.configured ? 'none' : 'block';
    const btn = document.getElementById('push-send-btn');
    if (btn) btn.disabled = !d.configured;
  } catch (e) { /* noop */ }
}

async function sendBroadcast() {
  const title = document.getElementById('push-title').value.trim();
  const body = document.getElementById('push-body').value.trim();
  const url = document.getElementById('push-url').value.trim() || '/app';
  if (!title || !body) { showToast('Titre et message requis'); return; }
  if (!confirm(`Envoyer cette notification à tous les abonnés ?\n\n${title}\n${body}`)) return;
  const btn = document.getElementById('push-send-btn');
  btn.disabled = true; btn.textContent = 'Envoi…';
  try {
    const res = await fetch('/admin/push/broadcast', {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ title, body, url }),
    });
    const d = await res.json().catch(() => ({}));
    if (!res.ok) { showToast('❌ ' + (d.detail || 'Erreur')); }
    else {
      showToast(`✅ Envoyé à ${d.sent} abonné${d.sent > 1 ? 's' : ''}`);
      document.getElementById('push-title').value = '';
      document.getElementById('push-body').value = '';
    }
  } catch (e) { showToast('❌ Erreur réseau'); }
  btn.disabled = false; btn.textContent = '📤 Envoyer à tous';
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

/* ── FEATURE 2 — Témoignages (admin) ──────────────────────────────────── */
function resetTemoignageForm() {
  ['tm-id', 'tm-nom', 'tm-tiktok', 'tm-texte', 'tm-metrique', 'tm-photo'].forEach(id => document.getElementById(id).value = '');
  document.getElementById('tm-statut').value = 'en_attente';
  document.getElementById('tm-avant').checked = false;
  document.getElementById('tm-save-btn').textContent = '➕ Ajouter';
}

async function loadTemoignages() {
  const list = document.getElementById('temoignages-admin-list');
  if (!list) return;
  list.innerHTML = '<div class="empty">Chargement…</div>';
  try {
    const res = await fetch('/admin/temoignages', { headers: authHeaders() });
    if (!res.ok) { if (res.status === 403) { showLogin(); return; } list.innerHTML = '<div class="empty">❌ Erreur</div>'; return; }
    const data = await res.json();
    const rows = data.temoignages || [];
    if (!rows.length) { list.innerHTML = '<div class="empty">Aucun témoignage.</div>'; return; }
    const badge = s => s === 'publie' ? '🟢 Publié' : s === 'masque' ? '⚫ Masqué' : '🟡 En attente';
    list.innerHTML = rows.map(t => `
      <div class="user-card">
        <div style="font-size:11px;font-weight:700;color:var(--muted)">${badge(t.statut)}${t.mis_en_avant ? ' · ⭐ À la une' : ''}${t.note ? ' · ' + t.note + '/5' : ''}</div>
        <div style="font-weight:700;margin:4px 0">${esc(t.nom)}${t.lien_tiktok ? ' · <a href="' + esc(t.lien_tiktok) + '" target="_blank" style="color:var(--accent)">TikTok</a>' : ''}</div>
        <div style="font-size:14px;margin-bottom:6px">${esc(t.texte)}</div>
        ${t.metrique ? '<div style="font-size:12px;color:#16A34A">📈 ' + esc(t.metrique) + '</div>' : ''}
        <div class="actions">
          ${t.statut !== 'publie' ? `<button class="btn btn-block" onclick="quickPublish(${t.id}, true)">✅ Publier</button>` : `<button class="btn btn-block" onclick="quickPublish(${t.id}, false)">🚫 Masquer</button>`}
          <button class="btn btn-block" onclick='editTemoignage(${JSON.stringify(t).replace(/'/g, "&#39;")})'>✏️ Éditer</button>
          <button class="btn btn-block" onclick="deleteTemoignage(${t.id})">🗑️</button>
        </div>
      </div>`).join('');
  } catch (e) { list.innerHTML = '<div class="empty">❌ Erreur réseau</div>'; }
}

function _tmBody() {
  return {
    nom: document.getElementById('tm-nom').value.trim(),
    texte: document.getElementById('tm-texte').value.trim(),
    lien_tiktok: document.getElementById('tm-tiktok').value.trim() || null,
    photo_url: document.getElementById('tm-photo').value.trim() || null,
    metrique: document.getElementById('tm-metrique').value.trim() || null,
    statut: document.getElementById('tm-statut').value,
    mis_en_avant: document.getElementById('tm-avant').checked,
  };
}

function editTemoignage(t) {
  document.getElementById('tm-id').value = t.id;
  document.getElementById('tm-nom').value = t.nom || '';
  document.getElementById('tm-tiktok').value = t.lien_tiktok || '';
  document.getElementById('tm-texte').value = t.texte || '';
  document.getElementById('tm-metrique').value = t.metrique || '';
  document.getElementById('tm-photo').value = t.photo_url || '';
  document.getElementById('tm-statut').value = t.statut || 'en_attente';
  document.getElementById('tm-avant').checked = !!t.mis_en_avant;
  document.getElementById('tm-save-btn').textContent = '💾 Enregistrer';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function saveTemoignage() {
  const id = document.getElementById('tm-id').value;
  const body = _tmBody();
  if (!body.nom || body.texte.length < 10) { showToast('Nom + témoignage (≥10) requis'); return; }
  try {
    const res = await fetch('/admin/temoignages' + (id ? '/' + id : ''), {
      method: id ? 'PUT' : 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(body),
    });
    if (!res.ok) { const d = await res.json().catch(() => ({})); showToast('❌ ' + (d.detail || 'Erreur')); return; }
    showToast(id ? '✅ Modifié' : '✅ Ajouté'); resetTemoignageForm(); loadTemoignages();
  } catch (e) { showToast('❌ Erreur réseau'); }
}

async function quickPublish(id, publish) {
  // récupère la ligne courante pour ne pas écraser les champs
  try {
    const res = await fetch('/admin/temoignages', { headers: authHeaders() });
    const data = await res.json();
    const t = (data.temoignages || []).find(x => x.id === id);
    if (!t) return;
    t.statut = publish ? 'publie' : 'masque';
    const r2 = await fetch('/admin/temoignages/' + id, {
      method: 'PUT', headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        nom: t.nom, texte: t.texte, lien_tiktok: t.lien_tiktok, photo_url: t.photo_url,
        metrique: t.metrique, note: t.note, statut: t.statut, mis_en_avant: t.mis_en_avant,
      }),
    });
    if (!r2.ok) { showToast('❌ Erreur'); return; }
    showToast(publish ? '✅ Publié' : '🚫 Masqué'); loadTemoignages();
  } catch (e) { showToast('❌ Erreur réseau'); }
}

async function deleteTemoignage(id) {
  if (!confirm('Supprimer ce témoignage ?')) return;
  try {
    const res = await fetch('/admin/temoignages/' + id, { method: 'DELETE', headers: authHeaders() });
    if (!res.ok) { showToast('❌ Erreur'); return; }
    showToast('✅ Supprimé'); loadTemoignages();
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

/* ── RECHERCHE GMV (outil minimal, pas de cache/quota) ────────────────── */
async function lookupRechercheGmv() {
  const handle = (document.getElementById('rgmv-handle').value || '').trim();
  const box = document.getElementById('rgmv-result');
  if (!handle) { showToast('Entre un handle.'); return; }
  box.innerHTML = '<div class="empty">⏳…</div>';
  try {
    const res = await fetch(`/admin/recherche-gmv?handle=${encodeURIComponent(handle)}`, {
      headers: authHeaders(),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      box.innerHTML = `<div class="empty">❌ ${data.detail || 'Erreur'}</div>`;
      return;
    }
    if (data.reliable === false) {
      box.innerHTML = `
        <div style="font-size:14px;color:#e67e22;font-weight:700">⚠️ Aucune donnée de ventes sur 90j (compte non couvert par KeyAPI ou sans ventes Shop)</div>
        <div style="color:var(--muted,#6b7280);margin-top:4px">@${data.unique_id || ''} · ${data.nickname || ''}</div>
        <div style="color:var(--muted,#6b7280);margin-top:6px;font-size:12px">Pas de fallback chiffré : le "GMV lifetime" des produits KeyAPI est le GMV global du produit (tous vendeurs), pas celui du compte.</div>`;
    } else if (data.last_sale_date) {
      box.innerHTML = `
        <div style="font-size:28px;font-weight:900">n/d</div>
        <div style="color:var(--muted,#6b7280)">@${data.unique_id || ''} · ${data.nickname || ''}</div>
        <div style="color:#e67e22;margin-top:6px;font-size:12px">⚠️ KeyAPI ne remonte plus de ventes pour ce compte depuis le <strong>${data.last_sale_date}</strong> (limite source, pas forcément arrêt réel)${data.gmv_prior_90d ? ` · dernier GMV connu : $${Math.round(data.gmv_prior_90d).toLocaleString()} sur le mois précédant cette date` : ''}.</div>`;
    } else {
      box.innerHTML = `
        <div style="font-size:28px;font-weight:900">$${(data.gmv_30d || 0).toLocaleString()}</div>
        <div style="color:var(--muted,#6b7280)">@${data.unique_id || ''} · ${data.nickname || ''} · ${(data.sales_30d || 0).toLocaleString()} ventes (30j)</div>`;
    }
  } catch (e) {
    box.innerHTML = '<div class="empty">❌ Erreur réseau</div>';
  }
}

/* ── AFFILIÉS ──────────────────────────────────────────────────────────── */
async function loadAffiliates() {
  const list = document.getElementById('affiliates-list');
  if (!list) return;
  list.innerHTML = '<div class="empty">Chargement…</div>';
  try {
    const res = await fetch('/admin/affiliates', { headers: authHeaders() });
    if (!res.ok) { if (res.status === 403) { showLogin(); return; } list.innerHTML = '<div class="empty">❌ Erreur</div>'; return; }
    const data = await res.json();
    const rows = data.affiliates || [];
    if (!rows.length) { list.innerHTML = '<div class="empty">Aucun affilié pour le moment.</div>'; return; }
    const badge = s => s === 'approved' ? '🟢 Approuvé' : s === 'pending' ? '🟡 En attente'
                     : s === 'disabled' ? '⚫ Désactivé' : '🔴 Rejeté';
    list.innerHTML = rows.map(a => {
      const em = esc(a.email);
      return `
      <div class="user-card">
        <div style="font-size:11px;font-weight:700;color:var(--muted)">${badge(a.status)}${a.code ? ' · code <code>' + esc(a.code) + '</code>' : ''}</div>
        <div style="font-weight:700;margin:4px 0">${em}</div>
        <div style="font-size:13px;margin-bottom:6px">👥 <strong>${a.signups || 0}</strong> inscrit(s) via ce lien</div>
        <div class="actions">
          ${a.status !== 'approved' ? `<button class="btn btn-block" onclick="setAffiliateStatus('${em}','approved')">✅ Approuver</button>` : ''}
          ${a.status === 'approved' ? `<button class="btn btn-block" onclick="setAffiliateStatus('${em}','disabled')">🚫 Désactiver</button>` : ''}
          ${a.status === 'pending' ? `<button class="btn btn-block" onclick="setAffiliateStatus('${em}','rejected')">🗑️ Rejeter</button>` : ''}
          ${a.status === 'disabled' || a.status === 'rejected' ? `<button class="btn btn-block" onclick="setAffiliateStatus('${em}','approved')">♻️ Réactiver</button>` : ''}
        </div>
      </div>`;
    }).join('');
  } catch (e) { list.innerHTML = '<div class="empty">❌ Erreur réseau</div>'; }
}

async function createAffiliate() {
  const input = document.getElementById('aff-email');
  const email = (input.value || '').trim().toLowerCase();
  if (!email || email.indexOf('@') < 0) { showToast('Email invalide'); return; }
  try {
    const res = await fetch('/admin/affiliates', {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ email }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) { showToast('❌ ' + (data.detail || 'Échec')); return; }
    input.value = '';
    showToast('✅ Affilié créé');
    loadAffiliates();
  } catch (e) { showToast('❌ Erreur réseau'); }
}

async function setAffiliateStatus(email, status) {
  try {
    const res = await fetch('/admin/affiliates/status', {
      method: 'POST',
      headers: authHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ email, status }),
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok) { showToast('❌ ' + (data.detail || 'Échec')); return; }
    showToast('✅ Mis à jour');
    loadAffiliates();
  } catch (e) { showToast('❌ Erreur réseau'); }
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
