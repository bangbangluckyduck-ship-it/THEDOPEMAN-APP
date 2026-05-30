/* ════════════════════════════════════════════════════════════════════════
 * Dope Admin — script de contrôle du back-office isolé (/dope-admin)
 * Sécurité : vérifie le token + le rôle admin au chargement, sinon redirige.
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

/* ── SÉCURITÉ : garde d'accès au chargement ───────────────────────────── */
async function guardAdmin() {
  const token = getToken();
  if (!token) { window.location.replace('/'); return false; }

  try {
    const res = await fetch('/api/user-info', { headers: authHeaders() });
    if (!res.ok) { window.location.replace('/'); return false; }
    const data = await res.json();
    const isAdmin = data && (data.is_admin === true || data.tier === 'admin');
    if (!isAdmin) { window.location.replace('/'); return false; }
    return true;
  } catch (e) {
    window.location.replace('/');
    return false;
  }
}

function adminLogout() {
  localStorage.removeItem(TOKEN_KEY);
  window.location.replace('/');
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
      if (res.status === 403) { window.location.replace('/'); return; }
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
  const tbody = document.getElementById('users-tbody');
  tbody.innerHTML = '<tr><td colspan="4" class="empty">Chargement…</td></tr>';
  try {
    const res = await fetch('/admin/users', { headers: authHeaders() });
    if (!res.ok) {
      if (res.status === 403) { window.location.replace('/'); return; }
      tbody.innerHTML = '<tr><td colspan="4" class="empty">❌ Erreur de chargement</td></tr>';
      return;
    }
    const data = await res.json();
    const users = (data && data.users) || [];
    if (!users.length) {
      tbody.innerHTML = '<tr><td colspan="4" class="empty">Aucun utilisateur</td></tr>';
      return;
    }
    tbody.innerHTML = users.map(u => {
      const email = esc(u.email || '');
      const expiry = u.expiry ? esc(u.expiry) : '<span style="color:var(--muted)">—</span>';
      return `
        <tr>
          <td>${email}</td>
          <td>${tierBadge(u.tier)}</td>
          <td>${expiry}</td>
          <td style="text-align:right">
            <button class="btn" onclick="changeUserTier('${email.replace(/'/g, "\\'")}', '${esc(u.tier)}')">⚙️ Changer plan</button>
          </td>
        </tr>`;
    }).join('');
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="4" class="empty">❌ Erreur réseau</td></tr>';
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
  const ok = await guardAdmin();
  if (!ok) return;
  // Révèle le back-office uniquement après validation du rôle admin
  const shell = document.getElementById('app-shell');
  if (shell) shell.style.display = 'flex';
  loadStats();
});
