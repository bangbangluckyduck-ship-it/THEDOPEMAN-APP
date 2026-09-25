/*!
 * Suivi de l'entonnoir de conversion — Google Analytics 4.
 *
 * S'appuie sur la file d'attente déjà posée par qeerah-consent.js : un
 * événement émis avant consentement est mis en attente et ne part que si
 * l'utilisateur accepte. Rien n'est envoyé sans accord.
 *
 * RÈGLE : aucune donnée personnelle dans les propriétés. Pas d'e-mail, pas
 * d'identifiant de compte, pas d'URL de vidéo. Uniquement des libellés de
 * parcours et des durées.
 *
 * Les événements sont nommés en français, comme le reste du produit, pour être
 * lisibles directement dans l'interface GA4 sans table de correspondance.
 */
(function () {
  'use strict';

  // ── Entonnoir interne (cf. entonnoir.py) ─────────────────────────────────
  // Compteur ANONYME, indépendant du consentement : aucun cookie, aucun
  // identifiant, seulement le nom de l'étape. Il existe parce que GA4 et le
  // pixel ne voient que les visiteurs qui acceptent les cookies — les taux de
  // passage entre marches y sont faux par construction.
  var INTERNE = {
    page_vue_accueil: 'accueil_vue',
    clic_cta_principal: 'cta_clic',
    analyse_demarree: 'analyse_lancee',
    resultat_partiel_affiche: 'resultat_partiel',
    clic_debloquer_resultat: 'debloquer_clic',
    clic_decrypter_feed_radar: 'feedradar_decrypter'
  };
  // Une seule fois par onglet : un visiteur qui recharge ou reclique ne doit
  // pas gonfler la marche.
  var UNE_FOIS_PAR_ONGLET = { accueil_vue: 1, cta_clic: 1 };

  function interne(etape) {
    try {
      if (UNE_FOIS_PAR_ONGLET[etape]) {
        var cle = 'q_evt_' + etape;
        if (sessionStorage.getItem(cle)) return;
        sessionStorage.setItem(cle, '1');
      }
    } catch (e) { /* stockage indisponible : on compte quand même */ }
    try {
      var corps = JSON.stringify({ e: etape });
      if (navigator.sendBeacon) {
        navigator.sendBeacon('/api/evt', new Blob([corps], { type: 'application/json' }));
      } else {
        fetch('/api/evt', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: corps, keepalive: true });
      }
    } catch (e) {}
  }

  // ── Pixel TikTok : les marches qui lui manquaient ─────────────────────────
  // QeerahTikTok ne fait rien sans consentement « publicité » (cf. qeerah-tiktok.js).
  // La vue de page part déjà seule (ttq.page) ; compte créé et paiement ont
  // leurs propres envois (CompleteRegistration navigateur, CompletePayment
  // serveur).
  var PIXEL = {
    cta_clic: ['ClickButton', { content_name: 'analyser_premiere_video' }],
    analyse_lancee: ['SubmitForm', { content_name: 'analyse_video' }],
    analyse_terminee: ['AnalyseTerminee', {}],
    mission_1: ['MissionEtape1', {}],
    mission_2: ['MissionEtape2', {}],
    mission_3: ['MissionEtape3', {}],
    mission_4: ['MissionEtape4', {}]
  };
  function pixel(etape) {
    try {
      var p = PIXEL[etape];
      if (p && window.QeerahTikTok && typeof window.QeerahTikTok.track === 'function') {
        window.QeerahTikTok.track(p[0], p[1], { event_id: window.QeerahTikTok.newEventId ? window.QeerahTikTok.newEventId() : undefined });
      }
    } catch (e) {}
  }

  /** Émet un événement : GA4 (si consentement), entonnoir interne, pixel. */
  function track(nom, props) {
    var etape = INTERNE[nom];
    if (nom === 'analyse_terminee' && props && props.resultat === 'succes') etape = 'analyse_terminee';
    if (nom === 'mission_etape_terminee' && props && props.etape) etape = 'mission_' + props.etape;
    if (etape) { interne(etape); pixel(etape); }
    try {
      if (typeof window.gtag !== 'function') return;
      window.gtag('event', nom, props || {});
    } catch (e) { /* le suivi ne doit jamais casser une page */ }
  }
  window.qTrack = track;

  /** Marque une étape franchie une seule fois par chargement de page. */
  var vus = {};
  function trackUnique(nom, props) {
    if (vus[nom]) return;
    vus[nom] = true;
    track(nom, props);
  }
  window.qTrackUnique = trackUnique;

  document.addEventListener('DOMContentLoaded', function () {
    var chemin = location.pathname.replace(/\/+$/, '') || '/';

    // 1 & 7 — vues de page structurantes
    // Accueil dans toutes les langues servies (/, /en, /en-ie, /pt-br, /es,
    // /es-mx, /it, /de) — seul « / » était compté.
    if (/^\/(|en|en-ie|pt-br|es|es-mx|it|de)$/.test(chemin)) trackUnique('page_vue_accueil');
    if (chemin === '/pricing' || chemin === '/pricing/compare') trackUnique('page_vue_tarifs');

    // 2 — clic sur l'appel à l'action principal
    document.addEventListener('click', function (e) {
      var el = e.target.closest && e.target.closest('a, button');
      if (!el) return;
      var txt = (el.textContent || '').trim().toLowerCase();
      var href = el.getAttribute('href') || '';

      if (/tester gratuitement|analyser une vidéo|essayer/.test(txt)) {
        track('clic_tester_gratuitement', { emplacement: el.closest('header') ? 'entete' : 'page' });
      }
      // 6 — accès à l'offre
      if (href.indexOf('/pricing') === 0 || /voir les (plans|tarifs)|découvrir qeerah pro/.test(txt)) {
        track('clic_voir_les_plans');
      }
      // 8 — intention d'abonnement
      if (/s'abonner|sabonner|passer à qeerah pro/.test(txt)) {
        track('clic_sabonner', { periodicite: window.BILLING || 'inconnue' });
      }
    }, true);

    // 9 — retour de paiement réussi (Stripe renvoie ?checkout=success)
    // `value` et `currency` sont indispensables : sans eux, GA4 ne peut calculer
    // ni chiffre d'affaires, ni coût d'acquisition, ni retour sur dépense. Le
    // montant est déduit de la périodicité choisie, posée par le front sur
    // window.BILLING avant la redirection vers Stripe.
    if (/[?&]checkout=success/.test(location.search)) {
      var annuel = (window.BILLING || localStorage.getItem('q_billing') || '') === 'year';
      trackUnique('abonnement_confirme', {
        value: annuel ? 299 : 29.99,
        currency: 'EUR',
        periodicite: annuel ? 'annuel' : 'mensuel',
      });
    }
  });

  // 10 — création de compte.
  //
  // ⚠️ Cet événement attendait `?signup=1` ou `?gauth=ok` dans l'URL — deux
  // paramètres qu'AUCUN code du site n'a jamais posés. L'inscription par e-mail
  // se fait en AJAX, sans redirection : l'étape la plus importante du tunnel
  // n'était donc mesurée nulle part. Le front appelle désormais cette fonction
  // directement, au moment où le serveur confirme la création (`created: true`).
  window.qTrackCompteCree = function (methode) {
    track('compte_cree', { methode: methode || 'email' });
  };

  // 3, 4, 5 — cycle d'analyse. L'application appelle ces fonctions aux moments
  // clés ; elles vivent ici pour que les noms d'événements restent groupés.
  var debutAnalyse = null;

  window.qTrackAnalyseDemarree = function (methode) {
    debutAnalyse = Date.now();
    track('analyse_demarree', { methode: methode || 'inconnue' });   // 'fichier' | 'lien'
  };

  window.qTrackAnalyseTerminee = function (succes) {
    var duree = debutAnalyse ? Math.round((Date.now() - debutAnalyse) / 1000) : null;
    track('analyse_terminee', {
      duree_secondes: duree,
      resultat: succes === false ? 'echec' : 'succes',
    });
    debutAnalyse = null;
  };

  window.qTrackResultatAffiche = function () {
    track('resultat_affiche');
  };
})();
