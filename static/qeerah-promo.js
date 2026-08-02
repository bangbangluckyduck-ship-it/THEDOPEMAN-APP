/*!
 * Bandeau promotionnel Qeerah — module autonome.
 *
 * Affiche un bandeau fixe en haut de page avec un décompte vers une échéance
 * RÉELLE, fixée depuis /dope-admin. Le décompte ne redémarre jamais par
 * visiteur : il vise la même date pour tout le monde, et le bandeau disparaît
 * de lui-même une fois l'échéance atteinte.
 *
 * L'horloge du visiteur n'est pas digne de confiance (fuseau faux, machine
 * désynchronisée). On calcule donc un décalage à partir du `server_now`
 * renvoyé par l'API, et on l'applique à toutes les mesures de temps.
 *
 * Aucune dépendance. Se charge en `defer`, ne bloque jamais le rendu.
 */
(function () {
  'use strict';

  var BANNER_ID = 'qeerah-promo-banner';
  var clockOffset = 0;      // ms à ajouter à Date.now() pour coller au serveur
  var tickTimer = null;
  var basePadding = null;   // espacement haut de la page avant insertion du bandeau

  function now() {
    return Date.now() + clockOffset;
  }

  function two(n) {
    return (n < 10 ? '0' : '') + n;
  }

  /** « 2 j 04:37:12 » — on n'affiche les jours que s'il y en a. */
  function formatRemaining(ms) {
    if (ms < 0) ms = 0;
    var totalSec = Math.floor(ms / 1000);
    var days = Math.floor(totalSec / 86400);
    var hours = Math.floor((totalSec % 86400) / 3600);
    var mins = Math.floor((totalSec % 3600) / 60);
    var secs = totalSec % 60;
    if (days > 0) {
      return days + ' j ' + two(hours) + ':' + two(mins) + ':' + two(secs);
    }
    return two(hours) + ':' + two(mins) + ':' + two(secs);
  }

  function removeBanner() {
    if (tickTimer) { clearInterval(tickTimer); tickTimer = null; }
    var el = document.getElementById(BANNER_ID);
    if (el) el.parentNode.removeChild(el);
    document.documentElement.style.removeProperty('--qeerah-promo-height');
    // On REMET la valeur d'origine au lieu de vider la propriété : si la page
    // déclare son espacement en raccourci (`padding: 24px`), poser
    // paddingTop = '' efface la composante haute du raccourci et le contenu
    // vient se coller au bord une fois le bandeau fermé.
    document.body.style.paddingTop = (typeof basePadding === 'number') ? basePadding + 'px' : '';
  }

  function injectStyles() {
    if (document.getElementById('qeerah-promo-style')) return;
    var css =
      '#' + BANNER_ID + '{position:fixed;top:0;left:0;right:0;z-index:9999;' +
        'background:linear-gradient(135deg,#1F3A70,#2563EB);color:#fff;' +
        'font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;' +
        'display:flex;align-items:center;justify-content:center;gap:14px;' +
        'flex-wrap:wrap;padding:10px 44px 10px 16px;font-size:14px;' +
        'line-height:1.4;box-shadow:0 2px 12px rgba(0,0,0,.18)}' +
      '#' + BANNER_ID + ' .qp-msg{font-weight:700}' +
      // Police système volontairement, PAS une chasse fixe : en monospace le O
      // majuscule se confond avec le zéro (« TIKTOKAOUT2026 » se lit
      // « TIKT0KA0UT2026 »), et le client recopie un code que Stripe refuse
      // sans lui dire pourquoi. L'espacement des lettres suffit à donner
      // l'aspect « code » sans créer l'ambiguïté.
      '#' + BANNER_ID + ' .qp-code{display:inline-block;background:rgba(255,255,255,.18);' +
        'border:1px dashed rgba(255,255,255,.55);border-radius:8px;padding:2px 10px;' +
        'font-weight:800;letter-spacing:.09em}' +
      '#' + BANNER_ID + ' .qp-count{font-variant-numeric:tabular-nums;font-weight:800;' +
        'background:rgba(0,0,0,.22);border-radius:8px;padding:3px 10px}' +
      '#' + BANNER_ID + ' .qp-cta{background:#fff;color:#1F3A70;text-decoration:none;' +
        'font-weight:800;padding:7px 15px;border-radius:9px;white-space:nowrap}' +
      '#' + BANNER_ID + ' .qp-cta:hover{background:#F0F4FF}' +
      '#' + BANNER_ID + ' .qp-close{position:absolute;right:10px;top:50%;' +
        'transform:translateY(-50%);background:transparent;border:0;color:rgba(255,255,255,.85);' +
        'font-size:20px;line-height:1;cursor:pointer;padding:4px 8px}' +
      '#' + BANNER_ID + ' .qp-close:hover{color:#fff}' +
      '@media(max-width:560px){#' + BANNER_ID + '{font-size:12.5px;gap:9px;padding:9px 38px 9px 12px}' +
        '#' + BANNER_ID + ' .qp-cta{padding:6px 12px}}';
    var st = document.createElement('style');
    st.id = 'qeerah-promo-style';
    st.textContent = css;
    document.head.appendChild(st);
  }

  /** Décale le contenu pour que le bandeau ne recouvre pas les en-têtes fixes.
   *
   * Le padding d'origine de la page est mémorisé une fois pour toutes, et le
   * décalage vaut TOUJOURS « origine + hauteur actuelle ». Une version
   * antérieure ne faisait qu'augmenter le padding : en étroit le bandeau passe
   * sur trois lignes, et le décalage restait figé à cette hauteur une fois la
   * fenêtre réélargie, laissant un grand blanc en haut de page. */
  function applyOffset(el) {
    if (basePadding === null) {
      basePadding = parseInt(window.getComputedStyle(document.body).paddingTop, 10) || 0;
    }
    var h = el.offsetHeight;
    document.documentElement.style.setProperty('--qeerah-promo-height', h + 'px');
    document.body.style.paddingTop = (basePadding + h) + 'px';
  }

  function render(promo) {
    injectStyles();

    var endsAt = promo.ends_at ? new Date(promo.ends_at).getTime() : null;
    if (endsAt && endsAt <= now()) return;          // déjà expirée

    var el = document.createElement('div');
    el.id = BANNER_ID;
    el.setAttribute('role', 'region');
    el.setAttribute('aria-label', 'Offre promotionnelle');

    var html = '<span class="qp-msg"></span>';
    if (promo.code) html += '<span class="qp-code"></span>';
    if (endsAt) html += '<span class="qp-count" aria-live="off">—</span>';
    html += '<a class="qp-cta" href="' + encodeURI(promo.cta_url || '/pricing') + '"></a>' +
            '<button class="qp-close" aria-label="Fermer le bandeau">&times;</button>';
    el.innerHTML = html;

    // textContent (et non innerHTML) : le message vient de l'admin, on ne lui
    // laisse pas injecter de balises dans toutes les pages du site.
    el.querySelector('.qp-msg').textContent = promo.message || 'Offre en cours';
    if (promo.code) el.querySelector('.qp-code').textContent = promo.code;
    el.querySelector('.qp-cta').textContent = promo.cta_label || 'En profiter';

    el.querySelector('.qp-close').addEventListener('click', function () {
      removeBanner();
      try { sessionStorage.setItem('qeerah_promo_closed', '1'); } catch (e) {}
    });

    document.body.appendChild(el);
    applyOffset(el);

    // La hauteur du bandeau bouge après l'insertion : chargement des polices,
    // passage du contenu à la ligne sur écran étroit, rotation du téléphone.
    // Une mesure ponctuelle laissait un décalage faux (mesuré 168 px pour un
    // bandeau qui finissait à 209 px). On observe donc la hauteur réelle.
    if (typeof ResizeObserver === 'function') {
      new ResizeObserver(function () { applyOffset(el); }).observe(el);
    } else {
      window.addEventListener('resize', function () { applyOffset(el); });
      setTimeout(function () { applyOffset(el); }, 300);   // repli : polices chargées
    }

    if (!endsAt) return;

    var countEl = el.querySelector('.qp-count');
    function tick() {
      var left = endsAt - now();
      if (left <= 0) { removeBanner(); return; }   // l'offre se termine vraiment
      countEl.textContent = formatRemaining(left);
    }
    tick();
    tickTimer = setInterval(tick, 1000);
  }

  function start() {
    // Refermé pour cette session de navigation : on respecte le choix.
    try {
      if (sessionStorage.getItem('qeerah_promo_closed') === '1') return;
    } catch (e) {}

    fetch('/api/promo', { headers: { 'Accept': 'application/json' } })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (promo) {
        if (!promo || !promo.active) return;
        if (promo.server_now) {
          var serverMs = new Date(promo.server_now).getTime();
          if (!isNaN(serverMs)) clockOffset = serverMs - Date.now();
        }
        render(promo);
      })
      .catch(function () { /* pas de bandeau, jamais d'erreur visible */ });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }
})();
