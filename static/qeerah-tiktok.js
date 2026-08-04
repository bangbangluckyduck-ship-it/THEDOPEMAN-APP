/* ============================================================================
 * QeerahTikTok — pixel TikTok Ads, chargé UNIQUEMENT après consentement.
 *
 * Ce fichier ne fait rien tant que deux conditions ne sont pas réunies :
 *   1. window.QEERAH_TIKTOK_PIXEL_ID est défini (injecté par le serveur depuis
 *      la variable d'environnement TIKTOK_PIXEL_ID — jamais écrit en dur ici) ;
 *   2. QeerahConsent accorde la finalité « publicite ».
 *
 * Tant que l'une manque, aucune requête ne part vers analytics.tiktok.com et
 * aucun cookie _ttp n'est déposé.
 *
 * ÉVÉNEMENTS
 *   ViewContent          — page /pricing et /tarifs (navigateur)
 *   CompleteRegistration — création de compte confirmée par le serveur
 *   CompletePayment      — PAS ici. Envoyé côté SERVEUR depuis le webhook
 *                          Stripe (tiktok_events.py). Le navigateur se contente
 *                          de fabriquer l'event_id et de le transmettre à Stripe
 *                          au moment du checkout : c'est ce qui permet à TikTok
 *                          de dédoublonner si un jour l'événement partait aussi
 *                          du navigateur.
 *
 * API : QeerahTikTok.track(nom, props) / .newEventId() / .checkoutContext()
 * ==========================================================================*/
(function () {
  "use strict";

  var PIXEL_ID = (window.QEERAH_TIKTOK_PIXEL_ID || "").trim();
  var CLE_TTCLID = "qeerah_ttclid";

  function consentPub() {
    try { return !!(window.QeerahConsent && window.QeerahConsent.hasAds()); }
    catch (e) { return false; }
  }

  // ── Chargement du pixel ───────────────────────────────────────────────────
  // Reprise fidèle du snippet officiel TikTok, écrit lisiblement plutôt que
  // minifié : il doit rester relisable pour vérifier qu'il ne fait rien d'autre.
  function chargerPixel(id) {
    if (window.__qTtqCharge) return;
    window.__qTtqCharge = true;

    var w = window, d = document, t = "ttq";
    w.TiktokAnalyticsObject = t;
    var ttq = (w[t] = w[t] || []);
    ttq.methods = ["page", "track", "identify", "instances", "debug", "on", "off",
                   "once", "ready", "alias", "group", "enableCookie", "disableCookie",
                   "holdConsent", "revokeConsent", "grantConsent"];
    ttq.setAndDefer = function (obj, methode) {
      obj[methode] = function () {
        obj.push([methode].concat(Array.prototype.slice.call(arguments, 0)));
      };
    };
    for (var i = 0; i < ttq.methods.length; i++) ttq.setAndDefer(ttq, ttq.methods[i]);
    ttq.instance = function (sdkid) {
      var file = ttq._i[sdkid] || [];
      for (var n = 0; n < ttq.methods.length; n++) ttq.setAndDefer(file, ttq.methods[n]);
      return file;
    };
    ttq.load = function (sdkid, options) {
      var url = "https://analytics.tiktok.com/i18n/pixel/events.js";
      ttq._i = ttq._i || {}; ttq._i[sdkid] = []; ttq._i[sdkid]._u = url;
      ttq._t = ttq._t || {}; ttq._t[sdkid] = +new Date();
      ttq._o = ttq._o || {}; ttq._o[sdkid] = options || {};
      var s = d.createElement("script");
      s.type = "text/javascript";
      s.async = true;
      s.src = url + "?sdkid=" + sdkid + "&lib=" + t;
      var premier = d.getElementsByTagName("script")[0];
      premier.parentNode.insertBefore(s, premier);
    };

    ttq.load(id);
    ttq.page();
  }

  /** Émet un événement. Sans effet si le pixel n'est pas chargé.
   *  Aucune file d'attente : un événement survenu AVANT le consentement ne doit
   *  pas partir rétroactivement une fois le consentement donné. Les événements
   *  de page, eux, sont rejoués proprement par demarrer(). */
  function track(nom, props, options) {
    if (!window.ttq || typeof window.ttq.track !== "function") return;
    try { window.ttq.track(nom, props || {}, options || {}); } catch (e) {}
  }

  /** Identifiant d'événement unique, partagé navigateur ↔ serveur.
   *  TikTok dédoublonne sur (event_name, event_id) pendant 48 h : deux envois
   *  portant le même identifiant ne comptent qu'une conversion. */
  function newEventId() {
    try {
      if (window.crypto && typeof window.crypto.randomUUID === "function")
        return window.crypto.randomUUID();
      if (window.crypto && window.crypto.getRandomValues) {
        var a = new Uint8Array(16);
        window.crypto.getRandomValues(a);
        return Array.prototype.map.call(a, function (o) {
          return ("0" + o.toString(16)).slice(-2);
        }).join("");
      }
    } catch (e) {}
    return "q" + Date.now() + "-" + Math.random().toString(16).slice(2);
  }

  function lireCookie(nom) {
    try {
      var m = document.cookie.match(new RegExp("(^|;\\s*)" + nom + "=([^;]*)"));
      return m ? decodeURIComponent(m[2]) : "";
    } catch (e) { return ""; }
  }

  /** Identifiant de clic publicitaire, posé par TikTok dans l'URL de destination.
   *  On ne le MÉMORISE qu'avec le consentement publicitaire : le stocker sans
   *  accord serait déjà un dépôt sur le terminal (ePrivacy art. 5-3). */
  function memoriserTtclid() {
    try {
      var v = new URLSearchParams(location.search).get("ttclid");
      if (v && consentPub()) localStorage.setItem(CLE_TTCLID, v);
    } catch (e) {}
  }
  function ttclid() {
    try {
      var v = new URLSearchParams(location.search).get("ttclid");
      if (v) return v;
      return localStorage.getItem(CLE_TTCLID) || "";
    } catch (e) { return ""; }
  }

  /** Contexte à joindre à la création de la session Stripe, pour que le serveur
   *  puisse envoyer CompletePayment à TikTok après le paiement.
   *  Renvoie {} sans consentement publicitaire → le serveur n'enverra rien. */
  function checkoutContext() {
    if (!consentPub() || !PIXEL_ID) return {};
    var id = newEventId();
    return {
      tt_consent: "1",
      tt_event_id: id,
      tt_ttp: lireCookie("_ttp"),
      tt_ttclid: ttclid(),
      tt_url: location.origin + location.pathname
    };
  }

  // ── Événements de page ────────────────────────────────────────────────────
  var CHEMINS_TARIFS = ["/pricing", "/tarifs", "/pricing/compare", "/tarifs/comparer"];

  function evenementsDePage() {
    var chemin = location.pathname.replace(/\/+$/, "") || "/";
    if (CHEMINS_TARIFS.indexOf(chemin) !== -1) {
      // Périodicité affichée au moment de la vue : posée par pricing.html sur
      // window.BILLING. Sert à distinguer les vues « mensuel » des « annuel ».
      var annuel = (window.BILLING || "") === "year";
      track("ViewContent", {
        content_type: "product",
        content_id: annuel ? "qeerah_pro_year" : "qeerah_pro_month",
        content_name: "Qeerah Pro",
        currency: "EUR",
        value: annuel ? 299 : 29.99
      }, { event_id: newEventId() });
    }
  }

  // ── Création de compte ────────────────────────────────────────────────────
  // qTrackCompteCree() est déjà appelée aux trois endroits où le serveur
  // confirme une création (homepage.html, app_v3.js × 2). On l'enveloppe plutôt
  // que d'ajouter un quatrième appel : un seul point d'accroche à maintenir.
  function brancherInscription() {
    var precedent = window.qTrackCompteCree;
    window.qTrackCompteCree = function (methode) {
      if (typeof precedent === "function") {
        try { precedent(methode); } catch (e) {}
      }
      track("CompleteRegistration", {
        content_name: "Compte Qeerah",
        currency: "EUR",
        value: 0
      }, { event_id: newEventId() });
    };
  }

  // ── Démarrage ─────────────────────────────────────────────────────────────
  function demarrer() {
    if (!PIXEL_ID || !consentPub()) return;
    memoriserTtclid();
    chargerPixel(PIXEL_ID);
    if (document.readyState === "loading")
      document.addEventListener("DOMContentLoaded", evenementsDePage);
    else evenementsDePage();
  }

  brancherInscription();

  if (PIXEL_ID) {
    if (window.QeerahConsent) {
      // onChange rappelle immédiatement si un choix est déjà enregistré, puis à
      // chaque changement : accepter la publicité charge le pixel sans recharger.
      window.QeerahConsent.onChange(demarrer);
    } else {
      document.addEventListener("qeerah:consent", demarrer);
    }
  }

  window.QeerahTikTok = {
    track: track,
    newEventId: newEventId,
    checkoutContext: checkoutContext,
    estActif: function () { return !!(PIXEL_ID && consentPub()); }
  };
})();
