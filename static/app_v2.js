/* ============================================================
   TikTok Shop Vidéo Analyzer — app_v2.js
   by Dope Ventures
   ============================================================ */

'use strict';

// ── CONSTANTES ────────────────────────────────────────────────
const STORAGE_KEY   = 'dv_history';
const USAGE_KEY     = 'dv_usage';
const USER_KEY      = 'dv_user';
const MAX_HISTORY   = 20;
const FREE_LIMIT    = 999; // limite levée pendant la beta

const LABELS = {
  accroche:              '🎯 Accroche',
  discours:              '🗣️ Discours',
  qualite_visuelle:      '🎥 Qualité visuelle',
  visibilite_produit:    '📦 Produit',
  call_to_action:        '📢 Appel à l\'action',
  energie_dynamisme:     '⚡ Énergie',
  credibilite_confiance: '🤝 Crédibilité',
};

// ── ÉTAT GLOBAL ───────────────────────────────────────────────
let selectedFile   = null;
let serverReady    = false;
let currentData    = null;
let currentFilename = '';
let deferredPrompt = null;

// ── INIT ──────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  wakeServer();
  updateUsageCounter();
  updateHistoryBadge();
  restoreUser();

  // PWA
  if ('serviceWorker' in navigator) navigator.serviceWorker.register('/static/sw.js');
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault(); deferredPrompt = e;
    document.getElementById('pwa-banner').style.display = 'flex';
  });
});

// ── SERVER WAKE ───────────────────────────────────────────────
async function wakeServer() {
  const status = document.getElementById('server-status');
  try {
    const res = await fetch('/health', { signal: AbortSignal.timeout(5000) });
    if (res.ok) { serverReady = true; return; }
  } catch {}
  status.style.display = 'block';
  for (let i = 0; i < 20; i++) {
    await new Promise(r => setTimeout(r, 3000));
    try {
      const res = await fetch('/health', { signal: AbortSignal.timeout(5000) });
      if (res.ok) { serverReady = true; status.style.display = 'none'; return; }
    } catch {}
  }
  status.textContent = '❌ Serveur indisponible. Rafraîchis la page.';
}

// ── TABS ──────────────────────────────────────────────────────
function switchTab(tab) {
  document.getElementById('tab-analyze-content').style.display  = tab === 'analyze'  ? 'block' : 'none';
  document.getElementById('tab-history-content').style.display  = tab === 'history'  ? 'block' : 'none';
  document.getElementById('tab-analyze').classList.toggle('active',  tab === 'analyze');
  document.getElementById('tab-history').classList.toggle('active',  tab === 'history');
  if (tab === 'history') renderHistory();
}

// ── UPLOAD ────────────────────────────────────────────────────
const uploadArea = document.getElementById('upload-area');
const fileInput  = document.getElementById('video-file');

uploadArea.addEventListener('click', () => fileInput.click());
fileInput.addEventListener('change', e => { if (e.target.files[0]) setFile(e.target.files[0]); });
uploadArea.addEventListener('dragover',  e => { e.preventDefault(); uploadArea.classList.add('active'); });
uploadArea.addEventListener('dragleave', () => uploadArea.classList.remove('active'));
uploadArea.addEventListener('drop', e => {
  e.preventDefault(); uploadArea.classList.remove('active');
  const f = e.dataTransfer.files[0];
  if (f && f.type.startsWith('video/')) setFile(f);
});

function setFile(f) {
  selectedFile = f;
  document.getElementById('error-box').style.display = 'none';
  const tag = document.getElementById('file-tag');
  tag.textContent = `📎 ${f.name} (${(f.size / 1024 / 1024).toFixed(1)} Mo)`;
  tag.style.display = 'block';
  document.getElementById('analyze-btn').disabled = false;
}

document.getElementById('analyze-btn').addEventListener('click', analyzeVideo);

// ── FRAME EXTRACTION ──────────────────────────────────────────
async function extractFrames(file, numFrames = 6) {
  return new Promise((resolve, reject) => {
    const video = document.createElement('video');
    video.muted = true; video.playsInline = true;
    const url = URL.createObjectURL(file);
    video.src = url;
    video.onloadedmetadata = async () => {
      const dur = video.duration;
      const W = 480;
      const H = Math.round(W * video.videoHeight / Math.max(video.videoWidth, 1)) || W;
      const canvas = document.createElement('canvas');
      canvas.width = W; canvas.height = H;
      const ctx = canvas.getContext('2d');
      // 1re image : aléatoire entre 1-3s
      const first = 1 + Math.random() * Math.min(2, Math.max(0, dur - 1.1));
      const ts = [first];
      for (let i = 1; i < numFrames; i++)
        ts.push(Math.random() * Math.max(dur - 0.1, 0.1));
      ts.sort((a, b) => a - b);
      const frames = [];
      for (const t of ts) {
        await new Promise(r => {
          video.currentTime = t;
          video.onseeked = () => {
            ctx.drawImage(video, 0, 0, W, H);
            frames.push(canvas.toDataURL('image/jpeg', 0.8).split(',')[1]);
            r();
          };
        });
      }
      URL.revokeObjectURL(url);
      resolve(frames);
    };
    video.onerror = () => { URL.revokeObjectURL(url); reject(new Error('Vidéo illisible sur ce navigateur')); };
  });
}

// ── AUDIO EXTRACTION ─────────────────────────────────────────
async function extractAudio(file) {
  try {
    const arrayBuffer = await file.arrayBuffer();
    const tmpCtx = new (window.AudioContext || window.webkitAudioContext)();
    const audioBuffer = await tmpCtx.decodeAudioData(arrayBuffer);
    await tmpCtx.close();
    const SR = 16000;
    const offline = new OfflineAudioContext(1, Math.ceil(audioBuffer.duration * SR), SR);
    const src = offline.createBufferSource();
    src.buffer = audioBuffer; src.connect(offline.destination); src.start();
    const rendered = await offline.startRendering();
    const samples  = rendered.getChannelData(0);
    const buf = new ArrayBuffer(44 + samples.length * 2);
    const v   = new DataView(buf);
    const str = (o, s) => { for (let i = 0; i < s.length; i++) v.setUint8(o + i, s.charCodeAt(i)); };
    str(0,'RIFF'); v.setUint32(4, 36 + samples.length * 2, true);
    str(8,'WAVE'); str(12,'fmt '); v.setUint32(16,16,true);
    v.setUint16(20,1,true); v.setUint16(22,1,true);
    v.setUint32(24,SR,true); v.setUint32(28,SR*2,true);
    v.setUint16(32,2,true); v.setUint16(34,16,true);
    str(36,'data'); v.setUint32(40, samples.length * 2, true);
    for (let i = 0; i < samples.length; i++) {
      const s = Math.max(-1, Math.min(1, samples[i]));
      v.setInt16(44 + i * 2, s < 0 ? s * 0x8000 : s * 0x7FFF, true);
    }
    return new Blob([buf], { type: 'audio/wav' });
  } catch { return null; }
}

// ── MAIN FLOW ────────────────────────────────────────────────
async function analyzeVideo() {
  if (!selectedFile) return;

  document.getElementById('error-box').style.display      = 'none';
  document.getElementById('upload-section').style.display  = 'none';
  document.getElementById('loading-section').style.display = 'block';
  setLoadingText('🎬 Extraction des images et de l\'audio…');

  if (!serverReady) {
    setLoadingText('⏳ Réveil du serveur…');
    for (let i = 0; i < 15 && !serverReady; i++)
      await new Promise(r => setTimeout(r, 2000));
  }

  try {
    const [frames, audioBlob] = await Promise.all([
      extractFrames(selectedFile, 6),
      extractAudio(selectedFile),
    ]);

    setLoadingText('🤖 Analyse IA en cours…');
    const fd = new FormData();
    fd.append('frames', JSON.stringify(frames));
    if (audioBlob) fd.append('audio', audioBlob, 'audio.wav');

    const ctrl    = new AbortController();
    const timer   = setTimeout(() => ctrl.abort(), 65000);
    const headers = {};
    const email   = localStorage.getItem(USER_KEY);
    if (email) headers['Authorization'] = `Bearer ${email}`;
    const res = await fetch('/analyze', { method: 'POST', body: fd, signal: ctrl.signal, headers });
    clearTimeout(timer);

    if (!res.ok) throw new Error((await res.json()).detail || 'Erreur serveur');

    const data = await res.json();
    currentData     = data;
    currentFilename = selectedFile.name;

    // Sync le compteur avec la réponse serveur si disponible
    if (data.usage?.used !== undefined) {
      localStorage.setItem(USAGE_KEY, data.usage.used);
      updateUsageCounter();
    } else {
      incrementUsage();
    }
    saveToHistory(data, currentFilename);
    showResults(data);

  } catch (e) {
    document.getElementById('loading-section').style.display = 'none';
    document.getElementById('upload-section').style.display  = 'block';
    showError(e.name === 'AbortError'
      ? '❌ Délai dépassé. Réessaie avec une vidéo plus courte.'
      : '❌ ' + e.message);
  }
}

function setLoadingText(txt) {
  document.getElementById('loading-text').textContent = txt;
}
function showError(msg) {
  const eb = document.getElementById('error-box');
  eb.textContent = msg; eb.style.display = 'block';
}

// ── SCORE COLORS ─────────────────────────────────────────────
function scoreColor(n) {
  if (n >= 7) return '#00e5a0';
  if (n >= 5) return '#ffc107';
  return '#ff4757';
}

// ── SHOW RESULTS ─────────────────────────────────────────────
function showResults(d) {
  document.getElementById('loading-section').style.display  = 'none';
  document.getElementById('results-section').style.display  = 'block';

  // Score global
  document.getElementById('score-global').textContent = d.score_global ?? '—';

  // Grille scores
  const grid = document.getElementById('scores-grid');
  grid.innerHTML = '';
  if (d.scores) {
    Object.entries(d.scores).forEach(([k, v]) => {
      const n   = v.note ?? 0;
      const col = scoreColor(n);
      const card = document.createElement('div');
      card.className = 'score-card';
      card.innerHTML = `
        <div class="score-label">${LABELS[k] || k}</div>
        <div class="score-value" style="color:${col}">${n}<span style="font-size:16px;color:var(--muted)">/10</span></div>
        <div class="score-bar"><div class="score-bar-fill" style="width:0%;background:${col}"></div></div>
        <div class="score-comment">${v.commentaire || ''}</div>
      `;
      grid.appendChild(card);
      requestAnimationFrame(() => requestAnimationFrame(() => {
        card.querySelector('.score-bar-fill').style.width = (n * 10) + '%';
      }));
    });
  }

  // Détection
  const detGrid = document.getElementById('detection-grid');
  detGrid.innerHTML = '';
  const det = d.detection;
  if (det) {
    const items = [
      { label: '📦 Produit',       val: det.produit || '—',       cls: det.produit && det.produit !== 'non détecté' ? 'det-neu' : 'det-bad' },
      { label: '💶 Prix estimé',   val: det.prix_estime || '—',   cls: det.prix_rentable ? 'det-ok' : 'det-neu' },
      { label: '🎯 Type d\'accroche', val: det.hook_type || '—',  cls: 'det-neu' },
      { label: '⚡ Force accroche', val: (det.hook_force ?? '—') + (det.hook_force ? '/10' : ''), cls: det.hook_force >= 7 ? 'det-ok' : det.hook_force >= 5 ? 'det-neu' : 'det-bad' },
    ];
    if (det.prix_rentable !== undefined) {
      items[1].val += det.prix_rentable ? ' ✓ rentable' : ' — à optimiser';
    }
    items.forEach(({ label, val, cls }) => {
      const div = document.createElement('div');
      div.className = 'detection-item';
      div.innerHTML = `<label>${label}</label><strong class="${cls}">${val}</strong>`;
      detGrid.appendChild(div);
    });
  }

  // Potentiel viral
  const vp = d.viral_potential;
  if (vp) {
    document.getElementById('viral-score').textContent      = vp.score ?? '—';
    document.getElementById('viral-prix').textContent       = vp.facteur_prix || '';
    document.getElementById('viral-explication').textContent = vp.explication || '';
  }

  // Points forts / faibles
  fillList('points-forts',  d.points_forts,     '', true);
  fillList('points-faibles',d.points_ameliorer, '', true);

  // Recommandations accroches
  const reco = d.recommendations_hooks;
  if (reco) {
    document.getElementById('hook-type-propose').textContent = reco.hook_type_propose || '—';
    document.getElementById('hook-reason').textContent       = reco.raison || '';
    const exList = document.getElementById('hook-examples');
    exList.innerHTML = (reco.exemples_concrets || []).map(e => `<li>${e}</li>`).join('');
  }

  // Conseils
  fillList('conseils-list', d.conseils_concrets, '', true);

  // Structure de vente
  const sv = d.structure_vente;
  if (sv) {
    document.getElementById('structure-vente-section').style.display = 'block';

    // Étapes du funnel
    const etapes = ['accroche', 'probleme', 'solution', 'produit', 'cta'];
    etapes.forEach(k => {
      const step = sv[k];
      if (!step) return;
      const n = step.score ?? 0;
      const el = document.getElementById(`sv-step-${k}`) || document.getElementById(`sv-${k}`);
      if (el) {
        el.classList.remove('sv-ok', 'sv-warn', 'sv-bad');
        el.classList.add(!step.present ? 'sv-bad' : n >= 7 ? 'sv-ok' : n >= 5 ? 'sv-warn' : 'sv-bad');
      }
      const scoreEl = document.getElementById(`sv-score-${k}`);
      if (scoreEl) scoreEl.textContent = step.present ? `${n}/10` : '—';
      scoreEl && (scoreEl.style.color = !step.present ? 'var(--danger)' : scoreColor(n));

      const feedEl = document.getElementById(`sv-feedback-${k}`);
      if (feedEl) feedEl.textContent = step.feedback || '';
    });

    // Score global structure
    const scoreStrEl = document.getElementById('score-structure');
    if (scoreStrEl) {
      scoreStrEl.textContent = sv.score_structure ?? '—';
      const s = sv.score_structure ?? 0;
      scoreStrEl.style.color = s >= 70 ? 'var(--primary)' : s >= 50 ? 'var(--warning)' : 'var(--danger)';
    }

    // Résumé
    const summaryEl = document.getElementById('structure-summary');
    if (summaryEl) {
      const parts = [];
      if (sv.ordre_naturel) parts.push('✅ Ordre naturel respecté');
      else parts.push('⚠️ Ordre du flux non respecté');
      if (sv.transitions === 'fluides') parts.push('✅ Transitions fluides');
      else if (sv.transitions) parts.push(`⚠️ Transitions : ${sv.transitions}`);
      if (sv.etapes_manquantes?.length) parts.push(`❌ Étapes absentes : ${sv.etapes_manquantes.join(', ')}`);
      if (sv.etapes_faibles?.length) parts.push(`⚠️ Étapes faibles : ${sv.etapes_faibles.join(', ')}`);
      summaryEl.textContent = parts.join(' · ') || 'Structure correcte ✅';
    }

    // Améliorations structure
    const amelioEl = document.getElementById('ameliorations-structure');
    if (amelioEl && d.ameliorations_structure?.length) {
      amelioEl.innerHTML = `
        <h3 style="color:var(--warning);margin-bottom:8px">💡 Améliorer le flux de vente</h3>
        <ul class="points-list neg">${(d.ameliorations_structure).map(a => `<li>${a}</li>`).join('')}</ul>`;
    }
  } else {
    document.getElementById('structure-vente-section').style.display = 'none';
  }

  // Potentiel de conversion par prix
  const pc = d.prix_conversion;
  if (pc) {
    document.getElementById('prix-conversion-section').style.display = 'block';

    document.getElementById('pc-montant').textContent =
      pc.montant ? `${pc.montant} €` : 'Non détecté';

    const catLabels = { economique: '🟢 Économique', moyen: '🟡 Moyen', premium: '🔴 Premium', inconnu: '— Inconnu' };
    document.getElementById('pc-categorie').textContent = catLabels[pc.categorie] || pc.categorie || '—';

    const pot = pc.potentiel_conversion || {};
    const delaiLabels = { j7: 'Jour 7', j30: 'Jour 30', inconnu: '—' };
    document.getElementById('pc-delai').textContent = delaiLabels[pot.temps_attendre] || pot.temps_attendre || '—';

    document.getElementById('pc-conseil').textContent = pc.conseil_prix || '—';

    document.getElementById('pc-disclaimer').textContent =
      d.disclaimer_realisme || '⚠️ Cette analyse est un guide, pas une certitude. L\'algo TikTok surprend toujours.';
  } else {
    document.getElementById('prix-conversion-section').style.display = 'none';
  }

  // Transcription
  if (d.transcript) {
    document.getElementById('transcript-section').style.display = 'block';
    document.getElementById('transcript-text').textContent = d.transcript;
  }

  // Verdict
  if (d.verdict) {
    document.getElementById('verdict-section').style.display = 'block';
    document.getElementById('verdict-text').textContent = d.verdict;
  }

  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function fillList(id, items, icon, noIcon) {
  const el = document.getElementById(id);
  if (!el) return;
  el.innerHTML = (items || []).map(t => `<li>${noIcon ? '' : icon}${t}</li>`).join('');
}

// ── RESET ────────────────────────────────────────────────────
function resetAnalysis() {
  selectedFile = null; currentData = null;
  document.getElementById('results-section').style.display    = 'none';
  document.getElementById('upload-section').style.display     = 'block';
  document.getElementById('file-tag').style.display           = 'none';
  document.getElementById('video-file').value                 = '';
  document.getElementById('analyze-btn').disabled             = true;
  document.getElementById('transcript-section').style.display       = 'none';
  document.getElementById('verdict-section').style.display           = 'none';
  document.getElementById('structure-vente-section').style.display   = 'none';
  document.getElementById('prix-conversion-section').style.display   = 'none';
  document.getElementById('error-box').style.display                = 'none';
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ── USAGE COUNTER ─────────────────────────────────────────────
function getUsage()       { return parseInt(localStorage.getItem(USAGE_KEY) || '0', 10); }
function incrementUsage() { localStorage.setItem(USAGE_KEY, getUsage() + 1); updateUsageCounter(); }
function updateUsageCounter() {
  const n = getUsage();
  const el = document.getElementById('usage-count');
  if (el) el.textContent = `${n} / ${FREE_LIMIT}`;
}

// ── HISTORY ──────────────────────────────────────────────────
function getHistory() {
  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); } catch { return []; }
}

function saveToHistory(data, filename) {
  const entries = getHistory();
  // Évite les doublons consécutifs
  if (entries[0]?.id === data.id) return;
  entries.unshift({
    id:                    Date.now(),
    date:                  new Date().toISOString(),
    filename:              filename || 'vidéo',
    score_global:          data.score_global,
    verdict:               data.verdict,
    scores:                data.scores,
    detection:             data.detection,
    viral_potential:       data.viral_potential,
    points_forts:          data.points_forts,
    points_ameliorer:      data.points_ameliorer,
    recommendations_hooks: data.recommendations_hooks,
    conseils_concrets:     data.conseils_concrets,
    transcript:            data.transcript,
  });
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries.slice(0, MAX_HISTORY)));
  updateHistoryBadge();
}

function updateHistoryBadge() {
  const n = getHistory().length;
  const b = document.getElementById('history-badge');
  if (b) { b.textContent = n; b.style.display = n > 0 ? 'inline-block' : 'none'; }
}

function renderHistory() {
  const entries = getHistory();
  const container = document.getElementById('history-list');
  if (!container) return;
  if (entries.length === 0) {
    container.innerHTML = '<div class="history-empty">📋 Aucune analyse pour l\'instant.</div>';
    return;
  }
  let html = `<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
    <span style="font-size:13px;color:var(--muted)">${entries.length} analyse${entries.length > 1 ? 's' : ''}</span>
    <button onclick="clearHistory()" style="background:none;border:1px solid rgba(255,71,87,.3);color:#ff6b7a;border-radius:6px;padding:4px 10px;font-size:11px;cursor:pointer">Tout effacer</button>
  </div>`;
  entries.forEach((e, i) => {
    const d = new Date(e.date);
    const ds = d.toLocaleDateString('fr-FR', { day:'2-digit', month:'short' }) + ' · ' + d.toLocaleTimeString('fr-FR', { hour:'2-digit', minute:'2-digit' });
    const snippet = (e.verdict || e.filename || '').slice(0, 55) + '…';
    html += `<div class="history-entry" onclick="openHistoryEntry(${i})">
      <div class="history-score">${e.score_global ?? '—'}</div>
      <div class="history-info">
        <div class="history-date">${ds} · ${e.filename}</div>
        <div class="history-snippet">${snippet}</div>
      </div>
      <button class="history-del" onclick="deleteEntry(event,${i})">✕</button>
    </div>`;
  });
  container.innerHTML = html;
}

function openHistoryEntry(i) {
  const e = getHistory()[i];
  if (!e) return;
  currentData = e; currentFilename = e.filename;
  switchTab('analyze');
  document.getElementById('upload-section').style.display = 'none';
  showResults(e);
}

function deleteEntry(event, i) {
  event.stopPropagation();
  const entries = getHistory();
  entries.splice(i, 1);
  localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
  updateHistoryBadge(); renderHistory();
}

function clearHistory() {
  if (!confirm('Effacer tout l\'historique ?')) return;
  localStorage.removeItem(STORAGE_KEY);
  updateHistoryBadge(); renderHistory();
}

// ── EXPORT PDF ───────────────────────────────────────────────
function exportPDF() {
  if (!currentData || !window.jspdf) return;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: 'mm', format: 'a4' });
  const GREEN = [0, 229, 160];
  const DARK  = [13, 15, 20];
  const BLUE  = [77, 159, 255];
  let y = 0;

  // En-tête
  doc.setFillColor(...DARK);
  doc.rect(0, 0, 210, 36, 'F');
  doc.setFillColor(...GREEN);
  doc.rect(0, 34, 210, 2, 'F');
  doc.setTextColor(...GREEN);
  doc.setFontSize(16); doc.setFont('helvetica', 'bold');
  doc.text('TikTok Shop Vidéo Analyzer', 105, 14, { align: 'center' });
  doc.setFontSize(9); doc.setFont('helvetica', 'normal');
  doc.setTextColor(140, 140, 140);
  doc.text('by Dope Ventures', 105, 21, { align: 'center' });
  doc.text(`${new Date().toLocaleDateString('fr-FR')} · ${currentFilename}`, 105, 28, { align: 'center' });
  y = 46;

  // Score global
  doc.setFillColor(...BLUE);
  doc.roundedRect(15, y, 180, 20, 3, 3, 'F');
  doc.setTextColor(212, 175, 55);
  doc.setFontSize(20); doc.setFont('helvetica', 'bold');
  doc.text(`Score global : ${currentData.score_global ?? '—'} / 100`, 105, y + 13, { align: 'center' });
  y += 26;

  // Verdict
  if (currentData.verdict) {
    doc.setFontSize(9); doc.setFont('helvetica', 'italic'); doc.setTextColor(100, 100, 100);
    const lines = doc.splitTextToSize(currentData.verdict, 180);
    doc.text(lines, 15, y); y += lines.length * 5 + 6;
  }

  const section = (title, col) => {
    if (y > 265) { doc.addPage(); y = 15; }
    doc.setFillColor(...col);
    doc.rect(15, y, 180, 8, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(10); doc.setFont('helvetica', 'bold');
    doc.text(title, 19, y + 5.5); y += 12;
  };

  // Scores détaillés
  section('Analyse détaillée', BLUE);
  if (currentData.scores) {
    const LABELS_PDF = { accroche:'Accroche', discours:'Discours', qualite_visuelle:'Qualité visuelle', visibilite_produit:'Produit', call_to_action:'Appel à l\'action', energie_dynamisme:'Énergie', credibilite_confiance:'Crédibilité' };
    Object.entries(currentData.scores).forEach(([k, v]) => {
      if (y > 265) { doc.addPage(); y = 15; }
      const n = v.note ?? 0;
      const col = n >= 7 ? [0,229,160] : n >= 5 ? [255,193,7] : [255,71,87];
      doc.setTextColor(40,40,40); doc.setFontSize(9); doc.setFont('helvetica', 'bold');
      doc.text(LABELS_PDF[k] || k, 15, y);
      doc.setTextColor(...col); doc.text(`${n}/10`, 195, y, { align:'right' });
      doc.setFillColor(220,220,220); doc.roundedRect(15, y+2, 180, 3, 1, 1, 'F');
      doc.setFillColor(...col); doc.roundedRect(15, y+2, 180*n/10, 3, 1, 1, 'F');
      y += 7;
      if (v.commentaire) {
        doc.setTextColor(100,100,100); doc.setFont('helvetica','normal'); doc.setFontSize(8);
        const lines = doc.splitTextToSize(v.commentaire, 176);
        doc.text(lines, 19, y); y += lines.length * 4 + 3;
      }
    });
  }

  const listSection = (title, col, items, prefix) => {
    if (!items?.length) return;
    section(title, col);
    items.forEach(p => {
      if (y > 270) { doc.addPage(); y = 15; }
      doc.setTextColor(40,40,40); doc.setFontSize(9); doc.setFont('helvetica','normal');
      const lines = doc.splitTextToSize(`${prefix} ${p}`, 176);
      doc.text(lines, 19, y); y += lines.length * 4.5 + 2;
    });
  };

  listSection('Points forts',     [34,139,34],    currentData.points_forts,     '+');
  listSection('À améliorer',      [200,100,0],    currentData.points_ameliorer, '!');
  listSection('Conseils concrets', BLUE,           currentData.conseils_concrets,'→');

  // Recommandations accroches
  const reco = currentData.recommendations_hooks;
  if (reco) {
    section('Recommandation accroche', [77,159,255]);
    doc.setTextColor(0,229,160); doc.setFontSize(10); doc.setFont('helvetica','bold');
    doc.text(reco.hook_type_propose || '', 15, y); y += 6;
    if (reco.raison) {
      doc.setTextColor(100,100,100); doc.setFont('helvetica','italic'); doc.setFontSize(8);
      const lines = doc.splitTextToSize(reco.raison, 178);
      doc.text(lines, 15, y); y += lines.length * 4 + 4;
    }
    (reco.exemples_concrets || []).forEach(e => {
      if (y > 270) { doc.addPage(); y = 15; }
      doc.setTextColor(60,60,60); doc.setFont('helvetica','normal'); doc.setFontSize(9);
      const lines = doc.splitTextToSize(`→ "${e}"`, 176);
      doc.text(lines, 19, y); y += lines.length * 4.5 + 2;
    });
  }

  if (currentData.transcript) {
    section('Transcription audio', [80,80,80]);
    doc.setTextColor(80,80,80); doc.setFontSize(8); doc.setFont('helvetica','italic');
    const lines = doc.splitTextToSize(currentData.transcript, 176);
    doc.text(lines, 19, y);
  }

  // Pied de page
  const pages = doc.getNumberOfPages();
  for (let i = 1; i <= pages; i++) {
    doc.setPage(i);
    doc.setFontSize(7); doc.setTextColor(100,100,100); doc.setFont('helvetica','normal');
    doc.text(`TikTok Shop Vidéo Analyzer · by Dope Ventures · ${i}/${pages}`, 105, 291, { align:'center' });
  }

  doc.save(`analyse-dv-${Date.now()}.pdf`);
}

// ── AUTH ─────────────────────────────────────────────────────
document.getElementById('btn-auth').addEventListener('click', () => {
  document.getElementById('auth-modal').classList.add('active');
});

function closeModal() {
  document.getElementById('auth-modal').classList.remove('active');
}

function handleAuth(event) {
  event.preventDefault();
  const email = document.getElementById('email-input').value;
  if (!email) return;
  localStorage.setItem(USER_KEY, email);
  restoreUser();
  closeModal();
}

function restoreUser() {
  const email = localStorage.getItem(USER_KEY);
  if (email) {
    document.getElementById('user-email').textContent = email;
    document.getElementById('btn-auth').textContent = 'Mon compte';
  }
}

// ── PWA ──────────────────────────────────────────────────────
function installPwa() {
  if (!deferredPrompt) return;
  deferredPrompt.prompt();
  deferredPrompt.userChoice.then(() => {
    deferredPrompt = null;
    document.getElementById('pwa-banner').style.display = 'none';
  });
}

// Fermer modal en cliquant dehors
document.getElementById('auth-modal').addEventListener('click', function(e) {
  if (e.target === this) closeModal();
});
