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

  /** Émet un événement. Sans effet si Analytics n'est pas chargé. */
  function track(nom, props) {
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
    if (chemin === '/') trackUnique('page_vue_accueil');
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
