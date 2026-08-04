/* ============================================================================
 * QeerahConsent — consentement cookies conforme RGPD / ePrivacy.
 *
 * AVANT : le script Google Analytics était chargé en dur dans le <head> de
 * 20 pages, et les boutons « Accepter / Refuser » ne faisaient qu'écrire dans
 * localStorage. Refuser ne bloquait donc rien → consentement non effectif
 * (RGPD art. 4-11 et 7, directive ePrivacy art. 5-3).
 *
 * MAINTENANT : aucun traceur n'est chargé tant que l'utilisateur n'a pas
 * accepté, et le consentement est donné FINALITÉ PAR FINALITÉ :
 *
 *   mesure    → Google Analytics (audience)
 *   publicite → pixel TikTok Ads + envoi des conversions à TikTok
 *
 * Pourquoi deux finalités et non un seul « oui » : le consentement doit être
 * spécifique (RGPD art. 4-11). Un accord donné pour « comprendre ce qui est
 * utile » ne couvre pas le partage de conversions avec une régie publicitaire.
 * Un site qui ajouterait un pixel Ads sous l'ancien consentement analytics
 * collecterait donc sans base légale.
 *
 * MIGRATION depuis l'ancienne clé binaire `cookieConsent` :
 *   "rejected" → refus intégral, conservé tel quel, on ne redemande RIEN.
 *   "accepted" → mesure accordée (l'accord portait bien sur l'audience), mais
 *                publicité inconnue → le bandeau se réaffiche UNE fois pour
 *                poser la question nouvelle. Analytics continue de tourner
 *                pendant ce temps : son consentement, lui, reste valable.
 *
 * API :
 *   QeerahConsent.get()        → { mesure:bool, publicite:bool, decide:bool }
 *   QeerahConsent.hasAds()     → bool
 *   QeerahConsent.acceptAll()  / .rejectAll() / .save({mesure,publicite})
 *   QeerahConsent.revoke()     → efface le choix + les cookies, recharge
 *   QeerahConsent.reopen()     → réaffiche le bandeau (lien « Cookies » du pied)
 *   QeerahConsent.onChange(fn) → notifié à chaque changement
 *   QeerahConsent.status()     → compat : "accepted" | "rejected" | null
 * ==========================================================================*/
(function () {
  "use strict";

  var GA_ID    = "G-HR4QQJ52DT";
  var KEY      = "qeerah_consent";   // { mesure, publicite, v, date }
  var KEY_OLD  = "cookieConsent";    // ancienne clé binaire

  // ── État ──────────────────────────────────────────────────────────────────
  var etat = { mesure: false, publicite: false, decide: false };
  var abonnes = [];

  function lire() {
    try {
      var brut = localStorage.getItem(KEY);
      if (brut) {
        var o = JSON.parse(brut);
        return { mesure: !!o.mesure, publicite: !!o.publicite, decide: true };
      }
    } catch (e) { /* JSON corrompu → on repart de l'ancienne clé */ }

    var ancien = null;
    try { ancien = localStorage.getItem(KEY_OLD); } catch (e) {}
    if (ancien === "rejected") return { mesure: false, publicite: false, decide: true };
    if (ancien === "accepted") return { mesure: true,  publicite: false, decide: false };
    return { mesure: false, publicite: false, decide: false };
  }

  function ecrire(m, p) {
    etat = { mesure: !!m, publicite: !!p, decide: true };
    try {
      localStorage.setItem(KEY, JSON.stringify({
        mesure: etat.mesure, publicite: etat.publicite,
        v: 2, date: new Date().toISOString()
      }));
      // L'ancienne clé reste tenue à jour : app_v3.js et index.html la lisent.
      localStorage.setItem(KEY_OLD, etat.mesure ? "accepted" : "rejected");
    } catch (e) {}
    notifier();
  }

  function notifier() {
    for (var i = 0; i < abonnes.length; i++) {
      try { abonnes[i](etat); } catch (e) {}
    }
    try {
      document.dispatchEvent(new CustomEvent("qeerah:consent", { detail: etat }));
    } catch (e) { /* navigateurs sans CustomEvent : les abonnés suffisent */ }
  }

  // ── Google Analytics ──────────────────────────────────────────────────────
  // File d'attente : un gtag() appelé avant consentement est mis en attente et
  // ne partira que si Analytics est réellement chargé plus tard.
  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== "function") {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }

  function loadAnalytics() {
    if (window.__qsAnalyticsLoaded) return;
    window.__qsAnalyticsLoaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(s);
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { anonymize_ip: true });
  }

  // ── Bandeau ───────────────────────────────────────────────────────────────
  var STYLE_ID = "qs-consent-style";
  var CSS = [
    "#qs-consent{position:fixed;left:0;right:0;bottom:0;z-index:99998;",
    "background:var(--surface,#fff);border-top:1px solid var(--border,rgba(0,0,0,.10));",
    "box-shadow:0 -6px 30px rgba(0,0,0,.10);padding:16px 18px;",
    "font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;}",
    "#qs-consent .qs-c-in{max-width:900px;margin:0 auto;display:flex;gap:16px;align-items:center;",
    "justify-content:space-between;flex-wrap:wrap;}",
    "#qs-consent .qs-c-t{font-weight:700;font-size:15px;color:var(--text,#1A1A1A);margin-bottom:3px;}",
    "#qs-consent .qs-c-b{font-size:13px;color:var(--muted,#6B7280);line-height:1.5;max-width:560px;}",
    "#qs-consent .qs-c-b a{color:var(--navy,#1F3A70);}",
    "#qs-consent .qs-c-btns{display:flex;gap:9px;flex-wrap:wrap;}",
    // Refuser et Accepter : MÊME taille, même graisse, même hauteur, même rang.
    // Un bouton de refus plus petit ou plus pâle rendrait le refus moins simple
    // que l'acceptation — ce que la CNIL sanctionne (délibération 2020-091).
    "#qs-consent button{font-size:14px;font-weight:700;border-radius:10px;padding:11px 20px;",
    "cursor:pointer;border:1px solid transparent;min-height:44px;}",
    "#qs-consent .qs-c-ok{background:var(--primary,#D4AF37);color:#111;}",
    "#qs-consent .qs-c-no{background:var(--surface,#fff);color:var(--text,#1A1A1A);",
    "border-color:var(--text,#1A1A1A);}",
    "#qs-consent .qs-c-more{background:transparent;color:var(--muted,#6B7280);",
    "border-color:var(--border,rgba(0,0,0,.20));font-weight:600;}",
    "#qs-consent button:focus-visible{outline:2px solid var(--navy,#1F3A70);outline-offset:2px;}",
    "#qs-consent .qs-c-panel{max-width:900px;margin:14px auto 0;border-top:1px solid var(--border,rgba(0,0,0,.10));",
    "padding-top:12px;display:none;}",
    "#qs-consent .qs-c-panel.open{display:block;}",
    "#qs-consent .qs-c-row{display:flex;gap:10px;align-items:flex-start;margin:10px 0;",
    "font-size:13px;color:var(--text,#1A1A1A);}",
    "#qs-consent .qs-c-row input{margin-top:3px;width:18px;height:18px;flex:none;}",
    "#qs-consent .qs-c-row .qs-c-d{color:var(--muted,#6B7280);font-size:12.5px;}",
    "@media(max-width:560px){#qs-consent .qs-c-in{flex-direction:column;align-items:stretch;}",
    "#qs-consent .qs-c-btns button{flex:1;}}"
  ].join("");

  function injectStyle() {
    if (document.getElementById(STYLE_ID)) return;
    var s = document.createElement("style");
    s.id = STYLE_ID; s.textContent = CSS;
    document.head.appendChild(s);
  }

  // Le bandeau historique d'index.html (#cookie-banner) ne parle QUE de mesure
  // d'audience et n'a pas de case « publicité » : le réutiliser ferait recueillir
  // un consentement pour une finalité qu'il n'affiche pas. On le masque et on
  // affiche partout le même bandeau, celui d'ici.
  function masquerAncienBandeau() {
    var b = document.getElementById("cookie-banner");
    if (b) b.style.display = "none";
  }

  function buildBanner() {
    injectStyle();
    masquerAncienBandeau();

    var el = document.createElement("div");
    el.id = "qs-consent";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", "Consentement aux cookies");
    el.innerHTML =
      '<div class="qs-c-in">' +
        "<div>" +
          '<div class="qs-c-t">🍪 Cookies</div>' +
          '<div class="qs-c-b">On aimerait mesurer l\'audience du site et mesurer nos ' +
          'campagnes publicitaires TikTok. Rien n\'est déposé ni envoyé tant que tu ' +
          'n\'as pas accepté, et tu peux changer d\'avis à tout moment. ' +
          '<a href="/privacy">Politique de confidentialité</a></div>' +
        "</div>" +
        '<div class="qs-c-btns">' +
          '<button type="button" class="qs-c-more" id="qs-c-more">Personnaliser</button>' +
          '<button type="button" class="qs-c-no" id="qs-c-no">Tout refuser</button>' +
          '<button type="button" class="qs-c-ok" id="qs-c-ok">Tout accepter</button>' +
        "</div>" +
      "</div>" +
      '<div class="qs-c-panel" id="qs-c-panel">' +
        '<label class="qs-c-row">' +
          '<input type="checkbox" id="qs-c-mesure">' +
          "<span><b>Mesure d'audience</b><br>" +
          '<span class="qs-c-d">Google Analytics — combien de personnes visitent le site ' +
          "et quelles pages servent vraiment. IP anonymisée.</span></span>" +
        "</label>" +
        '<label class="qs-c-row">' +
          '<input type="checkbox" id="qs-c-pub">' +
          "<span><b>Publicité</b><br>" +
          '<span class="qs-c-d">Pixel TikTok Ads — savoir quelles publicités amènent des ' +
          "inscriptions et des abonnements. Ton e-mail n'est transmis à TikTok que sous " +
          "forme chiffrée (empreinte SHA-256), jamais en clair.</span></span>" +
        "</label>" +
        '<div class="qs-c-btns" style="margin-top:6px">' +
          '<button type="button" class="qs-c-ok" id="qs-c-save">Enregistrer mes choix</button>' +
        "</div>" +
      "</div>";

    document.body.appendChild(el);

    var panel = el.querySelector("#qs-c-panel");
    var cbMesure = el.querySelector("#qs-c-mesure");
    var cbPub = el.querySelector("#qs-c-pub");
    // Cases décochées par défaut : le consentement doit être un acte positif,
    // jamais une case pré-cochée (RGPD cons. 32, arrêt Planet49 C-673/17).
    cbMesure.checked = false;
    cbPub.checked = false;

    el.querySelector("#qs-c-more").addEventListener("click", function () {
      panel.classList.toggle("open");
    });
    el.querySelector("#qs-c-ok").addEventListener("click", acceptAll);
    el.querySelector("#qs-c-no").addEventListener("click", rejectAll);
    el.querySelector("#qs-c-save").addEventListener("click", function () {
      save({ mesure: cbMesure.checked, publicite: cbPub.checked });
    });
    return el;
  }

  function showBanner() {
    masquerAncienBandeau();
    if (document.getElementById("qs-consent")) return;
    if (document.body) buildBanner();
    else document.addEventListener("DOMContentLoaded", buildBanner);
  }

  function hideBanner() {
    masquerAncienBandeau();
    var own = document.getElementById("qs-consent");
    if (own) own.remove();
  }

  // ── Application d'un choix ────────────────────────────────────────────────
  // On n'ACTIVE que ce qui est accordé. Rien n'est jamais désactivé à chaud :
  // un script déjà chargé ne se décharge pas — c'est revoke() (qui recharge la
  // page) qui garantit le retour à un état propre.
  function appliquer() {
    if (etat.mesure) loadAnalytics();
  }

  function save(choix) {
    ecrire(choix && choix.mesure, choix && choix.publicite);
    hideBanner();
    appliquer();
  }
  function acceptAll() { save({ mesure: true,  publicite: true  }); }
  function rejectAll() { save({ mesure: false, publicite: false }); }

  var COOKIES_TRACEURS = /^_ga|^_gid|^_gat|^_ttp|^_tt_enable_cookie/;

  /** Retrait du consentement — aussi simple que de le donner (RGPD art. 7-3).
   *  Les cookies déjà posés par Analytics et par le pixel TikTok sont supprimés
   *  et la page rechargée pour repartir d'un état propre. */
  function revoke() {
    try {
      localStorage.removeItem(KEY);
      localStorage.removeItem(KEY_OLD);
      localStorage.removeItem("qeerah_ttclid");
    } catch (e) {}
    try {
      document.cookie.split(";").forEach(function (c) {
        var name = c.split("=")[0].trim();
        if (COOKIES_TRACEURS.test(name)) {
          document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
          document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=." + location.hostname;
        }
      });
    } catch (e) {}
    location.reload();
  }

  /** Rouvre le bandeau sans effacer le choix courant (lien « Cookies »). */
  function reopen() { showBanner(); }

  // ── Démarrage ─────────────────────────────────────────────────────────────
  etat = lire();
  appliquer();
  if (!etat.decide) {
    if (document.readyState === "loading")
      document.addEventListener("DOMContentLoaded", showBanner);
    else showBanner();
  } else {
    if (document.readyState === "loading")
      document.addEventListener("DOMContentLoaded", masquerAncienBandeau);
    else masquerAncienBandeau();
  }

  window.QeerahConsent = {
    get: function () { return { mesure: etat.mesure, publicite: etat.publicite, decide: etat.decide }; },
    hasAds: function () { return !!etat.publicite; },
    acceptAll: acceptAll,
    rejectAll: rejectAll,
    save: save,
    revoke: revoke,
    reopen: reopen,
    loadAnalytics: loadAnalytics,
    onChange: function (fn) {
      if (typeof fn !== "function") return;
      abonnes.push(fn);
      if (etat.decide) { try { fn(etat); } catch (e) {} }
    },
    // Compat : anciens appels qui attendaient une chaîne.
    status: function () {
      if (!etat.decide) return null;
      return etat.mesure ? "accepted" : "rejected";
    },
    accept: acceptAll,
    reject: rejectAll
  };

  // Compat : les onclick historiques d'index.html continuent de fonctionner.
  // Ils ne peuvent plus accorder la publicité (le bandeau qui les porte ne la
  // mentionne pas) — ils ne pilotent que la mesure d'audience.
  window.acceptCookies = function () { save({ mesure: true,  publicite: etat.publicite }); };
  window.rejectCookies = function () { save({ mesure: false, publicite: false }); };
})();
